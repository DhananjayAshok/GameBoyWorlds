from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple, List, Optional
from enum import Enum
from gameboy_worlds.emulation.emulator import LowLevelActions, Emulator
from gameboy_worlds.utils import (
    verify_parameters,
    log_info,
    log_warn,
    log_error,
    load_parameters,
    get_lowest_level_subclass,
)
from gameboy_worlds.emulation import StateTracker, StateParser

import numpy as np
from gymnasium.spaces import Space, Discrete


class HighLevelAction(ABC):
    """
    Abstract base class for high level actions.

    The execute() method performs the high level action and returns a list of state tracker reports after each low level action executed, along with an action success status.

    The docstring of each subclass should specify the interpretation of the action success status.

    The execute() method may also return some additional information in the final state tracker report under the "core" key, "action_return" subkey (usually as a dict itself)
    """

    REQUIRED_STATE_TRACKER = StateTracker
    """ The state tracker that tracks the minimal state information required for the action to function. """

    REQUIRED_STATE_PARSER = StateParser
    """ The state parser that parses the minimal state information required for the action to function. """

    def __init__(self, parameters: dict, seed: Optional[int] = None):
        verify_parameters(parameters)
        self._parameters = parameters
        self._rng = np.random.default_rng(seed)
        self.unassign_emulator()

    def seed(self, seed: Optional[int] = None):
        """
        Sets the random seed for the high level action.
        Args:
            seed (int): The random seed to set.
        """
        self._rng = np.random.default_rng(seed)

    def assign_emulator(self, emulator: Emulator):
        """
        Sets a reference to the emulator instance.
        Args:
            emulator (Emulator): The emulator instance to be tracked.
        """
        if not isinstance(emulator, Emulator):
            log_error(
                f"HighLevelAction requires an Emulator instance, but got {type(emulator)}",
                self._parameters,
            )
        self._emulator = emulator
        self._state_tracker = emulator.state_tracker
        if not issubclass(type(self._state_tracker), self.REQUIRED_STATE_TRACKER):
            log_error(
                f"HighLevelAction requires a StateTracker of type {self.REQUIRED_STATE_TRACKER}, but got {type(self._state_tracker)}",
                self._parameters,
            )
        if not issubclass(type(emulator.state_parser), self.REQUIRED_STATE_PARSER):
            log_error(
                f"HighLevelAction requires a StateParser of type {self.REQUIRED_STATE_PARSER}, but got {type(emulator.state_parser)}",
                self._parameters,
            )

    def unassign_emulator(self):
        """
        Clears the reference to the emulator instance.
        """
        self._emulator = None
        self._state_tracker = None

    @abstractmethod
    def get_action_space(self) -> Space:
        """
        Returns the Gym defined Space that characterizes the high level action's parameter space.

        You can use this API to get a Space for sampling high level actions of this type.

        Returns:
            Space: The Gym space that characterizes the high level action's parameter space.
        """
        raise NotImplementedError

    @abstractmethod
    def space_to_parameters(self, space_action: Space) -> Optional[Dict[str, Any]]:
        """
        Converts a Gym space action into high level action parameters.
        If the provided space action is invalid, return None.

        :param space_action: The action in the high level action's parameter space.
        :type space_action: Space
        :return: The high level action's parameters corresponding to the space action.
        :rtype: Optional[Dict[str, Any]]
        """
        raise NotImplementedError

    @abstractmethod
    def parameters_to_space(self, **kwargs) -> Optional[Space]:
        """
        Converts high level action parameters into a Gym space action.
        If the provided parameters are invalid, return None.

        :param kwargs: The high level action's parameters.
        :type kwargs: Dict[str, Any]
        :return: The action in the high level action's parameter space.
        :rtype: Optional[Space]
        """
        raise NotImplementedError

    @abstractmethod
    def is_valid(self, **kwargs) -> bool:
        """
        Checks if the high level action can be performed in the current state.
        If kwargs is empty, then must check whether there exists any valid way to perform the action.

        Args:
            **kwargs: Additional arguments required for the specific high level action.
        Returns:
            bool: Whether the action is valid in the current state.
        """
        raise NotImplementedError

    @abstractmethod
    def _execute(self, **kwargs) -> Tuple[List[Dict[str, Dict[str, Any]]], int]:
        """
        Executes the specified, valid high level action on the emulator.
        Does not check for validity, assumes the action is valid.

        :param self: Description
        :param kwargs: Additional arguments required for the specific high level action.
        :return:
            - A list of state tracker reports after each low level action executed.

            - Action success status.
        :rtype: Tuple[List[Dict[str, Dict[str, Any]]], int]
        """
        raise NotImplementedError

    def get_all_valid_parameters(self) -> List[Dict[str, Any]]:
        """
        Returns a list of all valid parameterizations for the high level action in the current state.

        May not well defined for all high level actions, because some high level actions may have infinite parameterizations. (e.g. move to any (x, y) position.)

        Use this to enumerate all valid ways to perform the action, and provide a way to sample over all valid parameterizations.


        Returns:

            List[Dict[str, Any]]: A list of valid parameterizations for the high level action.
        """
        raise ValueError(
            "This high level action does not implement get_all_valid_parameters(). Most likely, it is not possible to enumerate an exhaustive list of all valid inputs. Use is_valid() instead. See documentation for more details. If you believe this is an error, please implement get_all_valid_parameters() in the high level action subclass."
        )

    def execute(
        self, **kwargs
    ) -> Tuple[Optional[List[Dict[str, Dict[str, Any]]]], Optional[int]]:
        """
        Executes the specified high level action on the emulator after checking for validity.

        :param kwargs: Additional arguments required for the specific high level action.
        :return: None, None if the action is not valid. Otherwise:

            - A list of state tracker reports after each low level action executed.

            - Action success status.
        :rtype: Tuple[Optional[List[Dict[str, Dict[str, Any]]]], Optional[int]]
        """
        if self._emulator is None:
            log_error(
                f"Tried to execute action on HighLevelAction without an emulator",
                self._parameters,
            )
        if not self.is_valid(**kwargs):
            return None, None
        return self._execute(**kwargs)

    def execute_space_action(
        self, space_action: Space
    ) -> Tuple[Optional[List[Dict[str, Dict[str, Any]]]], Optional[int]]:
        """
        Executes the specified high level action on the emulator after checking for validity.

        :param space_action: The action in the high level action's parameter space.
        :type space_action: Space
        :return: None, None if the action is not valid. Otherwise:

            - A list of state tracker reports after each low level action executed.

            - Action success status.
        :rtype: Tuple[Optional[List[Dict[str, Dict[str, Any]]]], Optional[int]]
        """
        parameters = self.space_to_parameters(space_action)
        if parameters is None:
            return None, None
        return self.execute(**parameters)

    @staticmethod
    @abstractmethod
    def get_action_name(**kwargs) -> str:
        """
        Returns a human readable name for the high level action with the given parameters.

        :param kwargs: The high level action's parameters.
        :type kwargs: Dict[str, Any]
        :return: A human readable name for the high level action.
        :rtype: str
        """
        raise NotImplementedError


class SingleHighLevelAction(HighLevelAction):
    """
    An abstract class for a high level action that has only one possible parameterization.
    """

    def space_to_parameters(self, space_action):
        return {}

    def parameters_to_space(self):
        return 0

    def get_action_space(self):
        return Discrete(1)

    def get_all_valid_parameters(self):
        if self.is_valid():
            return [{}]
        else:
            return []


class LowLevelAction(HighLevelAction):
    """A high level action that directly maps to a single low level action."""

    def get_action_space(self):
        """
        Returns the Gym defined Space that characterizes the low level action's parameter space.
        """
        return Discrete(len(LowLevelActions))

    def space_to_parameters(self, space_action: Space) -> Dict[str, Any]:
        action = list(LowLevelActions)[space_action]
        return {"low_level_action": action}

    def parameters_to_space(self, low_level_action: LowLevelActions) -> Space:
        if low_level_action is None or not isinstance(
            low_level_action, LowLevelActions
        ):
            # log_warn(
            #    "LowLevelAction requires a 'low_level_action' parameter of type LowLevelActions.",
            #    self._parameters,
            # )
            return None
        return low_level_action.value

    def _execute(
        self, low_level_action: LowLevelActions
    ) -> Tuple[List[Dict[str, Dict[str, Any]]], int]:
        self._emulator.step(low_level_action)
        state_report = self._state_tracker.report()
        return [
            state_report
        ], 0  # Low level actions are always successful in this context.

    def is_valid(self, low_level_action: LowLevelActions) -> bool:
        """
        Checks if the low level action can be performed in the current state.

        Args:
            low_level_action (LowLevelActions): The low level action to check.
        Returns:
            bool: Whether the action is valid in the current state.
        """
        return True

    def get_all_valid_parameters(self) -> List[Dict[str, Any]]:
        """
        Returns a list of all valid low level actions in the current state.

        :return: A list of valid low level actions.
        :rtype: List[Dict[str, Any]]
        """
        return [{"low_level_action": action} for action in LowLevelActions]

    @staticmethod
    def get_action_name(low_level_action: LowLevelActions) -> str:
        action = (
            str(low_level_action)
            .replace("LowLevelActions.PRESS_ARROW_", "")
            .replace("LowLevelActions.PRESS_BUTTON_", "")
        )
        return action


class LowLevelPlayAction(HighLevelAction):
    """A HighLevelAction subclass that directly maps to low level actions, except no menu button presses."""

    def __init__(self, parameters: dict, seed: Optional[int] = None):
        self.allowed_actions = [
            LowLevelActions.PRESS_ARROW_UP,
            LowLevelActions.PRESS_ARROW_DOWN,
            LowLevelActions.PRESS_ARROW_RIGHT,
            LowLevelActions.PRESS_ARROW_LEFT,
            LowLevelActions.PRESS_BUTTON_A,
            LowLevelActions.PRESS_BUTTON_B,
        ]
        super().__init__(parameters, seed=seed)

    def get_action_space(self):
        """
        Returns the Gym defined Space that characterizes the low level play action's parameter space.
        """
        return Discrete(len(self.allowed_actions))

    def space_to_parameters(self, space_action: Space) -> Dict[str, Any]:
        action = self.allowed_actions[space_action]
        return {"low_level_action": action}

    def parameters_to_space(self, low_level_action: LowLevelActions) -> Space:
        if low_level_action is None or low_level_action not in self.allowed_actions:
            # log_warn(
            #    "LowLevelPlayAction requires a 'low_level_action' parameter that is not a menu button press.",
            #    self._parameters,
            # )
            return None
        return self.allowed_actions.index(low_level_action)

    def _execute(
        self, low_level_action: LowLevelActions
    ) -> Tuple[List[Dict[str, Dict[str, Any]]], int]:
        self._emulator.step(low_level_action)
        state_report = self._state_tracker.report()
        return [
            state_report
        ], 0  # Low level actions are always successful in this context.

    def is_valid(self, low_level_action: LowLevelActions) -> bool:
        return low_level_action in self.allowed_actions

    def get_all_valid_parameters(self) -> List[Dict[str, Any]]:
        return [{"low_level_action": action} for action in self.allowed_actions]

    @staticmethod
    def get_action_name(low_level_action: LowLevelActions) -> str:
        action = (
            str(low_level_action)
            .replace("LowLevelActions.PRESS_ARROW_", "")
            .replace("LowLevelActions.PRESS_BUTTON_", "")
        )
        return action


class RandomPlayAction(HighLevelAction):
    """Execution either moves or presses A

    Action Success Interpretation:

    - 0: The frame changed after the action
    - 1: The frame did not change after the action

    """

    def get_action_space(self):
        """
        Returns the Gym defined Space that characterizes the random play action's parameter space.
        """
        return Discrete(2)  # 0 for move, 1 for press A

    def space_to_parameters(self, space_action: Space) -> Dict[str, Any]:
        if space_action == 0:
            return {"kind": "move"}
        else:
            return {"kind": "press"}

    def parameters_to_space(self, kind: str) -> Space:
        if kind == "move":
            return 0
        elif kind == "press":
            return 1
        else:
            # log_warn(
            #    "RandomPlayAction requires a 'kind' parameter of either 'move' or 'press'.",
            #    self._parameters,
            # )
            return None

    def _execute(self, kind: str):
        if kind == "move":
            actions = [
                LowLevelActions.PRESS_ARROW_DOWN,
                LowLevelActions.PRESS_ARROW_LEFT,
                LowLevelActions.PRESS_ARROW_RIGHT,
                LowLevelActions.PRESS_ARROW_UP,
            ]

        else:  # kind must be 'press'. Enforced in is_valid
            actions = [
                LowLevelActions.PRESS_BUTTON_A,
            ]
        action = self._rng.choice(actions)
        self._emulator.step(action)
        state_report = self._state_tracker.report()
        not_success = not state_report["core"][
            "frame_changed"
        ]  # Whether the frame changed after the action
        return [state_report], not_success

    def is_valid(self, kind: str) -> bool:
        if kind not in ["move", "press"]:
            return False
        return True

    def get_all_valid_parameters(self) -> List[Dict[str, Any]]:
        return [{"kind": "move"}, {"kind": "press"}]

    @staticmethod
    def get_action_name(kind: str) -> str:
        return kind
