from typing import Optional

import numpy as np

from gameboy_worlds.emulation.hamtaro.parsers import AgentState, HamtaroStateParser
from gameboy_worlds.emulation.tracker import MetricGroup


class HamtaroCoreMetrics(MetricGroup):
    """Tracks the coarse Hamtaro game state for dev-play inspection."""

    NAME = "hamtaro_core"
    REQUIRED_PARSER = HamtaroStateParser

    def start(self):
        super().start()

    def reset(self, first=False):
        self.current_state = AgentState.FREE_ROAM
        self.previous_state = self.current_state

    def close(self):
        self.reset()

    def step(self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]):
        self.previous_state = self.current_state
        self.current_state = self.state_parser.get_agent_state(current_frame)

    def report(self) -> dict:
        return {
            "agent_state": self.current_state,
            "in_free_roam": self.current_state == AgentState.FREE_ROAM,
            "in_dialogue": self.current_state == AgentState.IN_DIALOGUE,
            "in_menu": self.current_state == AgentState.IN_MENU,
        }

    def report_final(self) -> dict:
        return {}
