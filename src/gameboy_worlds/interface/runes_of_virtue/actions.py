from gameboy_worlds.utils import log_error, log_warn
from gameboy_worlds.interface.action import HighLevelAction, SingleHighLevelAction
from gameboy_worlds.emulation.runes_of_virtue.parsers import (
    AgentState,
    RunesOfVirtueStateParser,
)
from gameboy_worlds.emulation.runes_of_virtue.trackers import CoreRunesOfVirtueTracker
from gameboy_worlds.emulation import LowLevelActions
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
import numpy as np

from gymnasium.spaces import Discrete


HARD_MAX_STEPS = 5
""" The hard maximum number of steps we'll let agents take in a sequence """


def frame_changed(past: np.ndarray, preset: np.ndarray, epsilon=0.01):
    return np.abs(past - preset).mean() > epsilon


class PassDialogueAction(SingleHighLevelAction):
    """
    Skips dialogue by pressing the B button.

    Is Valid When:
    - In Dialogue State

    Action Success Interpretation:
    - -1: Frame did not change
    - 0: Frame changed and no longer in dialogue state
    - 1: Frame changed but still in dialogue state
    """

    REQUIRED_STATE_PARSER = RunesOfVirtueStateParser
    REQUIRED_STATE_TRACKER = CoreRunesOfVirtueTracker

    def is_valid(self, **kwargs):
        """
        Just checks if the agent is in dialogue state.
        """
        return (
            self._state_tracker.get_episode_metric(
                ("runes_of_virtue_core", "agent_state")
            )
            == AgentState.IN_DIALOGUE
        )

    def _execute(self):
        previous_frame = self._emulator.get_current_frame()
        frames, done = self._emulator.step(LowLevelActions.PRESS_BUTTON_B)
        report = self._state_tracker.report()
        if not frame_changed(previous_frame, frames[-1]):
            action_success = -1
        else:
            action_success = (
                0
                if self._emulator.state_parser.get_agent_state(frames[-1])
                != AgentState.IN_DIALOGUE
                else 1
            )
        return [report], action_success

    @staticmethod
    def get_action_name() -> str:
        return "PassDialogue"


class InteractAction(SingleHighLevelAction):
    """
    Presses the A button to interact with an object in front of the agent.

    Is Valid When:
    - In Free Roam State

    Action Success Interpretation:
    - -1: Frame did not change or agent still in free roam state
    - 1: Agent not in free roam state
    """

    REQUIRED_STATE_PARSER = RunesOfVirtueStateParser
    REQUIRED_STATE_TRACKER = CoreRunesOfVirtueTracker

    def is_valid(self, **kwargs):
        """
        Just checks if the agent is in free roam state.
        """
        return (
            self._state_tracker.get_episode_metric(
                ("runes_of_virtue_core", "agent_state")
            )
            == AgentState.FREE_ROAM
        )

    def _execute(self):
        previous_frame = self._emulator.get_current_frame()
        frames, done = self._emulator.step(LowLevelActions.PRESS_BUTTON_A)
        report = self._state_tracker.report()
        action_success = -1
        for frame in frames:
            if (
                self._emulator.state_parser.get_agent_state(frame)
                != AgentState.FREE_ROAM
            ):
                action_success = 1
                break
            if frame_changed(previous_frame, frame):
                action_success = 0
        return [report], action_success

    @staticmethod
    def get_action_name() -> str:
        return "Interact"


class OpenMenuAction(SingleHighLevelAction):
    """
    Opens the inventory/status menu by pressing the START button.

    Is Valid When:
    - In Free Roam State

    Action Success Interpretation:
    - -1: Frame did not change
    - 0: Menu opened successfully (agent now in IN_MENU state)
    - 1: Frame changed but agent not in menu state
    """

    REQUIRED_STATE_PARSER = RunesOfVirtueStateParser
    REQUIRED_STATE_TRACKER = CoreRunesOfVirtueTracker

    def is_valid(self, **kwargs):
        """
        Checks if the agent is in free roam state.
        """
        return (
            self._state_tracker.get_episode_metric(
                ("runes_of_virtue_core", "agent_state")
            )
            == AgentState.FREE_ROAM
        )

    def _execute(self):
        previous_frame = self._emulator.get_current_frame()
        frames, done = self._emulator.step(LowLevelActions.PRESS_BUTTON_START)
        report = self._state_tracker.report()
        if not frame_changed(previous_frame, frames[-1]):
            action_success = -1
        elif self._emulator.state_parser.is_in_menu(frames[-1]):
            action_success = 0
        else:
            action_success = 1
        return [report], action_success

    @staticmethod
    def get_action_name() -> str:
        return "OpenMenu"


class BaseMovementAction(HighLevelAction, ABC):
    """
    Base class for movement actions in the Runes of Virtue environment.
    Has utility methods for moving in directions.

    Is Valid When:
    - In Free Roam State

    Action Success Interpretation:
    - -1: Frame did not change, even on the first step
    - 0: Finished all steps
    - 1: Took some steps, but not all, and then frame stopped changing. This usually means we ran into an obstacle.
    - 2: Took some steps, but agent state changed from free roam. This often means we entered a dialogue or menu.

    Action Returns:
    - `n_steps_taken` (`int`): Number of steps actually taken

    Known Limitations:
    - Uses single-frame change detection. RoV maps do not have the consistent tile-grid texture needed for Pokemon-style quadrant-uniformity analysis, so obstacle detection may be less precise than Pokemon's `BaseMovementAction`.
    """

    REQUIRED_STATE_TRACKER = CoreRunesOfVirtueTracker
    REQUIRED_STATE_PARSER = RunesOfVirtueStateParser

    def move(self, direction: str, steps: int) -> Tuple[List[Dict], int]:
        """
        Move in a given direction for a number of steps.

        :param direction: One of "up", "down", "left", "right"
        :type direction: str
        :param steps: Number of steps to move in that direction
        :type steps: int
        :return: A tuple containing:

                - A list of state tracker reports after each low level action executed.

                - An integer action success status.
        :rtype: Tuple[List[Dict], int]
        """
        action_dict = {
            "right": LowLevelActions.PRESS_ARROW_RIGHT,
            "down": LowLevelActions.PRESS_ARROW_DOWN,
            "up": LowLevelActions.PRESS_ARROW_UP,
            "left": LowLevelActions.PRESS_ARROW_LEFT,
        }
        if direction not in action_dict:
            log_error(f"Got invalid direction to move {direction}", self._parameters)
        action = action_dict[direction]
        transition_state_dicts = []
        previous_frame = self._emulator.get_current_frame()
        n_step = 0
        n_successful_steps = 0
        agent_state = AgentState.FREE_ROAM
        while n_step < steps and agent_state == AgentState.FREE_ROAM:
            frames, done = self._emulator.step(action)
            transition_state_dicts.append(self._state_tracker.report())
            current_frame = self._emulator.get_current_frame()
            if done:
                break
            if not frame_changed(previous_frame, current_frame):
                # obstacle: frame did not change
                break
            n_successful_steps += 1
            agent_state = self._emulator.state_parser.get_agent_state(current_frame)
            if agent_state != AgentState.FREE_ROAM:
                break
            n_step += 1
            previous_frame = current_frame
        if agent_state != AgentState.FREE_ROAM:
            action_success = 2
        elif n_successful_steps == 0:
            action_success = -1
        elif n_successful_steps == steps:
            action_success = 0
        else:
            action_success = 1
        if transition_state_dicts:
            transition_state_dicts[-1]["core"]["action_return"] = {
                "n_steps_taken": n_successful_steps,
            }
        return transition_state_dicts, action_success

    def is_valid(self, **kwargs):
        """
        Just checks if the agent is in free roam state.
        """
        return (
            self._state_tracker.get_episode_metric(
                ("runes_of_virtue_core", "agent_state")
            )
            == AgentState.FREE_ROAM
        )


class MoveStepsAction(BaseMovementAction):
    """
    Moves the agent in a specified cardinal direction for a specified number of steps.

    Is Valid When:
    - In Free Roam State

    Action Success Interpretation:
    - -1: Frame did not change, even on the first step
    - 0: Finished all steps
    - 1: Took some steps, but not all, and then frame stopped changing. This usually means we ran into an obstacle.
    - 2: Took some steps, but agent state changed from free roam. This often means we entered a dialogue or menu.

    Action Returns:
    - `n_steps_taken` (`int`): Number of steps actually taken
    """

    def get_action_space(self):
        """
        Returns a Discrete space encoding (direction, steps).
        4 directions × HARD_MAX_STEPS step counts.
        """
        return Discrete(4 * HARD_MAX_STEPS)

    def space_to_parameters(self, space_action):
        if space_action < 0 or space_action >= 4 * HARD_MAX_STEPS:
            return None
        if space_action < HARD_MAX_STEPS:
            direction = "up"
            steps = space_action
        elif space_action < 2 * HARD_MAX_STEPS:
            direction = "down"
            steps = space_action - HARD_MAX_STEPS
        elif space_action < 3 * HARD_MAX_STEPS:
            direction = "left"
            steps = space_action - 2 * HARD_MAX_STEPS
        else:
            direction = "right"
            steps = space_action - 3 * HARD_MAX_STEPS
        return {"direction": direction, "steps": steps + 1}

    def parameters_to_space(self, direction: str, steps: int):
        if steps <= 0 or steps > HARD_MAX_STEPS:
            return None
        if direction == "up":
            return steps - 1
        elif direction == "down":
            return HARD_MAX_STEPS + steps - 1
        elif direction == "left":
            return 2 * HARD_MAX_STEPS + steps - 1
        elif direction == "right":
            return 3 * HARD_MAX_STEPS + steps - 1
        else:
            return None

    def _execute(self, direction, steps):
        transition_states, status = self.move(direction=direction, steps=steps)
        return transition_states, status

    def is_valid(self, **kwargs):
        direction = kwargs.get("direction")
        steps = kwargs.get("steps")
        if direction is not None and direction not in ["up", "down", "left", "right"]:
            return False
        if steps is not None:
            if not isinstance(steps, int):
                return False
            if steps <= 0 or steps > HARD_MAX_STEPS:
                return False
        return super().is_valid(**kwargs)

    @staticmethod
    def get_action_name(direction: str, steps: int) -> str:
        return f"Move {direction} {steps}"


class MenuAction(HighLevelAction):
    """
    Allows simple navigation and option selection of menus.

    Is Valid When:
    - In Menu State

    Action Success Interpretation:
    - -1: Frame did not change.
    - 0: Frame changed.
    """

    REQUIRED_STATE_PARSER = RunesOfVirtueStateParser
    REQUIRED_STATE_TRACKER = CoreRunesOfVirtueTracker

    _MENU_ACTION_MAP = {
        "up": LowLevelActions.PRESS_ARROW_UP,
        "down": LowLevelActions.PRESS_ARROW_DOWN,
        "confirm": LowLevelActions.PRESS_BUTTON_A,
        "left": LowLevelActions.PRESS_ARROW_LEFT,
        "right": LowLevelActions.PRESS_ARROW_RIGHT,
        "back": LowLevelActions.PRESS_BUTTON_B,
    }

    _MENU_ACTION_KEYS = list(_MENU_ACTION_MAP.keys())

    def is_valid(self, **kwargs):
        """
        Checks if the menu action is valid in the current state.

        Args:
            menu_action (str, optional): The menu action to check.
        Returns:
            bool: True if the action is valid, False otherwise.
        """
        menu_action = kwargs.get("menu_action", None)
        if menu_action is not None:
            if menu_action not in self._MENU_ACTION_KEYS:
                return False
        state = self._state_tracker.get_episode_metric(
            ("runes_of_virtue_core", "agent_state")
        )
        return state == AgentState.IN_MENU

    def get_action_space(self):
        """
        Returns a Discrete space representing menu actions.
        """
        return Discrete(len(self._MENU_ACTION_MAP))

    def parameters_to_space(self, menu_action):
        if menu_action not in self._MENU_ACTION_KEYS:
            return None
        return self._MENU_ACTION_KEYS.index(menu_action)

    def space_to_parameters(self, space_action):
        if space_action < 0 or space_action >= len(self._MENU_ACTION_MAP):
            return None
        return {"menu_action": self._MENU_ACTION_KEYS[space_action]}

    def _execute(self, menu_action):
        action = self._MENU_ACTION_MAP[menu_action]
        current_frame = self._emulator.get_current_frame()
        frames, done = self._emulator.step(action)
        action_success = 0 if frame_changed(current_frame, frames[-1]) else -1
        return [self._state_tracker.report()], action_success

    @staticmethod
    def get_action_name(menu_action: str) -> str:
        return f"Menu {menu_action}"
