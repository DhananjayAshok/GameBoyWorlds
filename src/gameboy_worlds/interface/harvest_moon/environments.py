from typing import Optional, Dict, Any, List, Tuple

from gymnasium import spaces

from gameboy_worlds.emulation.harvest_moon.base_metrics import CoreHarvestMoonMetrics
from gameboy_worlds.utils import load_parameters, log_dict, log_info
from gameboy_worlds.emulation.emulator import Emulator
from gameboy_worlds.emulation.harvest_moon.trackers import (
    CoreHarvestMoonTracker,
    HarvestMoonOCRTracker,
)
from gameboy_worlds.interface.environment import (
    DummyEnvironment,
    Environment,
    TestEnvironmentMixin,
    TrainEnvironmentMixin,
)
from gameboy_worlds.interface.controller import Controller

import gymnasium as gym
import numpy as np


class HarvestMoonEnvironment(DummyEnvironment):
    """
    A basic Harvest Moon Environment.
    """

    REQUIRED_EMULATOR = Emulator
    REQUIRED_STATE_TRACKER = CoreHarvestMoonMetrics


class HarvestMoonOCREnvironment(HarvestMoonEnvironment):
    """
    A Harvest Moon Environment that includes OCR region captures and agent state.
    """

    REQUIRED_STATE_TRACKER = HarvestMoonOCRTracker
    REQUIRED_EMULATOR = Emulator

    @staticmethod
    def override_emulator_kwargs(emulator_kwargs: dict) -> dict:
        Environment.override_state_tracker_class(
            emulator_kwargs, HarvestMoonOCREnvironment.REQUIRED_STATE_TRACKER
        )
        return emulator_kwargs


class HarvestMoonTestEnvironment(TestEnvironmentMixin, HarvestMoonOCREnvironment):
    pass


class HarvestMoonTrainEnvironment(TrainEnvironmentMixin, HarvestMoonOCREnvironment):
    pass
