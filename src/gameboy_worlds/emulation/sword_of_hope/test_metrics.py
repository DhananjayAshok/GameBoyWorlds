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


class SoH2PowerMenuLastSlideSubGoal(RegionMatchSubGoal):
    NAME = "power_menu_last_slide"
    _NAMED_REGION = "command_area"
    _TARGET_NAME = "power_menu_last_slide"


class SoH2DialogueVisibleSubGoal(RegionMatchSubGoal):
    NAME = "dialogue_visible"
    _NAMED_REGION = "status_command"
    _TARGET_NAME = "dialogue_visible"


class SoH2FirstAdjacentRoomTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "soh2_room_label"
    _TERMINATION_TARGET_NAME = "riccar_castle"


class SoH2StarterRoomSubGoal(RegionMatchSubGoal):
    NAME = "kings_room"
    _NAMED_REGION = "soh2_room_label"
    _TARGET_NAME = "kings_room"


class SoH2BattleWonTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "battle_won"


class SoH2BattleActiveSubGoal(RegionMatchSubGoal):
    NAME = "battle_active"
    _NAMED_REGION = "soh2_battle_command"
    _TARGET_NAME = "battle_active"


class SoH2EscapeConfirmedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "escape_confirmed"


class SoH2WheatPurchasedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "wheat_purchased"


class SoH2ShopMenuOpenTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "full_screen"
    _TERMINATION_TARGET_NAME = "shop_menu_open"


class SoH2ShopMenuOpenSubGoal(RegionMatchSubGoal):
    NAME = "shop_menu_open"
    _NAMED_REGION = "full_screen"
    _TARGET_NAME = "shop_menu_open"


class SoH2BattleMagicMenuTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "battle_magic_menu"


class SoH2MotionResultTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "motion_result"


class SoH2MagicMenuOpenSubGoal(RegionMatchSubGoal):
    NAME = "magic_menu_open"
    _NAMED_REGION = "full_screen"
    _TARGET_NAME = "magic_menu_open"


class SoH2ItemFoundTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "item_found"


class SoH2LookTargetSubGoal(RegionMatchSubGoal):
    NAME = "look_target"
    _NAMED_REGION = "full_screen"
    _TARGET_NAME = "look_target"


class SoH2CprSwordPurchasedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "cpr_sword_purchased"


class SoH2WeaponsShopMenuOpenSubGoal(RegionMatchSubGoal):
    NAME = "weapons_shop_menu_open"
    _NAMED_REGION = "full_screen"
    _TARGET_NAME = "weapons_shop_menu_open"


class SoH2CursorOnAutoTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "soh2_battle_command"
    _TERMINATION_TARGET_NAME = "cursor_on_auto"


class SoH2WheatFromTreeTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "wheat_from_tree"


class SoH2HitTreeTargetSubGoal(RegionMatchSubGoal):
    NAME = "hit_tree_target"
    _NAMED_REGION = "full_screen"
    _TARGET_NAME = "hit_tree_target"


class SoH2UseMenuOpenTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "full_screen"
    _TERMINATION_TARGET_NAME = "use_menu_open"


class SoH2ItemMenuOpenSubGoal(RegionMatchSubGoal):
    NAME = "item_menu_open"
    _NAMED_REGION = "full_screen"
    _TARGET_NAME = "item_menu_open"


class SoH2UseMenuOpenSubGoal(RegionMatchSubGoal):
    NAME = "use_menu_open"
    _NAMED_REGION = "full_screen"
    _TARGET_NAME = "use_menu_open"


class SoH2WheatConsumedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "wheat_consumed"


class SoH2CursorOnWheatSubGoal(RegionMatchSubGoal):
    NAME = "cursor_on_wheat"
    _NAMED_REGION = "full_screen"
    _TARGET_NAME = "cursor_on_wheat"


class SoH2PowerStatsExpPageTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "power_stats_exp_page"


class SoH2CursorOnPowerSubGoal(RegionMatchSubGoal):
    NAME = "cursor_on_power"
    _NAMED_REGION = "status_command"
    _TARGET_NAME = "cursor_on_power"


class SoH2PowerStatsFirstPageSubGoal(RegionMatchSubGoal):
    NAME = "power_stats_first_page"
    _NAMED_REGION = "status_command"
    _TARGET_NAME = "power_stats_first_page"


class SoH2CursorOnLookTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "cursor_on_look"


class SoH2CursorOnItemTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "cursor_on_item"


class SoH2CursorOnOpenTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "cursor_on_open"


class SoH2CursorOnMagicTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "cursor_on_magic"


class SoH2CursorOnHitTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "cursor_on_hit"


class SoH2CursorOnPowerTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope2Parser

    _TERMINATION_NAMED_REGION = "status_command"
    _TERMINATION_TARGET_NAME = "cursor_on_power"


# Subgoal versions of cursor_on_<command> for the cycle-through task.
# Same regions/targets as the terminator versions, just different role.

class SoH2CursorOnLookSubGoal(RegionMatchSubGoal):
    NAME = "cursor_on_look"
    _NAMED_REGION = "status_command"
    _TARGET_NAME = "cursor_on_look"


class SoH2CursorOnItemSubGoal(RegionMatchSubGoal):
    NAME = "cursor_on_item"
    _NAMED_REGION = "status_command"
    _TARGET_NAME = "cursor_on_item"


class SoH2CursorOnOpenSubGoal(RegionMatchSubGoal):
    NAME = "cursor_on_open"
    _NAMED_REGION = "status_command"
    _TARGET_NAME = "cursor_on_open"


class SoH2CursorOnMagicSubGoal(RegionMatchSubGoal):
    NAME = "cursor_on_magic"
    _NAMED_REGION = "status_command"
    _TARGET_NAME = "cursor_on_magic"


class SoH2CursorOnHitSubGoal(RegionMatchSubGoal):
    NAME = "cursor_on_hit"
    _NAMED_REGION = "status_command"
    _TARGET_NAME = "cursor_on_hit"


class SoH2LookShopkeeperSubGoal(RegionMatchSubGoal):
    NAME = "look_shopkeeper"
    _NAMED_REGION = "full_screen"
    _TARGET_NAME = "look_shopkeeper"


class SoH2ShopBuySellMenuSubGoal(RegionMatchSubGoal):
    NAME = "shop_buy_sell_menu"
    _NAMED_REGION = "full_screen"
    _TARGET_NAME = "shop_buy_sell_menu"


class SoH2CursorOnCprSwordSubGoal(RegionMatchSubGoal):
    NAME = "cursor_on_cpr_sword"
    _NAMED_REGION = "full_screen"
    _TARGET_NAME = "cursor_on_cpr_sword"
