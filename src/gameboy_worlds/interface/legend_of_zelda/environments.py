from gameboy_worlds.emulation.legend_of_zelda.trackers import (
    CoreLegendOfZeldaTracker,
)
from gameboy_worlds.interface.environment import (
    DummyEnvironment,
    TestEnvironmentMixin,
)


class LegendOfZeldaEnvironment(DummyEnvironment):
    REQUIRED_STATE_TRACKER = CoreLegendOfZeldaTracker


class LegendOfZeldaTestEnvironment(TestEnvironmentMixin, LegendOfZeldaEnvironment):
    pass
