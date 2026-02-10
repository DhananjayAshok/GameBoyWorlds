"""
Keeps a record of:
- Available `Controller`s for each game, with string identifiers. There is NO default controller for any game.
- Available `Environment`s for each game, with string identifiers and a default environment for each game.

Provides methods to access these.
"""

from typing import Dict, Type, Optional, Union, Mapping, List
from poke_worlds.utils import (
    log_error,
    load_parameters,
    log_warn,
    get_benchmark_tasks_df,
)
from poke_worlds.emulation.registry import (
    get_emulator,
    AVAILABLE_GAMES,
    infer_game,
    get_available_init_states,
)
from poke_worlds.interface.controller import Controller, _ALWAYS_VALID_CONTROLLERS
from poke_worlds.interface.environment import Environment, DummyEnvironment
from poke_worlds.interface.pokemon.environments import (
    PokemonEnvironment,
    PokemonRedChooseCharmanderEnvironment,
    PokemonOCREnvironment,
    PokemonRedExploreStartingSceneEnvironment,
    PokemonTestEnvironment,
)
from poke_worlds.interface.pokemon.controllers import PokemonStateWiseController

import pandas as pd
from gymnasium import register

_project_parameters = load_parameters()

AVAILABLE_ENVIRONMENTS: Dict[str, Dict[str, Type[Environment]]] = {
    "pokemon_red": {
        "dummy": DummyEnvironment,
        "default": PokemonOCREnvironment,
        "basic": PokemonEnvironment,
        "charmander": PokemonRedChooseCharmanderEnvironment,
        "starter_explore": PokemonRedExploreStartingSceneEnvironment,
        "test": PokemonTestEnvironment,
    },
    "pokemon_brown": {
        "default": PokemonOCREnvironment,
        "basic": PokemonEnvironment,
        "test": PokemonTestEnvironment,
    },
    "pokemon_starbeasts": {
        "default": PokemonOCREnvironment,
        "basic": PokemonEnvironment,
        "test": PokemonTestEnvironment,
    },
    "pokemon_crystal": {
        "default": PokemonOCREnvironment,
        "basic": PokemonEnvironment,
        "test": PokemonTestEnvironment,
    },
    "pokemon_prism": {
        "default": PokemonOCREnvironment,
        "basic": PokemonEnvironment,
        "test": PokemonTestEnvironment,
    },
    "pokemon_fools_gold": {
        "default": PokemonOCREnvironment,
        "basic": PokemonEnvironment,
        "test": PokemonTestEnvironment,
    },
    "legend_of_zelda": {
        "dummy": DummyEnvironment,
        "default": DummyEnvironment,
    },
}

AVAILABLE_CONTROLLERS: Dict[str, Dict[str, Type[Controller]]] = {
    "pokemon_red": {
        "state_wise": PokemonStateWiseController,
    },
    "pokemon_brown": {
        "state_wise": PokemonStateWiseController,
    },
    "pokemon_crystal": {
        "state_wise": PokemonStateWiseController,
    },
    "pokemon_starbeasts": {
        "state_wise": PokemonStateWiseController,
    },
    "pokemon_prism": {
        "state_wise": PokemonStateWiseController,
    },
    "pokemon_fools_gold": {
        "state_wise": PokemonStateWiseController,
    },
    "legend_of_zelda": {},
}

for game in AVAILABLE_GAMES:
    if game not in AVAILABLE_ENVIRONMENTS:
        log_warn(
            f"No environments registered for game variant '{game}'. Will error out if you try to get an environment for this game variant.",
            _project_parameters,
        )
    if game not in AVAILABLE_CONTROLLERS:
        log_warn(
            f"No controllers registered for game variant '{game}'. Will error out if you try to get a controller for this game variant.",
            _project_parameters,
        )
    else:
        for valid_controller_key in _ALWAYS_VALID_CONTROLLERS:
            if valid_controller_key in AVAILABLE_CONTROLLERS[game]:
                log_error(
                    f"Controller key '{valid_controller_key}' for game variant '{game}' is reserved for always valid controllers. Do not add a controller with this key in the registry.",
                    _project_parameters,
                )
            AVAILABLE_CONTROLLERS[game][valid_controller_key] = (
                _ALWAYS_VALID_CONTROLLERS[valid_controller_key]
            )


def get_controller(
    game: str,
    *,
    controller_variant: Union[str, Type[Controller], Controller],
    parameters: dict = None,
) -> Type[Controller]:
    """
    Factory function to get a Controller class for the specified game variant and controller variant.

    Args:
        game (str): The variant of the game to emulate.
        controller_variant (Union[str, Type[Controller], Controller]): The variant of the controller to create or the Controller class itself or an instance of Controller.
        parameters (dict, optional): Additional parameters for error logging.

    Returns:
        Controller: An instance of the requested Controller class.
    """
    parameters = load_parameters(parameters)
    game = infer_game(game, parameters)
    if game not in AVAILABLE_CONTROLLERS:
        log_error(f"No controllers registered for game variant '{game}'.", parameters)
    available_controllers = AVAILABLE_CONTROLLERS[game]
    if isinstance(controller_variant, str):
        if controller_variant not in available_controllers:
            log_error(
                f"Unsupported controller variant '{controller_variant}' for game variant '{game}'. Available variants are: {list(available_controllers.keys())}",
                parameters,
            )
        return available_controllers[controller_variant](parameters=parameters)
    available_variants = [cls for cls in available_controllers.values()]
    is_eqs = [controller_variant == cls for cls in available_variants]
    is_inst = [isinstance(controller_variant, cls) for cls in available_variants]
    if not any(is_eqs) and not any(is_inst):
        log_error(
            f"The provided controller_variant is not a registered Controller class for game variant '{game}'. Available variants are: {list(available_controllers.keys())}",
            parameters,
        )
    else:
        if any(is_inst):
            return controller_variant
        else:  # then it must be a class that matches one of the available variants
            return controller_variant(parameters=parameters)


def get_environment(
    game: str,
    *,
    environment_variant: str,
    controller_variant: Union[str, Type[Controller], Controller],
    parameters: dict = None,
    **emulator_kwargs,
) -> Environment:
    """
    Factory function to get an Environment instance for the specified game variant and environment variant.

    Args:
        game (str): The variant of the game to emulate.
        environment_variant (str): The variant of the environment to create.
        controller_variant (Union[str, Type[Controller], Controller]): The variant of the controller to create or the Controller class itself or an instance of Controller.
        parameters (dict, optional): Additional parameters for the environment and error logging. Must come from `load_parameters`.
        **emulator_kwargs: Additional keyword arguments passed to the `get_emulator` method.

    Returns:
        Environment: An instance of the requested Environment class.
    """
    parameters = load_parameters(parameters)
    game = infer_game(game, parameters)
    if game not in AVAILABLE_ENVIRONMENTS:
        log_error(f"No environments registered for game variant '{game}'.", parameters)
    available_environments = AVAILABLE_ENVIRONMENTS[game]
    if environment_variant not in available_environments:
        log_error(
            f"Unsupported environment variant '{environment_variant}' for game variant '{game}'. Available variants are: {list(available_environments.keys())}. Make sure to add your environment to the registry if you think this is a mistake.",
            parameters,
        )
    controller = get_controller(
        game, controller_variant=controller_variant, parameters=parameters
    )
    environment_class = available_environments[environment_variant]
    emulator_kwargs["game"] = game
    emulator_kwargs = environment_class.override_emulator_kwargs(emulator_kwargs)
    emulator = get_emulator(parameters=parameters, **emulator_kwargs)
    return environment_class(
        emulator=emulator, controller=controller, parameters=parameters
    )


def get_benchmark_tasks(game: str, parameters: dict = None) -> pd.DataFrame:
    """
    Loads the benchmark tasks for the specified game from the benchmark_tests/tasks.csv file

    Args:
        game (str): The variant of the game to get benchmark tasks for.
        parameters (dict, optional): Additional parameters for error logging.

    Returns:
        pd.DataFrame: DataFrame containing the benchmark tasks for the specified game.
    """
    parameters = load_parameters(parameters)
    tasks_df = get_benchmark_tasks_df(parameters)
    game_tasks_df = tasks_df[tasks_df["game"] == game]
    if len(game_tasks_df) == 0:
        log_error(
            f"No benchmark tasks found for game variant '{game}'. Please ensure that the tasks.csv file contains tasks for this game.",
            parameters,
        )
    return game_tasks_df


def get_test_environment(
    row: Mapping,
    controller_variant: Union[str, Type[Controller], Controller],
    parameters: dict = None,
    **emulator_kwargs,
) -> Environment:
    """
    Creates an Environment instance based on a row from the benchmark tasks / questions DataFrame.

    :param row: A row from the benchmark tasks / questions DataFrame.
    :type row: Mapping
    :param controller_variant: The variant of the controller to create or the Controller class itself or an instance of Controller.
    :type controller_variant: Union[str, Type[Controller], Controller]
    :param parameters: Additional parameters for error logging.
    :type parameters: dict, optional
    :param emulator_kwargs: Additional keyword arguments passed to the `get_emulator` method (e.g. `save_video`).
    :return: An instance of the requested Environment class.
    :rtype: Environment

    """
    parameters = load_parameters(parameters)
    return get_environment(
        game=row["game"],
        environment_variant="test",
        controller_variant=controller_variant,
        init_state=row["init_state"],
        state_tracker_class=row["state_tracker_class"],
        parameters=parameters,
        **emulator_kwargs,
    )


def get_training_environments_kwargs(
    row: Mapping,
    controller_variant: Union[str, Type[Controller], Controller],
    parameters: dict = None,
    **emulator_kwargs,
) -> List[Dict[str, str]]:
    """
    Creates a list of keyword arguments that can be passed into `get_environment` to create same-game training environments for the given benchmark task.
    This method does *not* return environments for the `shifted_environments` setting. For that, see `get_shifted_environments_kwargs`.

    :param row: A row from the benchmark tasks / questions DataFrame.
    :type row: Mapping
    :param controller_variant: Description
    :type controller_variant: Union[str, Type[Controller], Controller]
    :param parameters: Additional parameters for error logging.
    :type parameters: dict, optional
    :param emulator_kwargs: Additional keyword arguments passed to the `get_emulator` method (e.g. `save_video`).
    :return: A list of keyword argument dictionaries for creating training environments.
    :rtype: List[Dict[str, str]]
    """
    parameters = load_parameters(parameters)
    common_kwargs = {
        "game": row["game"],
        "controller_variant": controller_variant,
        "environment_variant": "default",
        "state_tracker_class": "default",
        **emulator_kwargs,
    }
    disallowed_init_states = [
        state.strip() for state in row["other_disallowed_states"].split(",")
    ] + [
        row["init_state"],
        "starter",
    ]  # TODO: I literally ONLY have this in here to avoid the agent going to options and messing up stuff. Fix properly later.
    training_envs_kwargs = []
    for init_state in get_available_init_states(row["game"]):
        if init_state not in disallowed_init_states and not init_state.startswith(
            "test_"
        ):
            env_kwargs = common_kwargs.copy()
            env_kwargs["init_state"] = init_state
            training_envs_kwargs.append(env_kwargs)
    if len(training_envs_kwargs) == 0:
        log_error(
            f"No available training environments found for benchmark task '{row['task_name']}' in game '{row['game']}'. Please ensure that there are available initial states for this game that are not in the disallowed states list.",
            parameters,
        )
    return training_envs_kwargs


def get_shifted_environments_kwargs(
    row: Mapping,
    controller_variant: Union[str, Type[Controller], Controller],
    parameters: dict = None,
    **emulator_kwargs,
) -> List[Dict[str, str]]:
    """
    Creates a list of keyword arguments that can be passed into `get_environment` to create shifted environments for the given benchmark task.
    For same-game training environments, see `get_training_environments_kwargs`.

    :param row: A row from the benchmark tasks / questions DataFrame.
    :type row: Mapping
    :param controller_variant: Description
    :type controller_variant: Union[str, Type[Controller], Controller]
    :param parameters: Additional parameters for error logging.
    :type parameters: dict, optional
    :param emulator_kwargs: Additional keyword arguments passed to the `get_emulator` method (e.g. `save_video`).
    :return: A list of keyword argument dictionaries for creating shifted environments.
    :rtype: List[Dict[str, str]]
    """
    parameters = load_parameters(parameters)
    common_kwargs = {
        "controller_variant": controller_variant,
        "environment_variant": "default",
        "state_tracker_class": "default",
        **emulator_kwargs,
    }
    allowed_games = [game.strip() for game in row["shifted_training_games"].split(",")]
    if row["game"] in allowed_games:
        allowed_games.remove(row["game"])
    disallowed_init_states = [
        state.strip() for state in row["other_disallowed_states"].split(",")
    ] + [
        row["init_state"],
        "starter",
    ]  # TODO: Same as above.
    shifted_envs_kwargs = []
    for game in allowed_games:
        for init_state in get_available_init_states(game):
            if init_state not in disallowed_init_states:
                env_kwargs = common_kwargs.copy()
                env_kwargs["game"] = game
                env_kwargs["init_state"] = init_state
                shifted_envs_kwargs.append(env_kwargs)
    if len(shifted_envs_kwargs) == 0:
        log_error(
            f"No available shifted environments found for benchmark task '{row['task_name']}' in games '{allowed_games}'. Please ensure that there are available initial states for these games that are not in the disallowed states list.",
            parameters,
        )
    return shifted_envs_kwargs
