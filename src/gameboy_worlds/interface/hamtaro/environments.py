
from gameboy_worlds.interface.environment import DummyEnvironment
from gameboy_worlds.emulation.hamtaro import HamtaroEmulator
from gameboy_worlds.emulation.hamtaro.trackers import HamtaroTracker

class HamtaroEnvironment(DummyEnvironment):
    """
    A basic Hamtaro Environment.
    """

    REQUIRED_EMULATOR = HamtaroEmulator
    REQUIRED_STATE_TRACKER = HamtaroTracker


