from typing import Optional, Union, Type, Dict
from poke_worlds.emulation.parser import StateParser
from poke_worlds.emulation.tracker import StateTracker
from poke_worlds.emulation.emulator import Emulator

from poke_worlds.emulation.deja_vu.parsers import (
    DejaVu1StateParser,
    DejaVu2StateParser,
)
from poke_worlds.emulation.deja_vu.trackers import (
    DejaVuOCRTracker,
)
from poke_worlds.emulation.deja_vu.emulators import DejaVuEmulator

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
        "default": DejaVuOCRTracker
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
