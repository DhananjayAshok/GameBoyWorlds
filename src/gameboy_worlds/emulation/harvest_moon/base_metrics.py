from typing import Optional
from abc import ABC
from gameboy_worlds.emulation.harvest_moon.parsers import (
    AgentState,
    HarvestMoon1Parser,
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
        """
        Reports the current Pokémon core metrics:
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

class HarvestMoonOCRMetric(OCRegionMetric):
    REQUIRED_PARSER = HarvestMoonStateParser

    def reset(self, first=False):
        super().reset(first)

    def start(self):
        self.kinds = {
            # "dialogue": "dialogue_box_full",
        }
        super().start()

    # def can_read_kind(self, current_frame: np.ndarray, kind: str) -> bool:
    #     self.state_parser: PokemonStateParser
    #     if kind == "dialogue":
    #         in_dialogue = self.state_parser.dialogue_box_open(
    #             current_screen=current_frame
    #         )
    #         dialogue_empty = self.state_parser.dialogue_box_empty(
    #             current_screen=current_frame
    #         )
    #         in_battle_menu = self.state_parser.is_in_base_battle_menu(
    #             current_screen=current_frame
    #         )
    #         in_fight_options = self.state_parser.is_in_fight_options_menu(
    #             current_screen=current_frame
    #         )
    #         in_bag = self.state_parser.is_in_fight_bag(current_screen=current_frame)
    #         return (
    #             in_dialogue
    #             and not dialogue_empty
    #             and not in_battle_menu
    #             and not in_fight_options
    #             and not in_bag
    #         )
    #     if kind == "battle_attack_options":
    #         in_fight_options = self.state_parser.is_in_fight_options_menu(
    #             current_screen=current_frame
    #         )
    #         if in_fight_options:
    #             if self.prev_was_in_fight_options:
    #                 self.prev_was_in_fight_options = True
    #                 return False
    #             else:
    #                 self.prev_was_in_fight_options = True
    #                 return True
    #         else:
    #             self.prev_was_in_fight_options = False
    #             return False
    #     return False

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
