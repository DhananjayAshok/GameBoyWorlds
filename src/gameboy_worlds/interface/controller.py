from abc import ABC
from typing import Any, Dict, Tuple, List, Optional, Type
from gameboy_worlds.utils import (
    verify_parameters,
    log_info,
    log_warn,
    log_error,
    load_parameters,
    get_lowest_level_subclass,
)
from gameboy_worlds.emulation.emulator import Emulator, LowLevelActions
from gameboy_worlds.interface.action import (
    HighLevelAction,
    LowLevelAction,
    RandomPlayAction,
    LowLevelPlayAction,
)

import numpy as np
from gymnasium.spaces import OneOf, Space


class Controller(ABC):
    """
    Abstract base class for controllers interfacing with the emulator.
    Handles conversion between high level actions and Gym action spaces.

    """

    ACTIONS: List[Type[HighLevelAction]] = [HighLevelAction]
    """ A list of HighLevelAction classes that define the possible high level actions. 
    This is (almost) always, the only part that must be customized in subclasses.
    """

    def __init__(self, parameters: Optional[dict] = None, seed: Optional[int] = None):
        self._parameters = load_parameters(parameters)
        self.actions: List[HighLevelAction] = [
            action(self._parameters) for action in self.ACTIONS
        ]
        """ A list of instantiated high level actions. """
        self.REQUIRED_STATE_TRACKER = get_lowest_level_subclass(
            [action.REQUIRED_STATE_TRACKER for action in self.actions]
        )
        """ The required state tracker class inferred from the high level actions. """
        self.action_space = OneOf(
            [action.get_action_space() for action in self.actions]
        )
        """ The Gym action Space consisting of a choice over all high level action spaces. """
        self.unassign_emulator()
        if seed is not None:
            self.seed(seed)

    def seed(self, seed: Optional[int] = None):
        """
        Sets the random seed for the controller and its actions.
        Args:
            seed (int): The random seed to set.
        """
        self._rng = np.random.default_rng(seed)
        self.action_space.seed(seed)
        seed_value = seed
        for action in self.actions:
            if isinstance(seed, int):
                seed_value = (
                    seed + 1
                )  # Simple way to get different seeds for each action
            else:
                seed_value = None
            action.seed(seed_value)

    def unassign_emulator(self):
        """
        Clears the reference to the emulator instance.
        """
        self._emulator = None
        for action in self.actions:
            action.unassign_emulator()

    def assign_emulator(self, emulator: Emulator):
        """
        Sets a reference to the emulator instance.
        Args:
            emulator (Emulator): The emulator instance to be tracked.
        """
        for action in self.actions:
            action.assign_emulator(emulator)
        self._emulator = emulator

    def get_action_space(self) -> OneOf:
        """
        Getter for the controller's Gym action space.
        Returns:
            OneOf: The Gym action Space consisting of a choice over all high level action spaces.
        """
        return self.action_space

    def sample(self) -> OneOf:
        """
        Samples a random action from the controller's action space.
        Returns:
            OneOf: A random action from the controller's action space.
        """
        return self.action_space.sample()

    def _space_action_to_high_level_action(
        self, space_action: OneOf
    ) -> Tuple[HighLevelAction, Dict[str, Any]]:
        """
        Interprets a Gym space action into a high level action and its parameters.

        :param space_action: The action in the controller's action space.
        :type space_action: OneOf
        :return: The high level action and its parameters.
        :rtype: Tuple[HighLevelAction, Dict[str, Any]]
        """
        action_index, space_action = space_action
        action = self.actions[action_index]
        action_class = self.ACTIONS[action_index]
        parameters = action.space_to_parameters(space_action)
        return action_class, parameters

    def _high_level_action_to_space_action(
        self, action: HighLevelAction, **kwargs
    ) -> OneOf:
        """
        Converts a high level action and its parameters into a Gym Space action.

        Args:
            action (HighLevelAction): The high level action to convert.
            **kwargs: Additional arguments required for the specific high level action.
        Returns:
            OneOf: The action in the controller's action space.
        """
        space_action = action.parameters_to_space(**kwargs)
        if space_action is None:
            return None
        action_index = self.actions.index(action)
        return (action_index, space_action)

    def _emulator_running(self) -> bool:
        """
        Checks if the emulator is currently running.

        Returns:
            bool: True if the emulator is running, False otherwise.
        """
        if self._emulator is None:
            log_error(
                "Emulator reference not assigned to controller.", self._parameters
            )
        return not self._emulator.check_if_done()

    def is_valid(self, action: Type[HighLevelAction], **kwargs) -> bool:
        """
        Checks if the specified high level action can be performed in the current state.

        Args:
            action (HighLevelAction): The high level action class to check.
            **kwargs: Additional arguments required for the specific high level action.
        Returns:
            bool: True if the action is valid, False otherwise.
        """
        if not self._emulator_running():
            return False
        if action not in self.ACTIONS:
            log_error(
                "Action not recognized by controller. Are you passing in an instance of the action class?",
                self._parameters,
            )
        # Find the action instance
        action_index = self.ACTIONS.index(action)
        checking_action = self.actions[action_index]
        return checking_action.is_valid(**kwargs)

    def get_valid_high_level_actions(
        self,
    ) -> Dict[Type[HighLevelAction], List[Dict[str, Any]]]:
        """
        Returns a list of all valid high level actions (including valid parameter inputs) that can be performed in the current state.

        WARNING: Will fail if there are high level actions with infinite valid parameterizations. Use get_possibly_valid_high_level_actions() instead if that is the case.

        :return: A dictionary mapping high level actions to their corresponding valid parameterizations.
        :rtype: Dict[type[HighLevelAction], List[Dict[str, Any]]]
        """
        valid_actions = {}
        if not self._emulator_running():
            return valid_actions
        for action in self.actions:
            valid_parameters = action.get_all_valid_parameters()
            if len(valid_parameters) > 0:
                valid_actions[action] = valid_parameters
        return valid_actions

    def get_valid_space_actions(self) -> Dict[Type[HighLevelAction], List[OneOf]]:
        """
        Returns a list of valid actions in the controller's action space that can be performed in the current state.

        WARNING: Will fail if there are high level actions with infinite valid parameterizations. Use get_possibly_valid_high_level_actions() instead if that is the case.

        :return: A dictionary mapping high level actions to their corresponding valid space actions.
        :rtype: Dict[type[HighLevelAction], List[OneOf]]
        """
        valid_space_actions = {}
        if not self._emulator_running():
            return valid_space_actions
        valid_high_level_actions = self.get_valid_high_level_actions()
        for action, parameter_list in valid_high_level_actions.items():
            valid_space_actions[action] = []
            for parameters in parameter_list:
                space_action = self._high_level_action_to_space_action(
                    action, **parameters
                )
                if space_action is None:
                    log_error(
                        f"Invalid action parameters combination for {action}: {parameters}. Ensure there are no bugs in {action}.get_all_valid_parameters",
                        self._parameters,
                    )
                valid_space_actions[action].append(space_action)
        return valid_space_actions

    def get_possibly_valid_high_level_actions(self) -> List[Type[HighLevelAction]]:
        """
        Returns a list of valid high level actions that can be performed (with some parameterized input) in the current state.

        Returns:
            List[Type[HighLevelAction]]: A list of valid high level actions.
        """
        if not self._emulator_running():
            return []
        actions = []
        for i, action_class in enumerate(self.ACTIONS):
            action = self.actions[i]
            if action.is_valid():
                actions.append(action_class)
        return actions

    def execute_space_action(
        self, action: OneOf
    ) -> Tuple[Optional[List[Dict[str, Dict[str, Any]]]], Optional[int]]:
        """
        Executes the specified high level action on the emulator after checking for validity.

        :param action: The action in the controller's action space.
        :type action: OneOf
        :return:
            - List[Dict[str, Dict[str, Any]]]: A list of state tracker reports after each low level action executed. Length is equal to the number of low level actions executed.

            - int: Action success status.
        :rtype: Tuple[List[Dict[str, Dict[str, Any]]] | None, int | None]
        """
        action_index, space_action = action
        executing_action: HighLevelAction = self.actions[action_index]
        return executing_action.execute_space_action(space_action)

    def execute(
        self, action: Type[HighLevelAction], **kwargs
    ) -> Tuple[Optional[List[Dict[str, Dict[str, Any]]]], Optional[int]]:
        """
        Executes the specified high level action on the emulator after checking for validity.

        :param action: The HighLevelAction
        :type action: Type[HighLevelAction]
        :param kwargs: Additional arguments required for the specific high level action.
        :type kwargs: Dict[str, Any]
        :return:
            - List[Dict[str, Dict[str, Any]]]: A list of state tracker reports after each low level action executed. Length is equal to the number of low level actions executed.

            - int: Action success status.
        :rtype: Tuple[List[Dict[str, Dict[str, Any]]] | None, int | None]
        """
        if action not in self.ACTIONS:
            log_error(
                "Action not recognized by controller. Are you passing in an instance of the action class?",
                self._parameters,
            )
        # Find the action instance
        action_index = self.ACTIONS.index(action)
        executing_action = self.actions[action_index]
        return executing_action.execute(**kwargs)

    def string_to_space_action(self, input_str: str) -> Optional[OneOf]:
        """
        Converts a string input to a space action
        Args:
            input_str (str): The string input representing the high level action and its parameters.

        Returns:
            OneOf: The action in the controller's action space.
        """
        action, kwargs = self.string_to_high_level_action(input_str=input_str)
        if action is None:
            return None
        return self._high_level_action_to_space_action(action, kwargs)

    def execute_string(
        self, input_str: str
    ) -> Tuple[Optional[List[Dict[str, Dict[str, Any]]]], Optional[int]]:
        """
        Executes the high level action implied by the input string.

        :param input_str: String representing the high level action and its parameters.
        :type input_str: str
        :param kwargs: Additional arguments required for the specific high level action.
        :type kwargs: Dict[str, Any]
        :return:
            - List[Dict[str, Dict[str, Any]]]: A list of state tracker reports after each low level action executed. Length is equal to the number of low level actions executed. Is None if the input string does not map to a valid action.

            - int: Action success status. Is None if the input string does not map to a valid action.
        :rtype: Tuple[List[Dict[str, Dict[str, Any]]] | None, int | None]
        """
        action, kwargs = self.string_to_high_level_action(input_str=input_str)
        if action is None:
            return None, None
        return self.execute(action, kwargs)

    def string_to_high_level_action(
        self, input_str: str
    ) -> Tuple[Type[HighLevelAction], Dict[str, Any]]:
        """
        Provide a way to map a string input to a HighLevelAction and parameters.

        Implement if you want to use the human_step_play method, or if you want to allow a LM based agent to give its actions in text.
        Must return None, None if the input_str does not map to an action.
        """
        raise NotImplementedError

    def get_action_strings(
        self, return_all: bool = False
    ) -> Dict[HighLevelAction, str]:
        """
        Provide a way to verbalize the allowed high level actions, along with the format of the input parameters.
        Useful for prompting a VLM to choose an action.

        This should match the mapping in string_to_high_level_action

        :param return_all: If True, returns all possible actions and parameter formats. If False, returns only the actions that are valid in the current state.
        :type return_all: bool
        :return: A dictionary mapping high level actions to their verbalizations and input formats.
        :rtype: Dict[HighLevelAction, str]
        """
        raise NotImplementedError


class LowLevelController(Controller):
    """A controller that executes low level actions directly on the emulator."""

    ACTIONS = [LowLevelAction]
    """ A HighLevelAction subclass that directly maps to low level actions. """


class LowLevelPlayController(Controller):
    """A controller that executes low level actions directly, but no menu button presses."""

    ACTIONS = [LowLevelPlayAction]
    """ A HighLevelAction subclass that directly maps to low level actions, but no menu button presses. """

    def string_to_high_level_action(self, input_str):
        string_low = input_str.lower()
        low_level_action = None
        mapper = {
            "a": LowLevelActions.PRESS_BUTTON_A,
            "u": LowLevelActions.PRESS_ARROW_UP,
            "b": LowLevelActions.PRESS_BUTTON_B,
            "d": LowLevelActions.PRESS_ARROW_DOWN,
            "l": LowLevelActions.PRESS_ARROW_LEFT,
            "r": LowLevelActions.PRESS_ARROW_RIGHT,
        }
        for map_opt in mapper:
            if map_opt in string_low:
                low_level_action = mapper[map_opt]
                break
        if low_level_action is None:
            return None, None
        return LowLevelPlayAction, {"low_level_action": low_level_action}

    def get_action_strings(self, return_all: bool = False):
        return {
            LowLevelPlayAction: "A, B for button. L, R, U, D for arrow keys",
        }


class RandomPlayController(Controller):
    """A controller that performs random play on the emulator using low level actions."""

    ACTIONS = [RandomPlayAction]
    """ A HighLevelAction subclass that performs random low level actions. """


_ALWAYS_VALID_CONTROLLERS = {
    "low_level": LowLevelController,
    "low_level_play": LowLevelPlayController,
    "random_play": RandomPlayController,
}
""" Controllers that are always valid for any game and environment. """
