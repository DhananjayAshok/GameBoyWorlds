from poke_worlds.utils import log_error
from poke_worlds.interface.deja_vu.actions import (
    TickUntilStable,
    MoveCursor,
    MoveGrid,
    OpenButtonMenu,
    CloseButtonMenu,
    SelectMenuOption,
    AdvanceDialogue,
)
from poke_worlds.interface.controller import Controller
from poke_worlds.interface.action import HighLevelAction
from poke_worlds.emulation.deja_vu.parsers import AgentState
from typing import Dict

class DejaVuStateWiseController(Controller):
    """
    High-level controller for Deja Vu. Only supports:
    - TickUntilStable: tick until screen is stable
    - MoveCursor: move menu cursor
    - MoveGrid: grid movement
    - OpenButtonMenu: open bottom menu
    - CloseButtonMenu: close bottom menu
    - SelectMenuOption: select menu option
    - AdvanceDialogue: advance dialogue
    """
    ACTIONS = [
        TickUntilStable,
        MoveCursor,
        MoveGrid,
        OpenButtonMenu,
        CloseButtonMenu,
        SelectMenuOption,
        AdvanceDialogue,
    ]

    def string_to_high_level_action(self, input_str):
        input_str = input_str.lower().strip()
        if "(" not in input_str or ")" not in input_str:
            return None, None
        action_name = input_str.split("(")[0].strip()
        action_args_str = input_str.split("(")[1].split(")")[0].strip()

        if action_name == "tickuntilstable":
            return TickUntilStable, {}
        if action_name == "movecursor":
            direction = action_args_str.strip()
            if direction in ["up", "down", "left", "right"]:
                return MoveCursor, {"direction": direction}
            return None, None
        if action_name == "movegrid":
            try:
                x, y = map(int, action_args_str.split(","))
                return MoveGrid, {"x_steps": x, "y_steps": y}
            except Exception:
                return None, None
        if action_name == "openbuttonmenu":
            return OpenButtonMenu, {}
        if action_name == "closebuttonmenu":
            return CloseButtonMenu, {}
        if action_name == "selectmenuoption":
            return SelectMenuOption, {}
        if action_name == "advancedialogue":
            return AdvanceDialogue, {}
        return None, None

    def get_action_strings(self, return_all: bool = False):
        return {
            TickUntilStable: "tickuntilstable(): Tick until screen is stable.",
            MoveCursor: "movecursor(<up,down,left,right>): Move menu cursor.",
            MoveGrid: "movegrid(<x:int>,<y:int>): Grid movement.",
            OpenButtonMenu: "openbuttonmenu(): Open bottom menu.",
            CloseButtonMenu: "closebuttonmenu(): Close bottom menu.",
            SelectMenuOption: "selectmenuoption(): Select current menu option.",
            AdvanceDialogue: "advancedialogue(): Advance dialogue.",
        }
