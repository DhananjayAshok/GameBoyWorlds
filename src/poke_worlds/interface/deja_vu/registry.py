from typing import Dict, Type
from poke_worlds.interface.controller import Controller
from poke_worlds.interface.deja_vu.controllers import DejaVuStateWiseController
from poke_worlds.interface.deja_vu.environments import (
    DejaVuEnvironment,
    DejaVuOCREnvironment,
    DejaVuTestEnvironment,
)
from poke_worlds.interface.environment import Environment, DummyEnvironment


AVAILABLE_ENVIRONMENTS: Dict[str, Dict[str, Type[Environment]]] = {
    "deja_vu_1": {
        "dummy": DummyEnvironment,
        "default": DejaVuOCREnvironment,
        "basic": DejaVuEnvironment,
        "test": DejaVuTestEnvironment,
    },
    "deja_vu_2": {
        "dummy": DummyEnvironment,
        "default": DummyEnvironment,
    },
}

AVAILABLE_CONTROLLERS: Dict[str, Dict[str, Type[Controller]]] = {
    "state_wise": DejaVuStateWiseController,
}
