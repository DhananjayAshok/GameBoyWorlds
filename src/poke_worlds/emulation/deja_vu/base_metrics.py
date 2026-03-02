from typing import Optional
from abc import ABC
from poke_worlds.emulation.deja_vu.parsers import (
    AgentState,
    # MemoryBasedDejaVuStateParser,
    DejaVuStateParser,
    DejaVu1StateParser,
)
from poke_worlds.emulation.tracker import (
    MetricGroup,
    OCRegionMetric,
    # TerminationTruncationMetric,
)


import numpy as np


class CoreDejaVuMetrics(MetricGroup):
    """
    Deja Vu-specific core metrics.

    Reports:
    - agent_state: The AgentState info. Is either Free Roam, In Dialogue or In Menu.

    Final Reports:
    - None
    """

    NAME = "dejavu_core"
    REQUIRED_PARSER = DejaVuStateParser

    def start(self):
        self.n_battles_total = []
        super().start()

    def reset(self, first=False):
        if not first:
            pass
        self.current_state: AgentState = (
            AgentState.IN_DIALOGUE
        )  # Start by default in dialogue because it has the least permissable actions.
        """ The current state of the agent in the game. """
        self._previous_state = self.current_state

    def close(self):
        self.reset()
        return

    def step(self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]):
        self._previous_state = self.current_state
        current_state = self.state_parser.get_agent_state(current_frame)
        self.current_state = current_state

    def report(self) -> dict:
        """
        Reports the current Deja Vu core metrics:
        - Agent state
        Returns:
            dict: A dictionary containing the current agent state.
        """
        return {
            "agent_state": self.current_state,
        }

    def report_final(self) -> dict:
        """
        Reports nothing:
        """
        return {}


class DejaVuOCRMetric(OCRegionMetric):
    REQUIRED_PARSER = DejaVuStateParser

    def reset(self, first=False):
        super().reset(first)
        self.prev_was_in_dialogue = False

    def start(self):
        self.kinds = {
            "dialogue": "dialogue_top_left_hook",
            "menu": "menu_bottom_line",
        }
        super().start()

    def can_read_kind(self, current_frame: np.ndarray, kind: str) -> bool:
        self.state_parser: DejaVuStateParser
        if kind == "dialogue":
            in_dialogue = self.state_parser.is_in_dialogue(current_screen=current_frame)
            in_menu = self.state_parser.is_in_menu(current_screen=current_frame)
            return (in_dialogue and not in_menu)
        if kind == "menu":
            in_menu = self.state_parser.is_in_menu(current_screen=current_frame)
            return in_menu
        return False

class DejaVuTestMetric(MetricGroup):
    """
    Deja Vu-specific test metrics.

    Reports:
    - is_in_fight: Whether the agent is currently in a fight
    - was_in_fight_last_step: Whether the agent was in a fight in the previous step
    """

    NAME = "dejavu_test"
    REQUIRED_PARSER = DejaVuStateParser

    def start(self):
        super().start()

    def reset(self, first=False):
        if not first:
            pass
        self.prev_was_fight = False
        self.is_in_fight = False

    def close(self):
        self.reset()
        return

    def step(self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]):
        self.state_parser: DejaVuStateParser
        is_fight = False
        self.prev_was_fight = self.is_in_fight
        self.is_in_fight = is_fight

    def report(self) -> dict:
        return {
            "is_in_fight": self.is_in_fight,
            "was_in_fight_last_step": self.prev_was_fight,
        }

    def report_final(self) -> dict:
        return {}
