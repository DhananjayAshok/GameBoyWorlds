from typing import Dict, Type
from gameboy_worlds.emulation.parser import StateParser
from gameboy_worlds.emulation.tracker import StateTracker
from gameboy_worlds.emulation.emulator import Emulator
from gameboy_worlds.emulation.ultima.parsers import UltimaRunesOfVirtueParser
from gameboy_worlds.emulation.ultima.trackers import CoreUltimaTracker

GAME_TO_GB_NAME = {
    "ultima_runes_of_virtue": "UltimaRunesOfVirtue.gb",
}
""" Expected save name for each game. Save the file to <storage_dir_from_config_file>/<game_name>_rom_data/<gb_name>"""

STRONGEST_PARSERS: Dict[str, Type[StateParser]] = {
    "ultima_runes_of_virtue": UltimaRunesOfVirtueParser,
}
""" Mapping of game names to their corresponding strongest StateParser classes. """

AVAILABLE_STATE_TRACKERS: Dict[str, Dict[str, Type[StateTracker]]] = {
    "ultima_runes_of_virtue": {"default": CoreUltimaTracker},
}
""" Mapping of game names to their available StateTracker classes with string identifiers. """

AVAILABLE_EMULATORS: Dict[str, Dict[str, Type[Emulator]]] = {
    "ultima_runes_of_virtue": {"default": Emulator},
}
""" Mapping of game names to their available Emulator classes with string identifiers. """
