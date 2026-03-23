from typing import Dict, Type
from gameboy_worlds.interface.controller import Controller
from gameboy_worlds.interface.environment import Environment, DummyEnvironment
from gameboy_worlds.interface.harrypotter.environments import (
    HarryPotterTestEnvironment,
)


AVAILABLE_ENVIRONMENTS: Dict[str, Dict[str, Type[Environment]]] = {
    "harrypotter_philosophersstone": {
        "dummy": DummyEnvironment,
        "default": DummyEnvironment,
        "test": HarryPotterTestEnvironment,
    },
}

AVAILABLE_CONTROLLERS: Dict[str, Dict[str, Type[Controller]]] = {}
