import glob
import json
import os
import random
import re
import sys
import time
import warnings

warnings.filterwarnings("ignore")

import click
import numpy as np
from pyboy import PyBoy

from gameboy_worlds.emulation.pokemon.memory import (
    PokemonBrownMemory,
    PokemonCrystalMemory,
    PokemonPrismMemory,
    PokemonRedMemory,
    SignalUnavailable,
    UnsupportedRom,
)
from gameboy_worlds.utils import load_parameters

GAMES = {
    "pokemon_red": ("PokemonRed.gb", PokemonRedMemory),
    "pokemon_crystal": ("PokemonCrystal.gbc", PokemonCrystalMemory),
    "pokemon_brown": ("PokemonBrown.gb", PokemonBrownMemory),
    "pokemon_prism": ("PokemonPrism.gbc", PokemonPrismMemory),
}
WALK_STATE = {
    "pokemon_red": "starter",
    "pokemon_crystal": "starter",
    "pokemon_brown": "custom_strategistbrownargon374",
    "pokemon_prism": "route_69",
}
CARD_STATE = {
    "pokemon_red": "pewter",
    "pokemon_crystal": "starter",
    "pokemon_brown": "custom_strategistbrownargon374",
    "pokemon_prism": "route_69",
}
KNOWN_OWNED_NOT_SEEN = {"custom_strategistredjudgebedroomb6"}


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

    def summary(self):
        print(f"\npassed {self.passed}, failed {len(self.failures)}")
        return not self.failures


class Session:
    def __init__(self, game, rom_root):
        rom, memory_class = GAMES[game]
        self.game = game
        self.rom_root = rom_root
        self.pyboy = PyBoy(os.path.join(rom_root, rom), window="null", sound_emulated=False)
        self.memory = memory_class(self.pyboy)

    def load(self, state):
        with open(os.path.join(self.rom_root, "states", f"{state}.state"), "rb") as handle:
            self.pyboy.load_state(handle)
        self.pyboy.tick(40, True)

    def press(self, button, hold=6, after=24):
        self.pyboy.button(button, hold)
        self.pyboy.tick(hold + after, True)

    def poke(self, label, values):
        bank, address, _ = self.memory.symbol_info(label)
        for index, value in enumerate(values):
            if self.memory._cgb and 0xC000 <= address < 0xE000:
                self.pyboy.memory[bank, address + index] = value
            else:
                self.pyboy.memory[address + index] = value

    def screen(self):
        return "\n".join(self.memory.screen_text())

    def cursor_to(self, word, button="up"):
        for _ in range(9):
            line = next((row for row in self.memory.screen_text() if "▶" in row), "")
            if word in line:
                return True
            self.press(button, after=18)
        return False

    def open_card(self):
        self.press("start", after=50)
        name = self.memory.read_text("wPlayerName")
        if self.game in ("pokemon_brown", "pokemon_red"):
            self.poke("wCurrentMenuItem", [0])
            for _ in range(3):
                self.press("down", after=18)
        else:
            self.cursor_to(name)
        self.press("a", after=150)

    def stop(self):
        self.pyboy.stop(save=False)


def states_of(rom_root):
    return sorted(
        os.path.basename(path)[:-6] for path in glob.glob(os.path.join(rom_root, "states", "*.state"))
    )


def static_layout_checks(results, data_dir):
    with open(os.path.join(data_dir, "pokered.json")) as handle:
        red = json.load(handle)
    with open(os.path.join(data_dir, "pokecrystal.json")) as handle:
        crystal = json.load(handle)

    def offset(data, label, base):
        return data["symbols"][label][1] - data["symbols"][base][1]

    for label, expected in {
        "wPartyMon1HP": 1, "wPartyMon1BoxLevel": 3, "wPartyMon1Status": 4, "wPartyMon1Type1": 5,
        "wPartyMon1CatchRate": 7, "wPartyMon1Moves": 8, "wPartyMon1OTID": 12, "wPartyMon1Exp": 14,
        "wPartyMon1HPExp": 17, "wPartyMon1DVs": 27, "wPartyMon1PP": 29, "wPartyMon1Level": 33,
        "wPartyMon1MaxHP": 34, "wPartyMon1Attack": 36, "wPartyMon2": 44,
    }.items():
        results.check(offset(red, label, "wPartyMon1") == expected, f"red party offset {label}")
    for label, expected in {
        "wBattleMonHP": 1, "wBattleMonStatus": 4, "wBattleMonType1": 5, "wBattleMonCatchRate": 7,
        "wBattleMonMoves": 8, "wBattleMonDVs": 12, "wBattleMonLevel": 14, "wBattleMonMaxHP": 15,
        "wBattleMonAttack": 17, "wBattleMonPP": 25,
    }.items():
        results.check(offset(red, label, "wBattleMon") == expected, f"red battle offset {label}")
    for label, expected in {
        "wPartyMon1Item": 1, "wPartyMon1Moves": 2, "wPartyMon1ID": 6, "wPartyMon1Exp": 8,
        "wPartyMon1HPExp": 11, "wPartyMon1DVs": 21, "wPartyMon1PP": 23, "wPartyMon1Happiness": 27,
        "wPartyMon1PokerusStatus": 28, "wPartyMon1CaughtData": 29, "wPartyMon1Level": 31,
        "wPartyMon1Status": 32, "wPartyMon1HP": 34, "wPartyMon1MaxHP": 36, "wPartyMon1Attack": 38,
        "wPartyMon1SpclDef": 46, "wPartyMon2": 48,
    }.items():
        results.check(offset(crystal, label, "wPartyMon1") == expected, f"crystal party offset {label}")
    for label, expected in {
        "wBattleMonItem": 1, "wBattleMonMoves": 2, "wBattleMonDVs": 6, "wBattleMonPP": 8,
        "wBattleMonHappiness": 12, "wBattleMonLevel": 13, "wBattleMonStatus": 14, "wBattleMonHP": 16,
        "wBattleMonMaxHP": 18, "wBattleMonAttack": 20, "wBattleMonSpclDef": 28, "wBattleMonType1": 30,
    }.items():
        results.check(offset(crystal, label, "wBattleMon") == expected, f"crystal battle offset {label}")
    results.check(offset(crystal, "wObject2Struct", "wObject1Struct") == 40, "crystal object stride")
    results.check(offset(crystal, "wObject1MapX", "wObject1Struct") == 16, "crystal object map x")


def red_events_match_existing_table(results, rom_root, data_dir):
    with open(os.path.join(data_dir, "pokered.json")) as handle:
        red = json.load(handle)
    with open(os.path.join(rom_root, "events.json")) as handle:
        existing = json.load(handle)
    base = red["symbols"]["wEventFlags"][1]
    pret_slots = {
        f"{base + index // 8:#06x}-{index % 8}".lower() for index in red["events"].values()
    }
    existing_slots = {
        slot.lower()
        for slot in existing
        if slot.lower().startswith("0x") and base <= int(slot.split("-")[0], 16) < base + 320
    }
    overlap = len(pret_slots & existing_slots)
    print(f"red events: pret {len(pret_slots)} events.json {len(existing_slots)} overlap {overlap}")
    results.check(overlap >= 0.9 * len(pret_slots), "red event slots agree with events.json")


def every_state_invariants(results, game, session, rom_root):
    memory = session.memory
    is_hack = memory._overlay is not None
    maps = memory._data["maps"]
    counts = dict(states=0, map_checked=0, bounds=0)
    for state in states_of(rom_root):
        with open(os.path.join(rom_root, "states", f"{state}.state"), "rb") as handle:
            session.pyboy.load_state(handle)
        counts["states"] += 1
        snapshot = memory.snapshot()
        results.check(bool(snapshot.get("player", {}).get("name")), f"{game}/{state}: player name")
        party = memory.party()
        for mon in party:
            results.check(1 <= mon["level"] <= 100, f"{game}/{state}: level {mon['level']}")
            results.check(mon["hp"] <= mon["max_hp"], f"{game}/{state}: hp {mon['hp']}/{mon['max_hp']}")
            results.check(mon["species_name"] is not None, f"{game}/{state}: species {mon['species_id']}")
            for move in mon["moves"]:
                results.check(move["name"] is not None, f"{game}/{state}: move {move['id']}")
        location = memory.location()
        if location.get("map_loaded"):
            width, height = location["width_blocks"], location["height_blocks"]
            counts["bounds"] += 1
            results.check(
                location["x"] < 2 * width and location["y"] < 2 * height,
                f"{game}/{state}: position {location['x']},{location['y']} outside {width}x{height}",
            )
            if not is_hack:
                key = (
                    str(location["map_id"])
                    if "map_id" in location
                    else f"{location['map_group']}:{location['map_number']}"
                )
                expected = maps.get(key)
                results.check(expected is not None, f"{game}/{state}: unknown map {key}")
                if expected and expected["width"] is not None:
                    counts["map_checked"] += 1
                    matches = (width, height) == (expected["width"], expected["height"])
                    results.check(
                        location["map_settled"] == matches,
                        f"{game}/{state}: map_settled disagrees with pret dims",
                    )
                    if not matches:
                        counts["mid_warp"] = counts.get("mid_warp", 0) + 1
                        session.pyboy.tick(60, True)
                        results.check(
                            memory.is_map_settled() is True,
                            f"{game}/{state}: map {key} never settled",
                        )
        pokedex = memory.pokedex()
        if pokedex and state not in KNOWN_OWNED_NOT_SEEN:
            seen = {entry.get("dex", entry.get("species_id")) for entry in pokedex["seen"]}
            owned = {entry.get("dex", entry.get("species_id")) for entry in pokedex["owned"]}
            results.check(owned <= seen, f"{game}/{state}: owned not subset of seen")
        for group in ("bag", "items", "ball_pocket", "key_items", "pc_items"):
            reader = getattr(memory, group, None)
            if reader is None:
                continue
            for item in reader():
                results.check(
                    item["name"] is not None or (is_hack and item["id"] > 100),
                    f"{game}/{state}: {group} item {item['id']}",
                )
        battle = memory.battle()
        if battle and battle["mode"] in ("none", "lost"):
            results.check("enemy_mon" not in battle, f"{game}/{state}: stale battle data exposed")
        if battle and "player_mon" in battle:
            active = battle.get("active_party_slot")
            if active is None and memory.has("wPlayerMonNumber"):
                active = memory.read_byte("wPlayerMonNumber")
            results.check(battle["player_mon"]["species_name"] is not None, f"{game}/{state}: blank active mon")
            if active is not None and active < len(party):
                results.check(
                    battle["player_mon"]["species_id"] == party[active]["species_id"]
                    and battle["player_mon"]["hp"] == party[active]["hp"],
                    f"{game}/{state}: active mon disagrees with party slot {active}",
                )
    print(f"{game}: {counts}")


def bank_independence(results, session):
    memory = session.memory
    if not memory._cgb:
        return
    with open(os.path.join(session.rom_root, "states", "custom_strategistcrystalargon4.state"), "rb") as handle:
        session.pyboy.load_state(handle)
    bank = session.pyboy.memory[0xFF70] & 7
    results.check(bank == 6, f"state expected on WRAM bank 6, found {bank}")
    unbanked_badges = session.pyboy.memory[0xD857]
    print(f"SVBK={bank}: unbanked johto badges {unbanked_badges}, banked {memory.read_byte('wJohtoBadges')}, name {memory.read_text('wPlayerName')!r}")
    results.check(memory.read_byte("wJohtoBadges") == 0, "banked badges correct while bank 6 is mapped")
    results.check(unbanked_badges == 255, "this state distinguishes banked and unbanked reads")
    results.check(memory.read_text("wPlayerName") == "You", "banked name while bank 6 is mapped")
    results.check(memory.player()["money"] == 3000, "banked money while bank 6 is mapped")


def registered_parsers(results):
    from gameboy_worlds import get_emulator

    expected = {
        "pokemon_red": ("starter", PokemonRedMemory),
        "pokemon_crystal": ("custom_strategistcrystalargon4", PokemonCrystalMemory),
        "pokemon_brown": (WALK_STATE["pokemon_brown"], PokemonBrownMemory),
        "pokemon_prism": (WALK_STATE["pokemon_prism"], PokemonPrismMemory),
    }
    for game, (state, memory_class) in expected.items():
        emulator = get_emulator(game=game, init_state=state, headless=True)
        emulator.reset()
        parser = emulator.state_parser
        results.check(isinstance(parser.memory, memory_class), f"{game}: registered parser exposes memory")
        results.check(bool(parser.memory.snapshot().get("player")), f"{game}: snapshot through registered parser")
        results.check(emulator.state_tracker is not None, f"{game}: default tracker still builds")
        results.check("memory_signals" in emulator.state_tracker.report(), f"{game}: signals metric reports")
        if game == "pokemon_crystal":
            results.check(parser.get_johto_badges().sum() == 0, "crystal: get_johto_badges correct under bank 6")
            results.check(not parser.has_badge("zephyr"), "crystal: has_badge correct under bank 6")
            results.check(not parser.has_completed_championship(), "crystal: championship correct under bank 6")
        emulator.close()


def walking(results, game, session):
    memory = session.memory
    session.load(WALK_STATE[game])
    moved = 0
    deltas = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
    for button in ("up", "left", "down", "right") * 2:
        before = (memory.read_byte("wXCoord"), memory.read_byte("wYCoord"))
        session.press(button, hold=12, after=20)
        after = (memory.read_byte("wXCoord"), memory.read_byte("wYCoord"))
        results.check(memory.location()["facing"] == button, f"{game}: facing after {button}")
        change = (after[0] - before[0], after[1] - before[1])
        results.check(change in (deltas[button], (0, 0)), f"{game}: moved {change} on {button}")
        moved += change == deltas[button]
    results.check(moved >= 4, f"{game}: player actually walked ({moved})")


def time_and_joypad(results, game, session):
    memory = session.memory
    session.load(WALK_STATE[game])
    seconds = "wPlayTimeSeconds" if memory.has("wPlayTimeSeconds") else "wGameTimeSeconds"
    minutes = "wPlayTimeMinutes" if memory.has("wPlayTimeMinutes") else "wGameTimeMinutes"
    start = memory.read_byte(minutes) * 60 + memory.read_byte(seconds)
    frames_label = "wPlayTimeFrames" if memory.has("wPlayTimeFrames") else "wGameTimeFrames"
    observed_frames = set()
    for _ in range(600):
        session.pyboy.tick(1, False)
        observed_frames.add(memory.read_byte(frames_label))
    results.check(len(observed_frames) == 60 and max(observed_frames) == 59, f"{game}: frame counter cycles 0-59, saw {len(observed_frames)}")
    elapsed = memory.read_byte(minutes) * 60 + memory.read_byte(seconds) - start
    results.check(9 <= elapsed <= 11, f"{game}: 600 frames advanced clock by {elapsed}s")
    held = "hJoyHeld" if memory.has("hJoyHeld") else "hJoyDown"
    session.pyboy.button_press("a")
    session.pyboy.tick(10, True)
    pressed_value = memory.read_byte(held)
    session.pyboy.button_release("a")
    session.pyboy.tick(10, True)
    results.check(pressed_value & 1 == 1, f"{game}: held A not visible ({pressed_value})")
    results.check(memory.read_byte(held) & 1 == 0, f"{game}: release not visible")


def trainer_card_pokes(results, game, session):
    memory = session.memory
    session.load(CARD_STATE[game])
    if game in ("pokemon_red", "pokemon_brown"):
        session.poke("wPlayerMoney", [0x12, 0x34, 0x56])
        session.poke("wPlayTimeHours", [7])
        session.poke("wPlayTimeMinutes", [41])
        session.poke("wPlayTimeSeconds", [0])
        money = "123456"
    else:
        session.poke("wMoney", [0x01, 0x23, 0x45])
        session.poke("wGameTimeHours", [0, 7])
        session.poke("wGameTimeMinutes", [41])
        session.poke("wGameTimeSeconds", [0])
        money = "74565"
    session.pyboy.tick(20, True)
    session.open_card()
    screen = session.screen()
    results.check(money in screen, f"{game}: poked money {money} on card\n{screen}")
    results.check(re.search(r"7\D{1,2}41", screen) is not None, f"{game}: poked time on card\n{screen}")
    decoded = memory.read_text("wPlayerName")
    results.check(decoded in screen, f"{game}: decoded name {decoded!r} on card\n{screen}")


def base_game_battle_hud(results, game, session, state):
    memory = session.memory
    session.load(state)
    battle = memory.battle()
    screen = session.screen()
    for key in ("player_mon", "enemy_mon"):
        results.check(battle[key]["species_name"] in screen, f"{game}: {key} name on HUD\n{screen}")
        results.check(str(battle[key]["level"]) in screen, f"{game}: {key} level on HUD\n{screen}")
        results.check(all(name is not None for name in battle[key]["type_names"]), f"{game}: {key} type names")
    player = battle["player_mon"]
    results.check(f"{player['hp']}/{player['max_hp']}" in screen.replace("/ ", "/"), f"{game}: player hp on HUD\n{screen}")


def red_named_signals(results, session):
    memory = session.memory
    session.load("battle_blue_cerulean_bridge")
    battle = memory.battle()
    results.check(battle["trainer_class"]["name"] == "RIVAL1", "red: trainer class")
    results.check(
        [entry["species_name"] for entry in battle["enemy_party_species"]] == ["PIDGEOTTO", "ABRA", "RATTATA", "SQUIRTLE"],
        f"red: rival team {battle['enemy_party_species']}",
    )
    results.check(battle["player_mon"]["type_names"] == ["FIRE", "FIRE"], "red: charmeleon types")
    session.load("pewter")
    location = memory.location()
    results.check(location["map_name"] == "PEWTER_CITY", "red: map name")
    results.check(location["connections"]["south"] == 13, "red: pewter connects south to route 2")
    owned = [entry["species_name"] for entry in memory.pokedex()["owned"]]
    results.check(owned == ["CHARMANDER"], f"red: pokedex numbering {owned}")
    results.check(memory.event("EVENT_BATTLED_RIVAL_IN_OAKS_LAB"), "red: named event")
    session.load("complete")
    results.check(memory.badges()["count"] == 8, "red: complete state has every badge")
    results.check(memory.pokedex()["owned_count"] == 151, "red: complete dex")
    results.check(memory.event("EVENT_BECAME_CHAMPION") if "EVENT_BECAME_CHAMPION" in memory._data["events"] else True, "red: champion event")
    boxes = memory.stored_boxes()
    results.check(all(box["count"] is not None for box in boxes), "red: stored boxes parse")
    results.check(all(entry["species_name"] for box in boxes for entry in box["species"]), "red: stored box species named")


def crystal_named_signals(results, session):
    memory = session.memory
    session.load("starter")
    location = memory.location()
    results.check(location["map_name"] == "ELMS_LAB", f"crystal: map name {location}")
    results.check(memory.engine_flag("ENGINE_POKEGEAR"), "crystal: named engine flag")
    results.check(memory.read_byte("hHours") < 24, "crystal: clock hours")
    session.load("battle_delibird")
    battle = memory.battle()
    results.check(battle["enemy_mon"]["type_names"] == ["ICE", "FLYING"], "crystal: delibird types")
    results.check(battle["player_mon"]["type_names"] == ["NORMAL", "FLYING"], "crystal: pidgeot types")


def status_screen(results, game, session, state, slot):
    memory = session.memory
    session.load(state)
    mon = memory.party()[slot]
    session.press("start", after=50)
    if game == "pokemon_brown":
        session.poke("wCurrentMenuItem", [0])
        session.press("down", after=18)
        session.press("a", after=90)
        for _ in range(slot):
            session.press("down", after=20)
        session.press("a", after=50)
        session.press("a", after=150)
        pages = [session.screen()]
        session.press("a", after=80)
        pages.append(session.screen())
    else:
        session.cursor_to("Pokémon")
        session.press("a", after=120)
        for _ in range(slot):
            session.press("down", after=20)
        session.press("a", after=60)
        session.press("a", after=180)
        pages = [session.screen()]
        for _ in range(2):
            session.press("right", after=60)
            pages.append(session.screen())
    text = "\n".join(pages)
    for name, value in mon["stats"].items():
        results.check(re.search(rf"\b{value}\b", text) is not None, f"{game}: {name}={value} on status\n{text}")
    results.check(str(mon["experience"]) in text, f"{game}: exp {mon['experience']} on status\n{text}")
    results.check(f"{mon['original_trainer_id']:05d}" in text, f"{game}: OT id on status\n{text}")
    results.check(mon["original_trainer"] in text, f"{game}: OT name on status\n{text}")
    for move in mon["moves"]:
        results.check(move["name"] in text, f"{game}: move {move['name']} on status\n{text}")
        results.check(f"{move['pp']}/" in text, f"{game}: pp of {move['name']} on status\n{text}")
    if "held_item_name" in mon and mon["held_item_name"]:
        results.check(mon["held_item_name"] in text, f"{game}: held item on status\n{text}")


def status_condition_poke(results, game, session, state):
    memory = session.memory
    session.load(state)
    bank, address, _ = memory.symbol_info("wPartyMons")
    offset = 4 if game == "pokemon_brown" else 32
    if memory._cgb:
        session.pyboy.memory[bank, address + offset] = 0x08
    else:
        session.pyboy.memory[address + offset] = 0x08
    session.pyboy.tick(20, True)
    results.check(memory.party()[0]["status"]["poisoned"], f"{game}: decoded poison")
    session.press("start", after=50)
    if game == "pokemon_brown":
        session.poke("wCurrentMenuItem", [0])
        session.press("down", after=18)
    else:
        session.cursor_to("Pokémon")
    session.press("a", after=120)
    screen = session.screen()
    marker = "のふへ" if game == "pokemon_brown" else "PSN"
    results.check(marker in screen, f"{game}: poked poison on party screen\n{screen}")


def hack_fields_are_withheld(results, session, labels, keys):
    memory = session.memory
    for label in labels:
        results.check(not memory.has(label), f"{label} must not be readable")
    for mon in memory.party():
        for key in keys:
            results.check(key not in mon, f"{key} must be withheld")


def brown_battle_hud(results, session):
    memory = session.memory
    session.load("capture_clefairy")
    battle = memory.battle()
    results.check(battle["mode"] == "wild", "brown: battle mode")
    screen = session.screen()
    for key in ("player_mon", "enemy_mon"):
        results.check(battle[key]["species_name"] in screen, f"brown: {key} name on HUD\n{screen}")
        results.check(str(battle[key]["level"]) in screen, f"brown: {key} level on HUD")
    player = battle["player_mon"]
    results.check(f"{player['hp']}/ {player['max_hp']}" in screen, f"brown: player hp on HUD\n{screen}")


def brown_bag_screen(results, session):
    memory = session.memory
    session.load(WALK_STATE["pokemon_brown"])
    bag = memory.bag()
    session.press("start", after=50)
    session.poke("wCurrentMenuItem", [0])
    session.press("down", after=18)
    session.press("down", after=18)
    session.press("a", after=120)
    screen = session.screen()
    named = [item["name"] for item in bag if item["name"]][:3]
    results.check(len(named) == 3, "brown: bag has named entries")
    for name in named:
        results.check(name in screen, f"brown: {name} on item screen\n{screen}")


def brown_badge_bits(results, session):
    memory = session.memory
    frames = {}
    for mask in (0, 1, 2, 4, 8, 16, 32, 64, 128):
        session.load(CARD_STATE["pokemon_brown"])
        session.poke("wObtainedBadges", [mask])
        session.pyboy.tick(20, True)
        session.open_card()
        frames[mask] = np.array(session.pyboy.screen.ndarray[:, :, 0]).astype(int)
    regions = set()
    for mask in (1, 2, 4, 8, 16, 32, 64, 128):
        changed = np.argwhere(frames[mask] != frames[0])
        results.check(len(changed) > 0, f"brown: badge bit {mask} changes the card")
        if len(changed):
            regions.add(tuple(changed.min(axis=0).tolist()))
    results.check(len(regions) == 8, f"brown: 8 distinct badge icons, got {len(regions)}")


def prism_battle_screen(results, session):
    memory = session.memory
    session.load("route_70")
    generator = random.Random(0)
    for step in range(600):
        session.press(generator.choice(["up", "down", "left", "right"]), hold=10, after=14)
        if step % 3 == 0:
            session.press("b", hold=3, after=6)
        if memory.read_byte("wBattleMode"):
            break
    results.check(memory.read_byte("wBattleMode") == 1, "prism: wild battle started")
    for _ in range(16):
        session.press("a", hold=3, after=40)
        if "Fight" in session.screen():
            break
    battle = memory.battle()
    screen = session.screen()
    for key in ("player_mon", "enemy_mon"):
        results.check(battle[key]["species_name"] in screen, f"prism: {key} name on HUD\n{screen}")
        results.check(str(battle[key]["level"]) in screen, f"prism: {key} level on HUD\n{screen}")
    player = battle["player_mon"]
    results.check(f"{player['hp']}/ {player['max_hp']}" in screen, f"prism: player hp on HUD\n{screen}")
    results.check(player["types"] == [5, 4], f"prism: larvitar rock/ground raw types {player['types']}")
    session.press("a", after=60)
    screen = session.screen()
    for move in player["moves"]:
        results.check(move["name"] in screen, f"prism: move {move['name']} on fight menu\n{screen}")


def prism_pack_pokes(results, session):
    memory = session.memory
    session.load("caper_ridge")
    results.check([item["name"] for item in memory.items()] == ["Potion", "Oran Berry"], f"prism: items {memory.items()}")
    session.poke("wNumItems", [2])
    session.poke("wItems", [18, 42, 19, 17, 0xFF])
    session.poke("wNumBalls", [1])
    session.poke("wBalls", [5, 33, 0xFF])
    session.poke("wNumKeyItems", [1])
    session.poke("wKeyItems", [67, 0xFF])
    session.pyboy.tick(20, True)
    results.check(memory.items()[0] == {"id": 18, "name": "Potion", "quantity": 42}, "prism: decoded poked items")
    results.check(memory.ball_pocket()[0]["name"] == "Poké Ball", "prism: decoded poked balls")
    results.check(memory.key_items()[0]["name"] == "Rijon Pass", "prism: decoded poked key items")
    session.press("start", after=50)
    session.cursor_to("Pack")
    session.press("a", after=150)
    screen = session.screen()
    results.check("×42" in screen and "Escape Rope" in screen and "×17" in screen, f"prism: items pocket\n{screen}")
    session.press("right", after=40)
    screen = session.screen()
    results.check("Poké Ball" in screen and "×33" in screen, f"prism: balls pocket\n{screen}")
    session.press("right", after=40)
    screen = session.screen()
    results.check("Rijon Pass" in screen, f"prism: key pocket\n{screen}")


def prism_pokedex(results, session):
    memory = session.memory
    session.load("pokedex")
    results.check(
        [entry["species_name"] for entry in memory.pokedex()["owned"]]
        == [mon["species_name"] for mon in memory.party()],
        "prism: Pokedex caught bit is the party species",
    )
    session.press("start", after=50)
    session.cursor_to("Pokédex")
    session.press("a", after=180)
    results.check("Larvitar" in session.screen(), "prism: Larvitar listed before zeroing")
    session.load("pokedex")
    session.poke("wPokedexCaught", [0] * 32)
    session.poke("wPokedexSeen", [0] * 32)
    session.pyboy.tick(20, True)
    session.press("start", after=50)
    session.cursor_to("Pokédex")
    session.press("a", after=180)
    results.check("Larvitar" not in session.screen(), "prism: zeroed Pokedex hides Larvitar")


def prism_badge_address_is_rejected(results, session):
    memory = session.memory
    for label in ("wJohtoBadges", "wKantoBadges", "wPlayerState", "wTMsHMs", "wStatusFlags"):
        try:
            memory.read_byte(label)
            results.check(False, f"prism: {label} should be unavailable")
        except SignalUnavailable:
            results.check(True, label)
    results.check("badges" not in memory.player(), "prism: badges omitted from player signals")


def brown_rejections(results, session):
    memory = session.memory
    for label in ("wPokedexOwned", "wPokedexSeen"):
        try:
            memory.read_byte(label)
            results.check(False, f"brown: {label} should be unavailable")
        except SignalUnavailable:
            results.check(True, label)
    results.check(memory.pokedex() == {}, "brown: pokedex omitted")
    results.check("names" not in memory.badges(), "brown: badge names are not claimed")


def wrong_rom_is_refused(results, rom_root_red):
    pyboy = PyBoy(os.path.join(rom_root_red, "PokemonRed.gb"), window="null", sound_emulated=False)
    try:
        PokemonBrownMemory(pyboy)
        results.check(False, "Brown memory must refuse the Red ROM")
    except UnsupportedRom:
        results.check(True, "wrong rom refused")
    pyboy.stop(save=False)


def snapshot_speed(game, session):
    session.load(WALK_STATE[game])
    start = time.perf_counter()
    for _ in range(20):
        session.memory.snapshot()
    print(f"{game}: snapshot {1000 * (time.perf_counter() - start) / 20:.1f} ms")


@click.command()
@click.option("--game", type=click.Choice(list(GAMES) + ["all"]), default="all")
def main(game):
    parameters = load_parameters(None)
    results = Results()
    data_dir = os.path.join(
        os.path.dirname(os.path.abspath(sys.modules[PokemonRedMemory.__module__].__file__)), "memory_data"
    )
    static_layout_checks(results, data_dir)
    red_root = parameters["pokemon_red_rom_data_path"]
    red_events_match_existing_table(results, red_root, data_dir)
    wrong_rom_is_refused(results, red_root)
    registered_parsers(results)
    for name in GAMES if game == "all" else [game]:
        print(f"=== {name}")
        root = parameters[f"{name}_rom_data_path"]
        session = Session(name, root)
        every_state_invariants(results, name, session, root)
        if name == "pokemon_crystal":
            bank_independence(results, session)
        walking(results, name, session)
        time_and_joypad(results, name, session)
        trainer_card_pokes(results, name, session)
        if name == "pokemon_red":
            base_game_battle_hud(results, name, session, "battle_blue_cerulean_bridge")
            red_named_signals(results, session)
        if name == "pokemon_crystal":
            base_game_battle_hud(results, name, session, "battle_delibird")
            crystal_named_signals(results, session)
        if name == "pokemon_brown":
            brown_battle_hud(results, session)
            brown_bag_screen(results, session)
            brown_badge_bits(results, session)
            brown_rejections(results, session)
            status_screen(results, name, session, WALK_STATE[name], 1)
            status_condition_poke(results, name, session, WALK_STATE[name])
            hack_fields_are_withheld(results, session, ("wPartyMon1DVs", "wPartyMon1HPExp", "wBattleMonDVs", "wPokedexOwned"), ("dvs", "stat_exp", "catch_rate"))
        if name == "pokemon_prism":
            prism_battle_screen(results, session)
            prism_pack_pokes(results, session)
            prism_pokedex(results, session)
            prism_badge_address_is_rejected(results, session)
            status_screen(results, name, session, "route_70", 0)
            status_condition_poke(results, name, session, "route_70")
            hack_fields_are_withheld(results, session, ("wPartyMon1DVs", "wPartyMon1Happiness", "wBattleMonDVs", "wNumPCItems"), ("dvs", "happiness", "pokerus", "caught_location"))
        snapshot_speed(name, session)
        session.stop()
    sys.exit(0 if results.summary() else 1)


if __name__ == "__main__":
    main()
