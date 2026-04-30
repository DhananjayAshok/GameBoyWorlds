"""
Harvest Moon GBC game state parser implementations.
Uses visual screen regions to parse game state, following the same design principles as the Pokemon parsers.

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
from gameboy_worlds.emulation.parser import StateParser, _get_proper_regions

from typing import Set, List, Type, Dict, Optional, Tuple
import os
from abc import ABC, abstractmethod
from enum import Enum

from pyboy import PyBoy

import json
import numpy as np
from bidict import bidict


class AgentState(Enum):
    """
    0. FREE_ROAM: The agent is freely roaming the game world.
    1. IN_DIALOGUE: The agent is currently in a dialogue state.
    2. IN_MENU: The agent has a menu open.
    """

    FREE_ROAM = 0
    IN_DIALOGUE = 1
    IN_MENU = 2
    IN_STORAGE_LIST = 3


class HarvestMoonStateParser(StateParser, ABC):
    """
    Base class for Harvest Moon GBC game state parsers. Uses visual screen regions to parse game state.
    Defines common named screen regions and methods for determining game states such as being in dialogue.

    Can be used to determine the exact AgentState.
    """

    COMMON_REGIONS = []
    """ List of common single-target named screen regions for Harvest Moon games. """

    COMMON_MULTI_TARGET_REGIONS = [
        ("screen", 0, 0, 150, 140),
        ("screen_middle", 65, 55, 20, 20),
        ("dialogue_box_top", 58, 10, 40, 10),
    ]
    """ List of common multi-target named screen regions for Harvest Moon games.

    - dialogue_bottom_right: Bottom-right corner of the dialogue box (x=153, y=135, 10x10px).
      Capture while dialogue is visible in dev_play: `c dialogue_bottom_right,<type_name>`
    - screen_bottom: Bottom strip of the screen (x=0, y=100, 160x40px).
      Useful for detecting locations and events. Capture in dev_play: `c screen_bottom,<target_name>`
    """

    COMMON_MULTI_TARGETS = {
        "screen_bottom": [
            "cow_barn_entrance",
            "chicken_coop_entrance",
        ],
        "screen": [
            "menu_open",
        ],
        "dialogue_box_top": [
            "dialogue_open",
        ],
    }
    """ Common multi-targets for the common multi-target named screen regions.
    - screen_bottom: Location/event captures for the bottom strip of the screen.
    """

    def __init__(
        self,
        variant: str,
        pyboy: PyBoy,
        parameters: dict,
        additional_named_screen_region_details: List[
            Tuple[str, int, int, int, int]
        ] = [],
        additional_multi_target_named_screen_region_details: List[
            Tuple[str, int, int, int, int]
        ] = [],
        override_multi_targets: Dict[str, List[str]] = {},
    ):
        """
        Initializes the HarvestMoonStateParser.
        Args:
            pyboy (PyBoy): The PyBoy emulator instance.
            parameters (dict): Configuration parameters for the emulator.
            additional_named_screen_region_details (List[Tuple[str, int, int, int, int]]): Parameters associated with additional named screen regions to include.
            additional_multi_target_named_screen_region_details (List[Tuple[str, int, int, int, int]]): Parameters associated with additional multi-target named screen regions to include.
            override_multi_targets (Dict[str, List[str]]): Dictionary mapping region names to lists of additional target names for multi-target regions.
        """
        verify_parameters(parameters)
        regions = _get_proper_regions(
            override_regions=additional_named_screen_region_details,
            base_regions=self.COMMON_REGIONS,
        )
        self.variant = variant
        if f"{variant}_rom_data_path" not in parameters:
            log_error(
                f"ROM data path not found for variant: {variant}. Add {variant}_rom_data_path to the config files. See configs/pokemon_red_vars.yaml for an example",
                parameters,
            )
        self.rom_data_path = parameters[f"{variant}_rom_data_path"]
        """ Path to the ROM data directory for the specific Harvest Moon variant."""
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

    # def is_in_menu(self, current_screen: np.ndarray) -> bool:
    #     return self.named_region_matches_multi_target(current_screen, "screen", "menu_open")

    

    def get_agent_state(self, current_screen: np.ndarray) -> AgentState:
        if self.is_in_dialogue(current_screen):
            return AgentState.IN_DIALOGUE
        return AgentState.FREE_ROAM


class BaseHarvestMoonStateParser(HarvestMoonStateParser, ABC):
    """
    Game state parser for all Harvest Moon GBC-based games.
    """

    REGIONS = [
    ]
    """ Additional named screen regions specific to Harvest Moon GBC games.
    """

    MULTI_TARGET_REGIONS = [
    ]
    """ Additional multi-target named screen regions specific to Harvest Moon GBC games. 
    """

    def __init__(
        self,
        pyboy: PyBoy,
        variant: str,
        parameters: dict,
        override_regions: List[Tuple[str, int, int, int, int]] = [],
        override_multi_target_regions: List[Tuple[str, int, int, int, int]] = [],
        override_multi_targets: Dict[str, List[str]] = {},
    ):
        self.REGIONS = _get_proper_regions(
            override_regions=override_regions, base_regions=self.REGIONS
        )
        self.MULTI_TARGET_REGIONS = _get_proper_regions(
            override_regions=override_multi_target_regions,
            base_regions=self.MULTI_TARGET_REGIONS,
        )
        super().__init__(
            variant=variant,
            pyboy=pyboy,
            parameters=parameters,
            additional_named_screen_region_details=self.REGIONS,
            additional_multi_target_named_screen_region_details=self.MULTI_TARGET_REGIONS,
            override_multi_targets=override_multi_targets,
        )
    
    def __repr__(self):
        return f"<HarvestMoonParser(variant={self.variant})>"

class HarvestMoon1Parser(BaseHarvestMoonStateParser):

    DIALOGUE_TYPES = [
        "home_dialogue",
        "shop_dialogue",
        "church_dialogue",
        "harvest_spirits_dialogue",
        "read_signs_dialogue",
        "evening_dialogue",
        "barn_dialogue",
        "winter_read_signs_dialogue",
        "winter_evening_dialogue",
    ]
    def __init__(self, pyboy, parameters):
        override_regions = [
            ("menu_top_right", 153, 0, 5, 5),
            ("storage_list_top_right", 153, 0, 6, 6),
        ]
        
        override_multi_target_regions = [
            ("dialogue_bottom_right", 153, 135, 10, 10),
            ("screen", 0, 0, 160, 143),
            ("screen_middle", 65, 63, 30, 30),
            ("screen_bottom", 0, 100, 160, 40),
            ("dialogue_box_top", 60, 11, 40, 8),
            ("dialogue_box_top_mid", 68, 11, 22, 8),
            ("dialogue_box_top_short", 71, 11, 15, 8),
            ("dialogue_box_bottom", 0, 105, 160, 35),
            ("field_middle", 75, 60, 10,10),
            ("item_bed", 0, 40, 40, 40),
            ("item_watercan_above", 56, 85, 15, 35),
            ("item_watercan_right", 55, 80, 30, 20),
            ("item_watercan_below", 56, 70, 15, 30),
            ("item_sickle_above", 88, 85, 15, 35),
            ("item_sickle_left", 70, 80, 30, 20),
            ("item_sickle_below", 88, 70, 15, 30),
            ("item_hoe_above", 102, 85, 15, 35),
            ("item_hoe_below", 102, 70, 15, 30),
            ("item_hammer_above", 120, 85, 15, 35),
            ("item_hammer_below", 120, 70, 15, 30),
            ("item_grass_seed_above", 56, 55, 15, 35),
            ("item_grass_seed_right", 55, 70, 30, 20),
            ("item_grass_seed_below", 56, 70, 15, 30),
            ("item_storage_list", 0, 40, 20, 30),
            ("item_spirit_left", 70, 50, 30, 30),
            ("item_spirit_below", 70, 50, 30, 30),
            ("item_spirit_above", 70, 50, 15, 50),
            ("item_lost_bird_left", 70, 65, 30, 25),
            ("item_lost_bird_right", 60, 65, 30, 25),
            ("item_lost_bird_below", 70, 50, 20, 35),
            ("item_blue_hair_girl_left", 80, 20, 30, 30),
            ("item_blue_hair_girl_right", 95, 20, 30, 30),
            ("item_blue_hair_girl_below", 95, 20, 20, 40),
            ("item_golden_hair_girl_above", 32, 40, 15, 40),
            ("item_golden_hair_girl_right", 30, 55, 35, 25),
            ("item_golden_hair_girl_below", 32, 55, 15, 35),
            ("item_pink_hair_girl_left", 32, 68, 33, 22),
            ("item_pink_hair_girl_right", 48, 68, 30, 22),
            ("item_pink_hair_girl_above", 48, 68, 15, 38),
            ("item_chicken_stall_block1", 5, 40, 25, 20),
            ("item_next_to_chicken_stall_block1", 5, 55, 25, 25),
            ("item_chicken_silo_left", 100, 40, 30, 30),
            ("item_chicken_silo_below1", 120, 50, 15, 35),
            ("item_chicken_silo_below2", 135, 50, 15, 35),
            ("turnip_center", 70, 90, 20, 20),
            ("turnip_top", 70, 70, 20, 35),
            ("center_sign", 55, 65, 50, 15),
            ("screen_top_half", 0, 0, 160, 65),
            ("screen_bottom_half", 0, 75, 160, 65),
            ("left_border_frame", 0, 0, 5, 140),
        ]
        
        override_multi_targets = {
            "dialogue_bottom_right":[
                "home_dialogue",
                "shop_dialogue",
                "church_dialogue",
                "harvest_spirits_dialogue",
                "read_signs_dialogue",
                "evening_dialogue",
                "barn_dialogue",
                "winter_read_signs_dialogue",
                "winter_evening_dialogue",
            ],
            "screen_middle":[
                "outside_cow_barn_left",
                "outside_cow_barn_right",
                "outside_cow_barn_up",
                "outside_chicken_coop_left",
                "outside_chicken_coop_right",
                "outside_chicken_coop_up",
                "outside_storage_left",
                "outside_storage_right",
                "outside_storage_up",
            ],
            "screen_bottom": [
                "cow_barn_entrance",
                "chicken_coop_entrance",
                "storage_shed_entrance",
            ],
            "dialogue_box_bottom":[
                "choose_yes_for_sleep",
                "fed_spirit",
                "select_potato_seeds",
                "select_potato_seeds_portion",
                "select_turnip_seeds",
                "select_turnip_seeds_portion",
                "select_rice_ball",
                "select_croissant",
                "select_cake",
                "found_bird_for_friend",
                "speaking_to_blue_hair_girl",
                "speaking_to_golden_hair_girl",
                "speaking_to_pink_hair_girl",
                "option_to_pray",
                "praying",
            ],
            "item_bed":[
                "sleep_in_bed",
            ],
            "item_storage_list":[
                "next_to_storage_list",
            ],
            "item_watercan_above":[
                "pickup_watercan_down",
            ],
            "item_watercan_right":[
                "pickup_watercan_left",
            ],
            "item_watercan_below":[
                "pickup_watercan_up",
            ],
            "item_sickle_above":[
                "pickup_sickle_down",
            ],
            "item_sickle_left":[
                "pickup_sickle_right",
            ],
            "item_sickle_below":[
                "pickup_sickle_up",
            ],
            "item_hoe_above":[
                "pickup_hoe_down",
            ],
            "item_hoe_below":[
                "pickup_hoe_up",
            ],
            "item_hammer_above":[
                "pickup_hammer_down",
            ],
            "item_hammer_below":[
                "pickup_hammer_up",
            ],
            "item_grass_seed_above":[
                "pickup_grass_seed_down",
            ],
            "item_grass_seed_right":[
                "pickup_grass_seed_left",
            ],
            "item_grass_seed_below":[
                "pickup_grass_seed_up",
            ],
            "item_spirit_left":[
                "feed_spirit_right",
            ],
            "item_spirit_above":[
                "feed_spirit_down",
            ],
            "item_spirit_below":[
                "feed_spirit_up",
            ],
            "item_lost_bird_left":[
                "find_lost_bird_right",
            ],
            "item_lost_bird_right":[
                "find_lost_bird_left",
            ], 
            "item_lost_bird_below":[
                "find_lost_bird_up",
            ],
            "item_blue_hair_girl_left":[
                "next_to_blue_hair_girl_right",
            ],
            "item_blue_hair_girl_right":[
                "next_to_blue_hair_girl_left",
            ],
            "item_blue_hair_girl_below":[
                "next_to_blue_hair_girl_up",
            ],
            "item_golden_hair_girl_above":[
                "next_to_golden_hair_girl_down",
            ],
            "item_golden_hair_girl_right":[
                "next_to_golden_hair_girl_left",
            ],
            "item_golden_hair_girl_below":[
                "next_to_golden_hair_girl_up",
            ],
            "item_pink_hair_girl_left":[
                "next_to_pink_hair_girl_right",
            ],
            "item_pink_hair_girl_right":[
                "next_to_pink_hair_girl_left",
            ],
            "item_pink_hair_girl_above":[
                "next_to_pink_hair_girl_down",
            ],
            "item_chicken_stall_block1":[
                "filled_chicken_stall_block1",
            ],
            "item_next_to_chicken_stall_block1":[
                "next_to_chicken_stall_block1",
            ],
            "item_chicken_silo_left":[
                "next_to_chicken_silo_right",
                "got_fodder_from_chicken_silo_right",
            ],
            "item_chicken_silo_below1":[
                "next_to_chicken_silo_up1",
                "got_fodder_from_chicken_silo_up1",
            ],
            "item_chicken_silo_below2":[
                "next_to_chicken_silo_up2",
                "got_fodder_from_chicken_silo_up2",
            ],
            "dialogue_box_top":[
                "pick_up_watercan",
                "pick_up_grass_seed",
            ],
            "dialogue_box_top_mid":[
                "pick_up_sickle",
                "pick_up_hammer",
            ],
            "dialogue_box_top_short":[
                "pick_up_hoe",
            ],
            "turnip_center":[
                "finish_watering",
            ],
            "turnip_top":[
                "ready_to_water",
            ],
            "center_sign":[
                "outside_flower_shop",
                "outside_restaurant",
                "outside_church",
            ],
            "screen_bottom_half":[
                "bought_potato_seeds",
                "bought_turnip_seeds",
                "option_to_buy_rice_ball",
                "bought_rice_ball",
                "option_to_buy_croissant",
                "bought_croissant",
                "option_to_buy_cake",
                "bought_cake",
            ],
            "screen_top_half":[
                "in_restaurant",
                "in_flower_shop",
                "in_church",
            ],
            "left_border_frame":[
                "open_storage_list",
            ],
        }

        super().__init__(
            pyboy,
            variant="harvest_moon_1",
            parameters=parameters,
            override_regions=override_regions,
            override_multi_target_regions=override_multi_target_regions,
            override_multi_targets=override_multi_targets,
        )

    def dialogue_box_open(self, current_screen: np.ndarray) -> bool:
        """
        Determines if a dialogue box is currently open by checking the dialogue bottom right region.
        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.
        Returns:
            bool: True if a dialogue box is open, False otherwise.
        """
        captured = self.capture_named_region(current_screen, "dialogue_bottom_right")
        return self.named_screen_regions["dialogue_bottom_right"].matches_any_multi_target(
            self.DIALOGUE_TYPES, captured
        )

    def dialogue_box_empty(self, current_screen: np.ndarray) -> bool:
        box = self.capture_named_region(
            current_frame=current_screen, name="dialogue_box_bottom"
        )
        perc_lt_255 = np.mean(box < 255)
        if perc_lt_255 < 0.082:  # Empirical threshold
            return True
        return False
    
    def is_in_menu(self, current_screen: np.ndarray) -> bool:
        return self.named_region_matches_target(current_screen, "menu_top_right")

    def is_in_storage_list(self, current_screen: np.ndarray) -> bool:
        return self.named_region_matches_target(current_screen, "storage_list_top_right")

    def is_in_dialogue(self, current_screen: np.ndarray) -> bool:
        """
        Returns True if the dialogue_bottom_right region matches any of the saved dialogue type targets.
        """
        captured = self.capture_named_region(current_screen, "dialogue_bottom_right")
        return self.named_screen_regions["dialogue_bottom_right"].matches_any_multi_target(
            self.DIALOGUE_TYPES, captured
        )

    def get_agent_state(self, current_screen: np.ndarray) -> AgentState:
        """
        Determines the current agent state based on the screen.

        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.

        Returns:
            AgentState: The current agent state.
        """
        if self.is_in_menu(current_screen):
            return AgentState.IN_MENU
        if self.is_in_storage_list(current_screen):
            return AgentState.IN_STORAGE_LIST
        if self.is_in_dialogue(current_screen):
            return AgentState.IN_DIALOGUE
        return AgentState.FREE_ROAM
        
class HarvestMoon2Parser(BaseHarvestMoonStateParser):
    DIALOGUE_TYPES = [
        "home_dialogue",
        "carpenter_dialogue",
        "hospital_dialogue",
        "tool_shop_dialogue",
        "animal_shop_dialogue",
        "restaurant_dialogue",
        "library_dialogue",
        "flower_shop_dialogue",
        "church_dialogue",
        "read_signs_dialogue",
        "barn_dialogue",
    ]

    def __init__(self, pyboy, parameters):
        override_regions = [
            ("menu_top_right", 153, 8, 6, 6),
            ("storage_list_top_right", 153, 0, 6, 6),
        ]
        override_multi_target_regions = [
            ("dialogue_bottom_right", 153, 135, 10, 10),
            ("screen_middle", 65, 63, 30, 30),
            ("screen_bottom", 0, 95, 160, 40),
            ("dialogue_box_top", 60, 11, 40, 8),
            ("dialogue_box_bottom", 0, 105, 160, 35),
            ("flower_shop_location", 30, 0, 105, 70),
            ("restaurant_location", 40, 0, 70, 70),
            ("item_bed", 0, 40, 40, 40),
            ("item_diary", 45, 40, 20, 40),
            ("item_storage_list", 0, 40, 20, 30),
            ("item_village_sign_above", 70, 85, 20, 35),
            ("item_village_sign_left", 55, 70, 30, 25),
            ("item_village_sign_right", 75, 70, 30, 25),
            ("item_farm_sign_above", 70, 85, 20, 35),
            ("item_farm_sign_left", 55, 70, 30, 25),
            ("item_farm_sign_right", 75, 70, 30, 25),
            ("item_secret_garden_sign_above", 74, 50, 15, 45),
            ("item_secret_garden_sign_right", 58, 50, 27, 25),
            ("item_secret_garden_sign_left", 72, 50, 30, 25),
            ("item_crop_field_sign_above", 71, 55, 24, 40),
            ("item_notice_board_above", 70, 85, 20, 35),
            ("item_notice_board_left", 55, 70, 30, 25),
            ("item_notice_board_right", 75, 70, 30, 25),
            ("turnip_center", 70, 90, 20, 20),
            ("turnip_top", 70, 70, 20, 35),
            ("center_sign", 55, 65, 50, 15),
            ("screen_top_half", 0, 0, 160, 65),
            ("screen_bottom_half", 0, 75, 160, 65),
            ("left_border_frame", 0, 0, 5, 140),
        ]
        override_multi_targets = {
            "dialogue_bottom_right": [
                "home_dialogue",
                "carpenter_dialogue",
                "hospital_dialogue",
                "tool_shop_dialogue",
                "animal_shop_dialogue",
                "restaurant_dialogue",
                "library_dialogue",
                "flower_shop_dialogue",
                "church_dialogue",
                "read_signs_dialogue",
                "barn_dialogue",
            ],
            "screen_middle": [
                "outside_storage_left",
                "outside_storage_right",
                "outside_storage_up",
            ],
            "screen_bottom": [
                "storage_shed_entrance",
            ],
            "dialogue_box_bottom": [
                "choose_yes_for_sleep",
                "option_to_diary_sleep",
                "reading_village_sign",
                "reading_farm_sign",
                "reading_secret_garden_sign",
                "reading_crop_field_sign",
                "reading_notice_board",
            ],
            "flower_shop_location": [
                "outside_flower_shop_up",
                "outside_flower_shop_left",
                "outside_flower_shop_right",
            ],
            "item_bed": [
                "sleep_in_bed",
            ],
            "item_diary": [
                "next_to_diary",
            ],
            "item_storage_list": [
                "next_to_storage_list",
            ],
            "item_village_sign_above": [
                "next_to_village_sign_down",
            ],
            "item_village_sign_left": [
                "next_to_village_sign_right",
            ],
            "item_village_sign_right": [
                "next_to_village_sign_left",
            ],
            "item_farm_sign_above": [
                "next_to_farm_sign_down",
            ],
            "item_farm_sign_left": [
                "next_to_farm_sign_right",
            ],
            "item_farm_sign_right": [
                "next_to_farm_sign_left",
            ],
            "item_secret_garden_sign_above": [
                "next_to_secret_garden_sign_down",
            ],
            "item_secret_garden_sign_right": [
                "next_to_secret_garden_sign_left",
            ],
            "item_secret_garden_sign_left": [
                "next_to_secret_garden_sign_right",
            ],
            "item_crop_field_sign_above": [
                "next_to_crop_field_sign_down",
            ],
            "item_notice_board_above": [
                "next_to_notice_board_down",
            ],
            "item_notice_board_left": [
                "next_to_notice_board_right",
            ],
            "item_notice_board_right": [
                "next_to_notice_board_left",
            ],
            "turnip_center": [
                "finish_watering",
            ],
            "turnip_top": [
                "ready_to_water",
            ],
            "center_sign": [
                "outside_flower_shop",
            ],
            "restaurant_location": [
                "outside_restaurant_up",
                "outside_restaurant_left",
                "outside_restaurant_right",
            ],
            "screen_top_half": [
                "in_flower_shop",
                "in_restaurant",
            ],
            "screen_bottom_half": [
                "bought_potato_seeds",
                "bought_asparagus_seeds",
                "select_potato_seeds",
                "select_potato_seeds_portion",
                "select_asparagus_seeds",
                "select_asparagus_seeds_portion",
                "bought_lunch_set",
                "select_lunch_set",
                "option_to_buy_lunch_set",
                "bought_beverage_set",
                "select_beverage_set",
                "option_to_buy_beverage_set",
                "bought_todays_special",
                "select_todays_special",
                "option_to_buy_todays_special",
            ],
            "dialogue_box_top": [
                "pick_up_watercan",
            ],
            "left_border_frame": [
                "open_storage_list",
            ],
        }
        super().__init__(
            pyboy,
            variant="harvest_moon_2",
            parameters=parameters,
            override_regions=override_regions,
            override_multi_target_regions=override_multi_target_regions,
            override_multi_targets=override_multi_targets,
        )

    def dialogue_box_open(self, current_screen: np.ndarray) -> bool:
        return self.named_region_matches_target(current_screen, "dialogue_bottom_right")

    def dialogue_box_empty(self, current_screen: np.ndarray) -> bool:
        box = self.capture_named_region(
            current_frame=current_screen, name="dialogue_box_bottom"
        )
        perc_lt_255 = np.mean(box < 255)
        if perc_lt_255 < 0.082:  # Empirical threshold
            return True
        return False

    def is_in_menu(self, current_screen: np.ndarray) -> bool:
        return self.named_region_matches_target(current_screen, "menu_top_right")

    def is_in_storage_list(self, current_screen: np.ndarray) -> bool:
        return self.named_region_matches_target(current_screen, "storage_list_top_right")

    def is_in_dialogue(self, current_screen: np.ndarray) -> bool:
        captured = self.capture_named_region(current_screen, "dialogue_bottom_right")
        return self.named_screen_regions["dialogue_bottom_right"].matches_any_multi_target(
            self.DIALOGUE_TYPES, captured
        )

    def get_agent_state(self, current_screen: np.ndarray) -> AgentState:
        if self.is_in_menu(current_screen):
            return AgentState.IN_MENU
        if self.is_in_storage_list(current_screen):
            return AgentState.IN_STORAGE_LIST
        if self.is_in_dialogue(current_screen):
            return AgentState.IN_DIALOGUE
        return AgentState.FREE_ROAM


class HarvestMoon3Parser(BaseHarvestMoonStateParser):
    DIALOGUE_TYPES = [
        "normal_dialogue",
        "mainland_dialogue",
    ]

    def __init__(self, pyboy, parameters):
        override_regions = [
            ("menu_top_right", 153, 0, 6, 6),
        ]
        override_multi_target_regions = [
            ("dialogue_bottom_right", 153, 135, 10, 10),
            ("screen_bottom", 0, 95, 160, 40),
            ("dialogue_box_bottom", 0, 98, 160, 45),
            ("item_secret_garden_sign_above", 60, 55, 20, 40),
            ("item_secret_garden_sign_right", 50, 55, 35, 25),
            ("item_turnip_seeds_above", 30, 55, 17, 41),
            ("item_turnip_seeds_below", 30, 40, 17, 39),
            ("item_potato_seeds_above", 63, 55, 17, 41),
            ("item_potato_seeds_below", 63, 40, 17, 39),
            ("screen_top_half", 0, 0, 160, 65),
            ("screen_bottom_half", 0, 75, 160, 65),
            ("npc_lukia_right", 38, 55, 34, 25),
            ("dialogue_box_upper_border", 0, 96, 160, 8),
            ("npc_lucus_above", 70, 55, 19, 40),
            ("npc_lucus_left", 70, 55, 34, 25),
            ("npc_lucus_right", 55, 55, 34, 25),
            ("npc_lyla_right", 54, 55, 34, 25),
            ("item_meal_set_above", 80, 56, 17, 39),
            ("item_meal_set_below", 80, 40, 17, 39),
            ("item_coffee_above", 72, 55, 15, 39),
            ("item_coffee_below", 72, 40, 13, 30),
            ("item_turnip_1", 75, 80, 10, 13),
            ("item_turnip_2", 75, 80, 10, 13),
            ("entrance", 40, 65, 80, 80),
        ]
        override_multi_targets = {
            "dialogue_bottom_right": [
                "normal_dialogue",
                "mainland_dialogue",
            ],
            "dialogue_box_bottom": [
                "reading_secret_garden_sign",
                "select_turnip_seeds",
                "select_turnip_seeds_portion",
                "select_potato_seeds",
                "select_potato_seeds_portion",
                "bought_turnip_seeds",
                "bought_potato_seeds",
                "select_meal_set",
                "bought_meal_set",
                "select_coffee",
                "bought_coffee",
                "shopping_mall_label",
                "farmers_union_label",
                "aquarium_label",
                "theatre_label",
            ],
            "dialogue_box_upper_border": [
                "speaking_to_lukia",
                "speaking_to_lucus",
                "speaking_to_lyla",
            ],
            "item_secret_garden_sign_above": [
                "next_to_secret_garden_sign_down",
            ],
            "item_secret_garden_sign_right": [
                "next_to_secret_garden_sign_left",
            ],
            "item_turnip_seeds_above": [
                "next_to_turnip_seeds_down",
            ],
            "item_turnip_seeds_below": [
                "next_to_turnip_seeds_up",
            ],
            "item_potato_seeds_above": [
                "next_to_potato_seeds_down",
            ],
            "item_potato_seeds_below": [
                "next_to_potato_seeds_up",
            ],
            "screen_top_half": [
                "in_flower_shop",
            ],
            "npc_lukia_right": [
                "next_to_lukia_left",
            ],
            "npc_lucus_above": [
                "next_to_lucus_down",
            ],
            "npc_lucus_left": [
                "next_to_lucus_right",
            ],
            "npc_lucus_right": [
                "next_to_lucus_left",
            ],
            "npc_lyla_right": [
                "next_to_lyla_left",
            ],
            "item_meal_set_above": [
                "next_to_meal_set_down",
            ],
            "item_meal_set_below": [
                "next_to_meal_set_up",
            ],
            "item_coffee_above": [
                "next_to_coffee_down",
            ],
            "item_coffee_below": [
                "next_to_coffee_up",
            ],
            "entrance": [
                "shopping_mall_entrance",
                "farmers_union_entrance",
                "aquarium_entrance",
                "theatre_entrance",
            ],
        }
        super().__init__(
            pyboy,
            variant="harvest_moon_3",
            parameters=parameters,
            override_regions=override_regions,
            override_multi_target_regions=override_multi_target_regions,
            override_multi_targets=override_multi_targets,
        )

    def dialogue_box_open(self, current_screen: np.ndarray) -> bool:
        return self.named_region_matches_target(current_screen, "dialogue_bottom_right")

    def dialogue_box_empty(self, current_screen: np.ndarray) -> bool:
        box = self.capture_named_region(
            current_frame=current_screen, name="dialogue_box_bottom"
        )
        perc_lt_255 = np.mean(box < 255)
        if perc_lt_255 < 0.082:  # Empirical threshold
            return True
        return False

    def is_in_menu(self, current_screen: np.ndarray) -> bool:
        return self.named_region_matches_target(current_screen, "menu_top_right")
    
    def is_in_dialogue(self, current_screen: np.ndarray) -> bool:
        captured = self.capture_named_region(current_screen, "dialogue_bottom_right")
        if self.named_screen_regions["dialogue_bottom_right"].matches_any_multi_target(
            self.DIALOGUE_TYPES, captured
        ):
            return True
        return False

    def get_agent_state(self, current_screen: np.ndarray) -> AgentState:
        if self.is_in_menu(current_screen):
            return AgentState.IN_MENU
        if self.is_in_dialogue(current_screen):
            return AgentState.IN_DIALOGUE
        return AgentState.FREE_ROAM
