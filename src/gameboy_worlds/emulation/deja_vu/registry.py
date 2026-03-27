from typing import Optional, Union, Type, Dict
from gameboy_worlds.emulation.parser import StateParser
from gameboy_worlds.emulation.tracker import StateTracker
from gameboy_worlds.emulation.emulator import Emulator

from gameboy_worlds.emulation.deja_vu.parsers import (
    DejaVu1StateParser,
    DejaVu2StateParser,
)
from gameboy_worlds.emulation.deja_vu.trackers import (
    DejaVuCoatTestTracker,
    DejaVuOCRTracker,
    DejaVuTakeGunTestTracker,
    DejaVuOpenDoorTestTracker,
    DejaVuCloseDoorTestTracker,
    DejaVuOpenPocketTestTracker,
    DejaVuOpenWalletTestTracker,
    DejaVuTakeGunTestTracker,
    DejaVuOpenDoorTestTracker,
    DejaVuCloseDoorTestTracker,
)
from gameboy_worlds.emulation.deja_vu.emulators import DejaVuEmulator

GAME_TO_GB_NAME = {
    "deja_vu_1": "DejaVu.gbc",
    "deja_vu_2": "DejaVu.gbc",
}
""" Expected save name for each game. Save the file to <storage_dir_from_config_file>/<game_name>_rom_data/<gb_name>"""

STRONGEST_PARSERS: Dict[str, Type[StateParser]] = {
    "deja_vu_1": DejaVu1StateParser,
    "deja_vu_2": DejaVu2StateParser,
}
""" Mapping of game names to their corresponding strongest StateParser classes. 
Unless you have a very good reason, you should always use the STRONGEST possible parser for a given game. 
The parser itself does not affect performance, as for it to perform a read / screen comparison operation , it must be called upon by the state tracker.
This means there is never a reason to use a weaker parser. 
"""


AVAILABLE_STATE_TRACKERS: Dict[str, Dict[str, Type[StateTracker]]] = {
    "deja_vu_1": {
        "default": DejaVuOCRTracker,
        "take_coat_test": DejaVuCoatTestTracker,
        "take_gun_test": DejaVuTakeGunTestTracker,
        "open_door_test": DejaVuOpenDoorTestTracker,
        "close_door_test": DejaVuCloseDoorTestTracker,
        "open_pocket_test": DejaVuOpenPocketTestTracker,
        "open_wallet_test": DejaVuOpenWalletTestTracker,

    },
    "deja_vu_2": {
        "default": DejaVuOCRTracker
    },
}
""" Mapping of game names to their available StateTracker classes with string identifiers. """


AVAILABLE_EMULATORS: Dict[str, Dict[str, Type[Emulator]]] = {
    "deja_vu_1": {
        "default": DejaVuEmulator,
    },
    "deja_vu_2": {
        "default": DejaVuEmulator,
    },
}
""" Mapping of game names to their available Emulator classes with string identifiers. """
