from typing import Optional

import numpy as np

from gameboy_worlds.emulation.legend_of_zelda.parsers import BaseLegendOfZeldaParser
from gameboy_worlds.emulation.signal_tracking import MemorySignalsMetric
from gameboy_worlds.emulation.tracker import MetricGroup, OCRegionMetric


class LegendOfZeldaMemorySignalsMetric(MemorySignalsMetric):
    REQUIRED_PARSER = BaseLegendOfZeldaParser
    SITUATIONAL_SIGNALS = (
        "health_units", "rupees", "ore_chunks", "bombs", "arrows", "magic_powder",
        "ember_seeds", "scent_seeds", "pegasus_seeds", "gale_seeds", "mystery_seeds", "gasha_seeds",
    )
    PROGRESS_SIGNALS = (
        "max_health_units", "heart_pieces", "sword_level", "shield_level", "power_bracelet_level",
        "satchel_level", "max_bombs", "seashells", "golden_leaves", "instruments", "essence_count",
        "enemies_killed", "deaths",
    )

    def is_ready(self) -> bool:
        return self.state_parser.memory.is_loaded()

    def read_clock_seconds(self) -> Optional[float]:
        frames = self.state_parser.memory.player().get("play_time_frames")
        return None if frames is None else frames / 60

    def read_situational(self) -> dict:
        memory = self.state_parser.memory
        player = memory.player()
        signals = {name: player[name] for name in self.SITUATIONAL_SIGNALS if name in player}
        if player["max_health_units"]:
            signals["health_fraction"] = player["health_units"] / player["max_health_units"]
        signals["inventory_item_count"] = memory.inventory()["item_count"]
        return signals

    def read_progress(self) -> dict:
        memory = self.state_parser.memory
        player = memory.player()
        signals = {name: player[name] for name in self.PROGRESS_SIGNALS if name in player}
        signals["rooms_visited"] = memory.rooms_visited()
        inventory = memory.inventory()
        if "treasures_obtained" in inventory:
            signals["treasures_obtained"] = inventory["treasures_obtained"]
        return signals

    def read_position(self):
        location = self.state_parser.memory.location()
        map_key = (location.get("is_indoor", location.get("group")), location.get("map_id"), location["room"])
        return map_key, (location["x"] // 16, location["y"] // 16), None

    def reset_combat(self) -> None:
        self.combat = {"damage_events": 0, "damage_taken_units": 0, "deaths_this_episode": 0}
        self._health = None
        self._deaths = None

    # UNTESTED: damage and death counts have not been validated against real play. A heal and a hit
    # inside one step cancel out, and the death counter is only written by the game on some paths.
    def update_combat(self) -> None:
        player = self.state_parser.memory.player()
        health = player["health_units"]
        if self._health is not None and health < self._health:
            self.combat["damage_events"] += 1
            self.combat["damage_taken_units"] += self._health - health
        self._health = health
        deaths = player["deaths"]
        if deaths is not None:
            if self._deaths is not None and deaths > self._deaths:
                self.combat["deaths_this_episode"] += deaths - self._deaths
            self._deaths = deaths


class CoreLegendOfZeldaMetrics(MetricGroup):
    """
    Zelda-specific core metrics.

    Reports:
    - agent_state: Current parser-derived agent state.

    Final Reports:
    - None
    """

    NAME = "legend_of_zelda_core"
    REQUIRED_PARSER = BaseLegendOfZeldaParser

    def reset(self, first: bool = False):
        self.current_state = "in_dialogue"
        self._previous_state = self.current_state

    def close(self):
        self.reset()
        return

    def step(self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]):
        self._previous_state = self.current_state
        self.current_state = self.state_parser.get_agent_state(current_frame)

    def report(self) -> dict:
        return {"agent_state": self.current_state}

    def report_final(self) -> dict:
        return {}


class LegendOfZeldaOCRMetric(OCRegionMetric):
    REQUIRED_PARSER = BaseLegendOfZeldaParser

    def reset(self, first=False):
        super().reset(first)

    def start(self):
        self.kinds = {
            "dialogue_top": "dialogue_top_ocr",
            "dialogue_bottom": "dialogue_bottom_ocr",
        }
        super().start()

    def can_read_kind(self, current_frame: np.ndarray, kind: str) -> bool:
        if kind in self.kinds:
            return (
                self.state_parser.named_region_matches_target(
                    current_frame, kind
                )
                and self.state_parser.get_agent_state(current_frame) == "in_dialogue"
            )
        return False
