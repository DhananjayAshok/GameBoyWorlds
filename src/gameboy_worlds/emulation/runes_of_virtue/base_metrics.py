from typing import Optional

import numpy as np

from gameboy_worlds.emulation.runes_of_virtue.parsers import (
    AgentState,
    RunesOfVirtueStateParser,
)
from gameboy_worlds.emulation.tracker import MetricGroup, OCRegionMetric


class CoreRunesOfVirtueMetrics(MetricGroup):
    """
    Runes of Virtue specific core metrics.

    Reports:
    - agent_state: The AgentState info. Is either FREE_ROAM or IN_MENU.

    Final Reports:
    - None
    """

    NAME = "runes_of_virtue_core"
    REQUIRED_PARSER = RunesOfVirtueStateParser

    def reset(self, first: bool = False):
        self.current_state: AgentState = AgentState.FREE_ROAM
        self._previous_state = self.current_state

    def close(self):
        self.reset()

    def step(self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]):
        self._previous_state = self.current_state
        self.current_state = self.state_parser.get_agent_state(current_frame)

    def report(self) -> dict:
        return {"agent_state": self.current_state}

    def report_final(self) -> dict:
        return {}


class RunesOfVirtueOCRMetric(OCRegionMetric):
    """
    Captures Runes of Virtue dialogue regions for downstream OCR.
    """

    REQUIRED_PARSER = RunesOfVirtueStateParser

    def start(self):
        self.kinds = {"dialogue": self.state_parser.get_dialogue_ocr_region_name()}
        super().start()

    def can_read_kind(self, current_frame: np.ndarray, kind: str) -> bool:
        self.state_parser: RunesOfVirtueStateParser
        if kind == "dialogue":
            in_dialogue = self.state_parser.dialogue_box_open(
                current_screen=current_frame
            )
            dialogue_empty = self.state_parser.dialogue_box_empty(
                current_screen=current_frame
            )
            in_menu = self.state_parser.is_in_menu(current_screen=current_frame)
            return in_dialogue and not dialogue_empty and not in_menu
        return False
