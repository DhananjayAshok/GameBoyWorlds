from gameboy_worlds.emulation.runes_of_virtue.emulators import RunesOfVirtueEmulator
from gameboy_worlds.emulation.runes_of_virtue.trackers import (
    CoreRunesOfVirtueTracker,
    RunesOfVirtueOCRTracker,
)
from gameboy_worlds.interface.environment import (
    DummyEnvironment,
    Environment,
    TestEnvironmentMixin,
    TrainEnvironmentMixin,
)


class RunesOfVirtueEnvironment(DummyEnvironment):
    """
    A basic Runes of Virtue Environment.
    """

    REQUIRED_EMULATOR = RunesOfVirtueEmulator
    REQUIRED_STATE_TRACKER = CoreRunesOfVirtueTracker


class RunesOfVirtueOCREnvironment(RunesOfVirtueEnvironment):
    """
    A Runes of Virtue Environment that includes OCR region captures and agent state.
    """

    REQUIRED_STATE_TRACKER = RunesOfVirtueOCRTracker
    REQUIRED_EMULATOR = RunesOfVirtueEmulator

    @staticmethod
    def override_emulator_kwargs(emulator_kwargs: dict) -> dict:
        Environment.override_state_tracker_class(
            emulator_kwargs, RunesOfVirtueOCREnvironment.REQUIRED_STATE_TRACKER
        )
        return emulator_kwargs


class RunesOfVirtueTestEnvironment(TestEnvironmentMixin, RunesOfVirtueOCREnvironment):
    pass


class RunesOfVirtueTrainEnvironment(TrainEnvironmentMixin, RunesOfVirtueOCREnvironment):
    pass
