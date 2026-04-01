from typing import Dict, Type
from gameboy_worlds.interface.controller import Controller
from gameboy_worlds.interface.environment import Environment, DummyEnvironment
from gameboy_worlds.interface.legend_of_zelda.environments import (
    LegendOfZeldaEnvironment,
    LegendOfZeldaTestEnvironment,
)

AVAILABLE_ENVIRONMENTS: Dict[str, Dict[str, Type[Environment]]] = {
    "legend_of_zelda_links_awakening": {
        "dummy": DummyEnvironment,
        "default": DummyEnvironment,
        "test": LegendOfZeldaTestEnvironment,
    },
    "legend_of_zelda_the_oracle_of_seasons": {
        "dummy": DummyEnvironment,
        "default": DummyEnvironment,
        "test": LegendOfZeldaTestEnvironment,
    },
}

AVAILABLE_CONTROLLERS: Dict[str, Dict[str, Type[Controller]]] = {}
