from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from gymnasium.spaces import Discrete

from gameboy_worlds.emulation import LowLevelActions
from gameboy_worlds.emulation.legend_of_zelda.parsers import BaseLegendOfZeldaParser
from gameboy_worlds.emulation.legend_of_zelda.trackers import CoreLegendOfZeldaTracker
from gameboy_worlds.interface.action import HighLevelAction, SingleHighLevelAction

HARD_MAX_STEPS = 5

STATE_METRIC_KEY = ("legend_of_zelda_core", "agent_state")
FREE_ROAM = "free_roam"
IN_DIALOGUE = "in_dialogue"
IN_INVENTORY = "in_inventory"


def frame_changed(previous: np.ndarray, current: np.ndarray, epsilon=0.01) -> bool:
    return np.abs(previous - current).mean() > epsilon


class MoveAction(HighLevelAction):
    """
    Move in a cardinal direction for a number of steps.
    """

    REQUIRED_STATE_TRACKER = CoreLegendOfZeldaTracker
    REQUIRED_STATE_PARSER = BaseLegendOfZeldaParser

    _DIRECTION_TO_ACTION = {
        "up": LowLevelActions.PRESS_ARROW_UP,
        "down": LowLevelActions.PRESS_ARROW_DOWN,
        "left": LowLevelActions.PRESS_ARROW_LEFT,
        "right": LowLevelActions.PRESS_ARROW_RIGHT,
    }

    def get_action_space(self):
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
        if (
            direction not in self._DIRECTION_TO_ACTION
            or steps <= 0
            or steps > HARD_MAX_STEPS
        ):
            return None
        offset = {"up": 0, "down": 1, "left": 2, "right": 3}[direction] * HARD_MAX_STEPS
        return offset + steps - 1

    def is_valid(self, **kwargs):
        direction = kwargs.get("direction", None)
        steps = kwargs.get("steps", None)
        if direction is not None and direction not in self._DIRECTION_TO_ACTION:
            return False
        if steps is not None and (not isinstance(steps, int) or steps <= 0):
            return False
        return self._state_tracker.get_episode_metric(STATE_METRIC_KEY) == FREE_ROAM

    def _execute(self, direction: str, steps: int):
        action = self._DIRECTION_TO_ACTION[direction]
        transition_state_dicts: List[Dict[str, Dict[str, Any]]] = []
        n_steps_taken = 0
        previous_frame = self._emulator.get_current_frame()
        action_success = -1
        for _ in range(steps):
            frames, done = self._emulator.step(action)
            report = self._state_tracker.report()
            transition_state_dicts.append(report)
            current_frame = frames[-1]
            if not frame_changed(previous_frame, current_frame):
                action_success = 1 if n_steps_taken > 0 else -1
                break
            n_steps_taken += 1
            state = self._state_tracker.get_episode_metric(STATE_METRIC_KEY)
            if state != FREE_ROAM:
                action_success = 2
                break
            if done:
                action_success = 0
                break
            previous_frame = current_frame
        else:
            action_success = 0
        if len(transition_state_dicts) > 0:
            transition_state_dicts[-1]["core"]["action_return"] = {
                "n_steps_taken": n_steps_taken
            }
        return transition_state_dicts, action_success

    @staticmethod
    def get_action_name(direction: str, steps: int) -> str:
        return f"Move {direction} {steps}"


class OpenInventoryAction(SingleHighLevelAction):
    REQUIRED_STATE_TRACKER = CoreLegendOfZeldaTracker
    REQUIRED_STATE_PARSER = BaseLegendOfZeldaParser

    def is_valid(self, **kwargs):
        return self._state_tracker.get_episode_metric(STATE_METRIC_KEY) == FREE_ROAM

    def _execute(self):
        previous = self._emulator.get_current_frame()
        frames, done = self._emulator.step(LowLevelActions.PRESS_BUTTON_START)
        report = self._state_tracker.report()
        state = self._state_tracker.get_episode_metric(STATE_METRIC_KEY)
        if not frame_changed(previous, frames[-1]):
            return [report], -1
        return [report], 1 if state == IN_INVENTORY else 0

    @staticmethod
    def get_action_name() -> str:
        return "OpenInventory"


class CloseInventoryAction(SingleHighLevelAction):
    REQUIRED_STATE_TRACKER = CoreLegendOfZeldaTracker
    REQUIRED_STATE_PARSER = BaseLegendOfZeldaParser

    def is_valid(self, **kwargs):
        return self._state_tracker.get_episode_metric(STATE_METRIC_KEY) == IN_INVENTORY

    def _execute(self):
        previous = self._emulator.get_current_frame()
        frames, done = self._emulator.step(LowLevelActions.PRESS_BUTTON_START)
        report = self._state_tracker.report()
        state = self._state_tracker.get_episode_metric(STATE_METRIC_KEY)
        if not frame_changed(previous, frames[-1]):
            return [report], -1
        return [report], 1 if state != IN_INVENTORY else 0

    @staticmethod
    def get_action_name() -> str:
        return "CloseInventory"


class SkipDialogueAction(SingleHighLevelAction):
    REQUIRED_STATE_TRACKER = CoreLegendOfZeldaTracker
    REQUIRED_STATE_PARSER = BaseLegendOfZeldaParser

    def is_valid(self, **kwargs):
        return self._state_tracker.get_episode_metric(STATE_METRIC_KEY) == IN_DIALOGUE

    def _execute(self):
        previous = self._emulator.get_current_frame()
        frames, done = self._emulator.step(LowLevelActions.PRESS_BUTTON_B)
        report = self._state_tracker.report()
        state = self._state_tracker.get_episode_metric(STATE_METRIC_KEY)
        if not frame_changed(previous, frames[-1]):
            return [report], -1
        return [report], 0 if state != IN_DIALOGUE else 1

    @staticmethod
    def get_action_name() -> str:
        return "SkipDialogue"


class InteractAction(SingleHighLevelAction):
    REQUIRED_STATE_TRACKER = CoreLegendOfZeldaTracker
    REQUIRED_STATE_PARSER = BaseLegendOfZeldaParser

    def is_valid(self, **kwargs):
        return self._state_tracker.get_episode_metric(STATE_METRIC_KEY) == FREE_ROAM

    def _execute(self):
        previous = self._emulator.get_current_frame()
        frames, done = self._emulator.step(LowLevelActions.PRESS_BUTTON_A)
        report = self._state_tracker.report()
        state = self._state_tracker.get_episode_metric(STATE_METRIC_KEY)
        if not frame_changed(previous, frames[-1]):
            return [report], -1
        return [report], 1 if state != FREE_ROAM else 0

    @staticmethod
    def get_action_name() -> str:
        return "Interact"


class UseOtherInventoryItemAction(SingleHighLevelAction):
    """
    Uses the secondary equipped item (B button) while in free roam.
    """

    REQUIRED_STATE_TRACKER = CoreLegendOfZeldaTracker
    REQUIRED_STATE_PARSER = BaseLegendOfZeldaParser

    def is_valid(self, **kwargs):
        return self._state_tracker.get_episode_metric(STATE_METRIC_KEY) == FREE_ROAM

    def _execute(self):
        previous = self._emulator.get_current_frame()
        frames, done = self._emulator.step(LowLevelActions.PRESS_BUTTON_B)
        report = self._state_tracker.report()
        if not frame_changed(previous, frames[-1]):
            return [report], -1
        return [report], 0

    @staticmethod
    def get_action_name() -> str:
        return "UseOtherInventoryItem"
