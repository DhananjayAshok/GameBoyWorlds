from typing import Dict, Type
from gameboy_worlds.interface.controller import Controller
from gameboy_worlds.interface.environment import Environment, DummyEnvironment
from gameboy_worlds.interface.sword_of_hope.environments import (
    SwordOfHope1TestEnvironment,
    SwordOfHope2TestEnvironment,
)


AVAILABLE_ENVIRONMENTS: Dict[str, Dict[str, Type[Environment]]] = {
    "sword_of_hope_1": {
        "dummy": DummyEnvironment,
        "default": DummyEnvironment,
        "test": SwordOfHope1TestEnvironment,
    },
    "sword_of_hope_2": {
        "dummy": DummyEnvironment,
        "default": DummyEnvironment,
        "test": SwordOfHope2TestEnvironment,
    },
}

AVAILABLE_CONTROLLERS: Dict[str, Dict[str, Type[Controller]]] = {}
