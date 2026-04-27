"""
Keeps a record of:
- Available games
- Expected save file names for each game
- Strongest available `State Parser`s for each game
- Available `State Tracker`s for each game, with string identifiers and a default tracker for each game
- Available `Emulator`s for each game, with string identifiers and a default emulator for each game

Provides methods to access these.
"""

from gameboy_worlds.utils import (
    log_error,
    load_parameters,
    log_warn,
    get_benchmark_tasks,
)
import os
from typing import Optional, Union, Type, Dict
from gameboy_worlds.emulation.parser import StateParser, DummyParser
from gameboy_worlds.emulation.tracker import StateTracker
from gameboy_worlds.emulation.emulator import Emulator

from gameboy_worlds.emulation.pokemon import registry as pokemon_registry
from gameboy_worlds.emulation.legend_of_zelda import (
    registry as legend_of_zelda_registry,
)
from gameboy_worlds.emulation.hamtaro import registry as hamtaro_registry
from gameboy_worlds.emulation.sword_of_hope import registry as sword_of_hope_registry
from gameboy_worlds.emulation.deja_vu import registry as deja_vu_registry
from gameboy_worlds.emulation.harvest_moon import registry as harvest_moon_registry
from gameboy_worlds.emulation.runes_of_virtue import registry as runes_of_virtue_registry
from gameboy_worlds.emulation.harrypotter import registry as harrypotter_registry
from gameboy_worlds.emulation.bomberman import registry as bomberman_registry


_game_registries = [
    hamtaro_registry,
    pokemon_registry,
    legend_of_zelda_registry,
    sword_of_hope_registry,
    deja_vu_registry,
    harvest_moon_registry,
    runes_of_virtue_registry,
    harrypotter_registry,
    bomberman_registry,
]

_project_parameters = load_parameters()


def _merge_into_dict(destination: dict, incoming: dict):
    """
    Merges incoming into destination, throwing an error if there are any overlapping keys.

    Args:
        destination (dict): The destination dictionary.
        incoming (dict): The incoming dictionary.

    Returns:
        dict: The merged dictionary.
    """
    for key in incoming:
        if key in destination:
            log_error(
                f"Duplicate key '{key}' found when merging dictionaries. This likely means there is a duplicate entry for '{key}' in the registry. Please check the registry for duplicates and remove them.\nDictionaries being merged:\nDestination: {destination}\nIncoming: {incoming}",
                _project_parameters,
            )
    destination.update(incoming)


GAME_TO_GB_NAME: Dict[str, str] = {}
""" Expected save name for each game. Save the file to <storage_dir_from_config_file>/<game_name>_rom_data/<gb_name>"""

_STRONGEST_PARSERS: Dict[str, Type[StateParser]] = {}
""" Mapping of game names to their corresponding strongest StateParser classes. 
Unless you have a very good reason, you should always use the STRONGEST possible parser for a given game. 
The parser itself does not affect performance, as for it to perform a read / screen comparison operation , it must be called upon by the state tracker.
This means there is never a reason to use a weaker parser. 
"""

AVAILABLE_STATE_TRACKERS: Dict[str, Dict[str, Type[StateTracker]]] = {}
""" Mapping of game names to their available StateTracker classes with string identifiers. """

AVAILABLE_EMULATORS: Dict[str, Dict[str, Type[Emulator]]] = {}
""" Mapping of game names to their available Emulator classes with string identifiers. """

for module in _game_registries:
    if hasattr(module, "GAME_TO_GB_NAME"):
        _merge_into_dict(GAME_TO_GB_NAME, module.GAME_TO_GB_NAME)
    else:
        log_error(
            f"Module '{module.__name__}' is missing the GAME_TO_GB_NAME mapping. ",
            _project_parameters,
        )
    if hasattr(module, "STRONGEST_PARSERS"):
        _merge_into_dict(_STRONGEST_PARSERS, module.STRONGEST_PARSERS)
    else:
        log_error(
            f"Module '{module.__name__}' is missing the STRONGEST_PARSERS mapping. This mapping is required for the registry to function properly.",
            _project_parameters,
        )
    if hasattr(module, "AVAILABLE_STATE_TRACKERS"):
        _merge_into_dict(AVAILABLE_STATE_TRACKERS, module.AVAILABLE_STATE_TRACKERS)
    else:
        log_error(
            f"Module '{module.__name__}' is missing the AVAILABLE_STATE_TRACKERS mapping. This mapping is required for the registry to function properly.",
            _project_parameters,
        )
    if hasattr(module, "AVAILABLE_EMULATORS"):
        _merge_into_dict(AVAILABLE_EMULATORS, module.AVAILABLE_EMULATORS)
    else:
        log_error(
            f"Module '{module.__name__}' is missing the AVAILABLE_EMULATORS mapping. This mapping is required for the registry to function properly.",
            _project_parameters,
        )


for game in AVAILABLE_STATE_TRACKERS:
    if "default" not in AVAILABLE_STATE_TRACKERS[game]:
        log_error(
            f"Game '{game}' is missing a default StateTracker mapping in the registry.",
            _project_parameters,
        )

for game in AVAILABLE_EMULATORS:
    if "default" not in AVAILABLE_EMULATORS[game]:
        log_error(
            f"Game '{game}' is missing a default Emulator mapping in the registry.",
            _project_parameters,
        )

AVAILABLE_GAMES = list(GAME_TO_GB_NAME.keys())
""" List of available games. """

for game in AVAILABLE_GAMES:
    if game not in _STRONGEST_PARSERS:
        if _project_parameters["debug_mode"]:
            log_warn(
                f"Warning: Game '{game}' is missing a strongest StateParser mapping in the registry.",
                _project_parameters,
            )
        else:
            log_error(
                f"Game '{game}' is missing a strongest StateParser mapping in the registry.",
                _project_parameters,
            )
    if game not in AVAILABLE_STATE_TRACKERS:
        if _project_parameters["debug_mode"]:
            log_warn(
                f"Warning: Game '{game}' is missing a StateTracker mapping in the registry.",
                _project_parameters,
            )
        else:
            log_error(
                f"Game '{game}' is missing a StateTracker mapping in the registry.",
                _project_parameters,
            )
    if game not in AVAILABLE_EMULATORS:
        if _project_parameters["debug_mode"]:
            log_warn(
                f"Warning: Game '{game}' is missing an Emulator mapping in the registry.",
                _project_parameters,
            )
        else:
            log_error(
                f"Game '{game}' is missing an Emulator mapping in the registry.",
                _project_parameters,
            )


def infer_game(game: str, parameters: dict = None) -> str:
    """
    Try to infer the proper string identifier for a game given a possibly similar user input

    Example Usage:
    ```python
    inferred_game = infer_game("pokemon red", parameters)
    print(inferred_game)  # Output: "pokemon_red"
    ```
    Args:
        game (str): The game variant name to infer.
        parameters (dict): Additional parameters for logging.

    Returns:
        str: The inferred variant name.
    """
    parameters = load_parameters(parameters)
    game = game.strip().lower()
    game = game.replace(" ", "_").replace("-", "_")
    if game in AVAILABLE_GAMES:
        return game
    else:
        log_error(
            f"Could not infer game from '{game}'. Available games are: {AVAILABLE_GAMES}",
            parameters,
        )


def get_state_parser_class(
    game: str, parameters: Optional[dict] = None
) -> Type[StateParser]:
    """
    Factory method to get the strongest available StateParser class for a given game.

    Args:
        game (str): The game variant name (e.g., `pokemon_red`).
        parameters (dict, optional): Additional parameters for logging.
    Returns:
        Type[StateParser]: The StateParser class for the specified game.
    """
    parameters = load_parameters(parameters)
    game = infer_game(game, parameters=parameters)
    state_parser_class = _STRONGEST_PARSERS.get(game, None)
    if state_parser_class is None:
        log_error(
            f"There is no StateParser for game '{game}' in the registry.", parameters
        )
    return state_parser_class


def get_state_tracker_class(
    game: str,
    tracker_variant: Union[str, Type[StateTracker]] = "default",
    parameters: Optional[dict] = None,
) -> Type[StateTracker]:
    """
    Factory method to get a StateTracker class for a given game and tracker variant.
    Args:
        game (str): The game variant name (e.g., `pokemon_red`).
        tracker_variant (Union[str, Type[StateTracker]]): The variant of the state tracker to use. Can either be a StateTracker class (in which case it is returned directly), or a string identifier for the tracker variant (e.g., `default`).
        parameters (dict, optional): Additional parameters for logging.

    Returns:
        Type[StateTracker]: The StateTracker class for the specified game and variant.
    """
    parameters = load_parameters(parameters)
    game = infer_game(game, parameters=parameters)
    available_trackers = AVAILABLE_STATE_TRACKERS.get(game, None)
    if available_trackers is None:
        log_error(
            f"There are no available StateTrackers for game '{game}' in the registry.",
            parameters,
        )
    if isinstance(tracker_variant, str):
        if tracker_variant not in available_trackers:
            log_error(
                f"StateTracker variant '{tracker_variant}' is not available for game '{game}'. Available variants are: {list(available_trackers.keys())}",
                parameters,
            )
        return available_trackers[tracker_variant]
    elif issubclass(tracker_variant, StateTracker):
        # just verify that the tracker is available for this game
        if tracker_variant not in available_trackers.values():
            log_error(
                f"StateTracker class '{tracker_variant.__name__}' is not registered as an allowed tracker for game '{game}'. Available variants are: {list(available_trackers.keys())}",
                parameters,
            )
        return tracker_variant
    else:
        log_error(
            f"tracker_variant must either be a string identifier or a StateTracker class. Got '{type(tracker_variant)}' instead.",
            parameters,
        )


def get_emulator_class(
    game: str,
    emulator_variant: Union[str, Type[Emulator]] = "default",
    parameters: Optional[dict] = None,
) -> Type[Emulator]:
    """
    Factory method to get an Emulator class for a given game and emulator variant.

    Args:
        game (str): The game variant name (e.g., `pokemon_red`).
        emulator_variant (Union[str, Type[Emulator]]): The variant of the emulator to use. Can either be an Emulator class (in which case it is returned directly), or a string identifier for the emulator variant (e.g., `default`).
        parameters (dict, optional): Additional parameters for logging.

    Returns:
        Type[Emulator]: The Emulator class for the specified game and variant.
    """
    parameters = load_parameters(parameters)
    game = infer_game(game, parameters=parameters)
    available_emulators = AVAILABLE_EMULATORS.get(game, None)
    if available_emulators is None:
        log_error(
            f"There are no available Emulators for game '{game}' in the registry.",
            parameters,
        )
    if isinstance(emulator_variant, str):
        if emulator_variant not in available_emulators:
            log_error(
                f"Emulator variant '{emulator_variant}' is not available for game '{game}'. Available variants are: {list(available_emulators.keys())}",
                parameters,
            )
        return available_emulators[emulator_variant]
    elif issubclass(emulator_variant, Emulator):
        # just verify that the emulator is available for this game
        if emulator_variant not in available_emulators.values():
            log_error(
                f"Emulator class '{emulator_variant.__name__}' is not registered as an allowed emulator for game '{game}'. Available variants are: {list(available_emulators.keys())}",
                parameters,
            )
        return emulator_variant
    else:
        log_error(
            f"emulator_variant must either be a string identifier or an Emulator class. Got '{type(emulator_variant)}' instead.",
            parameters,
        )


def get_emulator(
    game: str,
    *,
    parameters: Optional[dict] = None,
    init_state: str = None,
    state_tracker_class: Union[str, Type[StateTracker]] = "default",
    **emulator_kwargs,
) -> Emulator:
    """
    Factory method to get a Pokemon emulator instance based on the specified variant.
    Args:
        game (str): The variant of the Pokemon game (e.g., `pokemon_red`, `pokemon_crystal`).
        parameters (dict, optional): Additional parameters for emulator configuration.
        init_state_name (str, optional): Name of the initial state file to load (not the path).
        state_tracker_class (Union[str, Type[StateTracker]]): The string identifier variant of the state tracker to use, or the class itself.
        **emulator_kwargs: Additional keyword arguments to pass to the `Emulator` constructor (e.g. `headless`)
    Returns:
        Emulator: An instance of the Emulator class configured for the specified variant.
    """
    parameters = load_parameters(parameters)
    game = infer_game(game, parameters=parameters)
    if f"{game}_rom_data_path" not in parameters:
        log_error(
            f"ROM data path for game '{game}' is not specified in the parameters under key '{game}_rom_data_path'.",
            parameters,
        )
    gb_path = parameters[f"{game}_rom_data_path"] + "/" + GAME_TO_GB_NAME[game]
    if init_state is not None:
        if not init_state.endswith(".state"):
            init_state = init_state + ".state"
        init_state = parameters[f"{game}_rom_data_path"] + "/states/" + init_state
    else:
        init_state = parameters[f"{game}_rom_data_path"] + "/states/default.state"
    state_parser_class = get_state_parser_class(game, parameters=parameters)
    state_tracker_class: Type[StateTracker] = get_state_tracker_class(
        game, tracker_variant=state_tracker_class, parameters=parameters
    )
    emulator_class = get_emulator_class(game, parameters=parameters)
    emulator = emulator_class(
        game=game,
        gb_path=gb_path,
        init_state=init_state,
        state_parser_class=state_parser_class,
        state_tracker_class=state_tracker_class,
        parameters=parameters,
        **emulator_kwargs,
    )
    return emulator


def get_available_init_states(game: str, parameters: Optional[dict] = None) -> list:
    """
    Returns a list of available initial state names for the specified game.

    Args:
        game (str): The variant of the Pokemon game (e.g., `pokemon_red`, `pokemon_crystal`).
        parameters (dict, optional): Additional parameters for configuration.

    Returns:
        list: A list of available initial state names (without .state extension).
    """
    parameters = load_parameters(parameters)
    game = infer_game(game, parameters=parameters)
    if f"{game}_rom_data_path" not in parameters:
        log_error(
            f"ROM data path for game '{game}' is not specified in the parameters under key '{game}_rom_data_path'.",
            parameters,
        )
    states_dir = parameters[f"{game}_rom_data_path"] + "/states/"
    if not os.path.exists(states_dir):
        log_error(
            f"States directory '{states_dir}' does not exist for game '{game}'.",
            parameters,
        )
    state_names = [
        f.replace(".state", "") for f in os.listdir(states_dir) if f.endswith(".state")
    ]
    return state_names


def get_train_init_states(game: str, parameters: Optional[dict] = None) -> list:
    """
    Returns a list of allowed initial states for training agents to play the specified game.
    This is determined based on the benchmark tasks specified for the game - any state that is a test state for a benchmark task is disallowed as a training initial state.

    Args:
        game (str): The variant of the Pokemon game (e.g., `pokemon_red`, `pokemon_crystal`).
        parameters (dict, optional): Additional parameters for configuration.

    Returns:
        list: A list of available initial state names (without .state extension) that can be used for training.
    """
    parameters = load_parameters(parameters)
    benchmark_tasks_df = get_benchmark_tasks(game, parameters=parameters)
    test_init_states = benchmark_tasks_df["init_state"].unique().tolist()
    other_disallowed_states = []
    for i, row in benchmark_tasks_df.iterrows():
        others = row["other_disallowed_states"]
        if others and isinstance(others, str):
            other_disallowed_states.extend(others.split(","))
    test_init_states.extend(other_disallowed_states)
    test_init_states = list(set(test_init_states))
    available_init_states = get_available_init_states(game, parameters=parameters)
    train_init_states = []
    for state in available_init_states:
        if (
            state in test_init_states
            or state.startswith("test_")
            or "_test_" in state
            or state.endswith("_test")
            or state == "test"
        ):
            continue
        train_init_states.append(state)
    if len(train_init_states) == 0:
        if parameters["debug_mode"]:
            log_warn(
                f"No available training initial states found for game '{game}' after filtering out test states. Returning all available initial states for now, but you should add some training states that are not used as test states or other_disallowed_states in the benchmark tasks.",
                parameters,
            )
            return available_init_states
        else:
            log_error(
                f"No available training initial states found for game '{game}' after filtering out test states. Please ensure that there are some initial states available for training that are not used as test states or other_disallowed_states in the benchmark tasks.",
                parameters,
            )
    return train_init_states
