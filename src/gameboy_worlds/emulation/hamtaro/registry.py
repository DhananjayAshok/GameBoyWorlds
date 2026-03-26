from typing import Type, Dict

from gameboy_worlds.emulation.parser import StateParser
from gameboy_worlds.emulation.tracker import StateTracker
from gameboy_worlds.emulation.emulator import Emulator
from gameboy_worlds.emulation.hamtaro.parsers import (
    HamtaroHamHamsUniteParser,
)
from gameboy_worlds.emulation.hamtaro.trackers import HamtaroTracker
from gameboy_worlds.emulation.hamtaro.emulators import HamtaroEmulator


GAME_TO_GB_NAME = {
    "hamtaro_ham_hams_unite": "Hamtaro - Ham-Hams Unite! (USA).gbc",
}


STRONGEST_PARSERS: Dict[str, Type[StateParser]] = {
    "hamtaro_ham_hams_unite": HamtaroHamHamsUniteParser,
}


AVAILABLE_STATE_TRACKERS: Dict[str, Dict[str, Type[StateTracker]]] = {
    "hamtaro_ham_hams_unite": {"default": HamtaroTracker},
}


AVAILABLE_EMULATORS: Dict[str, Dict[str, Type[Emulator]]] = {
    "hamtaro_ham_hams_unite": {"default": HamtaroEmulator},
}
