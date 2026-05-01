from gameboy_worlds.emulation.bomberman.parsers import (
    BombermanMaxParser,
    BombermanPocketParser,
    BombermanQuestParser,
)
from gameboy_worlds.emulation.tracker import (
    RegionChangedTerminationMetric,
    RegionMatchTerminationMetric,
    TerminationMetric,
)


class PauseMenuOpenTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanMaxParser
    _TERMINATION_NAMED_REGION = "screen_top"
    _TERMINATION_TARGET_NAME = "pause_menu_open"


class StageSelectTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanMaxParser
    _TERMINATION_NAMED_REGION = "screen_top"
    _TERMINATION_TARGET_NAME = "stage_select"


class BombermanMaxGameOverTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanMaxParser
    _TERMINATION_NAMED_REGION = "screen_top"
    _TERMINATION_TARGET_NAME = "game_over"


class CharabomSelectOpenTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanMaxParser
    _TERMINATION_NAMED_REGION = "screen_top"
    _TERMINATION_TARGET_NAME = "charabom_select_open"


class StageBriefingTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanMaxParser
    _TERMINATION_NAMED_REGION = "stage_briefing_strip"
    _TERMINATION_TARGET_NAME = "stage_briefing_active"


class PitchAreaTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanMaxParser
    _TERMINATION_NAMED_REGION = "screen_top"
    _TERMINATION_TARGET_NAME = "pitch_area"


class HudBombCountChangedTerminateMetric(RegionChangedTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanMaxParser
    _CHANGED_NAMED_REGION = "hud_bomb_count"
    _CHANGE_MAE_THRESHOLD = 10


class HudEnemyCountChangedTerminateMetric(RegionChangedTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanMaxParser
    _CHANGED_NAMED_REGION = "hud_enemy_count"
    _CHANGE_MAE_THRESHOLD = 10


class HudFireChangedTerminateMetric(RegionChangedTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanMaxParser
    _CHANGED_NAMED_REGION = "hud_fire"
    _CHANGE_MAE_THRESHOLD = 10


class PauseActiveTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanPocketParser
    _TERMINATION_NAMED_REGION = "pause_indicator"
    _TERMINATION_TARGET_NAME = "pause_active"


class AreaIntroTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanPocketParser
    _TERMINATION_NAMED_REGION = "area_intro_block"
    _TERMINATION_TARGET_NAME = "area_intro_active"


class WorldClearTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanPocketParser
    _TERMINATION_NAMED_REGION = "area_intro_strip"
    _TERMINATION_TARGET_NAME = "world_clear"


class BombermanPocketGameOverTerminateMetric(
    RegionMatchTerminationMetric, TerminationMetric
):
    REQUIRED_PARSER = BombermanPocketParser
    _TERMINATION_NAMED_REGION = "area_intro_strip"
    _TERMINATION_TARGET_NAME = "game_over"


class JumpLevelSelectTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanPocketParser
    _TERMINATION_NAMED_REGION = "area_intro_strip"
    _TERMINATION_TARGET_NAME = "jump_level_select"


class JumpResultsTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanPocketParser
    _TERMINATION_NAMED_REGION = "area_intro_strip"
    _TERMINATION_TARGET_NAME = "jump_results"


class JumpRankingTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanPocketParser
    _TERMINATION_NAMED_REGION = "area_intro_strip"
    _TERMINATION_TARGET_NAME = "jump_ranking"


class HudChangedTerminateMetric(RegionChangedTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanPocketParser
    _CHANGED_NAMED_REGION = "hud_bomb_count"
    _CHANGE_MAE_THRESHOLD = 10


class HudPocketEnemyCountChangedTerminateMetric(RegionChangedTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanPocketParser
    _CHANGED_NAMED_REGION = "hud_enemy_count"
    _CHANGE_MAE_THRESHOLD = 10


class HudBottomRightChangedTerminateMetric(
    RegionChangedTerminationMetric, TerminationMetric
):
    REQUIRED_PARSER = BombermanPocketParser
    _CHANGED_NAMED_REGION = "hud_bottom_right"
    _CHANGE_MAE_THRESHOLD = 10


class HudHeartChangedTerminateMetric(RegionChangedTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanPocketParser
    _CHANGED_NAMED_REGION = "hud_heart"
    _CHANGE_MAE_THRESHOLD = 10


class BombermanQuestPauseMenuOpenTerminateMetric(
    RegionMatchTerminationMetric, TerminationMetric
):
    REQUIRED_PARSER = BombermanQuestParser
    _TERMINATION_NAMED_REGION = "screen_top"
    _TERMINATION_TARGET_NAME = "pause_menu_open"


class BombermanQuestGameOverTerminateMetric(
    RegionMatchTerminationMetric, TerminationMetric
):
    REQUIRED_PARSER = BombermanQuestParser
    _TERMINATION_NAMED_REGION = "screen_top"
    _TERMINATION_TARGET_NAME = "game_over"


class BombSelectOpenTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanQuestParser
    _TERMINATION_NAMED_REGION = "screen_top"
    _TERMINATION_TARGET_NAME = "bomb_select_open"


class DialogueActiveTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanQuestParser
    _TERMINATION_NAMED_REGION = "dialogue_strip"
    _TERMINATION_TARGET_NAME = "dialogue_active"


class BookReadTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanQuestParser
    _TERMINATION_NAMED_REGION = "book_bottom"
    _TERMINATION_TARGET_NAME = "book_read_active"


class NpcDialogueTerminateMetric(TerminationMetric):
    REQUIRED_PARSER = BombermanQuestParser

    def determine_terminated(self, current_frame, recent_frames):
        return self.state_parser.is_in_npc_dialogue(current_frame)


class SignDialogueTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanQuestParser
    _TERMINATION_NAMED_REGION = "dialogue_icon"
    _TERMINATION_TARGET_NAME = "sign_dialogue_active"


class BattleActiveTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanQuestParser
    _TERMINATION_NAMED_REGION = "hud_bottom"
    _TERMINATION_TARGET_NAME = "battle_active"


class ShieldSelectTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanQuestParser
    _TERMINATION_NAMED_REGION = "item_select_panel"
    _TERMINATION_TARGET_NAME = "shield_select_active"


class BombComponentSelectTerminateMetric(
    RegionMatchTerminationMetric, TerminationMetric
):
    REQUIRED_PARSER = BombermanQuestParser
    _TERMINATION_NAMED_REGION = "item_select_panel"
    _TERMINATION_TARGET_NAME = "bomb_component_select_active"


class EnterCampTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanQuestParser
    _TERMINATION_NAMED_REGION = "zone_background"
    _TERMINATION_TARGET_NAME = "in_camp"


class EnterHouseTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanQuestParser
    _TERMINATION_NAMED_REGION = "zone_background"
    _TERMINATION_TARGET_NAME = "in_house"


class SaveNpcActiveTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanQuestParser
    _TERMINATION_NAMED_REGION = "zone_background"
    _TERMINATION_TARGET_NAME = "save_npc_active"



class EnterCaveTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanQuestParser
    _TERMINATION_NAMED_REGION = "zone_background"
    _TERMINATION_TARGET_NAME = "in_cave"


class ButtonRegionChangedTerminateMetric(RegionChangedTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanQuestParser
    _CHANGED_NAMED_REGION = "button_region"
    _CHANGE_MAE_THRESHOLD = 10


class BoxPickedUpTerminateMetric(RegionChangedTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanQuestParser
    _CHANGED_NAMED_REGION = "box_detector"
    _CHANGE_MAE_THRESHOLD = 10


class SwitchActivatedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BombermanQuestParser
    _TERMINATION_NAMED_REGION = "switch_detector"
    _TERMINATION_TARGET_NAME = "switch_activated"


