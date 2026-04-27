from gameboy_worlds.emulation.sword_of_hope.parsers import SwordOfHope1Parser
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
