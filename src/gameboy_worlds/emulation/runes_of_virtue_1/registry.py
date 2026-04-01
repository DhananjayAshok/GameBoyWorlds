from typing import Dict, Type
from gameboy_worlds.emulation.parser import StateParser
from gameboy_worlds.emulation.tracker import StateTracker
from gameboy_worlds.emulation.emulator import Emulator
from gameboy_worlds.emulation.runes_of_virtue_1.parsers import RunesOfVirtue1Parser
from gameboy_worlds.emulation.runes_of_virtue_1.trackers import (
    CoreRunesOfVirtue1Tracker,
    RunesOfVirtue1OpenMenuTestTracker,
)

GAME_TO_GB_NAME = {
    "runes_of_virtue_1": "RunesOfVirtue1.gb",
}
""" Expected save name for each game. Save the file to <storage_dir_from_config_file>/<game_name>_rom_data/<gb_name>"""

STRONGEST_PARSERS: Dict[str, Type[StateParser]] = {
    "runes_of_virtue_1": RunesOfVirtue1Parser,
}
""" Mapping of game names to their corresponding strongest StateParser classes. """

AVAILABLE_STATE_TRACKERS: Dict[str, Dict[str, Type[StateTracker]]] = {
    "runes_of_virtue_1": {
        "default": CoreRunesOfVirtue1Tracker,
        "open_menu_test": RunesOfVirtue1OpenMenuTestTracker,
    },
}
""" Mapping of game names to their available StateTracker classes with string identifiers. """

AVAILABLE_EMULATORS: Dict[str, Dict[str, Type[Emulator]]] = {
    "runes_of_virtue_1": {"default": Emulator},
}
""" Mapping of game names to their available Emulator classes with string identifiers. """
