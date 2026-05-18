from gameboy_worlds.utils import log_error, log_warn
from gameboy_worlds.interface.action import HighLevelAction, SingleHighLevelAction
from gameboy_worlds.emulation.pokemon.parsers import (
    AgentState,
    PokemonStateParser,
    BasePokemonRedStateParser,
)
from gameboy_worlds.emulation.pokemon.trackers import CorePokemonTracker
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

    REQUIRED_STATE_PARSER = PokemonStateParser
    REQUIRED_STATE_TRACKER = CorePokemonTracker

    def is_valid(self, **kwargs):
        """
        Just checks if the agent is in dialogue state.
        """
        return (
            self._state_tracker.get_episode_metric(("pokemon_core", "agent_state"))
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

    REQUIRED_STATE_PARSER = PokemonStateParser
    REQUIRED_STATE_TRACKER = CorePokemonTracker

    def is_valid(self, **kwargs):
        """
        Just checks if the agent is in free roam state.
        """
        return (
            self._state_tracker.get_episode_metric(("pokemon_core", "agent_state"))
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

    @staticmethod
    def get_action_name() -> str:
        return "Interact"


class BaseMovementAction(HighLevelAction, ABC):
    """
    Base class for movement actions in the Pokemon environment.
    Has utility methods for moving in directions.

    Is Valid When:
    - In Free Roam State

    Action Success Interpretation:
    - -1: Frame did not change, even on the first step
    - 0: Finished all steps
    - 1: Took some steps, but not all, and then frame stopped changing OR the frame starts oscillating (trying to check for jitter). This usually means we ran into an obstacle.
    - 2: Took some steps, but agent state changed from free roam. This often means we entered a cutscene or battle.

    Action Returns:
    - `n_steps_taken` (`int`): Number of steps actually taken
    - `rotated` (`bool` or `None`): True if the player has not moved, but has rotated. If the player has moved, this will be None. If it is False, it means the player tried to walk straight into an obstacle.

    Known Limitations:
    - Struggles to handle oscillating frames when the player is next to an obstacle. So if you are surrounded by water or bouncing flowers on all quadrants (e.g. the pier in Cinnabar Island), the system will think that the agent has moved forward, even though it has not.
    """

    REQUIRED_STATE_TRACKER = CorePokemonTracker
    REQUIRED_STATE_PARSER = PokemonStateParser

    def _is_uniform_quadrant(self, frame, quadrant_name) -> bool:
        mapper = {
            "screen_quadrant_1": "tr",
            "screen_quadrant_2": "tl",
            "screen_quadrant_3": "bl",
            "screen_quadrant_4": "br",
        }
        quadrant_cells = self._emulator.state_parser.capture_grid_cells(
            frame, quadrant=mapper[quadrant_name]
        )
        keys = list(quadrant_cells.keys())
        x_min = 1e9
        y_min = 1e9
        x_max = -1e9
        y_max = -1e9
        for key in keys:
            x_coord, y_coord = key
            if x_coord * y_coord == 0:  # pop it to avoid checking player cell
                quadrant_cells.pop(key)
            else:
                x_min = min(x_min, x_coord)
                y_min = min(y_min, y_coord)
                x_max = max(x_max, x_coord)
                y_max = max(y_max, y_coord)
        x_min = int(x_min)
        y_min = int(y_min)
        x_max = int(x_max)
        y_max = int(y_max)
        keys = list(quadrant_cells.keys())
        vertical_uniform = True
        horizontal_uniform = True
        # check horizontal lines
        for y in range(y_min + 1, y_max):  # avoid edges
            first_cell = None
            for x in range(x_min + 1, x_max):
                cell = quadrant_cells[(x, y)]
                if first_cell is None:
                    first_cell = cell
                else:
                    if first_cell.shape == cell.shape:
                        if frame_changed(first_cell, cell):
                            horizontal_uniform = False
                            break
            if not horizontal_uniform:
                break
        if horizontal_uniform:
            return True
        # check vertical lines
        for x in range(x_min + 1, x_max):
            first_cell = None
            for y in range(y_min + 1, y_max):
                cell = quadrant_cells[(x, y)]
                if first_cell is None:
                    first_cell = cell
                else:
                    if first_cell.shape == cell.shape:
                        if frame_changed(first_cell, cell):
                            vertical_uniform = False
                            break
            if not vertical_uniform:
                break
        if vertical_uniform:
            return True
        return False

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
        # if the full screen hasn't changed at all, player has neither moved nor rotated
        if not frame_changed(previous_frame, current_frame):
            return False, False
        # split the screen into quadrants and check which quadrants have changed. If any of them stayed the same, the player has not moved, but may have rotated.
        # One caveat is if the quadrant is uniform tiles (i.e. all have the same grid texture in them). In this case, we can't say for sure that the quadrant hasn't changed, since it may just be that the uniform texture is the same. So we check for that too.
        flag = False
        for quadrant in [
            "screen_quadrant_1",
            "screen_quadrant_2",
            "screen_quadrant_3",
            "screen_quadrant_4",
        ]:
            prev_quad = self._emulator.state_parser.capture_named_region(
                previous_frame, quadrant
            )
            curr_quad = self._emulator.state_parser.capture_named_region(
                current_frame, quadrant
            )
            prev_uniform = (
                prev_quad.max() == prev_quad.min()  # screen is all black or all white
                or self._is_uniform_quadrant(
                    previous_frame, quadrant
                )  # screen quadrant is uniform tiles
            )
            curr_uniform = (
                curr_quad.max() == curr_quad.min()
                or self._is_uniform_quadrant(current_frame, quadrant)
            )
            if (
                not frame_changed(prev_quad, curr_quad)
                and not prev_uniform
                and not curr_uniform
            ):  # then screen isn't just black, but also hasn't changed.
                flag = True
                break
        if flag:  # then some frame stayed the same, so no movement, but maybe rotation.
            prev_player_cell = self._emulator.state_parser.capture_grid_cells(
                previous_frame
            )[(0, 0)]
            curr_player_cell = self._emulator.state_parser.capture_grid_cells(
                current_frame
            )[(0, 0)]
            if frame_changed(prev_player_cell, curr_player_cell):
                return False, True
            else:
                return False, False
        else:
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
            # We check all frames in sequence to try and catch oscillations. But nothing will catch 1 step into wall in areas like this
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
            self._state_tracker.get_episode_metric(("pokemon_core", "agent_state"))
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
    - 2: Took some steps, but agent state changed from free roam. This often means we entered a cutscene or battle.

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

    @staticmethod
    def get_action_name(direction: str, steps: int) -> str:
        return f"Move {direction} {steps}"


class MoveGridAction(BaseMovementAction):
    """
    Moves the agent on both axes. Will always try to move right first and then up.

    Is Valid When:
    - In Free Roam State
    Action Success Interpretation:
    - -1: Frame did not change, even on the first step
    - 0: Finished all steps
    - 1: Took some steps, but not all, and then frame stopped changing OR the frame starts oscillating (trying to check for jitter). This usually means we ran into an obstacle.
    - 2: Took some steps, but agent state changed from free roam. This often means we entered a cutscene or battle.

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

    @staticmethod
    def get_action_name(x_steps: int, y_steps: int) -> str:
        return f"MoveGrid ({x_steps}, {y_steps})"


class MenuAction(HighLevelAction):
    """
    Allows simple navigation and option selection of menus.

    Is Valid When:
    - In Menu State

    Action Success Interpretation:
    - -1: Frame did not change.
    - 0: Frame changed.
    """

    REQUIRED_STATE_PARSER = PokemonStateParser
    REQUIRED_STATE_TRACKER = CorePokemonTracker

    _MENU_ACTION_MAP = {
        "up": LowLevelActions.PRESS_ARROW_UP,
        "down": LowLevelActions.PRESS_ARROW_DOWN,
        "confirm": LowLevelActions.PRESS_BUTTON_A,
        "left": LowLevelActions.PRESS_ARROW_LEFT,
        "right": LowLevelActions.PRESS_ARROW_RIGHT,
        "back": LowLevelActions.PRESS_BUTTON_B,
        # "open": LowLevelActions.PRESS_BUTTON_START,  # In general, we won't be using this action, but prefer OpenMenuAction instead.
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
        state = self._state_tracker.get_episode_metric(("pokemon_core", "agent_state"))
        return state in [
            AgentState.IN_MENU,
            AgentState.IN_BATTLE,
        ]  # works in battle screens and menu state

    def get_action_space(self):
        """
        Returns a Discrete space representing menu actions.
        Returns:
            Discrete: A Discrete space with size equal to the number of menu actions.
        """
        return Discrete(len(self._MENU_ACTION_MAP))

    def parameters_to_space(self, menu_action):
        if menu_action not in self._MENU_ACTION_KEYS:
            return None
        return self._MENU_ACTION_KEYS.index(menu_action)

    def space_to_parameters(self, space_action):
        menu_action = None
        if space_action < 0 or space_action >= len(self._MENU_ACTION_MAP):
            return None
        menu_action = self._MENU_ACTION_KEYS[space_action]
        return {"menu_action": menu_action}

    def _execute(self, menu_action):
        action = self._MENU_ACTION_MAP[menu_action]
        current_frame = self._emulator.get_current_frame()
        frames, done = self._emulator.step(action)
        action_success = 0 if frame_changed(current_frame, frames[-1]) else -1
        return [self._state_tracker.report()], action_success

    @staticmethod
    def get_action_name(menu_action: str) -> str:
        return f"Menu {menu_action}"


class OpenMenuAction(HighLevelAction):
    """
    Opens the main menu from free roam and navigates to specified option.
    Is Valid When:
    - In Free Roam State

    Action Success Interpretation:
    - -1: Navigation Failure. Screen did not end up in expected end state. This is a bug and should not happen.
    - 0: Navigation Success. Screen ended up in expected end state.

    """

    options = ["pokedex", "pokemon", "bag", "trainer"]

    def get_action_space(self):
        return Discrete(len(self.options))

    def space_to_parameters(self, space_action):
        if space_action < 0 or space_action >= len(self.options):
            return None
        return {"option": self.options[space_action]}

    def parameters_to_space(self, option: str):
        if option not in self.options:
            return None
        return self.options.index(option)

    def is_valid(self, option: str = None):
        if option is not None and option not in self.options:
            return False
        state = self._state_tracker.get_episode_metric(("pokemon_core", "agent_state"))
        return state == AgentState.FREE_ROAM

    def is_red_variant(self):
        """
        Returns true iff the current game is a red/blue variant.
        """
        return isinstance(self._emulator.state_parser, BasePokemonRedStateParser)

    def _execute(self, option: str):
        n_steps_down = 0
        if option == "pokedex":
            pass
        elif option == "pokemon":
            n_steps_down = 1
        elif option == "bag":
            n_steps_down = 2
        elif option == "trainer":
            if self.is_red_variant():
                n_steps_down = 3
            else:
                n_steps_down = 4
        else:
            log_error(f"Invalid option {option}", self._parameters)
        # first open menu
        self._emulator.step(LowLevelActions.PRESS_BUTTON_START)
        ret_states = [self._state_tracker.report()]
        # go to the top
        flag = False
        for _ in range(6):
            self._emulator.step(LowLevelActions.PRESS_ARROW_UP)
            if self._emulator.state_parser.is_on_top_menu_option(
                self._emulator.get_current_frame()
            ):
                flag = True
                break
        if not flag:  # could not get to top. Some error
            return ret_states, -1
        # go down n_steps_down
        for _ in range(n_steps_down):
            self._emulator.step(LowLevelActions.PRESS_ARROW_DOWN)
            ret_states.append(self._state_tracker.report())
        # confirm
        self._emulator.step(LowLevelActions.PRESS_BUTTON_A)
        ret_states.append(self._state_tracker.report())
        return ret_states, 0

    @staticmethod
    def get_action_name(option: str) -> str:
        return f"OpenMenu {option}"


class BattleMenuAction(HighLevelAction):
    """
    Allows navigation of the battle menu.

    Is Valid When:
    - In Battle State

    Action Success Interpretation:
    - -1: Navigation Failure. Screen did not end up in expected end state.
    - 0: Navigation Success. Screen ended up in expected end state. For run, got away safely.
    - 1: Run Attempt Failed (cannot escape wild pokemon)
    - 2: Run Attempt Failed (cannot escape trainer battle)
    """

    _OPTIONS = ["fight", "bag", "pokemon", "run", "progress"]

    def is_valid(self, option: str = None):
        if option is not None and option not in self._OPTIONS:
            return False
        state = self._state_tracker.get_episode_metric(("pokemon_core", "agent_state"))
        # TODO: Must check we aren't in a 'learn new move' screen
        return state == AgentState.IN_BATTLE

    def get_action_space(self):
        return Discrete(len(self._OPTIONS))

    def get_all_valid_parameters(self):
        state = self._state_tracker.get_episode_metric(("pokemon_core", "agent_state"))
        if state != AgentState.IN_BATTLE:
            return []
        return [{"option": option} for option in self._OPTIONS]

    def parameters_to_space(self, option: str):
        return self._OPTIONS.index(option)

    def space_to_parameters(self, space_action):
        if space_action < 0 or space_action >= len(self._OPTIONS):
            return None
        return {"option": self._OPTIONS[space_action]}

    def go_to_battle_menu(self):
        # assumes we are in battle menu or will get there with some B's
        state_reports = []
        for i in range(3):
            self._emulator.step(LowLevelActions.PRESS_BUTTON_B)
            state_reports.append(self._state_tracker.report())
        return state_reports

    def button_sequence(self, low_level_actions: List[LowLevelActions]):
        state_reports = self.go_to_battle_menu()
        for action in low_level_actions:
            self._emulator.step(action)
        self._emulator.step(LowLevelActions.PRESS_BUTTON_A)  # confirm option
        return state_reports + [self._state_tracker.report()]

    def go_to_fight_menu(self):
        return self.button_sequence(
            [LowLevelActions.PRESS_ARROW_UP, LowLevelActions.PRESS_ARROW_LEFT]
        )

    def go_to_bag_menu(self):
        return self.button_sequence(
            [LowLevelActions.PRESS_ARROW_DOWN, LowLevelActions.PRESS_ARROW_LEFT]
        )

    def go_to_pokemon_menu(self):
        return self.button_sequence(
            [LowLevelActions.PRESS_ARROW_UP, LowLevelActions.PRESS_ARROW_RIGHT]
        )

    def go_to_run(self):
        return self.button_sequence(
            [LowLevelActions.PRESS_ARROW_DOWN, LowLevelActions.PRESS_ARROW_RIGHT]
        )

    def _execute(self, option):
        success = -1
        if option == "fight":
            state_reports = self.go_to_fight_menu()
            success = (
                0
                if self._emulator.state_parser.is_in_fight_options_menu(
                    self._emulator.get_current_frame()
                )
                else -1
            )
        elif option == "bag":
            state_reports = self.go_to_bag_menu()
            success = (
                0
                if self._emulator.state_parser.is_in_fight_bag(
                    self._emulator.get_current_frame()
                )
                else -1
            )
        elif option == "pokemon":
            state_reports = self.go_to_pokemon_menu()
            success = (
                0
                if self._emulator.state_parser.is_in_pokemon_menu(
                    self._emulator.get_current_frame()
                )
                else -1
            )
        elif option == "run":
            state_reports = self.go_to_run()
            current_frame = self._emulator.get_current_frame()
            got_away_safely = (
                self._emulator.state_parser.named_region_matches_multi_target(
                    current_frame, "dialogue_box_middle", "got_away_safely"
                )
            )
            cannot_escape = (
                self._emulator.state_parser.named_region_matches_multi_target(
                    current_frame, "dialogue_box_middle", "cannot_escape"
                )
            )
            cannot_run_from_trainer = (
                self._emulator.state_parser.named_region_matches_multi_target(
                    current_frame, "dialogue_box_middle", "cannot_run_from_trainer"
                )
            )
            if got_away_safely:
                success = 0
                self._emulator.step(
                    LowLevelActions.PRESS_BUTTON_B
                )  # to clear the dialogue
            elif cannot_escape:
                success = 1
                self._emulator.step(
                    LowLevelActions.PRESS_BUTTON_B
                )  # to clear the dialogue
            elif cannot_run_from_trainer:
                success = 2
                self._emulator.step(LowLevelActions.PRESS_BUTTON_B)
                state_reports.append(self._state_tracker.report())
                self._emulator.step(
                    LowLevelActions.PRESS_BUTTON_B
                )  # Twice, to clear the dialogue
            else:
                pass  # Should never happen, but might.
            state_reports.append(self._state_tracker.report())
            return state_reports, success
        elif option == "progress":
            current_frame = self._emulator.get_current_frame()
            state_reports = self.go_to_battle_menu()
            new_frame = self._emulator.get_current_frame()
            if frame_changed(current_frame, new_frame):
                success = 0  # valid frame change, screen changed
            else:
                success = -1  # uneccesary progress press
        else:
            pass  # Will never happen.
        return state_reports, success

    @staticmethod
    def get_action_name(option: str) -> str:
        return f"BattleMenu {option}"


class PickAttackAction(HighLevelAction):
    """
    Selects an attack option in the battle fight menu.

    Is Valid When:
    - In Battle State AND In Fight Menu

    Action Success Interpretation:
    - -1: Navigation Failure. Either could not get to the top of the attack menu (this should not happen) or the option index was too high (more likely the cause of failure).
    - 0: Used attack successfully.
    - 1: Tried to use a move with no PP remaining.
    """

    def get_action_space(self):
        return Discrete(4)

    def is_valid(self, option: int = None):
        option = option - 1
        if option is not None:
            if option < 0 or option >= 4:
                return False
        return self._emulator.state_parser.is_in_fight_options_menu(
            self._emulator.get_current_frame()
        )

    def parameters_to_space(self, option: int):
        option = option - 1
        return option

    def space_to_parameters(self, space_action):
        return {"option": space_action + 1}

    def _execute(self, option: int):
        # assume we are in the attack menu already
        # first go to the top:
        option = option - 1
        flag = False
        for _ in range(4):
            self._emulator.step(LowLevelActions.PRESS_ARROW_UP)
            if self._emulator.state_parser.is_on_top_attack_option(
                self._emulator.get_current_frame()
            ):
                flag = True
                break
        if not flag:  # could not get to top. Some error
            return [self._state_tracker.report()], -1
        # then go down option times
        for time in range(option):
            self._emulator.step(LowLevelActions.PRESS_ARROW_DOWN)
            if self._emulator.state_parser.is_on_top_attack_option(
                self._emulator.get_current_frame()
            ):
                # went back to top, means that option was invalid
                return [self._state_tracker.report()], -1
        state_reports = []
        self._emulator.step(LowLevelActions.PRESS_BUTTON_A)  # confirm option
        state_reports.append(self._state_tracker.report())
        if self._emulator.state_parser.tried_no_pp_move(
            self._emulator.get_current_frame()
        ):
            self._emulator.step(
                LowLevelActions.PRESS_BUTTON_B
            )  # to clear the no PP dialogue
            state_reports.append(self._state_tracker.report())
            return state_reports, 1  # tried to use a move with no PP
        else:
            self._emulator.step(
                LowLevelActions.PRESS_BUTTON_B
            )  # to get through any attack animation dialogue
            state_reports.append(self._state_tracker.report())
        return state_reports, 0

    @staticmethod
    def get_action_name(option: int) -> str:
        return f"PickAttack {option}"
