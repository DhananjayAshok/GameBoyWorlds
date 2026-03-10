from typing import Dict, Type
from poke_worlds.interface.controller import Controller
from poke_worlds.interface.environment import Environment, DummyEnvironment


AVAILABLE_ENVIRONMENTS: Dict[str, Dict[str, Type[Environment]]] = {
    "legend_of_zelda_links_awakening" :{
        "dummy": DummyEnvironment,
        "default": DummyEnvironment,
    },
    "legend_of_zelda_oracle_of_seasons" :{
        "dummy": DummyEnvironment,
        "default": DummyEnvironment,
    } 
}

AVAILABLE_CONTROLLERS: Dict[str, Dict[str, Type[Controller]]] = {}
