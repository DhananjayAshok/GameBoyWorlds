from typing import Optional, Union, Type, Dict
from gameboy_worlds.emulation.parser import StateParser
from gameboy_worlds.emulation.tracker import StateTracker
from gameboy_worlds.emulation.emulator import Emulator
from gameboy_worlds.emulation.harvest_moon.parsers import (
    HarvestMoon1Parser,
    HarvestMoon2Parser,
    HarvestMoon3Parser,
)
from gameboy_worlds.emulation.harvest_moon.trackers import (
    HarvestMoonOCRTracker,
    HarvestMoonCowBarnTracker,   
    HarvestMoonChickenCoopTracker,
    HarvestMoonStorageTracker,
    HarvestMoonPickupWaterCanTracker,
    HarvestMoonGoToSleepTracker,
    HarvestMoonFeedSpiritTracker,
    HarvestMoonWaterTurnipTracker,
    HarvestMoonBuyPotatoSeedsTracker,
    HarvestMoonBuyTurnipSeedsTracker,
    HarvestMoonBuyRiceBallTracker,
    HarvestMoonOpenMenuTracker,
    HarvestMoonOpenStorageListTracker,
    HarvestMoonFindLostBirdTracker,
    HarvestMoonSpeakToBlueHairGirlTracker,
    HarvestMoonFillChickenFodderTracker,
    HarvestMoonPickupSickleTracker,
    HarvestMoonPickupHoeTracker,
    HarvestMoonPickupHammerTracker,
    HarvestMoonPickupGrassSeedTracker,
    HarvestMoonBuyCroissantTracker,
    HarvestMoonBuyCakeTracker,
    HarvestMoonGoToChurchPrayTracker,
    HarvestMoonSpeakToGoldenHairGirlTracker,
    HarvestMoonSpeakToPinkHairGirlTracker,
    
    # HM2
    HarvestMoon2FlowerShopEntranceTracker,
    HarvestMoon2BuyPotatoSeedsTracker,
    HarvestMoon2BuyAsparagusSeedsTracker,
    
    HarvestMoonReadVillageSignTracker,
    HarvestMoonReadFarmSignTracker,
    HarvestMoon2ReadSecretGardenSignTracker,
    HarvestMoon3ReadSecretGardenSignTracker,
    HarvestMoon3BuyPotatoSeedsTracker,
    HarvestMoon3BuyTurnipSeedsTracker,
    HarvestMoon3SpeakToLukiaTracker,
    HarvestMoon3SpeakToLucusTracker,
    HarvestMoon3SpeakToLylaTracker,
    HarvestMoon3BuyMealSetTracker,
    HarvestMoon3BuyCoffeeTracker,
    HarvestMoon3ShoppingMallEntranceTracker,
    HarvestMoon3FarmersUnionEntranceTracker,
    HarvestMoon3AquariumEntranceTracker,
    HarvestMoon3TheatreEntranceTracker,
    HarvestMoon2ReadCropFieldSignTracker,
    HarvestMoonReadNoticeBoardTracker,
    HarvestMoon2RestaurantEntranceTracker,
    HarvestMoon2BuyLunchSetTracker,
    HarvestMoon2BuyBeverageSetTracker,
    HarvestMoon2BuyTodaysSpecialTracker,
    HarvestMoon2WriteDiaryAndSleepTracker,
)

GAME_TO_GB_NAME = {
    "harvest_moon_1": "HarvestMoon1.gbc",
    "harvest_moon_2": "HarvestMoon2.gbc",
    "harvest_moon_3": "HarvestMoon3.gbc",
}
""" Expected save name for each game. Save the file to <storage_dir_from_config_file>/<game_name>_rom_data/<gb_name>"""

STRONGEST_PARSERS: Dict[str, Type[StateParser]] = {
    "harvest_moon_1": HarvestMoon1Parser,
    "harvest_moon_2": HarvestMoon2Parser,
    "harvest_moon_3": HarvestMoon3Parser,
}
""" Mapping of game names to their corresponding strongest StateParser classes. 
Unless you have a very good reason, you should always use the STRONGEST possible parser for a given game. 
The parser itself does not affect performance, as for it to perform a read / screen comparison operation , it must be called upon by the state tracker.
This means there is never a reason to use a weaker parser. 
"""


AVAILABLE_STATE_TRACKERS: Dict[str, Dict[str, Type[StateTracker]]] = {
    "harvest_moon_1": {
        "default": HarvestMoonOCRTracker,
        "cow_barn_test": HarvestMoonCowBarnTracker,
        "chicken_coop_test": HarvestMoonChickenCoopTracker,
        "storage_shed_test": HarvestMoonStorageTracker,
        "pickup_watercan_test": HarvestMoonPickupWaterCanTracker,
        "go_to_sleep_test": HarvestMoonGoToSleepTracker,
        "feed_spirit_test": HarvestMoonFeedSpiritTracker,
        "water_turnip_test": HarvestMoonWaterTurnipTracker,
        "buy_potato_seeds_test": HarvestMoonBuyPotatoSeedsTracker,
        "buy_turnip_seeds_test": HarvestMoonBuyTurnipSeedsTracker,
        "buy_rice_ball_test": HarvestMoonBuyRiceBallTracker,
        "open_storage_list_test": HarvestMoonOpenStorageListTracker,
        "find_lost_bird_test": HarvestMoonFindLostBirdTracker,
        "speak_to_blue_hair_girl_test": HarvestMoonSpeakToBlueHairGirlTracker,
        "fill_chicken_fodder_test": HarvestMoonFillChickenFodderTracker,
        "pickup_sickle_test": HarvestMoonPickupSickleTracker,
        "pickup_hoe_test": HarvestMoonPickupHoeTracker,
        "pickup_hammer_test": HarvestMoonPickupHammerTracker,
        "pickup_grass_seed_test": HarvestMoonPickupGrassSeedTracker,
        "buy_croissant_test": HarvestMoonBuyCroissantTracker,
        "buy_cake_test": HarvestMoonBuyCakeTracker,
        "go_to_church_pray_test": HarvestMoonGoToChurchPrayTracker,
        "speak_to_golden_hair_girl_test": HarvestMoonSpeakToGoldenHairGirlTracker,
        "speak_to_pink_hair_girl_test": HarvestMoonSpeakToPinkHairGirlTracker,
        "open_menu_test": HarvestMoonOpenMenuTracker,
    },
    "harvest_moon_2": {
        "default": HarvestMoonOCRTracker,
        "cow_barn_test": HarvestMoonCowBarnTracker,
        "chicken_coop_test": HarvestMoonChickenCoopTracker,
        "flower_shop_entrance_test": HarvestMoon2FlowerShopEntranceTracker,
        "buy_potato_seeds_test": HarvestMoon2BuyPotatoSeedsTracker,
        "buy_asparagus_seeds_test": HarvestMoon2BuyAsparagusSeedsTracker,
        "restaurant_entrance_test": HarvestMoon2RestaurantEntranceTracker,
        "buy_lunch_set_test": HarvestMoon2BuyLunchSetTracker,
        "buy_beverage_set_test": HarvestMoon2BuyBeverageSetTracker,
        "buy_todays_special_test": HarvestMoon2BuyTodaysSpecialTracker,
        "write_diary_and_sleep_test": HarvestMoon2WriteDiaryAndSleepTracker,
        "read_secret_garden_sign_test": HarvestMoon2ReadSecretGardenSignTracker,
        "read_crop_field_sign_test": HarvestMoon2ReadCropFieldSignTracker,
        
        "storage_shed_test": HarvestMoonStorageTracker,
        "water_turnip_test": HarvestMoonWaterTurnipTracker,
        "open_storage_list_test": HarvestMoonOpenStorageListTracker,
        "read_village_sign_test": HarvestMoonReadVillageSignTracker,
        "read_farm_sign_test": HarvestMoonReadFarmSignTracker,
        "read_notice_board_test": HarvestMoonReadNoticeBoardTracker,
        "open_menu_test": HarvestMoonOpenMenuTracker,
    },
    "harvest_moon_3": {
        "default": HarvestMoonOCRTracker,
        "cow_barn_test": HarvestMoonCowBarnTracker,
        "chicken_coop_test": HarvestMoonChickenCoopTracker,
        "read_secret_garden_sign_test": HarvestMoon3ReadSecretGardenSignTracker,
        "buy_potato_seeds_test": HarvestMoon3BuyPotatoSeedsTracker,
        "buy_turnip_seeds_test": HarvestMoon3BuyTurnipSeedsTracker,
        "speak_to_Lukia_test": HarvestMoon3SpeakToLukiaTracker,
        "speak_to_Lucus_test": HarvestMoon3SpeakToLucusTracker,
        "speak_to_Lyla_test": HarvestMoon3SpeakToLylaTracker,
        "buy_meal_set_test": HarvestMoon3BuyMealSetTracker,
        "buy_coffee_test": HarvestMoon3BuyCoffeeTracker,
        "shopping_mall_entrance_test": HarvestMoon3ShoppingMallEntranceTracker,
        "farmers_union_entrance_test": HarvestMoon3FarmersUnionEntranceTracker,
        "aquarium_entrance_test": HarvestMoon3AquariumEntranceTracker,
        "theatre_entrance_test": HarvestMoon3TheatreEntranceTracker,
        "open_menu_test": HarvestMoonOpenMenuTracker,
    },
}
""" Mapping of game names to their available StateTracker classes with string identifiers. """


AVAILABLE_EMULATORS: Dict[str, Dict[str, Type[Emulator]]] = {
    "harvest_moon_1": {"default": Emulator},
    "harvest_moon_2": {"default": Emulator},
    "harvest_moon_3": {"default": Emulator},
}
""" Mapping of game names to their available Emulator classes with string identifiers. """
