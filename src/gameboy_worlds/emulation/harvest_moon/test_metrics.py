from typing import Optional
from abc import ABC

from gameboy_worlds.emulation.harvest_moon.parsers import HarvestMoonStateParser, BaseHarvestMoonStateParser
from gameboy_worlds.emulation.tracker import (
    RegionMatchTerminationOnlyMetric,
    TerminationMetric,
    RegionMatchTerminationMetric,
    TerminationTruncationMetric,
    RegionMatchSubGoal,
    AnyRegionMatchSubGoal,
)


class MultiRegionMatchTerminationMetric(TerminationTruncationMetric, ABC):
    """
    Terminates when OR_PAIRS and ALL_PAIRS conditions are both satisfied.
    OR_PAIRS: list of (region, target) — at least one must match.
    ALL_PAIRS: list of (region, target) — every one must match.
    Termination condition: (any OR_PAIR matches) AND (all ALL_PAIRS match).
    Either list may be empty, in which case its condition is trivially satisfied.
    """

    REQUIRED_PARSER = BaseHarvestMoonStateParser
    _OR_PAIRS: list = []
    _ALL_PAIRS: list = []

    def determine_terminated(self, current_frame, recent_frames):
        all_frames = [current_frame]
        if recent_frames is not None:
            all_frames = recent_frames
        for frame in all_frames:
            or_ok = (not self._OR_PAIRS) or any(
                self.state_parser.named_region_matches_multi_target(frame, region, target)
                for region, target in self._OR_PAIRS
            )
            all_ok = all(
                self.state_parser.named_region_matches_multi_target(frame, region, target)
                for region, target in self._ALL_PAIRS
            )
            if or_ok and all_ok:
                return True
        return False

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

class StorageTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom"
    _TERMINATION_TARGET_NAME = "storage_shed_entrance"

class OutsideStorageSubgoal(AnyRegionMatchSubGoal):
    NAME = "outside_storage_shed"
    _NAMED_REGIONS = [
        "screen_middle",
        "screen_middle",
        "screen_middle",
    ]
    _TARGET_NAMES = [
        "outside_storage_left",
        "outside_storage_right",
        "outside_storage_up",
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
    
class PickupSickleTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_top_mid"
    _TERMINATION_TARGET_NAME = "pick_up_sickle"

class NextToSickleSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_sickle"
    _NAMED_REGIONS = [
        "item_sickle_above",
        "item_sickle_left",
        "item_sickle_below",
    ]
    _TARGET_NAMES = [
        "pickup_sickle_down",
        "pickup_sickle_right",
        "pickup_sickle_up",
    ]

class PickupHoeTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_top_short"
    _TERMINATION_TARGET_NAME = "pick_up_hoe"

class NextToHoeSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_hoe"
    _NAMED_REGIONS = [
        "item_hoe_above",
        "item_hoe_below",
    ]
    _TARGET_NAMES = [
        "pickup_hoe_down",
        "pickup_hoe_up",
    ]

class PickupHammerTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_top_mid"
    _TERMINATION_TARGET_NAME = "pick_up_hammer"

class NextToHammerSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_hammer"
    _NAMED_REGIONS = [
        "item_hammer_above",
        "item_hammer_below",
    ]
    _TARGET_NAMES = [
        "pickup_hammer_down",
        "pickup_hammer_up",
    ]

class PickupGrassSeedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_top"
    _TERMINATION_TARGET_NAME = "pick_up_grass_seed"

class NextToGrassSeedSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_grass_seed"
    _NAMED_REGIONS = [
        "item_grass_seed_above",
        "item_grass_seed_right",
        "item_grass_seed_below",
    ]
    _TARGET_NAMES = [
        "pickup_grass_seed_down",
        "pickup_grass_seed_left",
        "pickup_grass_seed_up",
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

class BuyCroissantTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom_half"
    _TERMINATION_TARGET_NAME = "bought_croissant"

class SelectCroissantSubgoal(AnyRegionMatchSubGoal):
    NAME = "selected_croissant"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "select_croissant",
    ]

class BuyCroissantOptionSubgoal(AnyRegionMatchSubGoal):
    NAME = "buy_croissant_option"
    _NAMED_REGIONS = [
        "screen_bottom_half",
    ]
    _TARGET_NAMES = [
        "option_to_buy_croissant",
    ]

class BuyCakeTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom_half"
    _TERMINATION_TARGET_NAME = "bought_cake"

class SelectCakeSubgoal(AnyRegionMatchSubGoal):
    NAME = "selected_cake"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "select_cake",
    ]

class BuyCakeOptionSubgoal(AnyRegionMatchSubGoal):
    NAME = "buy_cake_option"
    _NAMED_REGIONS = [
        "screen_bottom_half",
    ]
    _TARGET_NAMES = [
        "option_to_buy_cake",
    ]

class GoToChurchPrayTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_bottom"
    _TERMINATION_TARGET_NAME = "praying"

class OutsideChurchSubgoal(AnyRegionMatchSubGoal):
    NAME = "outside_church"
    _NAMED_REGIONS = [
        "center_sign",
    ]
    _TARGET_NAMES = [
        "outside_church",
    ]

class InsideChurchSubgoal(AnyRegionMatchSubGoal):
    NAME = "inside_church"
    _NAMED_REGIONS = [
        "screen_top_half",
    ]
    _TARGET_NAMES = [
        "in_church",
    ]

class PrayOptionSubgoal(AnyRegionMatchSubGoal):
    NAME = "choose_to_pray"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "option_to_pray",
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
    
class SpeakToGoldenHairGirlTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_bottom"
    _TERMINATION_TARGET_NAME = "speaking_to_golden_hair_girl"

class NextToGoldenHairGirlSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_golden_hair_girl"
    _NAMED_REGIONS = [
        "item_golden_hair_girl_below",
        "item_golden_hair_girl_right",
        "item_golden_hair_girl_above",
    ]
    _TARGET_NAMES = [
        "next_to_golden_hair_girl_up",
        "next_to_golden_hair_girl_left",
        "next_to_golden_hair_girl_down",
    ]

class SpeakToPinkHairGirlTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_bottom"
    _TERMINATION_TARGET_NAME = "speaking_to_pink_hair_girl"

class NextToPinkHairGirlSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_pink_hair_girl"
    _NAMED_REGIONS = [
        "item_pink_hair_girl_above",
        "item_pink_hair_girl_left",
        "item_pink_hair_girl_right",
    ]
    _TARGET_NAMES = [
        "next_to_pink_hair_girl_down",
        "next_to_pink_hair_girl_right",
        "next_to_pink_hair_girl_left",
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




class FlowerShopEntranceTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "screen_top_half"
    _TERMINATION_TARGET_NAME = "in_flower_shop"

class OutsideFlowerShop2Subgoal(AnyRegionMatchSubGoal):
    NAME = "outside_flower_shop"
    _NAMED_REGIONS = [
        "flower_shop_location",
        "flower_shop_location",
        "flower_shop_location",
    ]
    _TARGET_NAMES = [
        "outside_flower_shop_up",
        "outside_flower_shop_left",
        "outside_flower_shop_right",
    ]


class SelectPotatoSeeds2Subgoal(AnyRegionMatchSubGoal):
    NAME = "selected_potato_seeds"
    _NAMED_REGIONS = [
        "screen_bottom_half",
    ]
    _TARGET_NAMES = [
        "select_potato_seeds",
    ]
    
class SelectPotatoSeedsOnePortion2Subgoal(AnyRegionMatchSubGoal):
    NAME = "select_potato_seeds_one_portion"
    _NAMED_REGIONS = [
        "screen_bottom_half",
    ]
    _TARGET_NAMES = [
        "select_potato_seeds_portion",
    ]
    
class BuyAsparagusSeedsTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom_half"
    _TERMINATION_TARGET_NAME = "bought_asparagus_seeds"
  
class SelectAsparagusSeeds2Subgoal(AnyRegionMatchSubGoal):
    NAME = "selected_asparagus_seeds"
    _NAMED_REGIONS = [
        "screen_bottom_half",
    ]
    _TARGET_NAMES = [
        "select_asparagus_seeds",
    ]

class SelectAsparagusSeedsOnePortion2Subgoal(AnyRegionMatchSubGoal):
    NAME = "select_asparagus_seeds_two_portion"
    _NAMED_REGIONS = [
        "screen_bottom_half",
    ]
    _TARGET_NAMES = [
        "select_asparagus_seeds_portion",
    ]


class RestaurantEntranceTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "screen_top_half"
    _TERMINATION_TARGET_NAME = "in_restaurant"

class OutsideRestaurant2Subgoal(AnyRegionMatchSubGoal):
    NAME = "outside_restaurant"
    _NAMED_REGIONS = [
        "restaurant_location",
        "restaurant_location",
        "restaurant_location",
    ]
    _TARGET_NAMES = [
        "outside_restaurant_up",
        "outside_restaurant_left",
        "outside_restaurant_right",
    ]

class BuyLunchSetTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom_half"
    _TERMINATION_TARGET_NAME = "bought_lunch_set"

class SelectLunchSetSubgoal(AnyRegionMatchSubGoal):
    NAME = "selected_lunch_set"
    _NAMED_REGIONS = [
        "screen_bottom_half",
    ]
    _TARGET_NAMES = [
        "select_lunch_set",
    ]

class BuyLunchSetOptionSubgoal(AnyRegionMatchSubGoal):
    NAME = "buy_lunch_set_option"
    _NAMED_REGIONS = [
        "screen_bottom_half",
    ]
    _TARGET_NAMES = [
        "option_to_buy_lunch_set",
    ]

class BuyBeverageSetTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom_half"
    _TERMINATION_TARGET_NAME = "bought_beverage_set"

class SelectBeverageSetSubgoal(AnyRegionMatchSubGoal):
    NAME = "selected_beverage_set"
    _NAMED_REGIONS = [
        "screen_bottom_half",
    ]
    _TARGET_NAMES = [
        "select_beverage_set",
    ]

class BuyBeverageSetOptionSubgoal(AnyRegionMatchSubGoal):
    NAME = "buy_beverage_set_option"
    _NAMED_REGIONS = [
        "screen_bottom_half",
    ]
    _TARGET_NAMES = [
        "option_to_buy_beverage_set",
    ]

class BuyTodaysSpecialTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom_half"
    _TERMINATION_TARGET_NAME = "bought_todays_special"

class SelectTodaysSpecialSubgoal(AnyRegionMatchSubGoal):
    NAME = "selected_todays_special"
    _NAMED_REGIONS = [
        "screen_bottom_half",
    ]
    _TARGET_NAMES = [
        "select_todays_special",
    ]

class BuyTodaysSpecialOptionSubgoal(AnyRegionMatchSubGoal):
    NAME = "buy_todays_special_option"
    _NAMED_REGIONS = [
        "screen_bottom_half",
    ]
    _TARGET_NAMES = [
        "option_to_buy_todays_special",
    ]

# TO DO
class ReadNoticeBoardTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_bottom"
    _TERMINATION_TARGET_NAME = "reading_notice_board"

class NextToNoticeBoardSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_notice_board"
    _NAMED_REGIONS = [
        "item_notice_board_above",
        "item_notice_board_left",
        "item_notice_board_right",
    ]
    _TARGET_NAMES = [
        "next_to_notice_board_down",
        "next_to_notice_board_right",
        "next_to_notice_board_left",
    ]

class ReadVillageSignTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_bottom"
    _TERMINATION_TARGET_NAME = "reading_village_sign"

class NextToVillageSignSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_village_sign"
    _NAMED_REGIONS = [
        "item_village_sign_above",
        "item_village_sign_left",
        "item_village_sign_right",
    ]
    _TARGET_NAMES = [
        "next_to_village_sign_down",
        "next_to_village_sign_right",
        "next_to_village_sign_left",
    ]

class ReadFarmSignTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_bottom"
    _TERMINATION_TARGET_NAME = "reading_farm_sign"

class NextToFarmSignSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_farm_sign"
    _NAMED_REGIONS = [
        "item_farm_sign_above",
        "item_farm_sign_left",
        "item_farm_sign_right",
    ]
    _TARGET_NAMES = [
        "next_to_farm_sign_down",
        "next_to_farm_sign_right",
        "next_to_farm_sign_left",
    ]

class ReadSecretGardenSignTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_bottom"
    _TERMINATION_TARGET_NAME = "reading_secret_garden_sign"

class NextToSecretGardenSignSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_secret_garden_sign"
    _NAMED_REGIONS = [
        "item_secret_garden_sign_above",
        "item_secret_garden_sign_right",
        "item_secret_garden_sign_left",
    ]
    _TARGET_NAMES = [
        "next_to_secret_garden_sign_down",
        "next_to_secret_garden_sign_left",
        "next_to_secret_garden_sign_right",
    ]

class ReadCropFieldSignTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_bottom"
    _TERMINATION_TARGET_NAME = "reading_crop_field_sign"

class NextToCropFieldSignSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_crop_field_sign"
    _NAMED_REGIONS = [
        "item_crop_field_sign_above",
    ]
    _TARGET_NAMES = [
        "next_to_crop_field_sign_down",
    ]

class NextToDiarySubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_diary"
    _NAMED_REGIONS = [
        "item_diary",
    ]
    _TARGET_NAMES = [
        "next_to_diary",
    ]

class DiaryOptionSubgoal(AnyRegionMatchSubGoal):
    NAME = "diary_sleep_option"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "option_to_diary_sleep",
    ]
    

class OpenMenuTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "menu_open"

## HM3
class NextToSecretGardenSign3Subgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_secret_garden_sign"
    _NAMED_REGIONS = [
        "item_secret_garden_sign_above",
        "item_secret_garden_sign_right",
    ]
    _TARGET_NAMES = [
        "next_to_secret_garden_sign_down",
        "next_to_secret_garden_sign_left",
    ]

class BuyPotatoSeeds3TerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_bottom"
    _TERMINATION_TARGET_NAME = "bought_potato_seeds"

class NextToPotatoSeeds3Subgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_potato_seeds"
    _NAMED_REGIONS = [
        "item_potato_seeds_above",
        "item_potato_seeds_below",
    ]
    _TARGET_NAMES = [
        "next_to_potato_seeds_down",
        "next_to_potato_seeds_up",
    ]

class NextToTurnipSeeds3Subgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_turnip_seeds"
    _NAMED_REGIONS = [
        "item_turnip_seeds_above",
        "item_turnip_seeds_below",
    ]
    _TARGET_NAMES = [
        "next_to_turnip_seeds_down",
        "next_to_turnip_seeds_up",
    ]

class SelectPotatoSeeds3Subgoal(AnyRegionMatchSubGoal):
    NAME = "selected_potato_seeds"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "select_potato_seeds",
    ]

class SelectPotatoSeedsOnePortion3Subgoal(AnyRegionMatchSubGoal):
    NAME = "select_potato_seeds_two_portion"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "select_potato_seeds_portion",
    ]

# class BuyTurnipSeeds3TerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
#     REQUIRED_PARSER = BaseHarvestMoonStateParser

#     _TERMINATION_NAMED_REGION = "dialogue_box_bottom"
#     _TERMINATION_TARGET_NAME = "bought_turnip_seeds"

class BuyTurnipSeeds3TerminateMetric(MultiRegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser
    _OR_PAIRS = [                                                                                                                                                                                                                                                                                                     
        ("item_turnip_1", "buying_turnip_seeds_1"),  # fallback if confirmation appears elsewhere 
        ("item_turnip_2", "buying_turnip_seeds_2"),                                                                                     
    ]                                                                                                                                                                                    
    _ALL_PAIRS = [                                                                                                                                                                     
        ("dialogue_box_bottom", "bought_turnip_seeds"),   # must still be inside the shop                                                                                                          
    ]   
      
class SelectTurnipSeeds3Subgoal(AnyRegionMatchSubGoal):
    NAME = "selected_turnip_seeds"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "select_turnip_seeds",
    ]

class SelectTurnipSeedsOnePortion3Subgoal(AnyRegionMatchSubGoal):
    NAME = "select_turnip_seeds_one_portion"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "select_turnip_seeds_portion",
    ]

class SpeakToLukiaTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_upper_border"
    _TERMINATION_TARGET_NAME = "speaking_to_lukia"

class NextToLukiaSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_Lukia"
    _NAMED_REGIONS = [
        "npc_lukia_right",
    ]
    _TARGET_NAMES = [
        "next_to_lukia_left",
    ]

class SpeakToLucusTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_upper_border"
    _TERMINATION_TARGET_NAME = "speaking_to_lucus"

class NextToLucusSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_lucus"
    _NAMED_REGIONS = [
        "npc_lucus_above",
        "npc_lucus_left",
        "npc_lucus_right",
    ]
    _TARGET_NAMES = [
        "next_to_lucus_down",
        "next_to_lucus_right",
        "next_to_lucus_left",
    ]

class SpeakToLylaTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_upper_border"
    _TERMINATION_TARGET_NAME = "speaking_to_lyla"

class NextToLylaSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_lyla"
    _NAMED_REGIONS = [
        "npc_lyla_right",
    ]
    _TARGET_NAMES = [
        "next_to_lyla_left",
    ]

class BuyMealSetTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_bottom"
    _TERMINATION_TARGET_NAME = "bought_meal_set"

class NextToMealSetSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_meal_set"
    _NAMED_REGIONS = [
        "item_meal_set_above",
        "item_meal_set_below",
    ]
    _TARGET_NAMES = [
        "next_to_meal_set_down",
        "next_to_meal_set_up",
    ]

class SelectMealSetSubgoal(AnyRegionMatchSubGoal):
    NAME = "selected_meal_set"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "select_meal_set",
    ]

class BuyCoffeeTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_bottom"
    _TERMINATION_TARGET_NAME = "bought_coffee"

class NextToCoffeeSubgoal(AnyRegionMatchSubGoal):
    NAME = "next_to_coffee"
    _NAMED_REGIONS = [
        "item_coffee_above",
        "item_coffee_below",
    ]
    _TARGET_NAMES = [
        "next_to_coffee_down",
        "next_to_coffee_up",
    ]

class SelectCoffeeSubgoal(AnyRegionMatchSubGoal):
    NAME = "selected_coffee"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "select_coffee",
    ]

class ShoppingMallEntranceTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "entrance"
    _TERMINATION_TARGET_NAME = "shopping_mall_entrance"

class NearShoppingMallSubgoal(AnyRegionMatchSubGoal):
    NAME = "outside_shopping_mall"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "shopping_mall_label",
    ]

class FarmersUnionEntranceTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "entrance"
    _TERMINATION_TARGET_NAME = "farmers_union_entrance"

class NearFarmersUnionSubgoal(AnyRegionMatchSubGoal):
    NAME = "outside_farmers_union"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "farmers_union_label",
    ]

class AquariumEntranceTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "entrance"
    _TERMINATION_TARGET_NAME = "aquarium_entrance"

class NearAquariumSubgoal(AnyRegionMatchSubGoal):
    NAME = "outside_aquarium"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "aquarium_label",
    ]

class TheatreEntranceTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = BaseHarvestMoonStateParser

    _TERMINATION_NAMED_REGION = "entrance"
    _TERMINATION_TARGET_NAME = "theatre_entrance"

class NearTheatreSubgoal(AnyRegionMatchSubGoal):
    NAME = "outside_theatre"
    _NAMED_REGIONS = [
        "dialogue_box_bottom",
    ]
    _TARGET_NAMES = [
        "theatre_label",
    ]