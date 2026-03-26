from gameboy_worlds.emulation.sword_of_hope.parsers import SwordOfHope1Parser
from gameboy_worlds.emulation.tracker import (
    RegionMatchTerminationMetric,
    TerminationMetric,
)


class MillRoomTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SwordOfHope1Parser

    _TERMINATION_NAMED_REGION = "room_label"
    _TERMINATION_TARGET_NAME = "mill_room"
