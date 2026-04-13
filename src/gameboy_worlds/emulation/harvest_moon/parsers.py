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
    """

    FREE_ROAM = 0
    IN_DIALOGUE = 1


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

    def get_agent_state(self, current_screen: np.ndarray) -> AgentState:
        """
        Determines the current agent state based on the screen.

        Returns:
            AgentState: FREE_ROAM or IN_DIALOGUE.
        """
        # if self.is_in_dialogue(current_screen):
        #     return AgentState.IN_DIALOGUE
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
    def __init__(self, pyboy, parameters):
        override_multi_target_regions = [
            ("screen", 0, 0, 160, 143),
            ("screen_middle", 65, 63, 30, 30),
            ("screen_bottom", 0, 100, 160, 40),
            ("dialogue_box_top", 60, 11, 40, 8),
            ("dialogue_box_bottom", 0, 105, 160, 35),
            ("field_middle", 75, 60, 10,10),
            ("item_bed", 0, 40, 40, 40),
            ("item_watercan_above", 56, 85, 15, 35),
            ("item_watercan_right", 55, 80, 30, 20),
            ("item_watercan_below", 56, 70, 15, 30),
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
            "screen_middle":[
                "outside_cow_barn_left",
                "outside_cow_barn_right",
                "outside_cow_barn_up",
                "outside_chicken_coop_left",
                "outside_chicken_coop_right",
                "outside_chicken_coop_up",
            ],
            "dialogue_box_bottom":[
                "choose_yes_for_sleep",
                "fed_spirit",
                "select_potato_seeds",
                "select_potato_seeds_portion",
                "select_turnip_seeds",
                "select_turnip_seeds_portion",
                "select_rice_ball",
                "found_bird_for_friend",
                "speaking_to_blue_hair_girl",
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
            ],
            "screen_bottom_half":[
                "bought_potato_seeds",                
                "bought_turnip_seeds",
                "option_to_buy_rice_ball",
                "bought_rice_ball",
            ],
            "screen_top_half":[
                "in_restaurant",
                "in_flower_shop",
            ],
            "left_border_frame":[
                "open_storage_list",
            ],
        }

        super().__init__(
            pyboy,
            variant="harvest_moon_1",
            parameters=parameters,
            override_multi_target_regions=override_multi_target_regions,
            override_multi_targets=override_multi_targets,
        )
        
class HarvestMoon2Parser(BaseHarvestMoonStateParser):
    def __init__(self, pyboy, parameters):
        override_multi_target_regions = [
            ("screen_bottom", 0, 95, 160, 40),
        ]
        super().__init__(
            pyboy,
            variant="harvest_moon_2",
            parameters=parameters,
            override_multi_target_regions=override_multi_target_regions,
        )


class HarvestMoon3Parser(BaseHarvestMoonStateParser):
    def __init__(self, pyboy, parameters):
        override_multi_target_regions = [
            ("screen_bottom", 0, 95, 160, 40),
        ]
        super().__init__(
            pyboy,
            variant="harvest_moon_3",
            parameters=parameters,
            override_multi_target_regions=override_multi_target_regions,
        )
