import os
from abc import ABC

import numpy as np

from gameboy_worlds.emulation.parser import NamedScreenRegion, StateParser
from gameboy_worlds.utils import log_error, verify_parameters


class BombermanParser(StateParser, ABC):
    VARIANT = ""
    MULTI_TARGET_REGIONS = []
    MULTI_TARGETS = {}

    def __init__(self, pyboy, parameters):
        verify_parameters(parameters)
        if f"{self.VARIANT}_rom_data_path" not in parameters:
            log_error(
                f"ROM data path not found for variant: {self.VARIANT}. Add {self.VARIANT}_rom_data_path to config files.",
                parameters,
            )
        self.rom_data_path = parameters[f"{self.VARIANT}_rom_data_path"]
        captures_dir = os.path.join(self.rom_data_path, "captures")
        regions = []
        for region_name, x, y, w, h in self.MULTI_TARGET_REGIONS:
            subdir = os.path.join(captures_dir, region_name)
            region_target_paths = {
                target_name: os.path.join(subdir, target_name)
                for target_name in self.MULTI_TARGETS.get(region_name, [])
            }
            regions.append(
                NamedScreenRegion(
                    name=region_name,
                    start_x=x,
                    start_y=y,
                    width=w,
                    height=h,
                    parameters=parameters,
                    multi_target_paths=region_target_paths,
                )
            )
        super().__init__(pyboy, parameters, named_screen_regions=regions)

    def _matches(self, current_screen: np.ndarray, region_name: str, target_name: str) -> bool:
        return self.named_region_matches_multi_target(
            current_screen, region_name, target_name
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(variant={self.VARIANT})"


class BombermanMaxParser(BombermanParser):
    VARIANT = "bomberman_max"

    MULTI_TARGET_REGIONS = [
        ("screen_top", 0, 0, 160, 16),
        ("stage_briefing_strip", 0, 87, 43, 41),
        ("stage_briefing_box", 0, 72, 160, 56),
        ("hud_enemy_count", 110, 136, 17, 8),
        ("hud_bomb_count", 127, 136, 15, 8),
        ("hud_fire", 142, 136, 18, 8),
        ("zone_background", 0, 0, 160, 32),
    ]

    MULTI_TARGETS = {
        "screen_top": [
            "pause_menu_open",
            "stage_select",
            "game_over",
            "charabom_select_open",
            "pitch_area",
        ],
        "stage_briefing_strip": ["stage_briefing_active"],
        "hud_enemy_count": [],
        "hud_bomb_count": [],
        "hud_fire": [],
        "zone_background": [],
    }

    def is_in_menu(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "screen_top", "pause_menu_open")

    def is_on_stage_select(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "screen_top", "stage_select")

    def is_game_over(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "screen_top", "game_over")

    def is_in_charabom_select(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "screen_top", "charabom_select_open")

    def is_stage_briefing_active(self, current_screen: np.ndarray) -> bool:
        return self._matches(
            current_screen, "stage_briefing_strip", "stage_briefing_active"
        )

    def is_in_zone_1(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "zone_background", "in_zone_1")

    def is_in_battle(self, current_screen: np.ndarray) -> bool:
        return False


class BombermanPocketParser(BombermanParser):
    VARIANT = "bomberman_pocket"

    MULTI_TARGET_REGIONS = [
        ("area_intro_strip", 0, 0, 160, 20),
        ("area_intro_block", 0, 0, 53, 20),
        ("pause_indicator", 96, 128, 64, 16),
        ("hud_heart", 54, 136, 10, 7),
        ("hud_enemy_count", 86, 136, 21, 7),
        ("hud_bomb_count", 110, 136, 20, 7),
        ("hud_bottom_right", 130, 136, 30, 7),
        ("zone_background", 0, 0, 160, 32),
    ]

    MULTI_TARGETS = {
        "area_intro_strip": [
            "world_clear",
            "game_over",
            "jump_level_select",
            "jump_results",
            "jump_ranking",
        ],
        "area_intro_block": ["area_intro_active"],
        "pause_indicator": ["pause_active"],
        "hud_heart": [],
        "hud_enemy_count": [],
        "hud_bomb_count": [],
        "hud_bottom_right": [],
        "zone_background": [
            "in_forest_world",
            "in_ocean_world",
            "in_wind_world",
            "in_cloud_world",
            "in_evil_world",
        ],
    }

    def is_paused(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "pause_indicator", "pause_active")

    def is_in_menu(self, current_screen: np.ndarray) -> bool:
        return self.is_paused(current_screen)

    def is_world_clear(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "area_intro_strip", "world_clear")

    def is_area_intro_active(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "area_intro_block", "area_intro_active")

    def is_in_any_area_intro(self, current_screen: np.ndarray) -> bool:
        return self.is_area_intro_active(current_screen)

    def is_in_forest_world(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "zone_background", "in_forest_world")

    def is_in_ocean_world(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "zone_background", "in_ocean_world")

    def is_in_wind_world(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "zone_background", "in_wind_world")

    def is_in_cloud_world(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "zone_background", "in_cloud_world")

    def is_in_evil_world(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "zone_background", "in_evil_world")



class BombermanQuestParser(BombermanParser):
    VARIANT = "bomberman_quest"

    MULTI_TARGET_REGIONS = [
        ("screen_top", 0, 0, 160, 16),
        ("dialogue_strip", 0, 12, 160, 10),
        ("dialogue_box", 0, 12, 160, 60),
        ("dialogue_icon", 124, 30, 31, 27),
        ("hud_bottom", 47, 136, 33, 8),
        ("item_select_panel", 95, 5, 65, 85),
        ("zone_background", 0, 0, 160, 32),
        ("book_bottom", 0, 120, 160, 20),
        ("bottom_strip", 0, 120, 160, 24),
        ("button_region", 80, 80, 16, 16),
        ("switch_detector", 64, 64, 16, 16),
        ("box_detector", 80, 64, 16, 16),
    ]

    MULTI_TARGETS = {
        "screen_top": ["pause_menu_open", "bomb_select_open", "game_over"],
        "dialogue_strip": ["dialogue_active"],
        "dialogue_icon": ["sign_dialogue_active"],
        "hud_bottom": ["battle_active"],
        "item_select_panel": [
            "shield_select_active",
            "bomb_component_select_active",
        ],
        "zone_background": [
            "in_camp",
            "in_house",
            "in_cave",
            "save_npc_active",
        ],
        "book_bottom": ["book_read_active"],
        "bottom_strip": [],
        "button_region": [],
        "switch_detector": ["switch_activated"],
        "box_detector": [],
    }

    def is_in_menu(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "screen_top", "pause_menu_open")

    def is_game_over(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "screen_top", "game_over")

    def is_in_battle(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "hud_bottom", "battle_active")

    def is_in_dialogue(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "dialogue_strip", "dialogue_active")

    def is_in_npc_dialogue(self, current_screen: np.ndarray) -> bool:
        return self.is_in_dialogue(current_screen) and not self.is_reading_sign(
            current_screen
        )

    def is_reading_sign(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "dialogue_icon", "sign_dialogue_active")

    def is_reading_book(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "book_bottom", "book_read_active")

    def is_shield_select_active(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "item_select_panel", "shield_select_active")

    def is_bomb_component_select_active(self, current_screen: np.ndarray) -> bool:
        return self._matches(
            current_screen, "item_select_panel", "bomb_component_select_active"
        )

    def is_in_camp(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "zone_background", "in_camp")

    def is_in_house(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "zone_background", "in_house")

    def is_in_cave(self, current_screen: np.ndarray) -> bool:
        return self._matches(current_screen, "zone_background", "in_cave")
