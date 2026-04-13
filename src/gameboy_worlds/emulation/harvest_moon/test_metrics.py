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
    
class PickupWaterCanTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_top"
    _TERMINATION_TARGET_NAME = "pick_up_watercan"

class NextToWaterCanSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_water_can"
    _NAMED_REGIONS = [
        "item_watercan_above",
        "item_watercan_right",
        "item_watercan_below",
    ]
    _TARGET_NAMES = [
        "pickup_watercan_down",
        "pickup_watercan_left",
        "pickup_watercan_up",
    ]
    
class GoToSleepTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "item_bed"
    _TERMINATION_TARGET_NAME = "sleep_in_bed"
    
class SleepOptionSubgoal(AnyRegionMatchSubGoal):
    NAME = "sleep_option"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "choose_yes_for_sleep",
    ]
    
class FeedSpiritTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_bottom"
    _TERMINATION_TARGET_NAME = "fed_spirit"

class NextToSpiritSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_spirit"
    _NAMED_REGIONS = [
        "item_spirit_left",
        "item_spirit_below",
        "item_spirit_above",       
    ]
    _TARGET_NAMES = [
        "feed_spirit_right",
        "feed_spirit_up",
        "feed_spirit_down",
    ]

class WaterTurnipTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "turnip_center"
    _TERMINATION_TARGET_NAME = "finish_watering"

class NextToTurnipSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_turnip"
    _NAMED_REGIONS = [
        "turnip_top",
    ]
    _TARGET_NAMES = [
        "ready_to_water",
    ]
    
class BuyPotatoSeedsTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom_half"
    _TERMINATION_TARGET_NAME = "bought_potato_seeds"
    
class OutsideFlowerShopSubgoal(AnyRegionMatchSubGoal):
    NAME = "outside_flower_shop"
    _NAMED_REGIONS = [
        "center_sign",
    ]
    _TARGET_NAMES = [
        "outside_flower_shop",
    ]
    
class ShopForSeedsSubgoal(AnyRegionMatchSubGoal):
    NAME = "shop_for_seeds"
    _NAMED_REGIONS = [
        "screen_top_half",
    ]
    _TARGET_NAMES = [
        "in_flower_shop",
    ]

class SelectPotatoSeedsSubgoal(AnyRegionMatchSubGoal):
    NAME = "selected_potato_seeds"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "select_potato_seeds",
    ]
    
class SelectPotatoSeedsOnePortionSubgoal(AnyRegionMatchSubGoal):
    NAME = "select_potato_seeds_one_portion"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "select_potato_seeds_portion",
    ]
    
class BuyTurnipSeedsTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom_half"
    _TERMINATION_TARGET_NAME = "bought_turnip_seeds"
    
class SelectTurnipSeedsSubgoal(AnyRegionMatchSubGoal):
    NAME = "selected_turnip_seeds"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "select_turnip_seeds",
    ]
    
class SelectTurnipSeedsOnePortionSubgoal(AnyRegionMatchSubGoal):
    NAME = "select_turnip_seeds_two_portion"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "select_turnip_seeds_portion",
    ]

class BuyRiceBallTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom_half"
    _TERMINATION_TARGET_NAME = "bought_rice_ball"
    
class OutsideRestaurantSubgoal(AnyRegionMatchSubGoal):
    NAME = "outside_restaurant"
    _NAMED_REGIONS = [
        "center_sign",
    ]
    _TARGET_NAMES = [
        "outside_restaurant",
    ]
    
class ShopForFoodSubgoal(AnyRegionMatchSubGoal):
    NAME = "shop_for_food"
    _NAMED_REGIONS = [
        "screen_top_half",
    ]
    _TARGET_NAMES = [
        "in_restaurant",
    ]
    
class SelectRiceBallSubgoal(AnyRegionMatchSubGoal):
    NAME = "selected_rice_ball"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "select_rice_ball",
    ]
    
class BuyRiceBallOptionSubgoal(AnyRegionMatchSubGoal):
    NAME = "buy_rice_ball_option"
    _NAMED_REGIONS = [
        "screen_bottom_half",
    ]
    _TARGET_NAMES = [
        "option_to_buy_rice_ball",
    ]

class OpenStorageListTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "left_border_frame"
    _TERMINATION_TARGET_NAME = "open_storage_list"
    
class NextToStorageListSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_storage_list"
    _NAMED_REGIONS = [
        "item_storage_list",
    ]
    _TARGET_NAMES = [
        "next_to_storage_list",
    ]

class FindLostBirdTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_bottom"
    _TERMINATION_TARGET_NAME = "found_bird_for_friend"
    
class NextToLostBirdSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_lost_bird"
    _NAMED_REGIONS = [
        "item_lost_bird_below",
        "item_lost_bird_left",
        "item_lost_bird_right",
    ]
    _TARGET_NAMES = [
        "find_lost_bird_up",
        "find_lost_bird_right",
        "find_lost_bird_left",
    ]

class SpeakToBlueHairGirlTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_bottom"
    _TERMINATION_TARGET_NAME = "speaking_to_blue_hair_girl"
    
class NextToBlueHairGirlSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_blue_hair_girl"
    _NAMED_REGIONS = [
        "item_blue_hair_girl_below",
        "item_blue_hair_girl_left",
        "item_blue_hair_girl_right",
    ]
    _TARGET_NAMES = [
        "next_to_blue_hair_girl_up",
        "next_to_blue_hair_girl_right",
        "next_to_blue_hair_girl_left",
    ]
    
class FillChickenFodderBlock1TerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "item_chicken_stall_block1"
    _TERMINATION_TARGET_NAME = "filled_chicken_stall_block1"
    
class NextToChickenFodderBlock1Subgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_chicken_stall_block1_with_fodder"
    _NAMED_REGIONS = [
        "item_next_to_chicken_stall_block1",
    ]
    _TARGET_NAMES = [
        "next_to_chicken_stall_block1",
    ]
    
class NextToChickenSiloSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_chicken_silo"
    _NAMED_REGIONS = [
        "item_chicken_silo_left",
        "item_chicken_silo_below1",
        "item_chicken_silo_below2",
    ]
    _TARGET_NAMES = [
        "next_to_chicken_silo_right",
        "next_to_chicken_silo_up1",
        "next_to_chicken_silo_up2",
    ]

class PickupChickenFodderSubgoal(AnyRegionMatchSubGoal):
    NAME = "picked_up_chicken_fodder_from_silo"
    _NAMED_REGIONS = [
        "item_chicken_silo_left",
        "item_chicken_silo_below1",
        "item_chicken_silo_below2",
    ]
    _TARGET_NAMES = [
        "got_fodder_from_chicken_silo_right",
        "got_fodder_from_chicken_silo_up1",
        "got_fodder_from_chicken_silo_up2",
    ]