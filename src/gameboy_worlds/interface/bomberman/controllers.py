from typing import Dict, Type

from gameboy_worlds.interface.action import HighLevelAction
from gameboy_worlds.interface.bomberman.actions import (
    BombermanMaxBattleAction,
    BombermanMaxCloseMenuAction,
    BombermanMaxKickBombAction,
    BombermanMaxMoveAction,
    BombermanMaxNavigateMenuAction,
    BombermanMaxOpenMenuAction,
    BombermanMaxPlaceBombAction,
    BombermanPocketClosePauseMenuAction,
    BombermanPocketJumpAction,
    BombermanPocketMoveAction,
    BombermanPocketOpenPauseMenuAction,
    BombermanPocketPlaceBombAction,
    BombermanQuestBattleAction,
    BombermanQuestCloseMenuAction,
    BombermanQuestMoveAction,
    BombermanQuestNavigateMenuAction,
    BombermanQuestOpenMenuAction,
    BombermanQuestPlaceBombAction,
    BombermanQuestUseBButtonItemAction,
)
from gameboy_worlds.interface.controller import Controller

MAX_MENU_METRIC = ("bomberman_max_core", "is_in_menu")
MAX_BATTLE_METRIC = ("bomberman_max_core", "is_in_battle")
POCKET_MENU_METRIC = ("bomberman_pocket_core", "is_in_menu")
QUEST_MENU_METRIC = ("bomberman_quest_core", "is_in_menu")
QUEST_BATTLE_METRIC = ("bomberman_quest_core", "is_in_battle")


class BombermanMaxStateWiseController(Controller):
    ACTIONS = [
        BombermanMaxMoveAction,
        BombermanMaxPlaceBombAction,
        BombermanMaxKickBombAction,
        BombermanMaxOpenMenuAction,
        BombermanMaxCloseMenuAction,
        BombermanMaxNavigateMenuAction,
        BombermanMaxBattleAction,
    ]

    def string_to_high_level_action(self, input_str):
        text = input_str.lower().strip()
        if "(" not in text or ")" not in text:
            return None, None
        action_name = text.split("(")[0].strip()
        action_args_str = text.split("(")[1].split(")")[0].strip()
        if action_name == "move":
            parts = [x.strip() for x in action_args_str.replace(",", " ").split() if x.strip()]
            if len(parts) == 2 and parts[0] in ["up", "down", "left", "right"] and parts[1].isdigit():
                return BombermanMaxMoveAction, {"direction": parts[0], "steps": int(parts[1])}
        elif action_name == "placebomb":
            return BombermanMaxPlaceBombAction, {}
        elif action_name == "kickbomb":
            return BombermanMaxKickBombAction, {}
        elif action_name == "openmenu":
            return BombermanMaxOpenMenuAction, {}
        elif action_name == "closemenu":
            return BombermanMaxCloseMenuAction, {}
        elif action_name == "navigatemenu" and action_args_str in ["up", "down", "left", "right", "confirm", "back"]:
            return BombermanMaxNavigateMenuAction, {"menu_action": action_args_str}
        elif action_name == "battle" and action_args_str in ["bomb", "up", "down", "left", "right"]:
            return BombermanMaxBattleAction, {"battle_action": action_args_str}
        return None, None

    def get_action_strings(self, return_all: bool = False) -> Dict[Type[HighLevelAction], str]:
        free_roam_strings = {
            BombermanMaxMoveAction: "move(<up/down/left/right> <steps>): Move in a direction for N steps.",
            BombermanMaxPlaceBombAction: "placebomb(): Place a bomb (A button).",
            BombermanMaxKickBombAction: "kickbomb(): Kick bomb or use B-button power-up.",
            BombermanMaxOpenMenuAction: "openmenu(): Open the pause/item menu (Start).",
        }
        menu_strings = {
            BombermanMaxNavigateMenuAction: "navigatemenu(<up/down/left/right/confirm/back>): Navigate the pause menu.",
            BombermanMaxCloseMenuAction: "closemenu(): Close the pause/item menu (Start).",
        }
        battle_strings = {
            BombermanMaxBattleAction: "battle(<bomb/up/down/left/right>): Act during a Charabom battle.",
        }
        if return_all:
            return {**free_roam_strings, **menu_strings, **battle_strings}
        if hasattr(self, "_state_tracker") and self._state_tracker.get_episode_metric(MAX_MENU_METRIC):
            return menu_strings
        if hasattr(self, "_state_tracker") and self._state_tracker.get_episode_metric(MAX_BATTLE_METRIC):
            return battle_strings
        return free_roam_strings


class BombermanPocketStateWiseController(Controller):
    ACTIONS = [
        BombermanPocketMoveAction,
        BombermanPocketJumpAction,
        BombermanPocketPlaceBombAction,
        BombermanPocketOpenPauseMenuAction,
        BombermanPocketClosePauseMenuAction,
    ]

    def string_to_high_level_action(self, input_str):
        text = input_str.lower().strip()
        if "(" not in text or ")" not in text:
            return None, None
        action_name = text.split("(")[0].strip()
        action_args_str = text.split("(")[1].split(")")[0].strip()
        if action_name == "move":
            parts = [x.strip() for x in action_args_str.replace(",", " ").split() if x.strip()]
            if len(parts) == 2 and parts[0] in ["left", "right"] and parts[1].isdigit():
                return BombermanPocketMoveAction, {"direction": parts[0], "steps": int(parts[1])}
        elif action_name == "jump":
            return BombermanPocketJumpAction, {}
        elif action_name == "placebomb":
            return BombermanPocketPlaceBombAction, {}
        elif action_name == "openpausemenu":
            return BombermanPocketOpenPauseMenuAction, {}
        elif action_name == "closepausemenu":
            return BombermanPocketClosePauseMenuAction, {}
        return None, None

    def get_action_strings(self, return_all: bool = False) -> Dict[Type[HighLevelAction], str]:
        gameplay_strings = {
            BombermanPocketMoveAction: "move(<left/right> <steps>): Move left or right for N steps.",
            BombermanPocketJumpAction: "jump(): Jump (B button).",
            BombermanPocketPlaceBombAction: "placebomb(): Place a bomb at current position (A button).",
            BombermanPocketOpenPauseMenuAction: "openpausemenu(): Open the pause menu (Start).",
        }
        pause_menu_strings = {
            BombermanPocketClosePauseMenuAction: "closepausemenu(): Close the pause menu (Start).",
        }
        if return_all:
            return {**gameplay_strings, **pause_menu_strings}
        if hasattr(self, "_state_tracker") and self._state_tracker.get_episode_metric(POCKET_MENU_METRIC):
            return pause_menu_strings
        return gameplay_strings


class BombermanQuestStateWiseController(Controller):
    ACTIONS = [
        BombermanQuestMoveAction,
        BombermanQuestPlaceBombAction,
        BombermanQuestUseBButtonItemAction,
        BombermanQuestOpenMenuAction,
        BombermanQuestCloseMenuAction,
        BombermanQuestNavigateMenuAction,
        BombermanQuestBattleAction,
    ]

    def string_to_high_level_action(self, input_str):
        text = input_str.lower().strip()
        if "(" not in text or ")" not in text:
            return None, None
        action_name = text.split("(")[0].strip()
        action_args_str = text.split("(")[1].split(")")[0].strip()
        if action_name == "move":
            parts = [x.strip() for x in action_args_str.replace(",", " ").split() if x.strip()]
            if len(parts) == 2 and parts[0] in ["up", "down", "left", "right"] and parts[1].isdigit():
                return BombermanQuestMoveAction, {"direction": parts[0], "steps": int(parts[1])}
        elif action_name == "placebomb":
            return BombermanQuestPlaceBombAction, {}
        elif action_name == "usebitem":
            return BombermanQuestUseBButtonItemAction, {}
        elif action_name == "openmenu":
            return BombermanQuestOpenMenuAction, {}
        elif action_name == "closemenu":
            return BombermanQuestCloseMenuAction, {}
        elif action_name == "navigatemenu" and action_args_str in ["up", "down", "left", "right", "confirm", "back"]:
            return BombermanQuestNavigateMenuAction, {"menu_action": action_args_str}
        elif action_name == "battle" and action_args_str in ["bomb", "item", "up", "down", "left", "right"]:
            return BombermanQuestBattleAction, {"battle_action": action_args_str}
        return None, None

    def get_action_strings(self, return_all: bool = False) -> Dict[Type[HighLevelAction], str]:
        free_roam_strings = {
            BombermanQuestMoveAction: "move(<up/down/left/right> <steps>): Move in a direction for N steps.",
            BombermanQuestPlaceBombAction: "placebomb(): Place a bomb / use A-button item.",
            BombermanQuestUseBButtonItemAction: "usebitem(): Use B-button item.",
            BombermanQuestOpenMenuAction: "openmenu(): Open the pause/item menu (Start).",
        }
        menu_strings = {
            BombermanQuestNavigateMenuAction: "navigatemenu(<up/down/left/right/confirm/back>): Navigate the pause menu.",
            BombermanQuestCloseMenuAction: "closemenu(): Close the pause/item menu (Start).",
        }
        battle_strings = {
            BombermanQuestBattleAction: "battle(<bomb/item/up/down/left/right>): Act during a monster battle.",
        }
        if return_all:
            return {**free_roam_strings, **menu_strings, **battle_strings}
        if hasattr(self, "_state_tracker") and self._state_tracker.get_episode_metric(QUEST_MENU_METRIC):
            return menu_strings
        if hasattr(self, "_state_tracker") and self._state_tracker.get_episode_metric(QUEST_BATTLE_METRIC):
            return battle_strings
        return free_roam_strings

