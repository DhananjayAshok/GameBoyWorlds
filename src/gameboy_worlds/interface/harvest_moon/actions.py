from gameboy_worlds.utils import log_error, log_warn
from gameboy_worlds.interface.action import HighLevelAction, SingleHighLevelAction
from gameboy_worlds.emulation.harvest_moon.parsers import (
    AgentState,
    HarvestMoonStateParser,
    BaseHarvestMoonStateParser,
)
from gameboy_worlds.emulation.harvest_moon.trackers import CoreHarvestMoonTracker
from gameboy_worlds.emulation import LowLevelActions
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
from gameboy_worlds.utils import show_frames
import numpy as np

from gymnasium.spaces import Box, Discrete, Text, OneOf
import matplotlib.pyplot as plt
from PIL import Image

HARD_MAX_STEPS = 5
""" The hard maximum number of steps we'll let agents take in a sequence """


def frame_changed(past: np.ndarray, preset: np.ndarray, epsilon=0.01):
    return np.abs(past - preset).mean() > epsilon


def _plot(past: np.ndarray, current: np.ndarray):
    # plot both side by side for debug
    fig, axs = plt.subplots(1, 2)
    axs[0].imshow(past)
    axs[1].imshow(current)
    plt.show()


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

    REQUIRED_STATE_PARSER = HarvestMoonStateParser
    REQUIRED_STATE_TRACKER = CoreHarvestMoonTracker

    def is_valid(self, **kwargs):
        """
        Just checks if the agent is in dialogue state.
        """
        return (
            self._state_tracker.get_episode_metric(("harvest_moon_core", "agent_state"))
            == AgentState.IN_DIALOGUE
        )

    def _execute(self):
        frames, done = self._emulator.step(LowLevelActions.PRESS_BUTTON_B)
        report = self._state_tracker.report()
        if not report["core"]["frame_changed"]:
            action_success = -1
        else:
            action_success = (
                0
                if self._emulator.state_parser.get_agent_state(frames[-1])
                != AgentState.IN_DIALOGUE
                else 1
            )
        return [report], action_success


class InteractAction(SingleHighLevelAction):
    """
    Presses the A button to interact with an object in front of the agent.

    Is Valid When:
    - In Free Roam State

    Action Success Interpretation:
    - -1: Frame did not change or agent still in free roam state
    - 1: Agent not in free roam state
    """

    REQUIRED_STATE_PARSER = HarvestMoonStateParser
    REQUIRED_STATE_TRACKER = CoreHarvestMoonTracker

    def is_valid(self, **kwargs):
        """
        Just checks if the agent is in free roam state.
        """
        return (
            self._state_tracker.get_episode_metric(("harvest_moon_core", "agent_state"))
            == AgentState.FREE_ROAM
        )

    def _execute(self):
        current_frame = self._emulator.get_current_frame()
        frames, done = self._emulator.step(LowLevelActions.PRESS_BUTTON_A)
        action_success = 0
        # Check if the frames have changed. Be strict and require all to not permit jittering screens.
        prev_frames = []
        for frame in frames:
            if (
                self._emulator.state_parser.get_agent_state(frame)
                != AgentState.FREE_ROAM
            ):  # something happened lol
                action_success = 1
                break
            for past_frame in prev_frames:
                if not frame_changed(past_frame, frame):
                    action_success = -1
                    break
            if action_success != 0:
                break
            prev_frames.append(frame)
        if action_success == 0:
            action_success = (
                -1
            )  # I guess? For some reason the previous thing doesn't catch same frames
        return [
            self._state_tracker.report()
        ], action_success  # 0 means something maybe happened. 1 means def happened.


class BaseMovementAction(HighLevelAction, ABC):
    """
    Base class for movement actions in the Harvest Moon environment.
    Has utility methods for moving in directions.

    Is Valid When:
    - In Free Roam State

    Action Success Interpretation:
    - -1: Frame did not change, even on the first step
    - 0: Finished all steps
    - 1: Took some steps, but not all, and then frame stopped changing OR the frame starts oscillating (trying to check for jitter). This usually means we ran into an obstacle.
    - 2: Took some steps, but agent state changed from free roam. This often means we entered a cutscene.

    Action Returns:
    - `n_steps_taken` (`int`): Number of steps actually taken
    - `rotated` (`bool` or `None`): True if the player has not moved, but has rotated. If the player has moved, this will be None. If it is False, it means the player tried to walk straight into an obstacle.
    """

    REQUIRED_STATE_TRACKER = CoreHarvestMoonTracker
    REQUIRED_STATE_PARSER = HarvestMoonStateParser

    def judge_movement(
        self, previous_frame: np.ndarray, current_frame: np.ndarray
    ) -> Tuple[bool, bool]:
        """
        Judges whether movement has occurred between two frames.

        Args:
            previous_frame (np.ndarray): The previous frame.
            current_frame (np.ndarray): The current frame.
        Returns:
            Tuple[bool, bool]: A tuple containing:
            - bool: True if movement has occurred, False otherwise.
            - bool: True if the player has not moved, but has rotated.
        """
        if not frame_changed(previous_frame, current_frame):
            return False, False
        return True, None

    def move(self, direction: str, steps: int) -> Tuple[np.ndarray, int]:
        """
        Move in a given direction for a number of steps.

        :param direction: One of "up", "down", "left", "right"
        :type direction: str
        :param steps: Number of steps to move in that direction
        :type steps: int
        :return:  A tuple containing:

                - A list of state tracker reports after each low level action executed. Length is equal to the number of low level actions executed.

                - An integer action success status
        :rtype: Tuple[ndarray[_AnyShape, dtype[Any]], int]
        """
        action_dict = {
            "right": LowLevelActions.PRESS_ARROW_RIGHT,
            "down": LowLevelActions.PRESS_ARROW_DOWN,
            "up": LowLevelActions.PRESS_ARROW_UP,
            "left": LowLevelActions.PRESS_ARROW_LEFT,
        }
        if direction not in action_dict.keys():
            log_error(f"Got invalid direction to move {direction}", self._parameters)
        action = action_dict[direction]
        # keep trying the action.
        # exit status 0 -> finished steps
        # 1 -> took some steps, but not all, and then frame stopped changing OR the frame starts oscillating (trying to check for jitter)
        # 2 -> took some steps, but agent state changed from free roam
        # -1 -> frame didn't change, even on the first step
        action_success = -1
        transition_state_dicts = []
        transition_frames = []
        previous_frame = (
            self._emulator.get_current_frame()
        )  # Do NOT get the state tracker frame, as it may have a grid on it.
        n_step = 0
        n_successful_steps = 0
        has_rotated = None
        agent_state = AgentState.FREE_ROAM
        while n_step < steps and agent_state == AgentState.FREE_ROAM:
            frames, done = self._emulator.step(action)
            transition_state_dicts.append(self._state_tracker.report())
            transition_frames.extend(frames)
            current_frame = (
                self._emulator.get_current_frame()
            )  # Do NOT use the emulator frame, as it may have a grid on it.
            if done:
                break
            # check if frames changed. If not, break out.
            player_moved, player_rotated = self.judge_movement(
                previous_frame, current_frame
            )
            if player_rotated == True:
                has_rotated = True
            if not player_moved and not player_rotated:
                break
            if player_moved:
                n_successful_steps += 1  # don't count rotation as a step
            agent_state = self._emulator.state_parser.get_agent_state(
                self._emulator.get_current_frame()
            )
            if agent_state != AgentState.FREE_ROAM:
                break
            n_step += 1
            previous_frame = current_frame
        if agent_state != AgentState.FREE_ROAM:
            action_success = 2
        else:
            if n_step <= 0:
                action_success = -1
            elif n_step == steps:
                action_success = 0
            else:
                action_success = 1
        transition_state_dicts[-1]["core"]["action_return"] = {
            "n_steps_taken": n_successful_steps,
            "rotated": has_rotated,
        }
        return transition_state_dicts, action_success

    def is_valid(self, **kwargs):
        """
        Just checks if the agent is in free roam state.
        """
        return (
            self._state_tracker.get_episode_metric(("harvest_moon_core", "agent_state"))
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
    - 1: Took some steps, but not all, and then frame stopped changing OR the frame starts oscillating (trying to check for jitter). This usually means we ran into an obstacle.
    - 2: Took some steps, but agent state changed from free roam. This often means we entered a cutscene.

    Action Returns:
    - `n_steps_taken` (`int`): Number of steps actually taken
    - `rotated` (`bool` or `None`): True if the player has not moved, but has rotated. If the player has moved, this will be None. If it is False, it means the player tried to walk straight into an obstacle.
    """

    def get_action_space(self):
        """
        Returns a Box space representing movement in 2D.
        The first dimension represents vertical movement (positive is up, negative is down).
        The second dimension represents horizontal movement (positive is right, negative is left).

        Returns:
            Box: A Box space with shape (2,) and values ranging from -HARD_MAX_STEPS//2 to HARD_MAX_STEPS//2.

        """
        return Discrete(4 * HARD_MAX_STEPS)

    def space_to_parameters(self, space_action):
        direction = None
        steps = None
        if space_action < 0 or space_action >= 4 * HARD_MAX_STEPS:
            # log_warn(f"Invalid space action {space_action}", self._parameters)
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
            # log_warn(f"Unrecognized direction {direction}", self._parameters)
            return None

    def _execute(self, direction, steps):
        transition_states, status = self.move(direction=direction, steps=steps)
        return transition_states, status

    def is_valid(self, **kwargs):
        direction = kwargs.get("direction")
        step = kwargs.get("step")
        if direction is not None and direction not in ["up", "down", "left", "right"]:
            return False
        if step is not None:
            if not isinstance(step, str):
                return False
            if step <= 0:
                return False
        return super().is_valid(**kwargs)


class MoveGridAction(BaseMovementAction):
    """
    Moves the agent on both axes. Will always try to move right first and then up.

    Is Valid When:
    - In Free Roam State
    Action Success Interpretation:
    - -1: Frame did not change, even on the first step
    - 0: Finished all steps
    - 1: Took some steps, but not all, and then frame stopped changing OR the frame starts oscillating (trying to check for jitter). This usually means we ran into an obstacle.
    - 2: Took some steps, but agent state changed from free roam. This often means we entered a cutscene.

    Action Returns:
    - `n_steps_taken` (`int`): Number of steps actually taken
    - `rotated` (`bool` or `None`): True if the player has not moved, but has rotated. If the player has moved, this will be None. If it is False, it means the player tried to walk straight into an obstacle.
    """

    def get_action_space(self):
        """
        Returns a Box space representing movement in 2D.
        The first dimension represents vertical movement (positive is up, negative is down).
        The second dimension represents horizontal movement (positive is right, negative is left).

        Returns:
            Box: A Box space with shape (2,) and values ranging from -HARD_MAX_STEPS//2 to HARD_MAX_STEPS//2.

        """
        return Box(
            low=-HARD_MAX_STEPS // 2,
            high=HARD_MAX_STEPS // 2,
            shape=(2,),
            dtype=np.int8,
        )

    def space_to_parameters(self, space_action):
        right_action = space_action[0]
        up_action = space_action[1]
        return {"x_steps": right_action, "y_steps": up_action}

    def parameters_to_space(self, x_steps, y_steps):
        move_vec = np.zeros(2)  # x, y
        move_vec[0] = x_steps
        move_vec[1] = y_steps
        return move_vec

    def _execute(self, x_steps, y_steps):
        x_direction = "right" if x_steps >= 0 else "left"
        y_direction = "up" if y_steps >= 0 else "down"
        if x_steps != 0:
            transition_states, status = self.move(
                direction=x_direction, steps=abs(x_steps)
            )
            if status != 0:
                return transition_states, status
        else:
            transition_states = []
        if y_steps != 0:
            more_transition_states, status = self.move(
                direction=y_direction, steps=abs(y_steps)
            )
            transition_states.extend(more_transition_states)
        try:
            status is not None
        except NameError:
            log_warn(
                f"Weird case where both x_steps and y_steps are 0 in MoveGridAction or something. {x_steps}, {y_steps}",
                self._parameters,
            )
            transition_states = [self._state_tracker.report()]
            status = -1
        return transition_states, status

    def is_valid(self, x_steps: int = None, y_steps: int = None):
        if x_steps is not None and y_steps is not None:
            if not isinstance(x_steps, int) or not isinstance(y_steps, int):
                return False
            if x_steps == 0 and y_steps == 0:
                return False
        return super().is_valid()

