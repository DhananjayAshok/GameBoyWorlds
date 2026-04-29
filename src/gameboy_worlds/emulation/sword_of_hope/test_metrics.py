from gameboy_worlds.emulation.sword_of_hope.parsers import (
    SwordOfHope1Parser,
    SwordOfHope2Parser,
)
from gameboy_worlds.emulation.tracker import (
    RegionMatchTerminationMetric,
    TerminationMetric,
    RegionMatchSubGoal,
)


class MillRoomTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "room_label"
    _TERMINATION_TARGET_NAME = "mill_room"


class ShamanRoomTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "room_label"
    _TERMINATION_TARGET_NAME = "shaman_room"


class OldmanHouseSubGoal(RegionMatchSubGoal):
    NAME = "oldman_house"
    _NAMED_REGION = "room_label"
    _TARGET_NAME = "oldman_house"


class InForestSubGoal(RegionMatchSubGoal):
    NAME = "in_forest"
    _NAMED_REGION = "room_label"
    _TARGET_NAME = "in_forest"


class ShamanHouseSubGoal(RegionMatchSubGoal):
    NAME = "shaman_house"
    _NAMED_REGION = "room_label"
    _TARGET_NAME = "shaman_house"


class DialogueClearedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "command_area"
    _TERMINATION_TARGET_NAME = "dialogue_cleared"


class DialogueActiveSubGoal(RegionMatchSubGoal):
    NAME = "dialogue_active"
    _NAMED_REGION = "command_area"
    _TARGET_NAME = "dialogue_active"


class BattleWonTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "battle_command"
    _TERMINATION_TARGET_NAME = "battle_won"


class BattleActiveSubGoal(RegionMatchSubGoal):
    NAME = "battle_active"
    _NAMED_REGION = "battle_command"
    _TARGET_NAME = "battle_active"


class ItemFoundTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "item_found"


class LookSelectedSubGoal(RegionMatchSubGoal):
    NAME = "look_selected"
    _NAMED_REGION = "command_area"
    _TARGET_NAME = "look_selected"


class LookTargetOptionsSubGoal(RegionMatchSubGoal):
    NAME = "look_target_options"
    _NAMED_REGION = "status_command"
    _TARGET_NAME = "look_target_options"


class PurchaseConfirmedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "purchase_confirmed"


class ShopMenuOpenSubGoal(RegionMatchSubGoal):
    NAME = "shop_menu_open"
    _NAMED_REGION = "status_command"
    _TARGET_NAME = "shop_menu_open"


class ExplorationMenuTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "command_area"
    _TERMINATION_TARGET_NAME = "exploration_menu"


class DialogueVisibleSubGoal(RegionMatchSubGoal):
    NAME = "dialogue_visible"
    _NAMED_REGION = "status_command"
    _TARGET_NAME = "dialogue_visible"


class DialogueAdvancedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "dialogue_advanced"


class DialogueInitiatedSubGoal(RegionMatchSubGoal):
    NAME = "dialogue_initiated"
    _NAMED_REGION = "status_command"
    _TARGET_NAME = "dialogue_initiated"


class MenuOpenSubGoal(RegionMatchSubGoal):
    NAME = "menu_open"
    _NAMED_REGION = "command_area"
    _TARGET_NAME = "menu_open"


class BattleMagicMenuTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "battle_command"
    _TERMINATION_TARGET_NAME = "battle_magic_menu"


class TeleportResultTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "teleport_result"


class MagicMenuOpenSubGoal(RegionMatchSubGoal):
    NAME = "magic_menu_open"
    _NAMED_REGION = "status_command"
    _TARGET_NAME = "magic_menu_open"


class MistressSecondDialogueTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "battle_full"
    _TERMINATION_TARGET_NAME = "mistress_second_dialogue"


class MistressFirstDialogueSubGoal(RegionMatchSubGoal):
    NAME = "mistress_first_dialogue"
    _NAMED_REGION = "battle_full"
    _TARGET_NAME = "mistress_first_dialogue"


class SaveConfirmedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "battle_full"
    _TERMINATION_TARGET_NAME = "save_confirmed"


class SavePromptVisibleSubGoal(RegionMatchSubGoal):
    NAME = "save_prompt_visible"
    _NAMED_REGION = "battle_full"
    _TARGET_NAME = "save_prompt_visible"


class HerbReceivedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "battle_full"
    _TERMINATION_TARGET_NAME = "herb_received"


class LookPathTargetSubGoal(RegionMatchSubGoal):
    NAME = "look_path_target"
    _NAMED_REGION = "battle_full"
    _TARGET_NAME = "look_path_target"


class TrtFruitReceivedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "battle_full"
    _TERMINATION_TARGET_NAME = "trtfruit_received"


class HitTargetShownSubGoal(RegionMatchSubGoal):
    NAME = "hit_target_shown"
    _NAMED_REGION = "battle_full"
    _TARGET_NAME = "hit_target_shown"


class TreantDefeatedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "battle_full"
    _TERMINATION_TARGET_NAME = "treant_defeated"


class PassageRevealedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "battle_full"
    _TERMINATION_TARGET_NAME = "passage_revealed"


class HitWallTargetSubGoal(RegionMatchSubGoal):
    NAME = "hit_wall_target"
    _NAMED_REGION = "battle_full"
    _TARGET_NAME = "hit_wall_target"


class GateOpenedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "battle_full"
    _TERMINATION_TARGET_NAME = "gate_opened"


class KeyMSelectedSubGoal(RegionMatchSubGoal):
    NAME = "key_m_selected"
    _NAMED_REGION = "battle_full"
    _TARGET_NAME = "key_m_selected"


class ScrollReceivedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "battle_full"
    _TERMINATION_TARGET_NAME = "scroll_received"


class InBackroomSubGoal(RegionMatchSubGoal):
    NAME = "in_backroom"
    _NAMED_REGION = "battle_full"
    _TARGET_NAME = "in_backroom"


class CharmReceivedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "battle_full"
    _TERMINATION_TARGET_NAME = "charm_received"


class GraceSelectedSubGoal(RegionMatchSubGoal):
    NAME = "grace_selected"
    _NAMED_REGION = "battle_full"
    _TARGET_NAME = "grace_selected"


class TeleportLandedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "teleport_landed"


class TeleportDestCursorSubGoal(RegionMatchSubGoal):
    NAME = "teleport_dest_cursor"
    _NAMED_REGION = "status_command"
    _TARGET_NAME = "teleport_dest_cursor"


class EscapeConfirmedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "battle_command"
    _TERMINATION_TARGET_NAME = "escape_confirmed"


# ---------------------------------------------------------------------------
# Sword of Hope 2 metrics (5-task starter set)
# ---------------------------------------------------------------------------


class SoH2DialogueClearedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "dialogue_cleared"


class SoH2DialogueActiveSubGoal(RegionMatchSubGoal):
    NAME = "dialogue_active"
    _NAMED_REGION = "status_command"
    _TARGET_NAME = "dialogue_active"


class SoH2DialogueAdvancedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "dialogue_advanced"


class SoH2DialogueInitiatedSubGoal(RegionMatchSubGoal):
    NAME = "dialogue_initiated"
    _NAMED_REGION = "status_command"
    _TARGET_NAME = "dialogue_initiated"


class SoH2ExplorationMenuTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "command_area"
    _TERMINATION_TARGET_NAME = "exploration_menu"


class SoH2MenuOpenSubGoal(RegionMatchSubGoal):
    NAME = "menu_open"
    _NAMED_REGION = "command_area"
    _TARGET_NAME = "menu_open"


class SoH2DialogueVisibleSubGoal(RegionMatchSubGoal):
    NAME = "dialogue_visible"
    _NAMED_REGION = "status_command"
    _TARGET_NAME = "dialogue_visible"


class SoH2FirstAdjacentRoomTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "room_label"
    _TERMINATION_TARGET_NAME = "castle_corridor"


class SoH2StarterRoomSubGoal(RegionMatchSubGoal):
    NAME = "castle_throne"
    _NAMED_REGION = "room_label"
    _TARGET_NAME = "castle_throne"
