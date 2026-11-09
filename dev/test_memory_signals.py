import glob
import json
import os
import random
import sys
import time
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

from gameboy_worlds import get_emulator, get_test_environment
from gameboy_worlds.emulation.emulator import LowLevelActions
from gameboy_worlds.utils import load_parameters

GEN1 = ("pokemon_red", "pokemon_brown")
GEN2 = ("pokemon_crystal", "pokemon_prism")
ZELDA = ("legend_of_zelda_links_awakening", "legend_of_zelda_the_oracle_of_seasons")
STATES = {
    "pokemon_red": "pewter",
    "pokemon_crystal": "outside_berry_tree",
    "pokemon_brown": "custom_strategistbrownargon374",
    "pokemon_prism": "route_69",
    "legend_of_zelda_links_awakening": "shore_state",
    "legend_of_zelda_the_oracle_of_seasons": "near_shop",
}
ARROWS = [
    LowLevelActions.PRESS_ARROW_UP,
    LowLevelActions.PRESS_ARROW_LEFT,
    LowLevelActions.PRESS_ARROW_DOWN,
    LowLevelActions.PRESS_ARROW_RIGHT,
]
EXPECTED_SIGNALS = {
    "pokemon_red": ({"money", "party_hp_fraction", "party_fainted", "bag_kinds", "hidden_objects", "events_raised_all"}, {"party_total_experience", "party_level_sum", "badge_count", "pokedex_caught", "pokedex_seen", "trainers_beaten", "story_flags_got"}),
    "pokemon_crystal": ({"money", "party_hp_fraction", "party_fainted", "bag_kinds", "events_raised_all"}, {"party_total_experience", "party_level_sum", "badge_count", "pokedex_caught", "pokedex_seen", "trainers_beaten", "story_flags_got", "engine_flags", "fly_points", "key_items"}),
    "pokemon_brown": ({"money", "party_hp_fraction", "party_fainted", "bag_kinds"}, {"party_total_experience", "party_level_sum", "badge_count", "event_bits_raw"}),
    "pokemon_prism": ({"money", "party_hp_fraction", "party_fainted", "bag_kinds"}, {"party_total_experience", "party_level_sum", "pokedex_caught", "pokedex_seen", "key_items"}),
    "legend_of_zelda_links_awakening": ({"health_units", "health_fraction", "rupees", "bombs", "inventory_item_count"}, {"max_health_units", "sword_level", "instruments", "rooms_visited", "deaths"}),
    "legend_of_zelda_the_oracle_of_seasons": ({"health_units", "health_fraction", "rupees", "ore_chunks", "inventory_item_count"}, {"max_health_units", "sword_level", "essence_count", "rooms_visited", "enemies_killed", "treasures_obtained", "deaths"}),
}


class Results:
    def __init__(self):
        self.failures = []
        self.passed = 0

    def check(self, condition, label):
        if condition:
            self.passed += 1
        else:
            self.failures.append(label)
            print(f"FAIL: {label}")


def poke(emulator, label, values, offset=0):
    memory = emulator.state_parser.memory
    bank, address, _ = memory.symbol_info(label)
    for index, value in enumerate(values):
        target = address + offset + index
        if memory._cgb and 0xC000 <= target < 0xE000:
            emulator._pyboy.memory[bank, target] = value
        else:
            emulator._pyboy.memory[target] = value


def set_money(emulator, game, amount):
    if game in GEN1:
        digits = f"{amount:06d}"
        poke(emulator, "wPlayerMoney", [int(digits[i : i + 2], 16) for i in (0, 2, 4)])
    elif game in GEN2:
        poke(emulator, "wMoney", [(amount >> 16) & 255, (amount >> 8) & 255, amount & 255])
    elif game == ZELDA[0]:
        digits = f"{amount:04d}"
        poke(emulator, "wRupeeCountHigh", [int(digits[:2], 16)])
        poke(emulator, "wRupeeCountLow", [int(digits[2:], 16)])
    else:
        digits = f"{amount:04d}"
        poke(emulator, "wNumRupees", [int(digits[2:], 16), int(digits[:2], 16)])


def set_first_mon_hp(emulator, game, value):
    offset = 1 if game in GEN1 else 34
    poke(emulator, "wPartyMons", [value >> 8, value & 255], offset)


def set_first_mon_exp(emulator, game, value):
    offset = 14 if game in GEN1 else 8
    poke(emulator, "wPartyMons", [(value >> 16) & 255, (value >> 8) & 255, value & 255], offset)


def money_signal(game):
    return "rupees" if game in ZELDA else "money"


def tracking_is_exact(results, game):
    emulator = get_emulator(game=game, init_state=STATES[game], headless=True)
    emulator.reset()
    tracker = emulator.state_tracker
    metric = tracker.metrics["memory_signals"]
    results.check(metric.ready and metric.steps == 1, f"{game}: one ready step after reset")
    expected_situational, expected_progress = EXPECTED_SIGNALS[game]
    report = tracker.report()["memory_signals"]
    missing = expected_situational - set(report["situational"])
    results.check(not missing, f"{game}: missing situational {missing}")
    missing = expected_progress - set(report["progress"])
    results.check(not missing, f"{game}: missing progress {missing}")

    name = money_signal(game)
    start = report["situational"][name]["current"]
    before_increase = report["situational"][name]["total_increase"]
    set_money(emulator, game, start + 50)
    emulator.step(ARROWS[0])
    summary = tracker.report()["memory_signals"]["situational"][name]
    results.check(summary["current"] == start + 50, f"{game}: tracked money {summary['current']}")
    results.check(summary["delta"] == 50, f"{game}: money delta {summary['delta']}")
    results.check(summary["total_increase"] == before_increase + 50, f"{game}: money increase {summary}")
    set_money(emulator, game, start + 20)
    emulator.step(ARROWS[1])
    summary = tracker.report()["memory_signals"]["situational"][name]
    results.check(summary["delta"] == -30, f"{game}: money drop {summary['delta']}")
    results.check(summary["total_decrease"] == 30, f"{game}: money decrease {summary}")
    results.check(summary["max"] == start + 50 and summary["min"] == start, f"{game}: money range {summary}")
    results.check(summary["steps_since_change"] == 0, f"{game}: steps since change {summary}")
    emulator.step(ARROWS[2])
    summary = tracker.report()["memory_signals"]["situational"][name]
    results.check(summary["steps_since_change"] == 1, f"{game}: steps since change grows {summary}")
    results.check(summary["delta"] == 0, f"{game}: delta returns to zero {summary}")

    if game in ZELDA:
        label = "wHealth" if game == ZELDA[0] else "wLinkHealth"
        poke(emulator, label, [2])
        emulator.step(ARROWS[3])
        report = tracker.report()["memory_signals"]
        results.check(report["situational"]["health_units"]["current"] == 2, f"{game}: tracked health")
        maximum = emulator.state_parser.memory.max_health_units()
        results.check(report["situational"]["health_fraction"]["current"] == 2 / maximum, f"{game}: health fraction")
    else:
        set_first_mon_hp(emulator, game, 1)
        emulator.step(ARROWS[3])
        party = emulator.state_parser.memory.party()
        expected = (1 + sum(mon["hp"] for mon in party[1:])) / sum(mon["max_hp"] for mon in party)
        report = tracker.report()["memory_signals"]
        results.check(report["situational"]["party_hp_fraction"]["current"] == expected, f"{game}: hp fraction")
        set_first_mon_hp(emulator, game, 0)
        emulator.step(ARROWS[0])
        report = tracker.report()["memory_signals"]
        results.check(report["situational"]["party_fainted"]["current"] >= 1, f"{game}: fainted count")

        peak_before = report["progress"]["party_total_experience"]["peak"]
        set_first_mon_exp(emulator, game, party[0]["experience"] + 1000)
        emulator.step(ARROWS[1])
        report = tracker.report()["memory_signals"]["progress"]["party_total_experience"]
        results.check(report["peak"] == peak_before + 1000, f"{game}: exp peak rises {report}")
        reached = report["peak_reached_step"]
        results.check(reached == metric.steps, f"{game}: peak step {report}")
        set_first_mon_exp(emulator, game, party[0]["experience"])
        emulator.step(ARROWS[2])
        report = tracker.report()["memory_signals"]["progress"]["party_total_experience"]
        results.check(report["peak"] == peak_before + 1000, f"{game}: high-water mark holds {report}")
        results.check(report["current"] == peak_before, f"{game}: current falls back {report}")
        results.check(report["peak_reached_step"] == reached, f"{game}: peak step holds {report}")

    array = metric.as_array(name)
    results.check(len(array) == metric.steps, f"{game}: expanded series length")
    results.check(not np.isnan(array).any(), f"{game}: expanded series complete")
    results.check(array[-1] == start + 20 and array[0] == start, f"{game}: expanded series endpoints {array}")
    history = metric.history(name)
    results.check([value for _, value in history] == [start, start + 50, start + 20], f"{game}: change points {history}")

    timings = []
    random.seed(0)
    for _ in range(40):
        emulator.step(random.choice(ARROWS))
        began = time.perf_counter()
        metric.step(None, None)
        metric.report()
        timings.append(time.perf_counter() - began)
    report = tracker.report()["memory_signals"]
    size = len(json.dumps(report, default=str))
    print(f"{game}: metric {1000 * np.mean(timings):.2f} ms/step, report {size} bytes, exploration {report['exploration']}, combat {report['combat']}")
    results.check(report["exploration"]["unique_tiles"] >= 1, f"{game}: exploration runs")
    json.dumps(report, default=str)

    steps = metric.steps
    emulator.reset()
    results.check(len(metric.episodes) == 1 and metric.episodes[0]["steps"] == steps, f"{game}: episode recorded")
    results.check(metric.steps == 1, f"{game}: reset clears steps")
    results.check(metric.history(name)[0][0] == 1 and len(metric.history(name)) == 1, f"{game}: reset clears history")
    emulator.step(ARROWS[0])
    emulator.close()
    emulator.close()
    results.check(len(tracker.report_final()["memory_signals"]["episodes"]) == 2, f"{game}: double close records once")


def zelda_states(results, game, rom_path):
    emulator = get_emulator(game=game, init_state=STATES[game], headless=True)
    memory = emulator.state_parser.memory
    count = unloaded = 0
    for path in sorted(glob.glob(os.path.join(rom_path, "states", "*.state"))):
        with open(path, "rb") as handle:
            emulator._pyboy.load_state(handle)
        count += 1
        snapshot = memory.snapshot()
        if not memory.is_loaded():
            unloaded += 1
            continue
        player, location = snapshot["player"], snapshot["location"]
        name = os.path.basename(path)
        results.check(player["health_units"] <= player["max_health_units"], f"{game}/{name}: health above max")
        results.check(player["rupees"] is not None, f"{game}/{name}: rupees not BCD")
        results.check(location["facing"] is not None, f"{game}/{name}: facing")
    print(f"{game}: {count} states, {unloaded} before game data loads")
    emulator.close()


def zelda_walking(results, game):
    state = "inside_fathouse" if game == ZELDA[0] else STATES[game]
    emulator = get_emulator(game=game, init_state=state, headless=True)
    emulator.reset()
    memory = emulator.state_parser.memory
    pyboy = emulator._pyboy
    pyboy.tick(40, True)
    moved = 0
    signs = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
    for button in ("up", "left", "down", "right") * 2:
        before = memory.location()
        pyboy.button(button, 20)
        pyboy.tick(40, True)
        after = memory.location()
        results.check(after["facing"] == button, f"{game}: facing after {button}: {after['facing']}")
        if after["room"] == before["room"]:
            dx, dy = after["x"] - before["x"], after["y"] - before["y"]
            sx, sy = signs[button]
            results.check(dx * sx >= 0 and dy * sy >= 0 and (dx * (sy != 0) == 0) and (dy * (sx != 0) == 0), f"{game}: {button} moved {dx},{dy}")
            moved += (dx != 0 or dy != 0)
    results.check(moved >= 2, f"{game}: Link walked ({moved})")
    emulator.close()


def seasons_hud(results):
    game = ZELDA[1]
    emulator = get_emulator(game=game, init_state=STATES[game], headless=True)
    emulator.reset()
    pyboy = emulator._pyboy
    pyboy.tick(40, True)
    base = np.array(pyboy.screen.ndarray[:, :, 0]).astype(int)
    poke(emulator, "wLinkHealth", [2])
    poke(emulator, "wNumRupees", [0x23, 0x01])
    pyboy.tick(240, True)
    after = np.array(pyboy.screen.ndarray[:, :, 0]).astype(int)
    changed = np.argwhere(after[:16] != base[:16])
    results.check(len(changed) > 0, "seasons: poked health and rupees redraw the HUD")
    memory = emulator.state_parser.memory
    results.check(memory.rupees() == 123 and memory.player()["hearts"] == 0.5, "seasons: decoded poked values")
    emulator.close()


def memory_free_games_still_build(results):
    parameters = dict(load_parameters(None))
    parameters["debug_mode"] = True
    emulator = get_emulator(game="pokemon_fools_gold", parameters=parameters, headless=True)
    emulator.reset()
    results.check("memory_signals" not in emulator.state_tracker.report(), "fools gold tracker has no memory signals")
    results.check("core" in emulator.state_tracker.report(), "fools gold tracker still reports")
    emulator.close()


def benchmark_environments(results, project_root):
    for benchmark, games in (("pokemon", ("pokemon_red", "pokemon_crystal")), ("legend_of_zelda", ZELDA), ("pokemon_brown", ("pokemon_brown",)), ("pokemon_prism", ("pokemon_prism",))):
        tasks = pd.read_csv(os.path.join(project_root, "benchmark", "tests", f"{benchmark}.csv"))
        for game in games:
            row = tasks[tasks["game"] == game].iloc[0]
            environment = get_test_environment(row, max_steps=20, session_name="memory_signal_test")
            environment.reset()
            info = None
            for _ in range(5):
                _, _, terminated, truncated, info = environment.step(environment.action_space.sample())
                if terminated or truncated:
                    break
            results.check("memory_signals" in info, f"{game}: benchmark info has memory signals")
            results.check("progress" in info.get("memory_signals", {}), f"{game}: benchmark signals populated")
            environment.close()


def main():
    parameters = load_parameters(None)
    results = Results()
    for game in STATES:
        print(f"=== {game}")
        tracking_is_exact(results, game)
    for game in ZELDA:
        zelda_states(results, game, parameters[f"{game}_rom_data_path"])
        zelda_walking(results, game)
    seasons_hud(results)
    memory_free_games_still_build(results)
    benchmark_environments(results, parameters["project_root"])
    print(f"\npassed {results.passed}, failed {len(results.failures)}")
    sys.exit(0 if not results.failures else 1)


if __name__ == "__main__":
    main()
