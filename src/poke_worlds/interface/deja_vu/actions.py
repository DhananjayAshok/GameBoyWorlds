from abc import ABC
from poke_worlds.utils import log_error, log_warn
from typing import List, Optional, Tuple, Dict
import numpy as np
from gymnasium.spaces import Box, Discrete
from poke_worlds.emulation import LowLevelActions
from poke_worlds.emulation.deja_vu.parsers import AgentState, DejaVuStateParser
from poke_worlds.emulation.deja_vu.trackers import CoreDejaVuTracker
from poke_worlds.interface.action import HighLevelAction, SingleHighLevelAction

HARD_MAX_STEPS = 20
MENU_NAV_MAX_STEPS = 8

def frame_changed(past: np.ndarray, present: np.ndarray, epsilon: float = 0.01) -> bool:
    """Return True if the mean pixel difference between two frames is greater than epsilon."""
    return np.abs(past - present).mean() > epsilon

class TickUntilStable(SingleHighLevelAction):
    """Tick the emulator until the screen becomes stable (no change)."""
    REQUIRED_STATE_PARSER = DejaVuStateParser
    REQUIRED_STATE_TRACKER = CoreDejaVuTracker
    def is_valid(self, **kwargs):
        return True
    def _execute(self, max_ticks: int = 30):
        prev = self._emulator.get_current_frame()
        for _ in range(max_ticks):
            self._emulator.step(None)
            curr = self._emulator.get_current_frame()
            if not frame_changed(prev, curr):
                return [self._state_tracker.report()], 0
            prev = curr
        return [self._state_tracker.report()], -1

class MoveCursor(SingleHighLevelAction):
    """Move the menu cursor in a given direction (up, down, left, right)."""
    REQUIRED_STATE_PARSER = DejaVuStateParser
    REQUIRED_STATE_TRACKER = CoreDejaVuTracker
    _ACTION_MAP = {
        "up": LowLevelActions.PRESS_ARROW_UP,
        "down": LowLevelActions.PRESS_ARROW_DOWN,
        "left": LowLevelActions.PRESS_ARROW_LEFT,
        "right": LowLevelActions.PRESS_ARROW_RIGHT,
    }
    def is_valid(self, direction=None, **kwargs):
        return direction in self._ACTION_MAP
    def _execute(self, direction):
        action = self._ACTION_MAP[direction]
        prev = self._emulator.get_current_frame()
        self._emulator.step(action)
        curr = self._emulator.get_current_frame()
        return [self._state_tracker.report()], 0 if frame_changed(prev, curr) else -1

class MoveGrid(HighLevelAction):
    """Move the agent on the grid by (x_steps, y_steps). X is horizontal, Y is vertical."""
    REQUIRED_STATE_PARSER = DejaVuStateParser
    REQUIRED_STATE_TRACKER = CoreDejaVuTracker
    def get_action_space(self):
        return Box(low=-HARD_MAX_STEPS//2, high=HARD_MAX_STEPS//2, shape=(2,), dtype=np.int8)
    def is_valid(self, x_steps=None, y_steps=None, **kwargs):
        state = self._state_tracker.get_episode_metric(("dejavu_core", "agent_state"))
        return state == AgentState.FREE_ROAM and (x_steps or y_steps)
    def _execute(self, x_steps, y_steps):
        reports = []
        for axis, steps, dir_pos, dir_neg in [
            ("x", x_steps, "right", "left"),
            ("y", y_steps, "down", "up")]:
            if steps:
                direction = dir_pos if steps > 0 else dir_neg
                for _ in range(abs(steps)):
                    prev = self._emulator.get_current_frame()
                    self._emulator.step(MoveStepsAction._ACTION_MAP[direction])
                    curr = self._emulator.get_current_frame()
                    reports.append(self._state_tracker.report())
                    if not frame_changed(prev, curr):
                        return reports, -1
        return reports, 0

class OpenButtonMenu(SingleHighLevelAction):
    """Open the bottom button menu (usually START button)."""
    REQUIRED_STATE_PARSER = DejaVuStateParser
    REQUIRED_STATE_TRACKER = CoreDejaVuTracker
    def is_valid(self, **kwargs):
        state = self._state_tracker.get_episode_metric(("dejavu_core", "agent_state"))
        return state == AgentState.FREE_ROAM
    def _execute(self):
        self._emulator.step(LowLevelActions.PRESS_BUTTON_START)
        return [self._state_tracker.report()], 0

class CloseButtonMenu(SingleHighLevelAction):
    """Close the bottom button menu (usually B button)."""
    REQUIRED_STATE_PARSER = DejaVuStateParser
    REQUIRED_STATE_TRACKER = CoreDejaVuTracker
    def is_valid(self, **kwargs):
        state = self._state_tracker.get_episode_metric(("dejavu_core", "agent_state"))
        return state == AgentState.IN_MENU
    def _execute(self):
        self._emulator.step(LowLevelActions.PRESS_BUTTON_B)
        return [self._state_tracker.report()], 0

class SelectMenuOption(SingleHighLevelAction):
    """Select the current menu option (A button)."""
    REQUIRED_STATE_PARSER = DejaVuStateParser
    REQUIRED_STATE_TRACKER = CoreDejaVuTracker
    def is_valid(self, **kwargs):
        state = self._state_tracker.get_episode_metric(("dejavu_core", "agent_state"))
        return state == AgentState.IN_MENU
    def _execute(self):
        self._emulator.step(LowLevelActions.PRESS_BUTTON_A)
        return [self._state_tracker.report()], 0

class AdvanceDialogue(SingleHighLevelAction):
    """Advance dialogue (B button)."""
    REQUIRED_STATE_PARSER = DejaVuStateParser
    REQUIRED_STATE_TRACKER = CoreDejaVuTracker
    def is_valid(self, **kwargs):
        state = self._state_tracker.get_episode_metric(("dejavu_core", "agent_state"))
        return state == AgentState.IN_DIALOGUE
    def _execute(self):
        self._emulator.step(LowLevelActions.PRESS_BUTTON_B)
        return [self._state_tracker.report()], 0

# Helper for MoveGrid
class MoveStepsAction:
    _ACTION_MAP = {
        "up": LowLevelActions.PRESS_ARROW_UP,
        "down": LowLevelActions.PRESS_ARROW_DOWN,
        "left": LowLevelActions.PRESS_ARROW_LEFT,
        "right": LowLevelActions.PRESS_ARROW_RIGHT,
    }
class InteractAction(SingleHighLevelAction):
    """
    Presses the A button to interact with an object in front of the agent.

    Is Valid When:
    - In Free Roam State

    Action Success Interpretation:
    - -1: Frame did not change or agent still in free roam state
    - 1: Agent not in free roam state
    """

    REQUIRED_STATE_PARSER = DejaVuStateParser
    REQUIRED_STATE_TRACKER = CoreDejaVuTracker

    def is_valid(self, **kwargs):
        return (
            self._state_tracker.get_episode_metric(("dejavu_core", "agent_state"))
            == AgentState.FREE_ROAM
        )

    def _execute(self):
        frames, done = self._emulator.step(LowLevelActions.PRESS_BUTTON_A)
        action_success = 0
        prev_frames = []
        for frame in frames:
            if (
                self._emulator.state_parser.get_agent_state(frame)
                != AgentState.FREE_ROAM
            ):
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
            action_success = -1
        return [self._state_tracker.report()], action_success


class BaseMovementAction(HighLevelAction, ABC):
    """
    Base class for movement actions in the Deja Vu environment.

    Is Valid When:
    - In Free Roam State

    Action Success Interpretation:
    - -1: Frame did not change, even on the first step
    - 0: Finished all steps
    - 1: Took some steps, but not all, and then frame stopped changing OR the frame starts oscillating (trying to check for jitter). This usually means we ran into an obstacle.
    - 2: Took some steps, but agent state changed from free roam. This often means we entered a cutscene or battle.

    Action Returns:
    - n_steps_taken (int): Number of steps actually taken
    - rotated (bool or None): True if the player has not moved, but has rotated.
    """

    REQUIRED_STATE_TRACKER = CoreDejaVuTracker
    REQUIRED_STATE_PARSER = DejaVuStateParser

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
            if x_coord * y_coord == 0:
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
        for y in range(y_min + 1, y_max):
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
    ) -> Tuple[bool, Optional[bool]]:
        if not frame_changed(previous_frame, current_frame):
            return False, False
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
                prev_quad.max() == prev_quad.min()
                or self._is_uniform_quadrant(previous_frame, quadrant)
            )
            curr_uniform = (
                curr_quad.max() == curr_quad.min()
                or self._is_uniform_quadrant(current_frame, quadrant)
            )
            if (
                not frame_changed(prev_quad, curr_quad)
                and not prev_uniform
                and not curr_uniform
            ):
                flag = True
                break
        if flag:
            prev_player_cell = self._emulator.state_parser.capture_grid_cells(
                previous_frame
            )[(0, 0)]
            curr_player_cell = self._emulator.state_parser.capture_grid_cells(
                current_frame
            )[(0, 0)]
            if frame_changed(prev_player_cell, curr_player_cell):
                return False, True
            return False, False
        return True, None

    def move(self, direction: str, steps: int) -> Tuple[List[Dict], int]:
        action_dict = {
            "right": LowLevelActions.PRESS_ARROW_RIGHT,
            "down": LowLevelActions.PRESS_ARROW_DOWN,
            "up": LowLevelActions.PRESS_ARROW_UP,
            "left": LowLevelActions.PRESS_ARROW_LEFT,
        }
        if direction not in action_dict.keys():
            log_error(f"Got invalid direction to move {direction}", self._parameters)
        action = action_dict[direction]
        action_success = -1
        transition_state_dicts = []
        transition_frames = []
        previous_frame = self._emulator.get_current_frame()
        n_step = 0
        n_successful_steps = 0
        has_rotated = None
        agent_state = AgentState.FREE_ROAM
        while n_step < steps and agent_state == AgentState.FREE_ROAM:
            frames, done = self._emulator.step(action)
            transition_state_dicts.append(self._state_tracker.report())
            transition_frames.extend(frames)
            current_frame = self._emulator.get_current_frame()
            if done:
                break
            player_moved, player_rotated = self.judge_movement(
                previous_frame, current_frame
            )
            if player_rotated is True:
                has_rotated = True
            if not player_moved and not player_rotated:
                break
            if player_moved:
                n_successful_steps += 1
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
        return (
            self._state_tracker.get_episode_metric(("dejavu_core", "agent_state"))
            == AgentState.FREE_ROAM
        )


class MoveStepsAction(BaseMovementAction):
    """
    Moves the agent in a specified cardinal direction for a specified number of steps.
    """

    def get_action_space(self):
        return Discrete(4 * HARD_MAX_STEPS)

    def space_to_parameters(self, space_action):
        direction = None
        steps = None
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
        if steps is None or steps <= 0 or steps > HARD_MAX_STEPS:
            return None
        if direction == "up":
            return steps - 1
        if direction == "down":
            return HARD_MAX_STEPS + steps - 1
        if direction == "left":
            return 2 * HARD_MAX_STEPS + steps - 1
        if direction == "right":
            return 3 * HARD_MAX_STEPS + steps - 1
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
            if steps <= 0:
                return False
        return super().is_valid(**kwargs)


class MoveGridAction(BaseMovementAction):
    """
    Moves the agent on both axes. Will always try to move right/left first and then up/down.
    """

    def get_action_space(self):
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
        move_vec = np.zeros(2)
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
                "Weird case where both x_steps and y_steps are 0 in MoveGridAction or something.",
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


class MenuAction(HighLevelAction):
    """
    Allows navigation and option selection within Deja Vu menus.

    Is Valid When:
    - In Menu State

    Action Success Interpretation:
    - -1: Frame did not change.
    - 0: Frame changed.
    """

    REQUIRED_STATE_PARSER = DejaVuStateParser
    REQUIRED_STATE_TRACKER = CoreDejaVuTracker

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
        menu_action = kwargs.get("menu_action", None)
        if menu_action is not None and menu_action not in self._MENU_ACTION_KEYS:
            return False
        state = self._state_tracker.get_episode_metric(("dejavu_core", "agent_state"))
        return state == AgentState.IN_MENU

    def get_action_space(self):
        return Discrete(len(self._MENU_ACTION_MAP))

    def parameters_to_space(self, menu_action):
        if menu_action not in self._MENU_ACTION_KEYS:
            return None
        return self._MENU_ACTION_KEYS.index(menu_action)

    def space_to_parameters(self, space_action):
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


class OpenMenuAction(HighLevelAction):
    """
    Opens the investigation menu from free roam and optionally navigates to a section.

    Is Valid When:
    - In Free Roam State

    Action Success Interpretation:
    - -1: Could not open the menu or reach the requested section.
    - 0: Menu opened (and section selected if specified).
    """

    OPTIONS = ["open", "case_notes", "evidence", "location"]

    REQUIRED_STATE_PARSER = DejaVuStateParser
    REQUIRED_STATE_TRACKER = CoreDejaVuTracker

    def get_action_space(self):
        return Discrete(len(self.OPTIONS))

    def space_to_parameters(self, space_action):
        if space_action < 0 or space_action >= len(self.OPTIONS):
            return None
        return {"option": self.OPTIONS[space_action]}

    def parameters_to_space(self, option: Optional[str] = None):
        if option is None:
            option = "open"
        if option not in self.OPTIONS:
            return None
        return self.OPTIONS.index(option)

    def is_valid(self, option: Optional[str] = None):
        if option is not None and option not in self.OPTIONS:
            return False
        state = self._state_tracker.get_episode_metric(("dejavu_core", "agent_state"))
        return state == AgentState.FREE_ROAM

    def _is_target_menu(self, option: str, frame: np.ndarray) -> bool:
        parser = self._emulator.state_parser
        if option == "case_notes":
            return parser.is_in_case_notes(frame)
        if option == "evidence":
            return parser.is_in_evidence_menu(frame)
        if option == "location":
            return parser.is_location_menu_open(frame)
        return False

    def _execute(self, option: Optional[str] = None):
        if option is None:
            option = "open"
        self._emulator.step(LowLevelActions.PRESS_BUTTON_START)
        state_reports = [self._state_tracker.report()]
        current_frame = self._emulator.get_current_frame()
        if not self._emulator.state_parser.is_in_menu(current_frame):
            return state_reports, -1
        if option == "open":
            return state_reports, 0
        if self._is_target_menu(option, current_frame):
            return state_reports, 0
        for action in [
            LowLevelActions.PRESS_ARROW_RIGHT,
            LowLevelActions.PRESS_ARROW_LEFT,
        ]:
            for _ in range(MENU_NAV_MAX_STEPS):
                self._emulator.step(action)
                state_reports.append(self._state_tracker.report())
                current_frame = self._emulator.get_current_frame()
                if self._is_target_menu(option, current_frame):
                    return state_reports, 0
        return state_reports, -1


class PuzzleAction(HighLevelAction):
    """
    Allows navigation and option selection within Deja Vu puzzle/deduction states.

    Is Valid When:
    - In Puzzle State

    Action Success Interpretation:
    - -1: Frame did not change.
    - 0: Frame changed.
    """

    REQUIRED_STATE_PARSER = DejaVuStateParser
    REQUIRED_STATE_TRACKER = CoreDejaVuTracker

    _PUZZLE_ACTION_MAP = {
        "up": LowLevelActions.PRESS_ARROW_UP,
        "down": LowLevelActions.PRESS_ARROW_DOWN,
        "confirm": LowLevelActions.PRESS_BUTTON_A,
        "left": LowLevelActions.PRESS_ARROW_LEFT,
        "right": LowLevelActions.PRESS_ARROW_RIGHT,
        "back": LowLevelActions.PRESS_BUTTON_B,
    }

    _PUZZLE_ACTION_KEYS = list(_PUZZLE_ACTION_MAP.keys())

    def is_valid(self, **kwargs):
        puzzle_action = kwargs.get("puzzle_action", None)
        if puzzle_action is not None and puzzle_action not in self._PUZZLE_ACTION_KEYS:
            return False
        state = self._state_tracker.get_episode_metric(("dejavu_core", "agent_state"))
        return state == AgentState.IN_PUZZLE

    def get_action_space(self):
        return Discrete(len(self._PUZZLE_ACTION_MAP))

    def parameters_to_space(self, puzzle_action):
        if puzzle_action not in self._PUZZLE_ACTION_KEYS:
            return None
        return self._PUZZLE_ACTION_KEYS.index(puzzle_action)

    def space_to_parameters(self, space_action):
        if space_action < 0 or space_action >= len(self._PUZZLE_ACTION_MAP):
            return None
        puzzle_action = self._PUZZLE_ACTION_KEYS[space_action]
        return {"puzzle_action": puzzle_action}

    def _execute(self, puzzle_action):
        action = self._PUZZLE_ACTION_MAP[puzzle_action]
        current_frame = self._emulator.get_current_frame()
        frames, done = self._emulator.step(action)
        action_success = 0 if frame_changed(current_frame, frames[-1]) else -1
        return [self._state_tracker.report()], action_success
