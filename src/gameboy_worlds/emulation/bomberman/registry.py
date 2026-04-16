from typing import Dict, Type

from gameboy_worlds.emulation.bomberman.parsers import (
    BombermanMaxParser,
    BombermanPocketParser,
    BombermanQuestParser,
)
from gameboy_worlds.emulation.bomberman.trackers import (
    BombermanMaxCharabomSelectTestTracker,
    BombermanMaxDefeatEnemyTestTracker,
    BombermanMaxGameOverTestTracker,
    BombermanMaxPauseMenuTestTracker,
    BombermanMaxPickupBombUpTestTracker,
    BombermanMaxPickupFireUpTestTracker,
    BombermanMaxPitchAreaTestTracker,
    BombermanMaxStageBriefingTestTracker,
    BombermanMaxStageSelectTestTracker,
    BombermanMaxTracker,
    BombermanPocketForestAreaIntroTestTracker,
    BombermanPocketGameOverTestTracker,
    BombermanPocketHudBottomRightChangedTestTracker,
    BombermanPocketHudChangedTestTracker,
    BombermanPocketHudHeartChangedTestTracker,
    BombermanPocketJumpLevelSelectTestTracker,
    BombermanPocketJumpResultsTestTracker,
    BombermanPocketJumpRankingTestTracker,
    BombermanPocketOceanAreaIntroTestTracker,
    BombermanPocketPauseMenuTestTracker,
    BombermanPocketTracker,
    BombermanPocketWorldClearTestTracker,
    BombermanQuestBattleTestTracker,
    BombermanQuestBombSelectTestTracker,
    BombermanQuestCloudZoneTestTracker,
    BombermanQuestBombComponentSelectTestTracker,
    BombermanQuestDesertZoneTestTracker,
    BombermanQuestEnterCampTestTracker,
    BombermanQuestFieldZoneTestTracker,
    BombermanQuestForestZoneTestTracker,
    BombermanQuestGameOverTestTracker,
    BombermanQuestBookReadTestTracker,
    BombermanQuestNpcDialogueTestTracker,
    BombermanQuestPauseMenuTestTracker,
    BombermanQuestShieldSelectTestTracker,
    BombermanQuestSignDialogueTestTracker,
    BombermanQuestTracker,
)
from gameboy_worlds.emulation.emulator import Emulator
from gameboy_worlds.emulation.parser import StateParser
from gameboy_worlds.emulation.tracker import StateTracker


GAME_TO_GB_NAME = {
    "bomberman_max": "BombermanMax.gbc",
    "bomberman_pocket": "PocketBomberman.gbc",
    "bomberman_quest": "BombermanQuest.gbc",
}

STRONGEST_PARSERS: Dict[str, Type[StateParser]] = {
    "bomberman_max": BombermanMaxParser,
    "bomberman_pocket": BombermanPocketParser,
    "bomberman_quest": BombermanQuestParser,
}

AVAILABLE_STATE_TRACKERS: Dict[str, Dict[str, Type[StateTracker]]] = {
    "bomberman_max": {
        "default": BombermanMaxTracker,
        "pause_menu_open_test": BombermanMaxPauseMenuTestTracker,
        "stage_select_test": BombermanMaxStageSelectTestTracker,
        "game_over_test": BombermanMaxGameOverTestTracker,
        "charabom_select_test": BombermanMaxCharabomSelectTestTracker,
        "stage_briefing_test": BombermanMaxStageBriefingTestTracker,
        "pickup_bomb_up_test": BombermanMaxPickupBombUpTestTracker,
        "defeat_enemy_test": BombermanMaxDefeatEnemyTestTracker,
        "pickup_fire_up_test": BombermanMaxPickupFireUpTestTracker,
        "pitch_area_test": BombermanMaxPitchAreaTestTracker,
    },
    "bomberman_pocket": {
        "default": BombermanPocketTracker,
        "pause_menu_open_test": BombermanPocketPauseMenuTestTracker,
        "forest_stage_clear_test": BombermanPocketForestAreaIntroTestTracker,
        "ocean_stage_clear_test": BombermanPocketOceanAreaIntroTestTracker,
        "world_clear_test": BombermanPocketWorldClearTestTracker,
        "game_over_test": BombermanPocketGameOverTestTracker,
        "jump_level_select_test": BombermanPocketJumpLevelSelectTestTracker,
        "jump_results_test": BombermanPocketJumpResultsTestTracker,
        "jump_ranking_test": BombermanPocketJumpRankingTestTracker,
        "pickup_bomb_up_test": BombermanPocketHudChangedTestTracker,
        "pickup_bomb_range_up_test": BombermanPocketHudBottomRightChangedTestTracker,
        "pickup_heart_test": BombermanPocketHudHeartChangedTestTracker,
    },
    "bomberman_quest": {
        "default": BombermanQuestTracker,
        "pause_menu_open_test": BombermanQuestPauseMenuTestTracker,
        "game_over_test": BombermanQuestGameOverTestTracker,
        "bomb_select_open_test": BombermanQuestBombSelectTestTracker,
        "npc_dialogue_test": BombermanQuestNpcDialogueTestTracker,
        "sign_read_test": BombermanQuestSignDialogueTestTracker,
        "charabom_battle_test": BombermanQuestBattleTestTracker,
        "field_zone_test": BombermanQuestFieldZoneTestTracker,
        "forest_zone_test": BombermanQuestForestZoneTestTracker,
        "desert_zone_test": BombermanQuestDesertZoneTestTracker,
        "cloud_zone_test": BombermanQuestCloudZoneTestTracker,
        "shield_select_test": BombermanQuestShieldSelectTestTracker,
        "bomb_component_select_test": BombermanQuestBombComponentSelectTestTracker,
        "enter_camp_test": BombermanQuestEnterCampTestTracker,
        "book_read_test": BombermanQuestBookReadTestTracker,
    },
}

AVAILABLE_EMULATORS: Dict[str, Dict[str, Type[Emulator]]] = {
    "bomberman_max": {"default": Emulator},
    "bomberman_pocket": {"default": Emulator},
    "bomberman_quest": {"default": Emulator},
}
