from typing import Dict, Type
from gameboy_worlds.interface.controller import Controller
from gameboy_worlds.interface.environment import Environment, DummyEnvironment
from gameboy_worlds.interface.harvest_moon.environments import (
    HarvestMoonEnvironment,
    HarvestMoonOCREnvironment,
    HarvestMoonTestEnvironment,
    HarvestMoonTrainEnvironment,
)
from gameboy_worlds.interface.harvest_moon.controllers import HarvestMoonStateWiseController

AVAILABLE_ENVIRONMENTS: Dict[str, Dict[str, Type[Environment]]] = {
    "harvest_moon_1":{
        "dummy": DummyEnvironment,
        "default": HarvestMoonOCREnvironment,
        "basic": HarvestMoonEnvironment,
        "train": HarvestMoonTrainEnvironment,
        "test": HarvestMoonTestEnvironment,
    },
    "harvest_moon_2":{
        "default": HarvestMoonOCREnvironment,
        "basic": HarvestMoonEnvironment,
        "train": HarvestMoonTrainEnvironment,
        "test": HarvestMoonTestEnvironment,
    },
    "harvest_moon_3":{
        "default": HarvestMoonOCREnvironment,
        "basic": HarvestMoonEnvironment,
        "train": HarvestMoonTrainEnvironment,
        "test": HarvestMoonTestEnvironment,
    },
}

AVAILABLE_CONTROLLERS: Dict[str, Dict[str, Type[Controller]]] = {
    "harvest_moon_1": {
        "state_wise": HarvestMoonStateWiseController,
    },
    "harvest_moon_2": {
        "state_wise": HarvestMoonStateWiseController,
    },
    "harvest_moon_3": {
        "state_wise": HarvestMoonStateWiseController,
    },
}
