from gameboy_worlds.utils import log_error, log_info
from gameboy_worlds.interface.harvest_moon.actions import (
    MoveStepsAction,
    InteractAction,
    PassDialogueAction,
    MoveGridAction,
)
from gameboy_worlds.interface.controller import Controller
from gameboy_worlds.interface.action import HighLevelAction
from gameboy_worlds.emulation.harvest_moon.parsers import AgentState
from typing import Dict, Any


class HarvestMoonStateWiseController(Controller):
    """
    High Level Actions for the Harvest Moon Environment:

    - In Free Roam:
        - MoveStepsAction(direction: str, steps: int): Move in a particular direction by a specified number of grid steps.
        - InteractAction(): Interact with cell directly in front of you. Only works if there is something to interact with.

    - In Dialogue:
        - PassDialogueAction(): Advance the dialogue by one step.
    """

    ACTIONS = [
        MoveStepsAction,
        InteractAction,
        PassDialogueAction,
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
        }
        dialogue_action_strings = {
            PassDialogueAction: "passdialogue(): Advance the dialogue by one step.",
        }
        if return_all:
            actions = {
                **free_roam_action_strings,
                **dialogue_action_strings,
            }
        else:
            if current_state == AgentState.FREE_ROAM:
                actions = free_roam_action_strings
            elif current_state == AgentState.IN_DIALOGUE:
                actions = dialogue_action_strings
            else:
                log_error(
                    f"Unknown agent state {current_state} when getting action strings."
                )
                actions = {}
        return actions
