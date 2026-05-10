from typing import Any, Dict, List, Type

import numpy as np
from gymnasium.spaces import Discrete

from gameboy_worlds.emulation import LowLevelActions
from gameboy_worlds.emulation.bomberman.parsers import (
    BombermanMaxParser,
    BombermanPocketParser,
    BombermanQuestParser,
)
from gameboy_worlds.emulation.bomberman.trackers import (
    BombermanMaxTracker,
    BombermanPocketTracker,
    BombermanQuestTracker,
)
from gameboy_worlds.interface.action import HighLevelAction, SingleHighLevelAction

HARD_MAX_STEPS = 10

MAX_MENU_METRIC = ("bomberman_max_core", "is_in_menu")
MAX_BATTLE_METRIC = ("bomberman_max_core", "is_in_battle")
POCKET_MENU_METRIC = ("bomberman_pocket_core", "is_in_menu")
QUEST_MENU_METRIC = ("bomberman_quest_core", "is_in_menu")
QUEST_BATTLE_METRIC = ("bomberman_quest_core", "is_in_battle")


def frame_changed(previous: np.ndarray, current: np.ndarray, epsilon: float = 0.01) -> bool:
    return np.abs(previous - current).mean() > epsilon


class _MoveAction(HighLevelAction):
    _DIRECTION_TO_ACTION = {}
    _BLOCKING_METRICS: List[tuple[str, str]] = []

    def get_action_space(self):
        return Discrete(len(self._DIRECTION_TO_ACTION) * HARD_MAX_STEPS)

    def space_to_parameters(self, space_action):
        directions = list(self._DIRECTION_TO_ACTION)
        if space_action < 0 or space_action >= len(directions) * HARD_MAX_STEPS:
            return None
        direction = directions[space_action // HARD_MAX_STEPS]
        steps = (space_action % HARD_MAX_STEPS) + 1
        return {"direction": direction, "steps": steps}

    def parameters_to_space(self, direction: str, steps: int):
        directions = list(self._DIRECTION_TO_ACTION)
        if direction not in directions or steps <= 0 or steps > HARD_MAX_STEPS:
            return None
        return directions.index(direction) * HARD_MAX_STEPS + steps - 1

    def is_valid(self, **kwargs):
        direction = kwargs.get("direction")
        steps = kwargs.get("steps")
        if direction is not None and direction not in self._DIRECTION_TO_ACTION:
            return False
        if steps is not None and (not isinstance(steps, int) or steps <= 0):
            return False
        return not any(
            self._state_tracker.get_episode_metric(metric_key)
            for metric_key in self._BLOCKING_METRICS
        )

    def _execute(self, direction: str, steps: int):
        action = self._DIRECTION_TO_ACTION[direction]
        transition_state_dicts: List[Dict[str, Any]] = []
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
            if any(
                self._state_tracker.get_episode_metric(metric_key)
                for metric_key in self._BLOCKING_METRICS
            ):
                action_success = 2
                break
            if done:
                action_success = 0
                break
            previous_frame = current_frame
        else:
            action_success = 0
        if transition_state_dicts:
            transition_state_dicts[-1]["core"]["action_return"] = {
                "n_steps_taken": n_steps_taken
            }
        return transition_state_dicts, action_success


class _MetricGatedSingleAction(SingleHighLevelAction):
    _BUTTON = None
    _REQUIRED_METRICS_FALSE: List[tuple[str, str]] = []
    _REQUIRED_METRICS_TRUE: List[tuple[str, str]] = []

    def is_valid(self, **kwargs):
        return all(
            not self._state_tracker.get_episode_metric(metric_key)
            for metric_key in self._REQUIRED_METRICS_FALSE
        ) and all(
            self._state_tracker.get_episode_metric(metric_key)
            for metric_key in self._REQUIRED_METRICS_TRUE
        )

    def _execute(self):
        previous = self._emulator.get_current_frame()
        frames, _ = self._emulator.step(self._BUTTON)
        report = self._state_tracker.report()
        return [report], 0 if frame_changed(previous, frames[-1]) else -1


class BombermanMaxMoveAction(_MoveAction):
    REQUIRED_STATE_TRACKER = BombermanMaxTracker
    REQUIRED_STATE_PARSER = BombermanMaxParser
    _DIRECTION_TO_ACTION = {
        "up": LowLevelActions.PRESS_ARROW_UP,
        "down": LowLevelActions.PRESS_ARROW_DOWN,
        "left": LowLevelActions.PRESS_ARROW_LEFT,
        "right": LowLevelActions.PRESS_ARROW_RIGHT,
    }
    _BLOCKING_METRICS = [MAX_MENU_METRIC, MAX_BATTLE_METRIC]


class BombermanMaxPlaceBombAction(_MetricGatedSingleAction):
    REQUIRED_STATE_TRACKER = BombermanMaxTracker
    REQUIRED_STATE_PARSER = BombermanMaxParser
    _BUTTON = LowLevelActions.PRESS_BUTTON_A
    _REQUIRED_METRICS_FALSE = [MAX_MENU_METRIC, MAX_BATTLE_METRIC]


class BombermanMaxKickBombAction(_MetricGatedSingleAction):
    REQUIRED_STATE_TRACKER = BombermanMaxTracker
    REQUIRED_STATE_PARSER = BombermanMaxParser
    _BUTTON = LowLevelActions.PRESS_BUTTON_B
    _REQUIRED_METRICS_FALSE = [MAX_MENU_METRIC, MAX_BATTLE_METRIC]


class BombermanMaxOpenMenuAction(_MetricGatedSingleAction):
    REQUIRED_STATE_TRACKER = BombermanMaxTracker
    REQUIRED_STATE_PARSER = BombermanMaxParser
    _BUTTON = LowLevelActions.PRESS_BUTTON_START
    _REQUIRED_METRICS_FALSE = [MAX_MENU_METRIC, MAX_BATTLE_METRIC]

    def _execute(self):
        self._emulator.step(self._BUTTON)
        report = self._state_tracker.report()
        return [report], 0 if self._state_tracker.get_episode_metric(MAX_MENU_METRIC) else -1


class BombermanMaxCloseMenuAction(_MetricGatedSingleAction):
    REQUIRED_STATE_TRACKER = BombermanMaxTracker
    REQUIRED_STATE_PARSER = BombermanMaxParser
    _BUTTON = LowLevelActions.PRESS_BUTTON_START
    _REQUIRED_METRICS_TRUE = [MAX_MENU_METRIC]

    def _execute(self):
        self._emulator.step(self._BUTTON)
        report = self._state_tracker.report()
        return [report], 0 if not self._state_tracker.get_episode_metric(MAX_MENU_METRIC) else -1


class BombermanMaxNavigateMenuAction(SingleHighLevelAction):
    REQUIRED_STATE_TRACKER = BombermanMaxTracker
    REQUIRED_STATE_PARSER = BombermanMaxParser
    _ACTION_MAP = {
        "up": LowLevelActions.PRESS_ARROW_UP,
        "down": LowLevelActions.PRESS_ARROW_DOWN,
        "left": LowLevelActions.PRESS_ARROW_LEFT,
        "right": LowLevelActions.PRESS_ARROW_RIGHT,
        "confirm": LowLevelActions.PRESS_BUTTON_A,
        "back": LowLevelActions.PRESS_BUTTON_B,
    }

    def get_action_space(self):
        return Discrete(len(self._ACTION_MAP))

    def space_to_parameters(self, space_action):
        keys = list(self._ACTION_MAP)
        if space_action < 0 or space_action >= len(keys):
            return None
        return {"menu_action": keys[space_action]}

    def parameters_to_space(self, menu_action: str):
        keys = list(self._ACTION_MAP)
        return keys.index(menu_action) if menu_action in keys else None

    def is_valid(self, **kwargs):
        menu_action = kwargs.get("menu_action")
        return (
            menu_action in self._ACTION_MAP if menu_action is not None else True
        ) and self._state_tracker.get_episode_metric(MAX_MENU_METRIC)

    def _execute(self, menu_action: str):
        previous = self._emulator.get_current_frame()
        frames, _ = self._emulator.step(self._ACTION_MAP[menu_action])
        report = self._state_tracker.report()
        return [report], 0 if frame_changed(previous, frames[-1]) else -1


class BombermanMaxBattleAction(SingleHighLevelAction):
    REQUIRED_STATE_TRACKER = BombermanMaxTracker
    REQUIRED_STATE_PARSER = BombermanMaxParser
    _ACTION_MAP = {
        "bomb": LowLevelActions.PRESS_BUTTON_A,
        "up": LowLevelActions.PRESS_ARROW_UP,
        "down": LowLevelActions.PRESS_ARROW_DOWN,
        "left": LowLevelActions.PRESS_ARROW_LEFT,
        "right": LowLevelActions.PRESS_ARROW_RIGHT,
    }

    def get_action_space(self):
        return Discrete(len(self._ACTION_MAP))

    def space_to_parameters(self, space_action):
        keys = list(self._ACTION_MAP)
        if space_action < 0 or space_action >= len(keys):
            return None
        return {"battle_action": keys[space_action]}

    def parameters_to_space(self, battle_action: str):
        keys = list(self._ACTION_MAP)
        return keys.index(battle_action) if battle_action in keys else None

    def is_valid(self, **kwargs):
        battle_action = kwargs.get("battle_action")
        return (
            battle_action in self._ACTION_MAP if battle_action is not None else True
        ) and self._state_tracker.get_episode_metric(MAX_BATTLE_METRIC)

    def _execute(self, battle_action: str):
        previous = self._emulator.get_current_frame()
        frames, _ = self._emulator.step(self._ACTION_MAP[battle_action])
        report = self._state_tracker.report()
        return [report], 0 if frame_changed(previous, frames[-1]) else -1


class BombermanPocketMoveAction(_MoveAction):
    REQUIRED_STATE_TRACKER = BombermanPocketTracker
    REQUIRED_STATE_PARSER = BombermanPocketParser
    _DIRECTION_TO_ACTION = {
        "left": LowLevelActions.PRESS_ARROW_LEFT,
        "right": LowLevelActions.PRESS_ARROW_RIGHT,
    }
    _BLOCKING_METRICS = [POCKET_MENU_METRIC]


class BombermanPocketJumpAction(_MetricGatedSingleAction):
    REQUIRED_STATE_TRACKER = BombermanPocketTracker
    REQUIRED_STATE_PARSER = BombermanPocketParser
    _BUTTON = LowLevelActions.PRESS_BUTTON_B
    _REQUIRED_METRICS_FALSE = [POCKET_MENU_METRIC]


class BombermanPocketPlaceBombAction(_MetricGatedSingleAction):
    REQUIRED_STATE_TRACKER = BombermanPocketTracker
    REQUIRED_STATE_PARSER = BombermanPocketParser
    _BUTTON = LowLevelActions.PRESS_BUTTON_A
    _REQUIRED_METRICS_FALSE = [POCKET_MENU_METRIC]


class BombermanPocketOpenPauseMenuAction(_MetricGatedSingleAction):
    REQUIRED_STATE_TRACKER = BombermanPocketTracker
    REQUIRED_STATE_PARSER = BombermanPocketParser
    _BUTTON = LowLevelActions.PRESS_BUTTON_START
    _REQUIRED_METRICS_FALSE = [POCKET_MENU_METRIC]

    def _execute(self):
        self._emulator.step(self._BUTTON)
        report = self._state_tracker.report()
        return [report], 0 if self._state_tracker.get_episode_metric(POCKET_MENU_METRIC) else -1


class BombermanPocketClosePauseMenuAction(_MetricGatedSingleAction):
    REQUIRED_STATE_TRACKER = BombermanPocketTracker
    REQUIRED_STATE_PARSER = BombermanPocketParser
    _BUTTON = LowLevelActions.PRESS_BUTTON_START
    _REQUIRED_METRICS_TRUE = [POCKET_MENU_METRIC]

    def _execute(self):
        self._emulator.step(self._BUTTON)
        report = self._state_tracker.report()
        return [report], 0 if not self._state_tracker.get_episode_metric(POCKET_MENU_METRIC) else -1


class BombermanQuestMoveAction(_MoveAction):
    REQUIRED_STATE_TRACKER = BombermanQuestTracker
    REQUIRED_STATE_PARSER = BombermanQuestParser
    _DIRECTION_TO_ACTION = {
        "up": LowLevelActions.PRESS_ARROW_UP,
        "down": LowLevelActions.PRESS_ARROW_DOWN,
        "left": LowLevelActions.PRESS_ARROW_LEFT,
        "right": LowLevelActions.PRESS_ARROW_RIGHT,
    }
    _BLOCKING_METRICS = [QUEST_MENU_METRIC, QUEST_BATTLE_METRIC]


class BombermanQuestPlaceBombAction(_MetricGatedSingleAction):
    REQUIRED_STATE_TRACKER = BombermanQuestTracker
    REQUIRED_STATE_PARSER = BombermanQuestParser
    _BUTTON = LowLevelActions.PRESS_BUTTON_A
    _REQUIRED_METRICS_FALSE = [QUEST_MENU_METRIC, QUEST_BATTLE_METRIC]


class BombermanQuestUseBButtonItemAction(_MetricGatedSingleAction):
    REQUIRED_STATE_TRACKER = BombermanQuestTracker
    REQUIRED_STATE_PARSER = BombermanQuestParser
    _BUTTON = LowLevelActions.PRESS_BUTTON_B
    _REQUIRED_METRICS_FALSE = [QUEST_MENU_METRIC, QUEST_BATTLE_METRIC]


class BombermanQuestOpenMenuAction(_MetricGatedSingleAction):
    REQUIRED_STATE_TRACKER = BombermanQuestTracker
    REQUIRED_STATE_PARSER = BombermanQuestParser
    _BUTTON = LowLevelActions.PRESS_BUTTON_START
    _REQUIRED_METRICS_FALSE = [QUEST_MENU_METRIC, QUEST_BATTLE_METRIC]

    def _execute(self):
        self._emulator.step(self._BUTTON)
        report = self._state_tracker.report()
        return [report], 0 if self._state_tracker.get_episode_metric(QUEST_MENU_METRIC) else -1


class BombermanQuestCloseMenuAction(_MetricGatedSingleAction):
    REQUIRED_STATE_TRACKER = BombermanQuestTracker
    REQUIRED_STATE_PARSER = BombermanQuestParser
    _BUTTON = LowLevelActions.PRESS_BUTTON_START
    _REQUIRED_METRICS_TRUE = [QUEST_MENU_METRIC]

    def _execute(self):
        self._emulator.step(self._BUTTON)
        report = self._state_tracker.report()
        return [report], 0 if not self._state_tracker.get_episode_metric(QUEST_MENU_METRIC) else -1


class BombermanQuestNavigateMenuAction(BombermanMaxNavigateMenuAction):
    REQUIRED_STATE_TRACKER = BombermanQuestTracker
    REQUIRED_STATE_PARSER = BombermanQuestParser

    def is_valid(self, **kwargs):
        menu_action = kwargs.get("menu_action")
        return (
            menu_action in self._ACTION_MAP if menu_action is not None else True
        ) and self._state_tracker.get_episode_metric(QUEST_MENU_METRIC)


class BombermanQuestBattleAction(BombermanMaxBattleAction):
    REQUIRED_STATE_TRACKER = BombermanQuestTracker
    REQUIRED_STATE_PARSER = BombermanQuestParser
    _ACTION_MAP = {
        "bomb": LowLevelActions.PRESS_BUTTON_A,
        "item": LowLevelActions.PRESS_BUTTON_B,
        "up": LowLevelActions.PRESS_ARROW_UP,
        "down": LowLevelActions.PRESS_ARROW_DOWN,
        "left": LowLevelActions.PRESS_ARROW_LEFT,
        "right": LowLevelActions.PRESS_ARROW_RIGHT,
    }

    def is_valid(self, **kwargs):
        battle_action = kwargs.get("battle_action")
        return (
            battle_action in self._ACTION_MAP if battle_action is not None else True
        ) and self._state_tracker.get_episode_metric(QUEST_BATTLE_METRIC)

