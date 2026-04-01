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
