from typing import Dict, Type
from gameboy_worlds.interface.controller import Controller
from gameboy_worlds.interface.environment import Environment, DummyEnvironment
from gameboy_worlds.interface.pokemon.environments import (
    PokemonEnvironment,
    PokemonRedChooseCharmanderEnvironment,
    PokemonRedChooseCharmanderEasyEnvironment,
    PokemonRedChooseCharmanderHardEnvironment,
    PokemonOCREnvironment,
    PokemonTestEnvironment,
    PokemonTrainEnvironment,
)
from gameboy_worlds.interface.pokemon.controllers import PokemonStateWiseController

AVAILABLE_ENVIRONMENTS: Dict[str, Dict[str, Type[Environment]]] = {
    "pokemon_red": {
        "dummy": DummyEnvironment,
        "default": PokemonOCREnvironment,
        "basic": PokemonEnvironment,
        "charmander": PokemonRedChooseCharmanderEnvironment,
        "charmander_easy": PokemonRedChooseCharmanderEasyEnvironment,
        "charmander_hard": PokemonRedChooseCharmanderHardEnvironment,
        "train": PokemonTrainEnvironment,
        "test": PokemonTestEnvironment,
    },
    "pokemon_starbeasts": {
        "default": PokemonOCREnvironment,
        "basic": PokemonEnvironment,
        "train": PokemonTrainEnvironment,
        "test": PokemonTestEnvironment,
    },
    "pokemon_starbeasts_comet": {
        "default": PokemonOCREnvironment,
        "basic": PokemonEnvironment,
        "train": PokemonTrainEnvironment,
        "test": PokemonTestEnvironment,
    },
    "pokemon_crystal": {
        "default": PokemonOCREnvironment,
        "basic": PokemonEnvironment,
        "train": PokemonTrainEnvironment,
        "test": PokemonTestEnvironment,
    },
    "pokemon_fools_gold": {
        "default": PokemonOCREnvironment,
        "basic": PokemonEnvironment,
        "train": PokemonTrainEnvironment,
        "test": PokemonTestEnvironment,
    },
}

AVAILABLE_CONTROLLERS: Dict[str, Dict[str, Type[Controller]]] = {
    "pokemon_red": {
        "state_wise": PokemonStateWiseController,
    },
    "pokemon_crystal": {
        "state_wise": PokemonStateWiseController,
    },
    "pokemon_starbeasts": {
        "state_wise": PokemonStateWiseController,
    },
    "pokemon_starbeasts_comet": {
        "state_wise": PokemonStateWiseController,
    },
    "pokemon_fools_gold": {
        "state_wise": PokemonStateWiseController,
    },
}
