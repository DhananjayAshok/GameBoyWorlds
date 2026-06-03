from typing import Dict, Type

from gameboy_worlds.interface.controller import Controller
from gameboy_worlds.interface.environment import DummyEnvironment, Environment
from gameboy_worlds.interface.runes_of_virtue.controllers import (
    RunesOfVirtueStateWiseController,
)
from gameboy_worlds.interface.runes_of_virtue.environments import (
    RunesOfVirtueEnvironment,
    RunesOfVirtueOCREnvironment,
    RunesOfVirtueTestEnvironment,
    RunesOfVirtueTrainEnvironment,
)


AVAILABLE_ENVIRONMENTS: Dict[str, Dict[str, Type[Environment]]] = {
    "runes_of_virtue_1": {
        "dummy": DummyEnvironment,
        "default": RunesOfVirtueOCREnvironment,
        "basic": RunesOfVirtueEnvironment,
        "ocr": RunesOfVirtueOCREnvironment,
        "train": RunesOfVirtueTrainEnvironment,
        "test": RunesOfVirtueTestEnvironment,
    },
    "runes_of_virtue_2": {
        "dummy": DummyEnvironment,
        "default": RunesOfVirtueOCREnvironment,
        "basic": RunesOfVirtueEnvironment,
        "ocr": RunesOfVirtueOCREnvironment,
        "train": RunesOfVirtueTrainEnvironment,
        "test": RunesOfVirtueTestEnvironment,
    },
}


AVAILABLE_CONTROLLERS: Dict[str, Dict[str, Type[Controller]]] = {
    "runes_of_virtue_1": {
        "state_wise": RunesOfVirtueStateWiseController,
    },
    "runes_of_virtue_2": {
        "state_wise": RunesOfVirtueStateWiseController,
    },
}
