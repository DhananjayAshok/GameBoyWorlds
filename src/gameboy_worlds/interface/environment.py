from abc import abstractmethod, ABC
from typing import Optional, Type, Dict, Any, List, Tuple

from gameboy_worlds.utils import (
    load_parameters,
    log_error,
    log_info,
    log_warn,
    get_lowest_level_subclass,
    verify_parameters,
    log_dict,
    import_pygame,
)


from gameboy_worlds.emulation import Emulator, StateTracker, TestTrackerMixin
from gameboy_worlds.emulation.registry import (
    get_state_tracker_class,
    get_train_init_states,
)
from gameboy_worlds.interface.controller import Controller
from gameboy_worlds.interface.action import HighLevelAction

import numpy as np
import gymnasium as gym
import warnings
from copy import deepcopy

warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html",
)
# This is to ignore deprecation warnings from pygame about pkg_resources


class Environment(gym.Env, ABC):
    """Base class for environments interfacing with the emulator."""

    REQUIRED_EMULATOR = Emulator
    """ The highest level emulator that the environment can interface with. """

    REQUIRED_STATE_TRACKER = StateTracker
    """ The state tracker that tracks the minimal state information required for the environment to function. """

    @staticmethod
    def override_emulator_kwargs(emulator_kwargs: dict) -> dict:
        """
        Override default emulator keyword arguments for this environment.

        Override this method in subclasses to modify the default emulator keyword arguments.

        You may want to use `override_state_tracker_class` or that style to ensure compatibility of state tracker classes.

        Args:
            emulator_kwargs (dict): Incoming emulator keyword arguments.
        Returns:
            dict: The overridden emulator keyword arguments.
        """
        return emulator_kwargs

    @staticmethod
    def override_state_tracker_class(
        emulator_kwargs: dict, required_state_tracker_class: Type[StateTracker]
    ):
        """
        Safely overrides the state tracker class for the environment.

        Use this in `override_emulator_kwargs` to ensure that the lowest level state tracker class is chosen.

        Args:
            emulator_kwargs (dict): Incoming emulator keyword arguments.
            required_state_tracker_class (Type[StateTracker]): Usually the required state tracker class for the environment.
        """
        game = emulator_kwargs["game"]
        has_option = "state_tracker_class" in emulator_kwargs
        incoming_state_tracker_class = emulator_kwargs.get(
            "state_tracker_class", "default"
        )
        if isinstance(incoming_state_tracker_class, str):
            incoming_state_tracker_class = get_state_tracker_class(
                game, incoming_state_tracker_class
            )
        if issubclass(incoming_state_tracker_class, required_state_tracker_class):
            return incoming_state_tracker_class
        elif issubclass(required_state_tracker_class, incoming_state_tracker_class):
            emulator_kwargs["state_tracker_class"] = required_state_tracker_class
        else:
            emulator_kwargs["state_tracker_class"] = (
                incoming_state_tracker_class  # Don't know which one to pick, so just go with the incoming one.
            )
        return

    def __init__(
        self,
        emulator: Emulator,
        controller: Controller,
        parameters: Optional[dict] = None,
    ):
        """
        Ensures that the environment has the required attributes.
        All subclasses must call this __init__ method AFTER setting up the required attributes.

        If you are implementing a subclass, ensure that the following attributes are set:
            - observation_space: gym space defining observation space structure

        """
        self._parameters = load_parameters(parameters)
        self._emulator = emulator
        self._controller = controller
        required_attributes = ["observation_space"]
        for attr in required_attributes:
            if not hasattr(self, attr):
                log_error(
                    f"Environment requires attribute '{attr}' to be set. Implement this in the subclass __init__",
                    self._parameters,
                )
        self.observation_space: gym.spaces.Space = self.observation_space
        if not issubclass(type(self._emulator), self.REQUIRED_EMULATOR):
            log_error(
                f"Environment requires an Emulator of type {self.REQUIRED_EMULATOR}, but got {type(self._emulator)}",
                self._parameters,
            )
        if not isinstance(self._controller, Controller):
            log_error(
                f"Environment requires a Controller instance, but got {type(self._controller)}",
                self._parameters,
            )
        self.REQUIRED_STATE_TRACKER = get_lowest_level_subclass(
            [self.REQUIRED_STATE_TRACKER, self._controller.REQUIRED_STATE_TRACKER]
        )
        if not issubclass(
            type(self._emulator.state_tracker), self.REQUIRED_STATE_TRACKER
        ):
            log_error(
                f"Environment requires a StateTracker of type {self.REQUIRED_STATE_TRACKER}, but got {type(self._emulator.state_tracker)}",
                self._parameters,
            )
        self._controller.assign_emulator(self._emulator)
        self._rng = np.random.default_rng()
        self.action_space = self._controller.get_action_space()
        """ The Gym action Space provided by the controller. """
        self.actions = self._controller.ACTIONS
        """ A list of HighLevelAction Types provided by the controller. """
        self.render_mode = "human"
        """ The render mode of the environment. Supports 'human' and 'rgb_array', but strongly assumes 'human' as can just read the emulator screen from `get_info` """
        self._window = None
        """ The pygame window for rendering in 'human' mode. Initialized on first render call. """
        self._clock = None
        """ The pygame clock for rendering in 'human' mode. Initialized on first render call. """
        self.reset()  # I don't think this will cause issues, but should check that resetting here works well with gymnasium SyncVectorEnv final_obs construction.

    @abstractmethod
    def get_observation(
        self,
        *,
        action: Optional[HighLevelAction] = None,
        action_kwargs: Optional[dict] = None,
        transition_states: Optional[List[Dict[str, Dict[str, Any]]]] = None,
        action_success: Optional[int] = None,
    ) -> gym.spaces.Space:
        """
        Returns the current observation from the emulator. Must match self.observation_space.
        Args:
            action (Optional[HighLevelAction]): The previous action taken.
            action_kwargs (dict): The keyword arguments used for the action.
            transition_states (Optional[List[Dict[str, Dict[str, Any]]]]): The states observed during the action execution.
            action_success (Optional[int]): The success code of the action.

        Returns:
            observation (gym.spaces.Space): The current observation.
        """
        raise NotImplementedError

    def get_info(
        self,
        *,
        action: Optional[HighLevelAction] = None,
        action_kwargs: Optional[dict] = None,
        transition_states: Optional[List[Dict[str, Dict[str, Any]]]] = None,
        action_success: Optional[int] = None,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Returns the full state information as defined by the emulator's state tracker.

        Creates additional fields:
        - "core"/"previous_action_details": A tuple of (action, action_kwargs, transition_states, action_success, action_return)
        - "core"/"transition_passed_frames": An array of all frames passed during the action execution
        - "ocr"/"transition_ocr_regions": A list of OCR regions captured during the action execution

        :param action: HighLevelAction taken
        :type action: Optional[HighLevelAction]
        :param action_kwargs: Keyword arguments for the action
        :type action_kwargs: Optional[dict]
        :param transition_states: List of states observed during the action execution
        :type transition_states: Optional[List[Dict[str, Dict[str, Any]]]]
        :param action_success:  Success code of the action
        :type action_success: Optional[int]
        :return: Full state information from the state tracker
        :rtype: Dict[str, Dict[str, Any]]
        """
        state_info = self._emulator.state_tracker.report()
        if action is not None:  # then transition_states should not be empty
            # Attach the action details to the info
            last_state = transition_states[-1]
            if "action_return" in last_state["core"]:
                action_return = last_state["core"]["action_return"]
            else:
                action_return = None
            state_info["core"]["previous_action_details"] = (
                action,
                action_kwargs,
                transition_states,
                action_success,
                action_return,
            )

            # Aggregate passed frames from transition states
            all_passed_frames = transition_states[0]["core"]["passed_frames"]
            for transition_state in transition_states[1:]:
                all_passed_frames = np.concatenate(
                    [all_passed_frames, transition_state["core"]["passed_frames"]],
                    axis=0,
                )
            state_info["core"][
                "transition_passed_frames"
            ] = all_passed_frames  # Will include the current state info last frame as as the final entry

            # Aggregate OCR texts from transition states
            all_ocr_regions = []
            for transition_state in transition_states:
                if (
                    "ocr" in transition_state
                    and "ocr_regions" in transition_state["ocr"]
                ):
                    all_ocr_regions.append(transition_state["ocr"]["ocr_regions"])
            if "ocr" in state_info:
                state_info["ocr"]["transition_ocr_regions"] = all_ocr_regions
            else:
                state_info["ocr"] = {"transition_ocr_regions": all_ocr_regions}
        return state_info

    def get_final_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Returns the final state information from the emulator when all episodes are done.
        Will involve summaries over all episodes played.
        Returns:
            info (dict): The final state information from the state tracker.
        """
        return self._emulator.state_tracker.report_final()

    def reset(
        self, *, seed: Optional[int] = None, options: Optional[dict] = None
    ) -> Tuple[gym.spaces.Space, Dict[str, Dict[str, Any]]]:
        """
        Resets the environment and emulator to the initial state.
        Args:
            seed (int, optional): Seed for random number generators.
            options (dict, optional): Additional options for resetting the environment.
        Returns:
            observation (object): The initial observation of the environment.

            info (dict): Additional information about the reset.
        """
        super().reset(seed=seed, options=options)
        self._emulator.reset()
        self.seed(seed)
        observation, info = self.get_observation(), self.get_info()
        return observation, info

    @abstractmethod
    def determine_reward(
        self,
        start_state: Dict[str, Dict[str, Any]],
        *,
        action: Optional[HighLevelAction] = None,
        action_kwargs: Optional[dict] = None,
        transition_states: Optional[List[Dict[str, Dict[str, Any]]]] = None,
        action_success: Optional[int] = None,
    ) -> float:
        """
        Determines the reward based on the transition from start_state through transition_states.
        Args:
            start_state (Dict[str, Dict[str, Any]]): The state before the action was taken.
            action (HighLevelAction): The HighLevelAction action taken.
            action_kwargs (dict): The keyword arguments used for the action.
            transition_states (List[Dict[str, Dict[str, Any]]]): A list of states observed during the action execution.
            action_success (bool): Whether the action was successful.
        Returns:
            float: The computed reward.
        """
        raise NotImplementedError

    def determine_truncated(
        self,
        start_state: Dict[str, Dict[str, Any]],
        *,
        action: Optional[HighLevelAction] = None,
        action_kwargs: Optional[dict] = None,
        transition_states: Optional[List[Dict[str, Dict[str, Any]]]] = None,
        action_success: Optional[int] = None,
    ) -> bool:
        """
        Determines whether the episode playthrough has exceeded some maximum step count or other truncation criteria based on the transition from start_state through transition_states.
        This method is can be overidden to implement custom truncation logic, but it must always return:
        `super().determine_truncated() or <custom_truncation_logic_bool>`

        Args:
            start_state (Dict[str, Dict[str, Any]]): The state before the action was taken.
            action (HighLevelAction): The HighLevelAction action taken.
            action_kwargs (dict): The keyword arguments used for the action.
            transition_states (List[Dict[str, Dict[str, Any]]]): A list of states observed during the action execution.
            action_success (bool): Whether the action was successful.
        Returns:
            bool: Whether the episode is terminated.
        """
        return self._emulator.check_if_done()

    @abstractmethod
    def determine_terminated(
        self,
        start_state: Dict[str, Dict[str, Any]],
        *,
        action: Optional[HighLevelAction] = None,
        action_kwargs: Optional[dict] = None,
        transition_states: Optional[List[Dict[str, Dict[str, Any]]]] = None,
        action_success: Optional[int] = None,
    ) -> bool:
        """
        Determines whether the episode reaches the goal / terminal state based on the transition from start_state through transition_states.
        This method is NOT meant to be used to determine if the step count has exceeded the maximum.

        Args:
            start_state (Dict[str, Dict[str, Any]]): The state before the action was taken.
            action (HighLevelAction): The HighLevelAction action taken.
            action_kwargs (dict): The keyword arguments used for the action.
            transition_states (List[Dict[str, Dict[str, Any]]]): A list of states observed during the action execution.
            action_success (bool): Whether the action was successful.
        Returns:
            bool: Whether the episode is terminated.
        """
        pass

    def before_step(self, action: Type[HighLevelAction], action_kwargs: dict):
        """
        Implement any logic that needs to be executed before each step in the environment.
        """
        return

    def after_step(
        self,
        start_state: Dict[str, Dict[str, Any]],
        action: Type[HighLevelAction],
        action_kwargs: dict,
        transition_states: List[Dict[str, Dict[str, Any]]],
        action_success: int,
    ):
        """
        Implement any logic that needs to be executed after each step in the environment.

        Args:
            start_state (Dict[str, Dict[str, Any]]): The state before the action was taken.
            action (HighLevelAction): The HighLevelAction action taken.
            action_kwargs (dict): The keyword arguments used for the action.
            transition_states (List[Dict[str, Dict[str, Any]]]): A list of states observed during the action execution.
            action_success (int): Whether the action was successful.
        """
        return

    def step(
        self, action: gym.spaces.OneOf
    ) -> Tuple[gym.spaces.Space, float, bool, bool, Dict[str, Dict[str, Any]]]:
        """
        Executes the given Gym Space action in the environment via the controller.
        Use step_high_level_action to execute high level actions directly.

        Args:
            action (gym.spaces.OneOf): The action to execute. Must be a valid action in the controller's action space.

        Returns:
            observation (gym.spaces.Space): The observation after executing the action.
            reward (float): The reward obtained from executing the action.
            terminated (bool): Whether the episode has ended (reached the terminal state of the MDP).
            truncated (bool): Whether the episode was truncated (exceeded the maximum allowed steps).
            info (Dict[str, Dict[str, Any]]): Full state information.
        """
        high_level_action, kwargs = self._controller._space_action_to_high_level_action(
            action
        )
        return self.step_high_level_action(high_level_action, **kwargs)

    def step_high_level_action(
        self, action: Type[HighLevelAction], **kwargs
    ) -> Tuple[gym.spaces.Space, float, bool, bool, Dict[str, Dict[str, Any]]]:
        """
        Executes the given High Level action in the environment via the controller.
        If the action is invalid according to the controller, will not perform any action and will simply return the current observation, a reward of 0, and terminated and truncated as False. The info will also include a field "invalid_action"=True to indicate that the action was invalid.

        :param action: The high level action class to execute.
        :type action: Type[HighLevelAction]
        :param kwargs: Additional arguments required for the specific high level action.
        :type kwargs: Dict[str, Any]
        :return:
            - observation (gym.spaces.Space): The observation after executing the action.

            - reward (float): The reward obtained from executing the action.

            - terminated (bool): Whether the episode has ended (reached the terminal state of the MDP).

            - truncated (bool): Whether the episode was truncated (exceeded the maximum allowed steps).

            - info (Dict[str, Dict[str, Any]]): Full state information.
        :rtype: Tuple[Space, float, bool, bool, Dict[str, Dict[str, Any]]]
        """
        if self._emulator.check_if_done():
            log_error(
                "Cannot step environment because emulator indicates done. Please reset the environment.",
                self._parameters,
            )  # TODO: This triggered once during demos/benchmark runs, need to investigate why.
        start_state = self.get_info()
        self.before_step(action, kwargs)
        transition_states, action_success = self._controller.execute(action, **kwargs)
        if (
            transition_states is None
        ):  # then the action was not a valid one according to the controller.
            observation = self.get_observation()
            current_state = self.get_info()
            terminated = self.determine_terminated(start_state=start_state)
            truncated = self.determine_truncated(start_state=start_state)
            reward = self.determine_reward(start_state=start_state) - abs(
                self._parameters["invalid_action_penalty"]
            )
            current_state["invalid_action"] = True
            return observation, reward, terminated, truncated, current_state
        self.after_step(start_state, action, kwargs, transition_states, action_success)
        truncated = self.determine_truncated(
            start_state=start_state,
            action=action,
            action_kwargs=kwargs,
            transition_states=transition_states,
            action_success=action_success,
        )

        observation = self.get_observation(
            action=action,
            action_kwargs=kwargs,
            transition_states=transition_states,
            action_success=action_success,
        )
        current_state = self.get_info(
            action=action,
            action_kwargs=kwargs,
            transition_states=transition_states,
            action_success=action_success,
        )
        terminated = self.determine_terminated(
            start_state=start_state,
            action=action,
            action_kwargs=kwargs,
            transition_states=transition_states,
            action_success=action_success,
        )

        reward = self.determine_reward(
            start_state=start_state,
            action=action,
            action_kwargs=kwargs,
            transition_states=transition_states,
            action_success=action_success,
        )
        return observation, reward, terminated, truncated, current_state

    def step_str(
        self, input_str: str
    ) -> Tuple[gym.spaces.Space, float, bool, bool, Dict[str, Dict[str, Any]]]:
        """
        Attempts to execute an input string representation of an action.
        Useful for human play or VLM interaction.
        If the action is an invalid string, will not perform any action and will simply return Nones.

        :param input_str: The input string representing the action.
        :type input_str: str
        :return:
            - observation (gym.spaces.Space): The observation after executing the action.

            - reward (float): The reward obtained from executing the action.

            - terminated (bool): Whether the episode has ended (reached the terminal state of the MDP).

            - truncated (bool): Whether the episode was truncated (exceeded the maximum allowed steps).

            - info (Dict[str, Dict[str, Any]]): Full state information.
        :rtype: Tuple[Space, float, bool, bool, Dict[str, Dict[str, Any]]]
        """
        action, kwargs = self.string_to_high_level_action(input_str)
        if (
            action is None
        ):  # not a valid action, will not perform an action and will simply return Nones.
            return None, None, None, None, None
        return self.step_high_level_action(action, **kwargs)

    def string_to_high_level_action(
        self, input_str: str
    ) -> Tuple[Optional[Type[HighLevelAction]], Optional[dict]]:
        """
        Attempts to convert an input string representation of an action into a HighLevelAction and its parameters.
        Useful for human play or VLM interaction.

        :param input_str: The input string representing the action.
        :type input_str: str
        :return: A tuple containing the HighLevelAction class and its execution parameters dictionary. If the input string is invalid, returns (None, None).
        :rtype: Tuple[Type[HighLevelAction] | None, dict | None]
        """
        return self._controller.string_to_high_level_action(input_str)

    def close(self):
        """
        Closes the environment and the underlying emulator.
        """
        log_info("Closing environment and emulator.", self._parameters)
        self._emulator.close()

    def _screen_render(self, screen: np.ndarray):
        """
        Renders the given screen using pygame in human mode.
        Args:
            screen (np.ndarray): The screen to render.

        """
        pygame = import_pygame(self._parameters)
        if self._window is None:
            pygame.init()
            pygame.display.init()
            self._window = pygame.display.set_mode(
                (self._emulator.screen_shape[0], self._emulator.screen_shape[1])
            )
        if self._clock is None:
            self._clock = pygame.time.Clock()
        rgb = np.stack([screen[:, :, 0], screen[:, :, 0], screen[:, :, 0]], axis=2)
        pygame.surfarray.blit_array(self._window, rgb.swapaxes(0, 1))
        pygame.display.flip()
        self._clock.tick(60)  # Limit to 60 FPS

    def render(self) -> Optional[np.ndarray]:
        """
        Gets the current screen from the emulator and renders it.

        Use this method only if you want to generally run the emulator in headless mode but still want to see the screen occasionally.

        Do not call this method if the emulator is not headless, you should already have a PyBoy interactive window open in that case.

        Returns:
            If render_mode is 'rgb_array', returns the current screen as a numpy array. However this is always accessible via self.get_info()['core']['current_frame'], so this is mostly for Gym compatibility.
        """
        if self._emulator.headless == False:
            log_error(
                "You probably don't want to call render() when the emulator is not headless.",
                self._parameters,
            )
        screen = self._emulator.get_current_frame()  # shape: 144, 160, 1
        if self.render_mode == "human":
            self._screen_render(screen)
        elif self.render_mode == "rgb_array":
            return screen
        else:
            log_error(f"Unsupported render mode: {self.render_mode}", self._parameters)

    def seed(self, seed: Optional[int] = None):
        """
        Seeds the environment's random number generator and the controller's RNG.

        Args:
            seed (int, optional): The seed value.
        """
        self._controller.seed(seed)
        self._rng = np.random.default_rng(seed)

    def render_obs(
        self,
        *,
        action: Optional[Type[HighLevelAction]] = None,
        action_kwargs: Optional[dict] = None,
        transition_states: Optional[List[Dict[str, Dict[str, Any]]]] = None,
        action_success: Optional[int] = None,
        action_return: Optional[Dict[str, Any]] = None,
    ):
        """
        Provide a way to render the output of `get_observation` to a human.
        Implement if you want to use the human_step_play method.

        Args:
            action (Optional[Type[HighLevelAction]]): The previous action taken.
            action_kwargs (dict): The keyword arguments used for the action.
            transition_states (Optional[List[Dict[str, Dict[str, Any]]]]): The states observed during the action execution.
            action_success (Optional[int]): The success code of the action.
        """
        raise NotImplementedError

    def render_info(
        self,
        *,
        action: Optional[Type[HighLevelAction]] = None,
        action_kwargs: Optional[dict] = None,
        transition_states: Optional[List[Dict[str, Dict[str, Any]]]] = None,
        action_success: Optional[int] = None,
        action_return: Optional[Dict[str, Any]] = None,
    ):
        """
        Provide a way to render the output of `get_info` to a human.
        Implement if you want to use the human_step_play method with show_info=True.
        Must always be a superset of render_obs (i.e. should also show what render_obs shows).

        Args:
            action (Optional[Type[HighLevelAction]]): The previous action taken.
            action_kwargs (dict): The keyword arguments used for the action.
            transition_states (Optional[List[Dict[str, Dict[str, Any]]]]): The states observed during the action execution.
            action_success (Optional[int]): The success code of the action.
        """
        raise NotImplementedError

    def get_action_strings(
        self, return_all: bool = False
    ) -> Dict[Type[HighLevelAction], str]:
        """
        Provide a way to verbalize the allowed high level actions, along with the format of the input parameters.
        Useful for prompting a VLM to choose an action.

        :param return_all: If True, returns all possible actions and parameter formats. If False, returns only the actions that are valid in the current state.
        :type return_all: bool
        :return: A dictionary mapping high level actions to their verbalizations and input formats.
        :rtype: Dict[Type[HighLevelAction], str]
        """
        return self._controller.get_action_strings(return_all=return_all)

    def human_step_play(
        self, max_steps: int = 50, show_obs: bool = True, show_info: bool = True
    ) -> Tuple[List[float], bool, bool]:
        """
        Opens a render window and allow the human to play through the environment as an agent would

        Args:
            max_steps (int): max steps to take
            show_obs (bool): whether to show the observation space rendering after each step
            show_info (bool): whether to show the info rendering after each step. Will force show_obs=False if enabled.

        Returns:
            rewards (List[float]): List of rewards obtained at each step.
            terminated (bool): Whether the episode has ended (reached the terminal state of the MDP).
            truncated (bool): Whether the episode was truncated (exceeded the maximum allowed emulator steps). It does not consider the max_steps parameter here.
        """
        observation, info = self.reset()
        self.render_mode = "human"
        log_info(f"Doing human step play for {max_steps} max steps...")
        steps = 0
        done = False
        terminated = False
        truncated = False
        rewards = []
        if show_info:
            self.render_info()
            show_obs = False
        if show_obs:
            self.render_obs()
        while not done and steps < max_steps:
            action_input = self._controller.get_action_strings()
            action_input_str = ""
            for action_class, action_str in action_input.items():
                action_input_str += f"- {action_str}\n"
            log_info(f"Allowed Actions: \n{action_input_str}", self._parameters)
            input_str = input("Enter Action: ").strip()
            (
                possible_obs,
                possible_reward,
                possible_terminated,
                possible_truncated,
                possible_info,
            ) = self.step_str(input_str)
            if possible_obs is not None:
                observation, reward, terminated, truncated, info = (
                    possible_obs,
                    possible_reward,
                    possible_terminated,
                    possible_truncated,
                    possible_info,
                )
                rewards.append(reward)
                if reward != 0:
                    log_info(f"Reward obtained: {reward}", self._parameters)
                (
                    action,
                    action_kwargs,
                    transition_states,
                    action_success,
                    action_return,
                ) = info["core"]["previous_action_details"]
                if show_info:
                    self.render_info(
                        action=action,
                        action_kwargs=action_kwargs,
                        transition_states=transition_states,
                        action_success=action_success,
                        action_return=action_return,
                    )
                if show_obs:
                    self.render_obs(
                        action=action,
                        action_kwargs=action_kwargs,
                        transition_states=transition_states,
                        action_success=action_success,
                        action_return=action_return,
                    )
            else:
                log_warn("That was not a valid input. did nothing", self._parameters)
            if terminated or truncated:
                log_info(
                    f"Episode finished! Terminated: {terminated}, Truncated: {truncated}",
                    self._parameters,
                )
                break
            steps += 1
            if steps >= max_steps:
                log_info(
                    f"Max steps {max_steps} reached. Ending episode.", self._parameters
                )
        return rewards, terminated, truncated


class DummyEnvironment(Environment):
    """A dummy environment that does nothing special."""

    def __init__(
        self,
        emulator: Emulator,
        controller: Controller,
        parameters: Optional[dict] = None,
    ):
        """
        Initializes the DummyEnvironment with the given emulator and controller.

        It is safe to overwrite the self.observation_space in the subclass after calling this __init__ method.
        """
        screen_shape = emulator.screen_shape
        self.observation_space = gym.spaces.Box(
            low=0, high=255, shape=(screen_shape[1], screen_shape[0]), dtype=np.uint8
        )
        """ The observation space is the raw pixel values of the emulator's screen. """
        super().__init__(
            emulator=emulator, controller=controller, parameters=parameters
        )

    def get_observation(
        self,
        *,
        action=None,
        action_kwargs=None,
        transition_states=None,
        action_success=None,
    ):
        if transition_states is None:
            current_state = self.get_info()
            screen = current_state["core"]["current_frame"]
        else:
            screen = transition_states[-1]["core"]["current_frame"]
        return screen

    def determine_reward(self, **kwargs):
        return 0.0

    def determine_terminated(self, **kwargs):
        return False

    def render_obs(
        self,
        action=None,
        action_kwargs=None,
        transition_states=None,
        action_success=None,
        action_return=None,
    ):  # Might cause issues if you try to render() as well
        """
        Renders the screen.
        """
        screen = self.get_observation()
        self._screen_render(screen)

    def render_info(
        self,
        action=None,
        action_kwargs=None,
        transition_states=None,
        action_success=None,
        action_return=None,
    ):
        info = deepcopy(self.get_info())
        if transition_states is not None and len(transition_states) > 0:
            screens = transition_states[0]["core"]["passed_frames"]
            for transition_state in transition_states[1:]:
                screens = np.concatenate(
                    [screens, transition_state["core"]["passed_frames"]], axis=0
                )
        else:
            if "passed_frames" in info["core"]:
                screens = info["core"]["passed_frames"]
            else:
                screens = None
        if screens is None:
            screens = [info["core"]["current_frame"]]
        for screen in screens:
            self._screen_render(screen)
        info["core"].pop("current_frame")
        info["core"].pop("passed_frames")
        if "ocr" in info:
            info.pop("ocr")
        if "transition_passed_frames" in info["core"]:
            info["core"].pop("transition_passed_frames")
        if "previous_action_details" in info["core"]:
            info["core"]["previous_action_details"] = (
                info["core"]["previous_action_details"][:2]
                + info["core"]["previous_action_details"][3:]
            )  # remove transition states to avoid huge logs
        log_info("State: ", self._parameters)
        log_dict(info, parameters=self._parameters)


class TestEnvironmentMixin:
    """
    Mixin class for testing environments.
    Ensures the State Tracker used is a TestTrackerMixin and checks these for termination / truncation.
    """

    REQUIRED_STATE_TRACKER = TestTrackerMixin

    def determine_truncated(
        self,
        start_state: Dict[str, Dict[str, Any]],
        *,
        action: Optional[HighLevelAction] = None,
        action_kwargs: Optional[dict] = None,
        transition_states: Optional[List[Dict[str, Dict[str, Any]]]] = None,
        action_success: Optional[int] = None,
    ) -> bool:
        if not isinstance(self._emulator.state_tracker, TestTrackerMixin):
            log_error(
                "TestEnvironmentMixin requires the emulator's state tracker to be a TestTrackerMixin.",
                self._parameters,
            )  # we don't need to repeat this for determine_terminated since its done here.
        if transition_states is None:
            return self._emulator.check_if_done()
        any_truncated = False
        for state in transition_states:
            if state["termination_truncation"]["truncated"]:
                any_truncated = True
                break
        return any_truncated or self._emulator.check_if_done()

    def determine_terminated(
        self,
        start_state: Dict[str, Dict[str, Any]],
        *,
        action: Optional[HighLevelAction] = None,
        action_kwargs: Optional[dict] = None,
        transition_states: Optional[List[Dict[str, Dict[str, Any]]]] = None,
        action_success: Optional[int] = None,
    ) -> bool:
        if transition_states is None:
            return False
        any_terminated = False
        for state in transition_states:
            if state["termination_truncation"]["terminated"]:
                any_terminated = True
                break
        return any_terminated


class TrainEnvironmentMixin:
    """
    Mixin class for training environments.
    Records the allowed initial states for training and random shuffles between them when resetting.
    """

    def reset(
        self, *, seed: Optional[int] = None, options: Optional[dict] = None
    ) -> Tuple[gym.spaces.Space, Dict[str, Dict[str, Any]]]:
        """

        Args:
            seed (int, optional): Seed for random number generators.
            options (dict, optional): Additional options for resetting the environment.
        Returns:
            observation (object): The initial observation of the environment.

            info (dict): Additional information about the reset.
        """
        game = self._emulator.game
        init_states = get_train_init_states(game, parameters=self._parameters)
        choice = self._rng.choice(len(init_states))
        init_state = init_states[choice]
        self._emulator.set_init_state(init_state)
        return super().reset(seed=seed, options=options)
