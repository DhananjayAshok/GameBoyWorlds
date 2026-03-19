from typing import Optional

import numpy as np

from gameboy_worlds.emulation.ultima.parsers import UltimaRunesOfVirtueParser
from gameboy_worlds.emulation.tracker import MetricGroup


class CoreUltimaMetrics(MetricGroup):
    """
    Ultima-specific core metrics.

    Reports:
    - agent_state: Current parser-derived agent state ("in_menu" or "free_roam").

    Final Reports:
    - None
    """

    NAME = "ultima_core"
    REQUIRED_PARSER = UltimaRunesOfVirtueParser

    def reset(self, first: bool = False):
        self.current_state = "free_roam"
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
