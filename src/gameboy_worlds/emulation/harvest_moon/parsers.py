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
            ("screen_bottom", 0, 100, 160, 40),
        ]

        super().__init__(
            pyboy,
            variant="harvest_moon_1",
            parameters=parameters,
            override_multi_target_regions=override_multi_target_regions,
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
