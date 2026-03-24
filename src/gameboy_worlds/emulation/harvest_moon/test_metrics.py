from typing import Optional

from gameboy_worlds.emulation.harvest_moon.parsers import HarvestMoonStateParser, BaseHarvestMoonStateParser
from gameboy_worlds.emulation.tracker import (
    RegionMatchTerminationOnlyMetric,
    TerminationMetric,
    RegionMatchTerminationMetric,
    RegionMatchSubGoal,
    AnyRegionMatchSubGoal,
)

class ChickenCoopTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom"
    _TERMINATION_TARGET_NAME = "chicken_coop_entrance"
    
class CowBarnTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom"
    _TERMINATION_TARGET_NAME = "cow_barn_entrance"
    
class OutsideCowBarnSubgoal(AnyRegionMatchSubGoal):
    NAME = "outside_cow_barn"
    _NAMED_REGIONS = [
        "screen_middle",
        "screen_middle",
        "screen_middle",
    ]
    _TARGET_NAMES = [
        "outside_cow_barn_left",
        "outside_cow_barn_right",
        "outside_cow_barn_up",
    ]
    
class OutsideChickenCoopSubgoal(AnyRegionMatchSubGoal):
    NAME = "outside_chicken_coop"
    _NAMED_REGIONS = [
        "screen_middle",
        "screen_middle",
        "screen_middle",
    ]
    _TARGET_NAMES = [
        "outside_chicken_coop_left",
        "outside_chicken_coop_right",
        "outside_chicken_coop_up",
    ]