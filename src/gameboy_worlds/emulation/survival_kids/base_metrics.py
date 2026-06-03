"""Base metric groups for Survival Kids."""

from typing import Any, Dict, Optional, Set

import numpy as np

from gameboy_worlds.emulation.tracker import MetricGroup, OCRegionMetric
from gameboy_worlds.emulation.survival_kids.parsers import (
    AgentState,
    SurvivalKidsParser,
)


class CoreSurvivalKidsMetrics(MetricGroup):
    NAME = "survival_kids_core"
    REQUIRED_PARSER = SurvivalKidsParser

    def start(self):
        self.total_steps_all: int = 0
        self.episode_count: int = 0
        super().start()

    def reset(self, first: bool = False):
        if not first:
            self.total_steps_all += self.step_count
            self.episode_count += 1
        self.step_count: int = 0
        self.agent_state: AgentState = AgentState.FREE_ROAM
        self.in_dialogue: bool = False
        self.in_menu: bool = False

    def close(self):
        self.final_metrics: Dict[str, Any] = {
            "total_steps_all_episodes": self.total_steps_all + self.step_count,
            "total_episodes": self.episode_count,
        }

    def step(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ):  # noqa: ARG002
        self.step_count += 1
        self.agent_state = self.state_parser.get_agent_state(current_frame)
        self.in_dialogue = self.agent_state == AgentState.IN_DIALOGUE
        self.in_menu = self.agent_state == AgentState.IN_MENU

    def report(self) -> Dict[str, Any]:
        return {
            "agent_state": self.agent_state,
            "in_dialogue": self.in_dialogue,
            "in_menu": self.in_menu,
            "step_count": self.step_count,
        }

    def report_final(self) -> Dict[str, Any]:
        return {
            "total_steps_all_episodes": self.total_steps_all + self.step_count,
            "total_episodes": self.episode_count,
        }


class SurvivalKidsExploreMetrics(MetricGroup):
    NAME = "survival_kids_explore"
    REQUIRED_PARSER = SurvivalKidsParser

    _HASH_W = 20
    _HASH_H = 18

    def start(self):
        self._all_seen_hashes: Set[int] = set()
        self.total_episodes: int = 0
        super().start()

    def reset(self, first: bool = False):
        if not first:
            self.total_episodes += 1
        self._episode_hashes: Set[int] = set()
        self.steps_exploring: int = 0
        self.step_count: int = 0

    def close(self):
        self.final_metrics: Dict[str, Any] = {
            "unique_frames_total": len(self._all_seen_hashes),
            "total_episodes": self.total_episodes,
        }

    @staticmethod
    def _hash_frame(frame: np.ndarray, w: int, h: int) -> int:
        small = frame[::144 // h, ::160 // w, 0]
        return hash(small.tobytes())

    def step(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ):  # noqa: ARG002
        self.step_count += 1
        h = self._hash_frame(current_frame, self._HASH_W, self._HASH_H)
        if h not in self._episode_hashes:
            self._episode_hashes.add(h)
            self._all_seen_hashes.add(h)
            self.steps_exploring += 1

    def report(self) -> Dict[str, Any]:
        unique = len(self._episode_hashes)
        ratio = unique / self.step_count if self.step_count > 0 else 0.0
        return {
            "unique_frames_episode": unique,
            "total_steps_exploring": self.steps_exploring,
            "exploration_ratio": round(ratio, 4),
        }

    def report_final(self) -> Dict[str, Any]:
        return {
            "unique_frames_total": len(self._all_seen_hashes),
            "total_episodes": self.total_episodes,
        }


class SurvivalKidsVitalMetrics(MetricGroup):
    NAME = "survival_kids_vitals"
    REQUIRED_PARSER = SurvivalKidsParser

    _ADDR_HP: Optional[int] = None
    _ADDR_HUNGER: Optional[int] = None
    _ADDR_THIRST: Optional[int] = None
    _ADDR_STAMINA: Optional[int] = None
    _CRITICAL_THRESHOLD: int = 200

    def _read(self, address: Optional[int]) -> Optional[int]:
        if address is None:
            return None
        return self.state_parser.read_memory_byte(address)

    def start(self):
        super().start()

    def reset(self, first: bool = False):
        self.hp: Optional[int] = None
        self.hunger: Optional[int] = None
        self.thirst: Optional[int] = None
        self.stamina: Optional[int] = None
        self._min_hp: Optional[int] = None
        self._times_starving: int = 0
        self._times_dehydrated: int = 0

    def close(self):
        self.final_metrics: Dict[str, Any] = {
            "min_hp_seen": self._min_hp,
            "times_starving": self._times_starving,
            "times_dehydrated": self._times_dehydrated,
        }

    def step(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ):  # noqa: ARG002
        self.hp = self._read(self._ADDR_HP)
        self.hunger = self._read(self._ADDR_HUNGER)
        self.thirst = self._read(self._ADDR_THIRST)
        self.stamina = self._read(self._ADDR_STAMINA)
        if self.hp is not None:
            if self._min_hp is None or self.hp < self._min_hp:
                self._min_hp = self.hp
        if self.hunger is not None and self.hunger >= self._CRITICAL_THRESHOLD:
            self._times_starving += 1
        if self.thirst is not None and self.thirst >= self._CRITICAL_THRESHOLD:
            self._times_dehydrated += 1

    def report(self) -> Dict[str, Any]:
        return {
            "hp": self.hp,
            "hunger": self.hunger,
            "thirst": self.thirst,
            "stamina": self.stamina,
        }

    def report_final(self) -> Dict[str, Any]:
        return {
            "min_hp_seen": self._min_hp,
            "times_starving": self._times_starving,
            "times_dehydrated": self._times_dehydrated,
        }


class SurvivalKidsHudMetrics(MetricGroup):
    NAME = "survival_kids_hud"
    REQUIRED_PARSER = SurvivalKidsParser

    _REGIONS = [
        "status_bar",
        "hp_area",
        "hunger_area",
        "thirst_area",
        "stamina_area",
        "equipped_items_area",
        "equipped_item_area",
        "pack_icon_area",
    ]
    _CHANGE_MAE_THRESHOLD = 10

    def reset(self, first: bool = False):  # noqa: ARG002
        self._baselines: Dict[str, Optional[np.ndarray]] = {
            region: None for region in self._REGIONS
        }
        self._mae: Dict[str, float] = {region: 0.0 for region in self._REGIONS}
        self._changed: Dict[str, bool] = {region: False for region in self._REGIONS}

    def close(self):
        self.final_metrics = {
            f"{region}_changed": self._changed[region] for region in self._REGIONS
        }

    def step(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ):  # noqa: ARG002
        for region in self._REGIONS:
            cropped = self.state_parser.capture_named_region(current_frame, region)
            if self._baselines[region] is None:
                self._baselines[region] = cropped.copy()
                self._mae[region] = 0.0
                self._changed[region] = False
                continue
            mae = np.abs(
                cropped.astype(float) - self._baselines[region].astype(float)
            ).mean()
            self._mae[region] = float(mae)
            self._changed[region] = mae > self._CHANGE_MAE_THRESHOLD

    def report(self) -> Dict[str, Any]:
        report: Dict[str, Any] = {}
        for region in self._REGIONS:
            report[f"{region}_mae"] = round(self._mae[region], 4)
            report[f"{region}_changed"] = self._changed[region]
        return report

    def report_final(self) -> Dict[str, Any]:
        return self.final_metrics


class SurvivalKidsOCRMetric(OCRegionMetric):
    """Expose OCR regions only when Survival Kids shows readable UI text."""

    REQUIRED_PARSER = SurvivalKidsParser

    def start(self):
        self.kinds = {
            "dialogue": "dialogue_area",
            "dialogue_bottom": "screen_bottom",
            "menu": "menu_area",
        }
        super().start()

    def can_read_kind(self, current_frame: np.ndarray, kind: str) -> bool:
        if kind in {"dialogue", "dialogue_bottom"}:
            return self.state_parser.is_in_dialogue(current_frame)
        if kind == "menu":
            return self.state_parser.is_in_menu(current_frame)
        return False
