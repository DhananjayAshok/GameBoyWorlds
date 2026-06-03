"""
Survival Kids game state parsers.
"""

import os
from enum import Enum
from typing import Dict, List, Optional, Tuple

import numpy as np

from gameboy_worlds.emulation.parser import (
    NamedScreenRegion,
    StateParser,
    _get_proper_regions,
)
from gameboy_worlds.utils import log_error, verify_parameters


def _merge_multi_targets(
    *multi_targets: Dict[str, List[str]],
) -> Dict[str, List[str]]:
    merged: Dict[str, List[str]] = {}
    for targets in multi_targets:
        for region_name, target_names in targets.items():
            region_targets = merged.setdefault(region_name, [])
            for target_name in target_names:
                if target_name not in region_targets:
                    region_targets.append(target_name)
    return merged


class AgentState(Enum):
    FREE_ROAM = 0
    IN_DIALOGUE = 1
    IN_MENU = 2


class SurvivalKidsParser(StateParser):
    """Game state parser for Survival Kids 1 (GBC)."""

    VARIANT = "survival_kids_1"
    LOAD_ONLY_EXISTING_MULTI_TARGETS = False
    FORCE_LOAD_MISSING_MULTI_TARGETS: Dict[str, List[str]] = {}

    MULTI_TARGET_REGIONS: List[Tuple[str, int, int, int, int]] = [
        ("screen", 0, 0, 160, 144),
        ("screen_bottom", 0, 108, 160, 36),
        ("game_viewport", 0, 0, 160, 128),
        ("status_bar", 0, 128, 160, 16),
        ("hp_area", 0, 128, 40, 16),
        ("hunger_area", 0, 136, 42, 8),
        ("thirst_area", 42, 136, 42, 8),
        ("stamina_area", 84, 136, 42, 8),
        ("equipped_items_area", 20, 128, 24, 8),
        ("equipped_item_area", 0, 105, 160, 39),
        ("pack_icon_area", 144, 128, 16, 16),
        ("bag_icon_area", 64, 32, 48, 48),
        ("object_area", 64, 32, 48, 48),
        ("choose_item_area", 0, 20, 160, 80),
        ("dialogue_area", 8, 112, 144, 28),
        ("inventory_select_area", 0, 0, 88, 72),
        ("item_action_menu", 0, 0, 64, 56),
        ("item_action_menu_two_options", 0, 0, 64, 40),
        ("item_action_menu_three_options", 0, 0, 64, 57),
        ("item_use_menu_area", 0, 84, 160, 56),
        ("merge_menu_area", 0, 24, 160, 76),
        ("item_action_cursor", 6, 8, 12, 8),
        ("item_action_options", 18, 8, 42, 28),
        ("menu_area", 0, 0, 160, 144),
        ("merge_confirm_area", 0, 101, 160, 31),
    ]

    MULTI_TARGETS: Dict[str, List[str]] = {
        "screen": [
            "after_filling_water",
            "day_reference",
            "entered_shelter",
            "found_river",
            "got_the_brdfeather",
            "got_the_stick",
            "got_the_tree_bark",
            "got_the_water",
            "inventory_select_item",
            "night_reference",
            "water_menu_open",
        ],
        "menu_area": [
            "inventory_open",
        ],
        "merge_menu_area": [
            "merge_menu",
            "select_stick",
        ],
        "merge_confirm_area": [
            "merge_confirm",
        ],
        "item_action_menu_two_options": [
            "select_take",
            "take_leave_menu",
            "feather_take_leave_menu",
        ],
        "dialogue_area": [
            "pickup_item_dialogue",
            "canteen_pickup_dialogue",
        ],
        "bag_icon_area": [
            "bag_icon",
        ],
        "equipped_item_area": [
            "knife_equipped",
            "use_kindling",
        ],
        "choose_item_area": [
            "canteen_chosen",
            "knife_chosen",
            "select_kindling",
        ],
        "inventory_select_area": [
            "kindling_merged",
        ],
        "item_use_menu_area": [
            "canteen_action_menu",
            "canteen_drink_selected",
            "canteen_use_selected",
        ],
        "item_action_menu": [
            "canteen_take_leave_menu",
            "meat_take_eat_leave_menu",
        ],
        "game_viewport": [
            "animal_killed",
            "chapter1_path_cleared",
            "fire_lit",
            "in_the_shelter",
            "path_after_blocking_grass",
        ],
    }

    _DARK_PIXEL_THRESHOLD = 24
    _BRIGHT_PIXEL_THRESHOLD = 220
    _DIALOGUE_BRIGHT_RATIO_THRESHOLD = 0.55
    _MENU_DARK_RATIO_THRESHOLD = 0.08
    _MENU_BRIGHT_RATIO_THRESHOLD = 0.18
    _FULL_MENU_BRIGHT_RATIO_THRESHOLD = 0.75
    _BOTTOM_MENU_DARK_RATIO_MAX = 0.025

    def __init__(
        self,
        pyboy,
        parameters: dict,
        additional_multi_target_regions: Optional[
            List[Tuple[str, int, int, int, int]]
        ] = None,
        override_multi_targets: Optional[Dict[str, List[str]]] = None,
    ):
        verify_parameters(parameters)
        additional_multi_target_regions = additional_multi_target_regions or []
        override_multi_targets = override_multi_targets or {}
        if f"{self.VARIANT}_rom_data_path" not in parameters:
            log_error(
                f"ROM data path not found for variant: {self.VARIANT}. "
                f"Add {self.VARIANT}_rom_data_path to the config files.",
                parameters,
            )
        self.rom_data_path = parameters[f"{self.VARIANT}_rom_data_path"]
        captures_dir = os.path.join(self.rom_data_path, "captures")

        multi_target_regions = _get_proper_regions(
            override_regions=additional_multi_target_regions,
            base_regions=self.MULTI_TARGET_REGIONS,
        )

        multi_targets: Dict[str, List[str]] = {}
        for key, val in self.MULTI_TARGETS.items():
            multi_targets[key] = list(val)
        for key, val in override_multi_targets.items():
            if key in multi_targets:
                multi_targets[key].extend(val)
            else:
                multi_targets[key] = list(val)

        named_screen_regions: List[NamedScreenRegion] = []
        for region_name, x, y, w, h in multi_target_regions:
            target_paths: Dict[str, str] = {}
            subdir = os.path.join(captures_dir, region_name)
            for target_name in multi_targets.get(region_name, []):
                target_path = os.path.join(subdir, target_name)
                force_load_missing = target_name in self.FORCE_LOAD_MISSING_MULTI_TARGETS.get(
                    region_name, []
                )
                if (
                    self.LOAD_ONLY_EXISTING_MULTI_TARGETS
                    and not force_load_missing
                    and not os.path.exists(f"{target_path}.npy")
                ):
                    continue
                target_paths[target_name] = target_path
            region = NamedScreenRegion(
                region_name,
                x,
                y,
                w,
                h,
                parameters=parameters,
                multi_target_paths=target_paths,
            )
            named_screen_regions.append(region)

        super().__init__(pyboy, parameters, named_screen_regions)

    @staticmethod
    def _as_gray(current_screen: np.ndarray) -> np.ndarray:
        if current_screen.ndim == 3:
            return current_screen[:, :, 0]
        return current_screen

    def _region_gray(self, current_screen: np.ndarray, region_name: str) -> np.ndarray:
        return self.capture_named_region(current_screen, region_name)[:, :, 0]

    def _has_text_box_like_region(self, region: np.ndarray) -> bool:
        dark_ratio = np.mean(region <= self._DARK_PIXEL_THRESHOLD)
        bright_ratio = np.mean(region >= self._BRIGHT_PIXEL_THRESHOLD)
        return (
            bright_ratio >= self._DIALOGUE_BRIGHT_RATIO_THRESHOLD
            and dark_ratio >= 0.02
        )

    def is_in_dialogue(self, current_screen: np.ndarray) -> bool:
        dialogue_area = self._region_gray(current_screen, "dialogue_area")
        return self._has_text_box_like_region(dialogue_area)

    def is_in_menu(self, current_screen: np.ndarray) -> bool:
        screen = self._as_gray(current_screen)
        top_area = screen[:96, :]
        bottom_dialogue = self._region_gray(current_screen, "dialogue_area")
        top_dark_ratio = np.mean(top_area <= self._DARK_PIXEL_THRESHOLD)
        top_bright_ratio = np.mean(top_area >= self._BRIGHT_PIXEL_THRESHOLD)
        bottom_dark_ratio = np.mean(bottom_dialogue <= self._DARK_PIXEL_THRESHOLD)
        if top_bright_ratio >= self._FULL_MENU_BRIGHT_RATIO_THRESHOLD:
            return True
        return (
            top_dark_ratio >= self._MENU_DARK_RATIO_THRESHOLD
            and top_bright_ratio >= self._MENU_BRIGHT_RATIO_THRESHOLD
            and bottom_dark_ratio <= self._BOTTOM_MENU_DARK_RATIO_MAX
        )

    def get_agent_state(self, current_screen: np.ndarray) -> AgentState:
        if self.is_in_menu(current_screen):
            return AgentState.IN_MENU
        if self.is_in_dialogue(current_screen):
            return AgentState.IN_DIALOGUE
        return AgentState.FREE_ROAM

    def read_memory_byte(self, address: int) -> int:
        return self._pyboy.memory[address]

    def __repr__(self) -> str:
        return f"<SurvivalKidsParser(variant={self.VARIANT})>"


class SurvivalKids2Parser(SurvivalKidsParser):
    """Game state parser for Survival Kids 2 (GBC)."""

    VARIANT = "survival_kids_2"
    LOAD_ONLY_EXISTING_MULTI_TARGETS = True
    FORCE_LOAD_MISSING_MULTI_TARGETS = {
        "screen": ["knife_equipped"],
    }
    MULTI_TARGET_REGIONS = _get_proper_regions(
        override_regions=[
            ("dialogue_area", 0, 104, 160, 40),
            ("merge_confirm_area", 0, 104, 160, 40),
        ],
        base_regions=SurvivalKidsParser.MULTI_TARGET_REGIONS,
    )
    MULTI_TARGETS: Dict[str, List[str]] = _merge_multi_targets(
        SurvivalKidsParser.MULTI_TARGETS,
        {
            "dialogue_area": [
                "fruit_found_dialogue",
                "fruit_taken_dialogue",
                "fruit_eaten_dialogue",
                "tree_bark_pickup_dialogue",
            ],
            "game_viewport": [
                "fruit_eaten",
                "new_path_1_found",
                "new_path_2_found",
                "sharp_stone_found",
            ],
            "hunger_area": [
                "fruit_eaten",
            ],
            "item_action_menu": [
                "fruit_action_menu",
                "fruit_eat_selected",
            ],
            "item_action_menu_two_options": [
                "fruit_action_menu",
                "fruit_eat_selected",
            ],
            "menu_area": [
                "inventory_select_item",
            ],
            "object_area": [
                "bag_icon",
            ],
            "equipped_item_area": [
                "knife_equipped",
            ],
            "screen": [
                "afternoon_reference",
                "day_reference",
                "fruit_eaten",
                "got_the_sharp_stone",
                "got_the_stone",
                "got_the_vine",
                "knife_equipped",
                "night_reference",
            ],
        },
    )

    def __repr__(self) -> str:
        return f"<SurvivalKids2Parser(variant={self.VARIANT})>"
