from typing import Optional
from abc import ABC
from gameboy_worlds.emulation.harvest_moon.parsers import (
    AgentState,
    HarvestMoon1Parser,
    HarvestMoon2Parser,
    HarvestMoon3Parser,
    HarvestMoonStateParser,
)
from gameboy_worlds.emulation.tracker import (
    MetricGroup,
    OCRegionMetric,
    TerminationTruncationMetric,
)

import numpy as np


class CoreHarvestMoonMetrics(MetricGroup):
    """
    Harvest Moon-specific metrics.

    Reports:
    - `agent_state`: The AgentState info. Is either FREE_ROAM or IN_DIALOGUE.

    Final Reports:
    - None
    """

    NAME = "harvest_moon_core"
    REQUIRED_PARSER = HarvestMoonStateParser

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
        return {
            "agent_state": self.current_state,
        }

    def report_final(self) -> dict:
        return {}


class HarvestMoonOCRMetric(OCRegionMetric):
    REQUIRED_PARSER = HarvestMoonStateParser

    def reset(self, first=False):
        super().reset(first)
        self.prev_was_in_menu = False

    def start(self):
        self.kinds = {
            "dialogue": "screen",
            "menu": "screen",
        }
        super().start()

    def can_read_kind(self, current_frame: np.ndarray, kind: str) -> bool:
        self.state_parser: PokemonStateParser
        if kind == "dialogue":
            in_dialogue = self.state_parser.dialogue_box_open(
                current_screen=current_frame
            )
            # dialogue_empty = self.state_parser.dialogue_box_empty(
            #     current_screen=current_frame
            # )
            return (
                in_dialogue
                # and not dialogue_empty
            )
        if kind == "menu":
            in_menu = self.state_parser.is_in_menu(current_screen=current_frame)
            return in_menu
        return False


class HarvestMoon1OCRMetric(HarvestMoonOCRMetric):
    REQUIRED_PARSER = HarvestMoon1Parser

    def start(self):
        self.kinds = {
            "dialogue": "dialogue_box_bottom",
            "menu": "screen",
        }
        OCRegionMetric.start(self)


class HarvestMoon2OCRMetric(HarvestMoonOCRMetric):
    REQUIRED_PARSER = HarvestMoon2Parser

    def start(self):
        self.kinds = {
            "dialogue": "dialogue_box_bottom",
            "menu": "screen",
        }
        OCRegionMetric.start(self)


class HarvestMoon3OCRMetric(HarvestMoonOCRMetric):
    REQUIRED_PARSER = HarvestMoon3Parser

    def start(self):
        self.kinds = {
            "dialogue": "dialogue_box_bottom",
            "menu": "screen",
        }
        OCRegionMetric.start(self)


class HarvestMoonTestMetric(MetricGroup):
    """
    Harvest Moon metrics for test environments.

    Reports:
    - `agent_state`: The current AgentState (FREE_ROAM or IN_DIALOGUE).
    - `previous_agent_state`: The AgentState from the previous step.

    Final Reports:
    - None
    """

    NAME = "harvest_moon_test"
    REQUIRED_PARSER = HarvestMoonStateParser

    def start(self):
        super().start()

    def reset(self, first=False):
        self.agent_state: AgentState = AgentState.IN_DIALOGUE
        self.previous_agent_state: AgentState = self.agent_state

    def close(self):
        self.reset()
        return

    def step(self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]):
        self.state_parser: HarvestMoonStateParser
        self.previous_agent_state = self.agent_state
        self.agent_state = self.state_parser.get_agent_state(current_frame)

    def report(self) -> dict:
        return {
            "agent_state": self.agent_state,
            "previous_agent_state": self.previous_agent_state,
        }

    def report_final(self) -> dict:
        return {}
