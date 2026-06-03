"""
Runes of Virtue specific game state parser implementations.

Visual screen-region matching is used (mirroring the Pokemon module's design) so that
adding additional Runes of Virtue variants only requires per-variant capture data and
optional region overrides, not a fork of the parser logic.

CORE DESIGN PRINCIPLE: Never branch the parser subclasses for a given variant. The inheritance tree for a parser after the game variant parser should always be a tree with only one child per layer.
This is to ensure that we don't double effort, any capability added to a parser will always be valid for that game variant.
If this principle is followed, any state tracker can always use the STRONGEST (lowest level) parser for a given variant without concern for missing functionality.
"""

import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Tuple

import numpy as np
from pyboy import PyBoy

from gameboy_worlds.emulation.parser import (
    NamedScreenRegion,
    StateParser,
    _get_proper_regions,
)
from gameboy_worlds.utils import log_error, verify_parameters


class AgentState(Enum):
    """
    0. FREE_ROAM: The agent is freely roaming the game world.
    1. IN_MENU: The agent is in the inventory/status menu.
    2. IN_DIALOGUE: The agent is in an NPC dialogue overlay.
    """

    FREE_ROAM = 0
    IN_MENU = 1
    IN_DIALOGUE = 2


class RunesOfVirtueStateParser(StateParser, ABC):
    """
    Base class for Runes of Virtue game state parsers. Uses visual screen regions to parse game state.
    Defines common named screen regions and methods for determining game states such as being in a menu.

    Can be used to determine the exact AgentState.
    """

    COMMON_REGIONS: List[Tuple[str, int, int, int, int]] = []
    """ List of common named screen regions for Runes of Virtue games. Subclasses extend this with variant-specific regions via override_regions. """

    COMMON_MULTI_TARGET_REGIONS: List[Tuple[str, int, int, int, int]] = []
    """ List of common multi-target named screen regions for Runes of Virtue games. """

    COMMON_MULTI_TARGETS: Dict[str, List[str]] = {}
    """ Common multi-targets for the common multi-target named screen regions. """

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
        Initializes the RunesOfVirtueStateParser.
        Args:
            variant (str): The variant of the Runes of Virtue game.
            pyboy (PyBoy): The PyBoy emulator instance.
            parameters (dict): Configuration parameters for the emulator.
            additional_named_screen_region_details: Additional named screen region tuples to register.
            additional_multi_target_named_screen_region_details: Additional multi-target named screen region tuples to register.
            override_multi_targets: Dictionary mapping region names to lists of target names for multi-target regions.
        """
        verify_parameters(parameters)
        regions = _get_proper_regions(
            override_regions=additional_named_screen_region_details,
            base_regions=self.COMMON_REGIONS,
        )
        self.variant = variant
        if f"{variant}_rom_data_path" not in parameters:
            log_error(
                f"ROM data path not found for variant: {variant}. Add {variant}_rom_data_path to the config files. See configs/rom_data_path_vars.yaml for an example",
                parameters,
            )
        self.rom_data_path = parameters[f"{variant}_rom_data_path"]
        """ Path to the ROM data directory for the specific Runes of Virtue variant."""
        captures_dir = os.path.join(self.rom_data_path, "captures")
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
        multi_targets = {k: list(v) for k, v in self.COMMON_MULTI_TARGETS.items()}
        for key in override_multi_targets:
            if key in multi_targets:
                multi_targets[key].extend(override_multi_targets[key])
            else:
                multi_targets[key] = list(override_multi_targets[key])
        if not set(multi_targets.keys()).issubset(set(multi_target_region_names)):
            log_error(
                f"Multi-target regions provided in multi_targets do not match the defined multi-target regions. Provided: {list(multi_targets.keys())}, Defined: {multi_target_region_names}",
                parameters,
            )
        for region_name, x, y, w, h in multi_target_regions:
            region_target_paths = {}
            subdir = os.path.join(captures_dir, region_name)
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

    @abstractmethod
    def is_in_menu(self, current_screen: np.ndarray) -> bool:
        """
        Determines if the inventory/status menu is currently open.

        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.
        Returns:
            bool: True if the menu is open, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def is_in_dialogue(self, current_screen: np.ndarray) -> bool:
        """
        Determines if an NPC dialogue overlay is currently visible.

        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.
        Returns:
            bool: True if any dialogue overlay is visible, False otherwise.
        """
        raise NotImplementedError

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
        if self.is_in_dialogue(current_screen):
            return AgentState.IN_DIALOGUE
        return AgentState.FREE_ROAM

    def dialogue_box_open(self, current_screen: np.ndarray) -> bool:
        """
        Determines if a dialogue box is currently open.
        """
        box = self.capture_named_region(
            current_frame=current_screen, name=self.get_dialogue_ocr_region_name()
        )
        white_rows = np.mean(box == 255, axis=(1, 2))
        return np.count_nonzero(white_rows > 0.98) >= 10

    def dialogue_box_empty(self, current_screen: np.ndarray) -> bool:
        """
        Determines if the dialogue OCR region has no meaningful text content.
        """
        box = self.capture_named_region(
            current_frame=current_screen, name=self.get_dialogue_ocr_region_name()
        )
        return np.mean(box < 255) < 0.05

    def get_dialogue_ocr_region_name(self) -> str:
        return "dialogue_ocr_region"

    def __repr__(self) -> str:
        return f"<RunesOfVirtueParser(variant={self.variant})>"


class RunesOfVirtue1StateParser(RunesOfVirtueStateParser):
    """
    State parser for Ultima: Runes of Virtue (1991).

    Screen regions:
    - menu_indicator: A region (y=30-50, x=20-60) that is uniformly white when the
      inventory/status menu is open (triggered by START), and contains game world
      content during normal gameplay.
    - dialog_indicator: A multi-target dialogue box region shared by NPC dialogue
      targets with the same screen coordinates.
    - dialogue_ocr_region: Dialogue text area captured for OCR.
    """

    REGIONS = [
        ("menu_indicator", 20, 30, 40, 20),
    ]
    """ Additional named screen regions specific to Runes of Virtue 1.
    - menu_indicator: A patch above the dialogue box that goes white when the inventory/status menu opens. Open the START menu to capture this.
    """

    MULTI_TARGET_REGIONS = [
        ("king_dialog_indicator", 5, 100, 115, 40),
        ("dialog_indicator", 5, 90, 115, 40),
        ("cave_indicator", 0, 0, 100, 70),
        ("playfield_indicator", 0, 0, 144, 144),
        ("top_playfield_indicator", 0, 0, 144, 24),
        ("telescope_view_indicator", 40, 40, 80, 60),
        ("death_screen_indicator", 60, 100, 30, 30),
        ("dialogue_ocr_region", 5, 90, 135, 54),
    ]
    """ Additional multi-target named screen regions specific to Runes of Virtue 1. """

    MULTI_TARGETS = {
        "king_dialog_indicator": ["king_dialog"],
        "dialog_indicator": [
            "chuckles_dialog",
            "gnu_gnu_1_dialog",
            "gnu_gnu_2_dialog",
            "sherry_dialog",
            "dr_cat_cats_lair_dialog",
            "cavern_of_cowardice_sherry_floor_4_dialog",
        ],
        "cave_indicator": [
            "cavern_of_hatred",
            "cavern_of_deceit",
            "cavern_of_cowardice",
        ],
        "playfield_indicator": [
            "king_dialog",
            "chuckles_dialog",
            "gnu_gnu_1_dialog",
            "gnu_gnu_2_dialog",
            "sherry_dialog",
            "dr_cat_cats_lair_dialog",
            "cavern_of_cowardice_sherry_floor_4_dialog",
            "cavern_of_hatred_chest_floor_1_opened",
            "dr_cat_dialog",
            "ship_ridden",
            "basement_ladder_unlocked",
            "basement_chest_opened",
            "cavern_of_cowardice_enter_floor_2",
            "cavern_of_cowardice_enter_floor_3",
            "cavern_of_cowardice_floor_3_chest_opened",
            "cavern_of_cowardice_take_stew_floor_4",
            "cavern_of_cowardice_obtain_coin_floor_4",
            "cavern_of_hatred_enter_floor_2",
            "cavern_of_hatred_sherry_floor_2_dialog",
            "cavern_of_hatred_choose_door_with_sherry",
            "cavern_of_hatred_choose_right_door_melissa_dialog",
            "cavern_of_hatred_enter_floor_3",
        ],
        "top_playfield_indicator": [
            "cavern_of_hatred_enter_floor_4",
            "cavern_of_cowardice_enter_floor_4",
        ],
        "telescope_view_indicator": ["telescope_view"],
        "death_screen_indicator": ["death_screen"],
    }
    """ Multi-target names for Runes of Virtue 1 regions. """

    def __init__(
        self,
        pyboy: PyBoy,
        parameters: dict,
        override_regions: List[Tuple[str, int, int, int, int]] = [],
        override_multi_target_regions: List[Tuple[str, int, int, int, int]] = [],
        override_multi_targets: Dict[str, List[str]] = {},
    ):
        regions = _get_proper_regions(
            override_regions=override_regions, base_regions=self.REGIONS
        )
        multi_target_regions = _get_proper_regions(
            override_regions=override_multi_target_regions,
            base_regions=self.MULTI_TARGET_REGIONS,
        )
        multi_targets = {k: list(v) for k, v in self.MULTI_TARGETS.items()}
        for key in override_multi_targets:
            if key in multi_targets:
                multi_targets[key].extend(override_multi_targets[key])
            else:
                multi_targets[key] = list(override_multi_targets[key])
        super().__init__(
            variant="runes_of_virtue_1",
            pyboy=pyboy,
            parameters=parameters,
            additional_named_screen_region_details=regions,
            additional_multi_target_named_screen_region_details=multi_target_regions,
            override_multi_targets=multi_targets,
        )

    _DIALOG_TARGETS = (
        ("king_dialog_indicator", "king_dialog"),
        ("dialog_indicator", "chuckles_dialog"),
        ("dialog_indicator", "gnu_gnu_1_dialog"),
        ("dialog_indicator", "gnu_gnu_2_dialog"),
        ("dialog_indicator", "sherry_dialog"),
        ("dialog_indicator", "dr_cat_cats_lair_dialog"),
        ("dialog_indicator", "cavern_of_cowardice_sherry_floor_4_dialog"),
    )
    """ Multi-target screen regions that indicate an NPC dialogue overlay is visible. """

    def is_in_menu(self, current_screen: np.ndarray) -> bool:
        return self.named_region_matches_target(current_screen, "menu_indicator")

    def is_in_dialogue(self, current_screen: np.ndarray) -> bool:
        return any(
            self.named_region_matches_multi_target(current_screen, name, target_name)
            for name, target_name in self._DIALOG_TARGETS
        )


class RunesOfVirtue2StateParser(RunesOfVirtueStateParser):
    """
    State parser for Ultima: Runes of Virtue II.

    Screen regions:
    - menu_indicator: A first-pass region matching the RoV1 menu detector. Recapture
      this for RoV2 before relying on the task.
    - playfield_indicator: Playfield multi-target for opened-book and location screens,
      excluding the right HUD strip.
    - dialog_indicator: The left multi-target dialogue panel used for NPC dialogue.
    - death_screen_indicator: Small death/game-over screen indicator matching RoV1's
      task region.
    """

    REGIONS: List[Tuple[str, int, int, int, int]] = [
        ("menu_indicator", 20, 30, 40, 20),
    ]
    """ Additional named screen regions specific to Runes of Virtue 2. """

    MULTI_TARGET_REGIONS: List[Tuple[str, int, int, int, int]] = [
        ("playfield_indicator", 0, 0, 144, 144),
        ("left_playfield_indicator", 0, 0, 56, 144),
        ("dialog_indicator", 5, 5, 135, 136),
        ("death_screen_indicator", 60, 100, 30, 30),
    ]
    """ Additional multi-target named screen regions specific to Runes of Virtue 2. """

    MULTI_TARGETS = {
        "playfield_indicator": [
            "book_open",
            "cave_of_dishonour",
            "cavern_of_hatred",
            "cave_of_dishonour_enter_floor_2",
            "cave_of_dishonour_enter_floor_3",
            "kitchen_cheese_grabbed",
            "cheese_given_to_sherry",
            "ladder_behind_locked_door_climbed",
            "table_map_interacted",
            "castle_ladder_back_found",
            "cavern_of_hatred_gate_1_unlocked",
            "blocked_room_entered",
            "cavern_of_hatred_ladder_room_2",
            "cavern_of_hatred_ladder_2",
            "cavern_of_hatred_grab_key",
            "cavern_of_hatred_enter_floor_4",
            "cavern_of_hatred_enter_floor_5",
            "cavern_of_hatred_enter_floor_6",
            "cavern_of_hatred_enter_floor_7",
        ],
        "left_playfield_indicator": ["cavern_of_hatred_ladder_out_found"],
        "dialog_indicator": [
            "nystul_dialog",
            "blacksmith_fail_buy_shield",
            "sherry_mouse_dialog",
            "sandy_cook_dialog",
            "lord_whitsaber_dialog",
            "tholden_saved",
            "tholden_brought_back_to_king",
            "castle_ceremony_attended",
        ],
        "death_screen_indicator": ["death_screen"],
    }
    """ Multi-target names for Runes of Virtue 2 regions. """

    def __init__(
        self,
        pyboy: PyBoy,
        parameters: dict,
        override_regions: List[Tuple[str, int, int, int, int]] = [],
        override_multi_target_regions: List[Tuple[str, int, int, int, int]] = [],
        override_multi_targets: Dict[str, List[str]] = {},
    ):
        regions = _get_proper_regions(
            override_regions=override_regions, base_regions=self.REGIONS
        )
        multi_target_regions = _get_proper_regions(
            override_regions=override_multi_target_regions,
            base_regions=self.MULTI_TARGET_REGIONS,
        )
        multi_targets = {k: list(v) for k, v in self.MULTI_TARGETS.items()}
        for key in override_multi_targets:
            if key in multi_targets:
                multi_targets[key].extend(override_multi_targets[key])
            else:
                multi_targets[key] = list(override_multi_targets[key])
        super().__init__(
            variant="runes_of_virtue_2",
            pyboy=pyboy,
            parameters=parameters,
            additional_named_screen_region_details=regions,
            additional_multi_target_named_screen_region_details=multi_target_regions,
            override_multi_targets=multi_targets,
        )

    _DIALOG_TARGETS = (
        ("dialog_indicator", "nystul_dialog"),
        ("dialog_indicator", "blacksmith_fail_buy_shield"),
        ("dialog_indicator", "sherry_mouse_dialog"),
        ("dialog_indicator", "sandy_cook_dialog"),
        ("dialog_indicator", "lord_whitsaber_dialog"),
        ("dialog_indicator", "tholden_saved"),
        ("dialog_indicator", "tholden_brought_back_to_king"),
        ("dialog_indicator", "castle_ceremony_attended"),
    )
    """ Multi-target screen regions that indicate an NPC dialogue overlay is visible. """

    def is_in_menu(self, current_screen: np.ndarray) -> bool:
        if "menu_indicator" not in self.named_screen_regions:
            return False
        return self.named_region_matches_target(current_screen, "menu_indicator")

    def is_in_dialogue(self, current_screen: np.ndarray) -> bool:
        return any(
            self.named_region_matches_multi_target(current_screen, name, target_name)
            for name, target_name in self._DIALOG_TARGETS
        )

    def get_dialogue_ocr_region_name(self) -> str:
        return "dialog_indicator"
