from typing import Optional, Union, Type, Dict
from gameboy_worlds.emulation.parser import StateParser
from gameboy_worlds.emulation.tracker import StateTracker
from gameboy_worlds.emulation.emulator import Emulator
from gameboy_worlds.emulation.sword_of_hope.parsers import (
    SwordOfHope1Parser,
    SwordOfHope2Parser,
)
from gameboy_worlds.emulation.sword_of_hope.trackers import (
    SwordOfHope1MillRoomTestTracker,
    SwordOfHope1ShamanRoomTestTracker,
)

GAME_TO_GB_NAME = {
    "sword_of_hope_1": "SwordOfHope.gb",
    "sword_of_hope_2": "SwordOfHope2.gb",
}
""" Expected save name for each game. Save the file to <storage_dir_from_config_file>/<game_name>_rom_data/<gb_name>"""

STRONGEST_PARSERS: Dict[str, Type[StateParser]] = {
    "sword_of_hope_1": SwordOfHope1Parser,
    "sword_of_hope_2": SwordOfHope2Parser,
}
""" Mapping of game names to their corresponding strongest StateParser classes. 
Unless you have a very good reason, you should always use the STRONGEST possible parser for a given game. 
The parser itself does not affect performance, as for it to perform a read / screen comparison operation , it must be called upon by the state tracker.
This means there is never a reason to use a weaker parser. 
"""


AVAILABLE_STATE_TRACKERS: Dict[str, Dict[str, Type[StateTracker]]] = {
    "sword_of_hope_1": {
        "default": StateTracker,
        "mill_room_test": SwordOfHope1MillRoomTestTracker,
        "shaman_room_test": SwordOfHope1ShamanRoomTestTracker,
    },
    "sword_of_hope_2": {"default": StateTracker},
}
""" Mapping of game names to their available StateTracker classes with string identifiers. """


AVAILABLE_EMULATORS: Dict[str, Dict[str, Type[Emulator]]] = {
    "sword_of_hope_1": {"default": Emulator},
    "sword_of_hope_2": {"default": Emulator},
}
""" Mapping of game names to their available Emulator classes with string identifiers. """
