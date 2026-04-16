# These are all the utils functions or classes that you may want to import in your project
from gameboy_worlds.utils.parameter_handling import load_parameters
from gameboy_worlds.utils.log_handling import log_error, log_info, log_warn, log_dict
from gameboy_worlds.utils.fundamental import file_makedir, check_optional_installs
from pandas import isna
from typing import Type, List
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
from time import perf_counter_ns


def import_cv2(parameters: dict = None):
    """
    Import cv2 lazily so headless runs without video writing do not load extra SDL libraries.
    """
    try:
        import cv2
    except ImportError:
        log_error(
            "OpenCV (cv2) is required for emulator video recording utilities.",
            parameters,
        )
    return cv2


def import_pygame(parameters: dict):
    """
    Import pygame lazily so headless runs don't pull in SDL unless rendering is requested.
    """
    try:
        import pygame
    except ImportError:
        log_error(
            "pygame is required for render() / human play display. Install pygame or run without render.",
            parameters,
        )
    return pygame


def is_none_str(s) -> bool:
    """
    Checks if a string is None or represents a null value.

    Args:
        s (str or None): The string to check.

    Returns:
        bool: True if the string is None or represents a null value, False otherwise.
    """
    if s is None:
        return True
    if isinstance(s, str):
        options = ["none", "null", "nan", ""]
        for option in options:
            if s.lower() == option:
                return True
    return isna(s)


def nested_dict_to_str(
    nested_dict: dict, *, indent: int = 0, indent_char: str = "  "
) -> str:
    """
    Converts a nested dictionary to a formatted string representation.
    Example Usage:
    ```python
    nested_dict={2: 4, 3: {4: 5, 6: {7: 8}}}
    print(nested_dict_to_str(nested_dict))
    2: 4
    3: Dict:
      4: 5
      6: Dict:
        7: 8
    ```

    Args:
        nested_dict (dict): The nested dictionary to convert.
        indent (int): The current indentation level.
        indent_char (str): The character(s) used for indentation.
    Returns:
        str: A formatted string representation of the nested dictionary.

    """
    result = ""
    for key, value in nested_dict.items():
        result += indent_char * indent + str(key) + ": "
        if isinstance(value, dict):
            result += "Dict: \n" + nested_dict_to_str(
                value, indent + 1, indent_char=indent_char
            )
        else:
            result += str(value) + "\n"
    return result


def verify_parameters(parameters: dict):
    """
    Does a basic sanity check to ensure parameters is a non-empty dictionary.
    """
    if parameters is None:
        raise ValueError("Parameters cannot be None.")
    if not isinstance(parameters, dict):
        raise ValueError("Parameters must be a dictionary.")
    if len(parameters) == 0:
        raise ValueError("Parameters dictionary cannot be empty.")


def get_lowest_level_subclass(class_list: List[Type]) -> Type:
    """
    Given a list of classes, returns the class that is the lowest level subclass in the inheritance hierarchy.
    """
    lowest_level_tracker = None
    for cls in class_list:
        if lowest_level_tracker is None:
            lowest_level_tracker = cls
        elif issubclass(cls, lowest_level_tracker):
            lowest_level_tracker = cls
    return lowest_level_tracker


def show_frames(
    frames: np.ndarray, titles: List[str] = None, save=False, parameters: dict = None
):
    """
    Plots each frame as an image in matplotlib. If save is true, will save each frame as title.png in the frame_saves/ directory.
    titles length must be equal to frame length if specified.
    """
    parameters = load_parameters(parameters)
    if isinstance(frames, list):
        for i in range(len(frames)):
            if frames[i].ndim == 2:
                frames[i] = np.expand_dims(frames[i], axis=-1)
    else:
        if not isinstance(frames, np.ndarray):
            log_error(
                f"Frames must be a numpy array or list of numpy arrays, but got {type(frames)}",
                parameters,
            )
        if frames.ndim == 2:
            frames = [np.expand_dims(frames, axis=-1)]
        elif frames.ndim == 3:
            # now either we have (num_frames, height, width) or (height, width, channels)
            if frames.shape[2] == 1:
                frames = [frames]
            else:
                frames = [
                    np.expand_dims(frames[i], axis=-1) for i in range(frames.shape[0])
                ]
    if isinstance(titles, str):
        titles = [titles]
    if save:
        if titles is None:
            log_error(f"Cannot save frames without titles specified.", parameters)
    if titles is not None:
        if len(titles) == 1 and len(frames) > 1:
            titles = [titles[0] + f"_{i}" for i in range(len(frames))]
    if titles is not None and len(titles) != len(frames):
        log_error(
            f"Length of titles {len(titles)} does not match number of frames {len(frames)}",
            parameters,
        )
    save_dir = "frame_saves/"
    os.makedirs(save_dir, exist_ok=True)

    for i in range(len(frames)):
        plt.imshow(frames[i])
        if titles is not None:
            plt.title(titles[i])
        if save:
            filename = os.path.join(
                save_dir, titles[i].replace(" ", "_").replace("/", "_") + ".png"
            )
            plt.imsave(filename, frames[i][:, :, 0], cmap="gray")
        else:
            plt.show()


def get_benchmark_tasks_dfs(parameters: dict = None) -> dict[str, pd.DataFrame]:
    """
    Loads the benchmark tasks from the benchmark_tests/tasks.csv file

    Args:
        parameters (dict, optional): Additional parameters for error logging.
    Returns:
        dict[str, pd.DataFrame]: A dictionary mapping game names to their corresponding DataFrames containing the benchmark tasks.
    """
    parameters = load_parameters(parameters)
    project_root = parameters["project_root"]
    module_paths = os.listdir(project_root + "/benchmark_tests/")
    benchmark_dfs = {}
    for module_path in module_paths:
        if module_path.endswith(".csv"):
            tasks_filepath = os.path.join(project_root, "benchmark_tests", module_path)
            benchmark_name = module_path.strip(".csv")
            benchmark_dfs[benchmark_name] = pd.read_csv(tasks_filepath)
    return benchmark_dfs


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
    tasks_dfs = get_benchmark_tasks_dfs(parameters)
    available_games = set()
    task_df = None
    for benchmark_name, df in tasks_dfs.items():
        available_games.update(set(df["game"].unique()))
        if game in df["game"].unique():
            if task_df is not None:
                log_error(
                    f"Multiple benchmark modules contain tasks for game variant '{game}'. Please ensure that only one benchmark CSV file contains tasks for this game.",
                    parameters,
                )
            task_df = df

    if game not in available_games:
        log_error(
            f"Game variant '{game}' not found in benchmark tasks. Available game variants: {available_games}",
            parameters=parameters,
        )
    game_tasks_df = task_df[task_df["game"] == game]
    if len(game_tasks_df) == 0:
        log_error(
            f"No benchmark tasks found for game variant '{game}'. Please ensure that the benchmark_tests/tasks.csv file contains tasks for this game.",
            parameters,
        )
    return game_tasks_df


class _Profiler:
    """
    A simple profiler class to track the time taken by different events in the code. It can also group events together and show the percentage of time taken by each event in the group.
    """

    LOG_EVENTS = False
    last_event_time = None
    last_event = None
    group = None
    group_name = None

    @staticmethod
    def event(event_name):
        current_time = perf_counter_ns()
        if _Profiler.last_event_time is not None:
            elapsed_time = current_time - _Profiler.last_event_time
            if _Profiler.LOG_EVENTS:
                log_info(
                    f"{_Profiler.last_event} -> {event_name}: {elapsed_time / 1e6:.2f} ms",
                )
        _Profiler.last_event_time = current_time
        _Profiler.last_event = event_name
        if _Profiler.group_name is not None:
            _Profiler.group.append((event_name, current_time))

    @staticmethod
    def start_group(group_name):
        if _Profiler.group_name is not None:
            fractions = []
            total_time = 0
            for i in range(1, len(_Profiler.group)):
                event_name, event_time = _Profiler.group[i]
                prev_event_name, prev_event_time = _Profiler.group[i - 1]
                elapsed_time = event_time - prev_event_time
                total_time += elapsed_time
            for i in range(1, len(_Profiler.group)):
                event_name, event_time = _Profiler.group[i]
                prev_event_name, prev_event_time = _Profiler.group[i - 1]
                elapsed_time = event_time - prev_event_time
                fractions.append(elapsed_time / total_time if total_time > 0 else 0)
                log_info(
                    f"{_Profiler.group_name} - {prev_event_name} -> {event_name}: {elapsed_time / 1e6:.2f} ms ({fractions[-1]*100:.2f}%)",
                )

        _Profiler.group_name = group_name
        _Profiler.group = []

    @staticmethod
    def close_group():
        _Profiler.start_group(None)
