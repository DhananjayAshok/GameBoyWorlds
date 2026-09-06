from gameboy_worlds.utils import log_error, log_info
from gameboy_worlds.interface.pokemon.actions import (
    MoveStepsAction,
    MenuAction,
    InteractAction,
    PassDialogueAction,
    BattleMenuAction,
    PickAttackAction,
    MoveGridAction,
    OpenMenuAction,
    GetTeamInfoAction,
)
from gameboy_worlds.interface.controller import Controller
from gameboy_worlds.interface.action import HighLevelAction
from gameboy_worlds.emulation.pokemon.parsers import AgentState
from typing import Dict, Any


class PokemonStateWiseController(Controller):
    """
    High Level Actions for the Pokemon Environment:

    - In Free Roam:
        - MoveStepsAction(direction: str, steps: int): Move in a particular direction by a specified number of grid steps.
        - InteractAction(): Interact with cell directly in front of you. Only works if there is something to interact with.
        - OpenMenuAction(option: str): Open a specific player menu option.

    - In Dialogue:
        - PassDialogueAction(): Advance the dialogue by one step.

    - In Battle:
        - BattleMenuAction(option: str): Navigate the battle menu to select an option. Fight to choose an attack, Pokemon to switch Pokemon, Bag to use an item, Run to attempt to flee the battle, and Progress to continue dialogue or other battle events.
        - In Fight Options Menu:
            - PickAttackAction(option: int): Select an attack option in the battle fight menu.

    - In Menu:
        - MenuAction(menu_action: str): Navigate the game menu.
    """

    ACTIONS = [
        MoveStepsAction,
        MenuAction,
        InteractAction,
        PassDialogueAction,
        BattleMenuAction,
        PickAttackAction,
        MoveStepsAction,
        OpenMenuAction,
        GetTeamInfoAction,
    ]

    def string_to_high_level_action(self, input_str):
        input_str = input_str.lower().strip()
        if "(" not in input_str or ")" not in input_str:
            return None, None  # Invalid format
        action_name = input_str.split("(")[0].strip()
        action_args_str = input_str.split("(")[1].split(")")[0].strip()
        # First handle the no arg actions
        if action_name == "interact":
            return InteractAction, {}
        if action_name == "passdialogue":
            return PassDialogueAction, {}
        if action_name == "getteaminfo":
            return GetTeamInfoAction, {}
        # Now handle the actions with fixed options
        if action_name == "battlemenu":
            option = action_args_str.strip()
            if option in ["fight", "pokemon", "bag", "run", "progress"]:
                return BattleMenuAction, {"option": option}
            else:
                return None, None
        if action_name == "pickattack":
            if not action_args_str.strip().isnumeric():
                return None, None
            option = int(action_args_str.strip())
            if option < 1 or option > 4:
                return None, None
            return PickAttackAction, {"option": option}
        if action_name == "menu":
            option = action_args_str.strip()
            if option in ["up", "down", "left", "right", "confirm", "back"]:
                return MenuAction, {"menu_action": option}
            else:
                return None, None
        if action_name == "move":
            cardinal = None
            if "up" in action_args_str:
                cardinal = "up"
            if "down" in action_args_str:
                if cardinal is not None:
                    return None, None
                cardinal = "down"
            if "left" in action_args_str:
                if cardinal is not None:
                    return None, None
                cardinal = "left"
            if "right" in action_args_str:
                if cardinal is not None:
                    return None, None
                cardinal = "right"
            if cardinal is None:
                return None, None
            steps_part = action_args_str.replace(cardinal, "").strip()
            if not steps_part.isnumeric():
                return None, None
            steps = int(steps_part)
            return MoveStepsAction, {"direction": cardinal, "steps": steps}
        if action_name == "openmenu":
            option = action_args_str.strip()
            return OpenMenuAction, {"option": option}
        return None, None

    def get_action_strings(
        self, return_all: bool = False
    ) -> Dict[HighLevelAction, str]:
        current_state = self._emulator.state_parser.get_agent_state(
            self._emulator.get_current_frame()
        )
        free_roam_action_strings = {
            MoveStepsAction: "move(<up, down, right or left> <steps: int>): Move in a particular direction by a specified number of grid steps.",
            InteractAction: "interact(): Interact with cell directly in front of you. Only works if there is something to interact with.",
            OpenMenuAction: "openmenu(<pokedex, pokemon, bag, trainer>): Open a specific player menu option.",
            GetTeamInfoAction: "getteaminfo(): Open POKéMON from the START menu and return the visible team screen.",
        }
        dialogue_action_strings = {
            PassDialogueAction: "passdialogue(): Advance the dialogue by one step.",
        }
        battle_action_strings = {
            BattleMenuAction: "battlemenu(<fight, pokemon, bag, run or progress>): Navigate the battle menu to select an option. Fight to choose an attack, Pokemon to switch Pokemon, Bag to use an item, Run to attempt to flee the battle, and Progress to continue dialogue or other battle events.",
        }
        pick_attack_action_strings = {
            PickAttackAction: "pickattack(<1-4>): Select an attack option in the battle fight menu.",
        }
        menu_action_strings = {
            MenuAction: "menu(<up, down, left, right, confirm or back>): Navigate the game menu.",
        }
        if return_all:
            actions = {
                **free_roam_action_strings,
                **dialogue_action_strings,
                **battle_action_strings,
                **pick_attack_action_strings,
                **menu_action_strings,
            }
        else:
            if current_state == AgentState.FREE_ROAM:
                actions = free_roam_action_strings
            elif current_state == AgentState.IN_DIALOGUE:
                actions = dialogue_action_strings
            elif current_state == AgentState.IN_BATTLE:
                if self._emulator.state_parser.is_in_fight_options_menu(
                    self._emulator.get_current_frame()
                ):
                    actions = {**battle_action_strings, **pick_attack_action_strings}
                else:
                    actions = battle_action_strings
            elif current_state == AgentState.IN_MENU:
                actions = menu_action_strings
            else:
                log_error(
                    f"Unknown agent state {current_state} when getting action strings."
                )
        return actions
