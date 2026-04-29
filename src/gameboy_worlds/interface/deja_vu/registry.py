from typing import Dict, Type
from gameboy_worlds.interface.controller import Controller
from gameboy_worlds.interface.deja_vu.controllers import DejaVuStateWiseController
from gameboy_worlds.interface.deja_vu.environments import (
    DejaVuEnvironment,
    DejaVuOCREnvironment,
    DejaVuTestEnvironment,
)
from gameboy_worlds.interface.environment import Environment, DummyEnvironment


AVAILABLE_ENVIRONMENTS: Dict[str, Dict[str, Type[Environment]]] = {
    "deja_vu_1": {
        "dummy": DummyEnvironment,
        "default": DejaVuOCREnvironment,
        "basic": DejaVuEnvironment,
        "test": DejaVuTestEnvironment,
    },
    "deja_vu_2": {
        "dummy": DummyEnvironment,
        "default": DejaVuOCREnvironment,
        "basic": DejaVuEnvironment,
        "test": DejaVuTestEnvironment,
    },
}

AVAILABLE_CONTROLLERS: Dict[str, Dict[str, Type[Controller]]] = {
    "state_wise": DejaVuStateWiseController,
}
