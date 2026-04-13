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
    HarvestMoonPickupWaterCanTracker,
    HarvestMoonGoToSleepTracker,
    HarvestMoonFeedSpiritTracker,
    HarvestMoonWaterTurnipTracker,
    HarvestMoonBuyPotatoSeedsTracker,
    HarvestMoonBuyTurnipSeedsTracker,
    HarvestMoonBuyRiceBallTracker,
    HarvestMoonOpenStorageListTracker,
    HarvestMoonFindLostBirdTracker,
    HarvestMoonSpeakToBlueHairGirlTracker,
    HarvestMoonFillChickenFodderTracker,
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
    },
    "harvest_moon_2": {
        "default": HarvestMoonOCRTracker,
        "cow_barn_test": HarvestMoonCowBarnTracker,
        "chicken_coop_test": HarvestMoonChickenCoopTracker,
    },
    "harvest_moon_3": {
        "default": HarvestMoonOCRTracker,
        "cow_barn_test": HarvestMoonCowBarnTracker,
        "chicken_coop_test": HarvestMoonChickenCoopTracker,
    },
}
""" Mapping of game names to their available StateTracker classes with string identifiers. """


AVAILABLE_EMULATORS: Dict[str, Dict[str, Type[Emulator]]] = {
    "harvest_moon_1": {"default": Emulator},
    "harvest_moon_2": {"default": Emulator},
    "harvest_moon_3": {"default": Emulator},
}
""" Mapping of game names to their available Emulator classes with string identifiers. """
