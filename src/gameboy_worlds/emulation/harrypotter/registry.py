from typing import Optional, Union, Type, Dict
from gameboy_worlds.emulation.parser import StateParser
from gameboy_worlds.emulation.tracker import StateTracker
from gameboy_worlds.emulation.emulator import Emulator
from gameboy_worlds.emulation.harrypotter.parsers import (
    HarryPotterPhilosophersStoneParser,
)
from gameboy_worlds.emulation.harrypotter.trackers import (
    PotionsShopTestTracker,
)

GAME_TO_GB_NAME = {
    "harrypotter_philosophersstone": "HarryPotterPhilosophersStone.gbc",
}
""" Expected save name for each game. Save the file to <storage_dir_from_config_file>/<game_name>_rom_data/<gb_name>"""

STRONGEST_PARSERS: Dict[str, Type[StateParser]] = {
    "harrypotter_philosophersstone": HarryPotterPhilosophersStoneParser,
}
""" Mapping of game names to their corresponding strongest StateParser classes.
Unless you have a very good reason, you should always use the STRONGEST possible parser for a given game.
The parser itself does not affect performance, as for it to perform a read / screen comparison operation , it must be called upon by the state tracker.
This means there is never a reason to use a weaker parser.
"""


AVAILABLE_STATE_TRACKERS: Dict[str, Dict[str, Type[StateTracker]]] = {
    "harrypotter_philosophersstone": {
        "default": StateTracker,
        "potions_shop_test": PotionsShopTestTracker,
    },
}
""" Mapping of game names to their available StateTracker classes with string identifiers. """


AVAILABLE_EMULATORS: Dict[str, Dict[str, Type[Emulator]]] = {
    "harrypotter_philosophersstone": {"default": Emulator},
}
""" Mapping of game names to their available Emulator classes with string identifiers. """
