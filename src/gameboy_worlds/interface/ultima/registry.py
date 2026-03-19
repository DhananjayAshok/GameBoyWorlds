from typing import Dict, Type
from gameboy_worlds.interface.controller import Controller
from gameboy_worlds.interface.environment import Environment, DummyEnvironment


AVAILABLE_ENVIRONMENTS: Dict[str, Dict[str, Type[Environment]]] = {
    "ultima_runes_of_virtue": {
        "dummy": DummyEnvironment,
        "default": DummyEnvironment,
    },
}

AVAILABLE_CONTROLLERS: Dict[str, Dict[str, Type[Controller]]] = {}
