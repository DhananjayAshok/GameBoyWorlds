from typing import Optional

import numpy as np

from gameboy_worlds.emulation.runes_of_virtue_1.parsers import RunesOfVirtue1Parser
from gameboy_worlds.emulation.tracker import MetricGroup


class CoreRunesOfVirtue1Metrics(MetricGroup):
    """
    Runes of Virtue 1 specific core metrics.

    Reports:
    - agent_state: Current parser-derived agent state ("in_menu" or "free_roam").

    Final Reports:
    - None
    """

    NAME = "runes_of_virtue_1_core"
    REQUIRED_PARSER = RunesOfVirtue1Parser

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
