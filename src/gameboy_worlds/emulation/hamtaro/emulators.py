from gameboy_worlds.emulation.emulator import Emulator
from gameboy_worlds.emulation.hamtaro.parsers import HamtaroStateParser
from gameboy_worlds.emulation.hamtaro.trackers import HamtaroTracker


class HamtaroEmulator(Emulator):
    """Minimal emulator scaffold for Hamtaro variants."""

    REQUIRED_STATE_PARSER = HamtaroStateParser
    REQUIRED_STATE_TRACKER = HamtaroTracker
