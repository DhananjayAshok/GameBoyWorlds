from typing import Optional, Union, Type, Dict
from gameboy_worlds.emulation.parser import StateParser
from gameboy_worlds.emulation.tracker import StateTracker
from gameboy_worlds.emulation.emulator import Emulator

from gameboy_worlds.emulation.legend_of_zelda.parsers import (
    LegendOfZeldaLinksAwakeningParser,
    LegendOfZeldaTheOracleOfSeasonsParser,
)

from gameboy_worlds.emulation.legend_of_zelda.trackers import (
    CoreLegendOfZeldaTracker,
    ZeldaLinksAwakeningOwlTestTracker,
    ZeldaLinksAwakeningShieldTestTracker,
    ZeldaLinksAwakeningOutsideTarinHouseTestTracker,
    ZeldaLinksAwakeningOpenInventoryTestTracker,
    ZeldaLinksAwakeningTalkToKidTestTracker,
    ZeldaLinksAwakeningReadSignboardTestTracker,
    ZeldaLinksAwakeningGoInsideShopTestTracker,
    ZeldaLinksAwakeningMakeCallTestTracker,
    ZeldaLinksAwakeningEnterDarkForestTestTracker,
    ZeldaLinksAwakeningOpenChestTestTracker,
)



GAME_TO_GB_NAME = {
    "legend_of_zelda_links_awakening": "LegendOfZeldaLinksAwakening.gbc",
    "legend_of_zelda_the_oracle_of_seasons": "LegendOfZeldaTheOracleOfSeasons.gbc",
}
""" Expected save name for each game. Save the file to <storage_dir_from_config_file>/<game_name>_rom_data/<gb_name>"""

STRONGEST_PARSERS: Dict[str, Type[StateParser]] = {
    "legend_of_zelda_links_awakening": LegendOfZeldaLinksAwakeningParser,
    "legend_of_zelda_the_oracle_of_seasons": LegendOfZeldaTheOracleOfSeasonsParser,
}
""" Mapping of game names to their corresponding strongest StateParser classes. 
Unless you have a very good reason, you should always use the STRONGEST possible parser for a given game. 
The parser itself does not affect performance, as for it to perform a read / screen comparison operation , it must be called upon by the state tracker.
This means there is never a reason to use a weaker parser. 
"""


AVAILABLE_STATE_TRACKERS: Dict[str, Dict[str, Type[StateTracker]]] = {
    "legend_of_zelda_links_awakening": {
        "default": CoreLegendOfZeldaTracker,
        "pickup_sword_test": ZeldaLinksAwakeningOwlTestTracker,
        "shield_test": ZeldaLinksAwakeningShieldTestTracker,
        "outside_tarinhouse_test": ZeldaLinksAwakeningOutsideTarinHouseTestTracker,
        "open_inventory_test": ZeldaLinksAwakeningOpenInventoryTestTracker,
        "talk_to_kid_test": ZeldaLinksAwakeningTalkToKidTestTracker,
        "read_signboard_test": ZeldaLinksAwakeningReadSignboardTestTracker,
        "go_inside_shop_test": ZeldaLinksAwakeningGoInsideShopTestTracker,
        "make_call_test": ZeldaLinksAwakeningMakeCallTestTracker,
        "enter_dark_forest_test": ZeldaLinksAwakeningEnterDarkForestTestTracker,
        "open_chest_test": ZeldaLinksAwakeningOpenChestTestTracker,
        },
    "legend_of_zelda_the_oracle_of_seasons": {"default": CoreLegendOfZeldaTracker},
}
""" Mapping of game names to their available StateTracker classes with string identifiers. """


AVAILABLE_EMULATORS: Dict[str, Dict[str, Type[Emulator]]] = {
    "legend_of_zelda_links_awakening": {"default": Emulator},
    "legend_of_zelda_the_oracle_of_seasons": {"default": Emulator},
}
""" Mapping of game names to their available Emulator classes with string identifiers. """
