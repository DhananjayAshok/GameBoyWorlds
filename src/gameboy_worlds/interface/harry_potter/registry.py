from typing import Dict, Type
from gameboy_worlds.interface.controller import Controller
from gameboy_worlds.interface.environment import Environment, DummyEnvironment
from gameboy_worlds.interface.harry_potter.environments import (
    HarryPotterTestEnvironment,
)


AVAILABLE_ENVIRONMENTS: Dict[str, Dict[str, Type[Environment]]] = {
    "harry_potter_philosophers_stone": {
        "dummy": DummyEnvironment,
        "default": DummyEnvironment,
        "test": HarryPotterTestEnvironment,
    },
    "harry_potter_chamber_of_secrets": {
        "dummy": DummyEnvironment,
        "default": DummyEnvironment,
        "test": HarryPotterTestEnvironment,
    },
}

AVAILABLE_CONTROLLERS: Dict[str, Dict[str, Type[Controller]]] = {}
