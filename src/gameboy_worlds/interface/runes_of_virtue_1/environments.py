from gameboy_worlds.interface.environment import (
    DummyEnvironment,
    TestEnvironmentMixin,
)


class RunesOfVirtue1Environment(DummyEnvironment):
    """A basic Runes of Virtue 1 Environment."""

    pass


class RunesOfVirtue1TestEnvironment(TestEnvironmentMixin, RunesOfVirtue1Environment):
    """Test environment for Runes of Virtue 1 benchmark tasks."""

    pass
