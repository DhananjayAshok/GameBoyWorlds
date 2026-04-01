from typing import Dict, Type
from gameboy_worlds.interface.controller import Controller
from gameboy_worlds.interface.environment import Environment, DummyEnvironment
from gameboy_worlds.interface.runes_of_virtue_1.environments import (
    RunesOfVirtue1Environment,
    RunesOfVirtue1TestEnvironment,
)


AVAILABLE_ENVIRONMENTS: Dict[str, Dict[str, Type[Environment]]] = {
    "runes_of_virtue_1": {
        "dummy": DummyEnvironment,
        "default": DummyEnvironment,
        "basic": RunesOfVirtue1Environment,
        "test": RunesOfVirtue1TestEnvironment,
    },
}

AVAILABLE_CONTROLLERS: Dict[str, Dict[str, Type[Controller]]] = {}
