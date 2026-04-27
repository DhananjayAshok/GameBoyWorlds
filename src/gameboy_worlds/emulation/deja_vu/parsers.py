"""
DejaVu I & II: The Casebooks of Ace Harding game state parser implementations.

Deja Vu is a detective mystery game focused on investigation and puzzle-solving.

This parser provides visual-based state detection for:
1. FREE_ROAM: Walking around investigation areas and locations
2. IN_DIALOGUE: Interacting with NPCs, getting clues, and story progression
3. IN_MENU: Accessing case notes, evidence view, location map, or other menus

CORE DESIGN PRINCIPLE: Never branch the parser subclasses for a given variant. The inheritance tree for a parser after the game variant parser should always be a tree with only one child per layer.
This is to ensure that we don't double effort, any capability added to a parser will always be valid for that game variant.
If this principle is followed, any state tracker can always use the STRONGEST (lowest level) parser for a given variant without concern for missing functionality.
"""

from gameboy_worlds.emulation.parser import NamedScreenRegion
from gameboy_worlds.utils import (
    log_warn,
    log_info,
    log_error,
    load_parameters,
    verify_parameters,
)
from gameboy_worlds.emulation.parser import StateParser

from typing import Set, List, Type, Dict, Optional, Tuple
import os
from abc import ABC, abstractmethod
from enum import Enum

from pyboy import PyBoy

import numpy as np
from bidict import bidict


class AgentState(Enum):
    """
    0. FREE_ROAM: The agent is freely roaming the game world.
    1. IN_DIALOGUE: The agent is currently in a dialogue state. (e.g. receiving clues, action feedback)
    2. IN_MENU: The agent is currently in a menu state. (e.g. looking at items)
    """

    FREE_ROAM = 0
    IN_DIALOGUE = 1
    IN_MENU = 2


def _get_proper_regions(
    override_regions: List[Tuple[str, int, int, int, int]],
    base_regions: List[Tuple[str, int, int, int, int]],
) -> List[Tuple[str, int, int, int, int]]:
    """Merges base regions with override regions, giving precedence to override regions."""
    if len(override_regions) == 0:
        return base_regions
    proper_regions = override_regions.copy()
    override_names = [region[0] for region in override_regions]
    for region in base_regions:
        if region[0] not in override_names:
            proper_regions.append(region)
    return proper_regions


class DejaVuStateParser(StateParser, ABC):
    """
    Base class for DejaVu game state parsers. Uses visual screen regions to parse game state.
    Defines common named screen regions and methods for determining game states such as being in battle, menu, or dialogue.

    Can be used to determine the exact AgentState
    """

    COMMON_REGIONS = [
        ("dialogue_top_left_hook", 0, 73, 10, 6),
        ("menu_bottom_line", 0, 143, 160, 1),
        ("selected_outfit_button", 120, 17, 14, 15),
        ("pointed_at_13_on_map", 136, 80, 8, 8),
        ("pointed_at_21_on_map", 120, 72, 8, 8),
    ]
    """ 
    List of common named screen regions for Deja Vu game.
    
    Deja Vu uses a primarily text/menu-driven interface. These regions help identify:
    - dialogue_top_left_hook: A hook that appears in the top left after certain events, can be used to determine if certain game mechanics are available.
    - menu_bottom_line: A line that appears at the bottom of the screen when any menu is open, can be used to prevent agent interaction with the UI frame of the emulator.
    - selected_outfit_button: The area where the "Selected Outfit" button appears when the outfit menu is open, can be used to determine if the outfit menu is open.
    (the map is divided into a 5x5 grid of locations, with (1,1) being the bottom left and (5,5) being the top right - (i,j) corresponds to i-th row from the bottom and j-th column from the left)
    - pointed_at_13_on_map: The agent is currently pointing at location (1,3) on the map.
    - pointed_at_21_on_map: The agent is currently pointing at location (2,1) on the map.
    """

    COMMON_MULTI_TARGET_REGIONS = [
        ("dialogue_box_area", 0, 74, 160, 55),
        ("menu_box_area", 0, 70, 160, 70),
        ("action_bar_in_normal", 0, 114, 160, 14),
        ("action_bar_in_menu", 0, 26, 160, 14),
        ("menu_title_area", 23, 56, 96, 17),
        ("game_screen_area", 0, 0, 112, 112),
        # ("map_area", 120, 48, 40, 40),
    ]
    """
    List of common multi-target named screen regions for Deja Vu games.

    Deja Vu has certain regions that can contain multiple important visual cues.
    - dialogue_box_area: The area where dialogue text appears. Can contain multiple targets such as clues
    - menu_box_area: The area where menu options appear. Can contain multiple targets such as items or actions.
    - action_bar_in_normal: The upper area of the action bar in normal state.
    - action_bar_in_menu: The upper area of the action bar in when menu activated.
    - menu_title_area: The area where the menu title appears.
    - game_screen_area: The entire game screen area.
    - map_area: The area where the map appears when the map is open.
    """

    COMMON_MULTI_TARGETS = {
        "dialogue_box_area": [
            "a_default_target",
            "nothing_usual",
            "opened_door",
            "closed_door",
        ],
        "action_bar_in_normal": [
            "a_default_target",
            "no_action_selected",
            "selected_watch_action",
            "selected_use_action",
            "selected_take_action",
            "selected_open_action",
            "selected_close_action",
            "selected_talk_action",
            "selected_hit_action",
            "selected_throw_action",
        ],
        "action_bar_in_menu": [
            "a_default_target",
            "no_action_selected",
            "selected_watch_action",
            "selected_use_action",
            "selected_take_action",
            "selected_open_action",
            "selected_close_action",
            "selected_talk_action",
            "selected_hit_action",
            "selected_throw_action",
        ],
        "menu_title_area": [
            "a_default_target",
            "address_menu",
            "goods_menu",
        ],
        "game_screen_area": [
            "a_default_target",
            "socko_on_screen",
        ],
        # "map_area": [
        #     "a_default_target",
        #     "pointed_at_1_3",
        #     "pointed_at_2_1",
        # ],
    }
    """
    Common multi-targets for Deja Vu game regions.
    - dialogue_box_area:
        - nothing_usual: Point at useless area.
        - opened_door: Open the door in front of you.
    - action_bar_in_normal:
        - selected_watch_action: The "Watch" action is currently selected in the action bar.
        - selected_take_action: The "Take" action is currently selected in the action bar.
        - selected_open_action: The "Open" action is currently selected in the action bar.
        - selected_close_action: The "Close" action is currently selected in the action bar.
        - selected_use_action: The "Use" action is currently selected in the action bar.
    - action_bar_in_menu:
        - selected_watch_action: The "Watch" action is currently selected in the action bar.
        - selected_take_action: The "Take" action is currently selected in the action bar.
        - selected_open_action: The "Open" action is currently selected in the action bar.
        - selected_close_action: The "Close" action is currently selected in the action bar.
        - selected_use_action: The "Use" action is currently selected in the action bar.
    - menu_title_area:
        - address_menu: The address menu is currently open.
        - goods_menu: The goods menu is currently open.
    - game_screen_area:
        - socko_on_screen: The character "SOCKO" is currently visible on the screen.
    """

    def __init__(
        self,
        variant: str,
        pyboy: PyBoy,
        parameters: dict,
        additional_named_screen_region_details: List[Tuple[str, int, int, int, int]] = [],
        additional_multi_target_named_screen_region_details: List[Tuple[str, int, int, int, int]] = [],
        override_multi_targets: Dict[str, List[str]] = {},
    ):
        """
        Initializes the DejaVuStateParser.
        Args:
            variant (str): The variant of the Deja Vu game.
            pyboy (PyBoy): The PyBoy emulator instance.
            parameters (dict): Configuration parameters for the emulator.
            additional_named_screen_region_details (List[Tuple[str, int, int, int, int]]): Parameters associated with additional named screen regions to include.
            additional_multi_target_named_screen_region_details (List[Tuple[str, int, int, int, int]]): Parameters associated with additional multi-target named screen regions to include.
            override_multi_targets (Dict[str, List[str]]): Dictionary mapping region names to lists of target names for multi-target regions.
        """
        verify_parameters(parameters)
        regions = _get_proper_regions(
            override_regions=additional_named_screen_region_details,
            base_regions=self.COMMON_REGIONS,
        )
        self.variant = variant
        if f"{variant}_rom_data_path" not in parameters:
            log_error(
                f"ROM data path not found for variant: {variant}. Add {variant}_rom_data_path to the config files. See configs/deja_vu_vars.yaml for an example",
                parameters,
            )
        self.rom_data_path = parameters[f"{variant}_rom_data_path"]
        """ Path to the ROM data directory for the specific Deja Vu variant."""
        captures_dir = self.rom_data_path + "/captures/"
        named_screen_regions = []
        for region_name, x, y, w, h in regions:
            region = NamedScreenRegion(
                region_name,
                x,
                y,
                w,
                h,
                parameters=parameters,
                target_path=os.path.join(captures_dir, region_name),
            )
            named_screen_regions.append(region)
        multi_target_regions = _get_proper_regions(
            override_regions=additional_multi_target_named_screen_region_details,
            base_regions=self.COMMON_MULTI_TARGET_REGIONS,
        )
        multi_target_region_names = [region[0] for region in multi_target_regions]
        multi_targets = self.COMMON_MULTI_TARGETS.copy()
        for key in override_multi_targets:
            if key in multi_targets:
                multi_targets[key].extend(override_multi_targets[key])
            else:
                multi_targets[key] = override_multi_targets[key]
        multi_target_provided_region_names = list(multi_targets.keys())
        if not set(multi_target_provided_region_names).issubset(
            set(multi_target_region_names)
        ):
            log_error(
                f"Multi-target regions provided in multi_targets do not match the defined multi-target regions. Provided: {multi_target_provided_region_names}, Defined: {multi_target_region_names}",
                parameters,
            )
        for region_name, x, y, w, h in multi_target_regions:
            region_target_paths = {}
            subdir = captures_dir + f"/{region_name}/"
            for target_name in multi_targets.get(region_name, []):
                region_target_paths[target_name] = os.path.join(subdir, target_name)
            region = NamedScreenRegion(
                region_name,
                x,
                y,
                w,
                h,
                parameters=parameters,
                multi_target_paths=region_target_paths,
            )
            named_screen_regions.append(region)
        super().__init__(pyboy, parameters, named_screen_regions)

    def is_in_menu(self, current_screen: np.ndarray) -> bool:
        """
        Determines if any form of menu is currently open (Case Notes, Evidence, Location, etc).

        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.
            trust_previous (bool): If True, trusts that checks for other states have been done.

        Returns:
            bool: True if a menu is open, False otherwise.
        """
        return self.named_region_matches_target(current_screen, "menu_bottom_line")

    def is_in_dialogue(self, current_screen: np.ndarray) -> bool:
        """
        Determines if the player is currently in a dialogue state.
        Includes talking to NPCs, receiving clues, story narration, etc.

        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.
            trust_previous (bool): If True, trusts that checks for menu state have been done.

        Returns:
            bool: True if in dialogue, False otherwise.
        """
        if self.is_in_menu(current_screen):
            return False
        return self.named_region_matches_target(
            current_screen, "dialogue_top_left_hook"
        )

    def get_agent_state(self, current_screen: np.ndarray) -> AgentState:
        """
        Determines the current agent state based on the screen.

        Uses trust_previous to optimize checks.

        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.

        Returns:
            AgentState: The current agent state (FREE_ROAM, IN_DIALOGUE, or IN_MENU).
        """
        if self.is_in_menu(current_screen):
            return AgentState.IN_MENU
        elif self.is_in_dialogue(current_screen):
            return AgentState.IN_DIALOGUE
        else:
            return AgentState.FREE_ROAM


class DejaVu1StateParser(DejaVuStateParser):
    """Game state parser for Deja Vu I: The Casebooks of Ace Harding."""

    def __init__(self, pyboy, parameters):
        override_regions = [
            ("selected_coat_item", 0, 79, 160, 8),
            ("selected_wallet_item", 0, 120, 160, 8),
            ("selected_coin_item", 0, 95, 160, 8),
            ("using_coin_item", 0, 95, 160, 8),
            ("using_key3_item", 0, 88, 160, 8),
            ("using_key2_item", 0, 128, 160, 8),
        ]
        override_multi_target_regions = []
        override_multi_targets = {
            "dialogue_box_area": [
                "took_coat",
                "took_gun",
                "opened_pocket",
                "opened_wallet",
                "closed_pocket",
                "closed_wallet",
                "checked_coat",
                "checked_gun",
                "opened_spigot",
                "hit_bottle",
                "entered_cellar",
                "entered_connecting_room",
                "made_bet",
                "entered_empty_room",
                "unlocked_front_door",
                "met_mugger",
                "hit_mugger",
                "unlocked_car_door",
            ],
            "menu_title_area": [
                "coat_pocket_menu",
                "wallet_menu",
            ],
            "game_screen_area": [
                "opened_cellar_door",
            ]
        }

        super().__init__(
            variant="deja_vu_1",
            pyboy=pyboy,
            parameters=parameters,
            additional_named_screen_region_details=override_regions,
            additional_multi_target_named_screen_region_details=override_multi_target_regions,
            override_multi_targets=override_multi_targets,
        )

    def __repr__(self):
        return f"<DejaVuParser(variant={self.variant})>"


class DejaVu2StateParser(DejaVuStateParser):
    """Game state parser for Deja Vu II: The Casebooks of Ace Harding."""

    def __init__(self, pyboy, parameters):
        override_regions = [
            ("selected_gum_item", 0, 79, 160, 8),
            ("selected_pants_item", 0, 112, 160, 8),
            ("selected_trench_coat_item", 0, 88, 160, 8),
            ("selected_wallet1_item", 0, 96, 160, 8),
            ("selected_newsclip1_item", 0, 79, 160, 8),
            ("selected_license1_item", 0, 79, 160, 8),
        ]
        override_multi_target_regions = []
        override_multi_targets = {
            "dialogue_box_area": [
                "opened_trench_coat_pocket",
                "taken_gum",
                "opened_pants_pocket",
                "taken_pants",
                "closed_pants_pocket",
                "put_on_trench_coat",
                "put_on_pants",
                "opened_wallet1",
                "taken_newsclip1",
                "taken_license1",
                "closed_wallet1",
                "opened_cold_tap",
                "closed_cold_tap",
                "checked_newsclip1",
                "taken_ring1",
                "opened_room_door",
                "closed_room_door",
                "entered_hallway",
                "selected_2_chips",
                "bought_2_chips",
            ],
            "menu_title_area": [
                "trench_coat_pocket_menu",
                "wallet1_menu",
            ],
        }

        super().__init__(
            variant="deja_vu_2",
            pyboy=pyboy,
            parameters=parameters,
            additional_named_screen_region_details=override_regions,
            additional_multi_target_named_screen_region_details=override_multi_target_regions,
            override_multi_targets=override_multi_targets,
        )

    def __repr__(self):
        return f"<DejaVuParser(variant={self.variant})>"
