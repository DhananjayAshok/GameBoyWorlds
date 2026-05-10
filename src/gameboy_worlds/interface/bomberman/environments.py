from gameboy_worlds.emulation.bomberman.trackers import (
    BombermanMaxTracker,
    BombermanPocketTracker,
    BombermanQuestTracker,
)
from gameboy_worlds.emulation.emulator import Emulator
from gameboy_worlds.interface.environment import DummyEnvironment, TestEnvironmentMixin


class BombermanMaxEnvironment(DummyEnvironment):
    REQUIRED_EMULATOR = Emulator
    REQUIRED_STATE_TRACKER = BombermanMaxTracker


class BombermanPocketEnvironment(DummyEnvironment):
    REQUIRED_EMULATOR = Emulator
    REQUIRED_STATE_TRACKER = BombermanPocketTracker


class BombermanQuestEnvironment(DummyEnvironment):
    REQUIRED_EMULATOR = Emulator
    REQUIRED_STATE_TRACKER = BombermanQuestTracker


class BombermanMaxTestEnvironment(TestEnvironmentMixin, BombermanMaxEnvironment):
    pass


class BombermanPocketTestEnvironment(TestEnvironmentMixin, BombermanPocketEnvironment):
    pass


class BombermanQuestTestEnvironment(TestEnvironmentMixin, BombermanQuestEnvironment):
    pass

