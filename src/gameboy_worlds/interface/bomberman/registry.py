from typing import Dict, Type

from gameboy_worlds.interface.bomberman.controllers import (
    BombermanMaxStateWiseController,
    BombermanPocketStateWiseController,
    BombermanQuestStateWiseController,
)
from gameboy_worlds.interface.bomberman.environments import (
    BombermanMaxEnvironment,
    BombermanMaxTestEnvironment,
    BombermanPocketEnvironment,
    BombermanPocketTestEnvironment,
    BombermanQuestEnvironment,
    BombermanQuestTestEnvironment,
)
from gameboy_worlds.interface.controller import Controller
from gameboy_worlds.interface.environment import DummyEnvironment, Environment


AVAILABLE_ENVIRONMENTS: Dict[str, Dict[str, Type[Environment]]] = {
    "bomberman_max": {
        "dummy": DummyEnvironment,
        "default": BombermanMaxEnvironment,
        "test": BombermanMaxTestEnvironment,
    },
    "bomberman_pocket": {
        "dummy": DummyEnvironment,
        "default": BombermanPocketEnvironment,
        "test": BombermanPocketTestEnvironment,
    },
    "bomberman_quest": {
        "dummy": DummyEnvironment,
        "default": BombermanQuestEnvironment,
        "test": BombermanQuestTestEnvironment,
    },
}

AVAILABLE_CONTROLLERS: Dict[str, Dict[str, Type[Controller]]] = {
    "bomberman_max": {
        "state_wise": BombermanMaxStateWiseController,
    },
    "bomberman_pocket": {
        "state_wise": BombermanPocketStateWiseController,
    },
    "bomberman_quest": {
        "state_wise": BombermanQuestStateWiseController,
    },
}
