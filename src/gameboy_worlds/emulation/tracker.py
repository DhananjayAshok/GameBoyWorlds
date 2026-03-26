from gameboy_worlds.emulation.parser import StateParser
from gameboy_worlds.utils import (
    nested_dict_to_str,
    verify_parameters,
    log_info,
    log_error,
    log_warn,
    log_dict,
    show_frames,
)


import numpy as np
from typing import Optional, Type, Dict, Any, Tuple, List, Set

from abc import ABC, abstractmethod

EPSILON = 0.001
""" Default epsilon for frame change detection. """


class MetricGroup(ABC):
    """
    Abstract Base class for organizing related metrics.

    ### Documentation Guidlines:
    Every subchild should document the following in their class docstrings:
    - Reports (List of keys that are present in the return dict of `report`)
    - Final Reports (List of keys that are present in the return dict of `report_final`)

    """

    NAME = "base"
    """ Name of the MetricGroup. """

    REQUIRED_PARSER = StateParser
    """ The StateParser which implements the minimum required functionality for this MetricGroup to work. """

    def __init__(self, state_parser: StateParser, parameters: dict):
        verify_parameters(parameters)
        if not issubclass(type(state_parser), self.REQUIRED_PARSER):
            log_error(
                f"StateParser of type {type(state_parser)} is not compatible with MetricGroup requiring {self.REQUIRED_PARSER}."
            )
        self.state_parser = state_parser
        """ An instance of the StateParser to parse game state variables. """
        self._parameters = parameters
        self.start()
        self.final_metrics: Dict[str, Any] = None
        """ Dictionary to store final metrics after environment close. """

    def start(self):
        """
        Called once when environment starts.
        All subclasses should call super() AFTER initializing their own variables.
        Only variables that will persist across episodes should be initialized here.
        """
        self.reset(first=True)

    @abstractmethod
    def reset(self, first: bool = False):
        """Called when environment resets.

        Args:
            first (bool): Whether this is the first reset of the environment. If True, might need to aggregate metrics into running final totals.
        """
        raise NotImplementedError

    @abstractmethod
    def close(self):
        """
        Called when environment closes. Good for computing summary stats.

        Step will not be called after this.
        """
        raise NotImplementedError

    @abstractmethod
    def step(self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]):
        """
        Called each environment step to update metrics.
        Args:
            current_frame (np.ndarray): The current frame rendered by the emulator.
            recent_frames (Optional[np.ndarray]): The stack of frames that were rendered during the last action. Shape is [n_frames, height, width, channels]. Can be None if rendering is disabled.
        """
        raise NotImplementedError

    @abstractmethod
    def report(self) -> Dict[str, Any]:
        """
        Return metrics as dictionary for instantaneous variable tracking.

        :return: Dictionary of metrics
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError

    @abstractmethod
    def report_final(self) -> dict:
        """
        Return metrics as dictionary for logging. Called at end of environment (before close).
        Will never be called before `self.close`.

        :return: Dictionary of metrics
        :rtype: Dict[str, Any]
        """
        raise NotImplementedError

    def log_info(self, message: str):
        """
        Logs with MetricGroup's name. Primarily for debugging.
        """
        log_info(f"[Metric({self.NAME})]: {message}", self._parameters)

    def log_warn(self, message: str):
        """
        Logs with MetricGroup's name. Primarily for debugging.
        """
        log_warn(f"[Metric({self.NAME})]: {message}", self._parameters)

    def log_report(self):
        """
        Logs the current metrics report with MetricGroup's name. Primarily for debugging.
        """
        log_info(f"Metric({self.NAME}):\n")
        log_dict(self.report(), parameters=self._parameters)


class CoreMetrics(MetricGroup):
    """
    Tracks basic metrics that are guaranteed to be available in state tracker reports for any and all games:

    Reports:
    - `steps`: Number of steps taken in the episode.
    - `frame_changed`: Whether the frame has changed since the last step.
    - `current_frame`: The current frame.
    - `passed_frames`: All frames that have passed since the last step.

    Final Reports:
    - `total_episodes`: Total number of episodes completed.
    - `average_steps_per_episode`: Average number of steps taken per episode.
    - `max_steps`: Maximum number of steps taken in any episode.
    - `min_steps`: Minimum number of steps taken in any episode.
    - `std_steps`: Standard deviation of steps taken across episodes.

    """

    NAME = "core"

    def start(self):
        self.steps_per_episode = []
        """ List of steps taken in each episode. """
        super().start()

    def reset(self, first=False):
        if not first:
            self.steps_per_episode.append(self.steps)
        else:
            self.steps = 0
            """ Number of steps taken in the episode. """
            self.previous_frame = None
            """ Previous frame for detecting changes. """
            self.current_frame = None
            """ Current frame. """
            self.frame_changed = True
            """ Whether the frame has changed at all since last step. """
            self.passed_frames = None
            """ Stack of frames since the last step """

    def close(self):
        if len(self.steps_per_episode) > 0:
            total_episodes = len(self.steps_per_episode)
            average_steps = np.mean(self.steps_per_episode)
            max_steps = np.max(self.steps_per_episode)
            min_steps = np.min(self.steps_per_episode)
            std_steps = np.std(self.steps_per_episode)
        else:
            total_episodes = 0
            average_steps = 0.0
            max_steps = 0
            min_steps = 0
            std_steps = 0.0
        self.final_metrics = {
            "total_episodes": int(total_episodes),
            "average_steps_per_episode": float(average_steps),
            "max_steps": int(max_steps),
            "min_steps": int(min_steps),
            "std_steps": float(std_steps),
        }

    def step(self, current_frame, recent_frames):
        self.steps += 1
        self.current_frame = current_frame
        self.passed_frames = recent_frames
        if self.previous_frame is None:
            self.previous_frame = current_frame
            self.frame_changed = True
        else:
            frame_changed = False
            comparison_frame = self.previous_frame
            if recent_frames is None:
                recent_frames = np.array([current_frame])
            for frame in recent_frames:
                if np.abs(frame - comparison_frame).mean() > EPSILON:
                    frame_changed = True
                else:
                    frame_changed = False
                    comparison_frame = frame
                if frame_changed:
                    break
            self.frame_changed = frame_changed
        self.previous_frame = current_frame

    def report(self):
        """
        Provides the following metrics:
        - `steps`: Number of steps taken in the episode.
        - `frame_changed`: Whether the frame has changed since the last step.
        - `current_frame`: The current frame.
        - `passed_frames`: All frames that have passed since the last step.
        """
        return {
            "steps": self.steps,
            "frame_changed": self.frame_changed,
            "current_frame": self.current_frame,
            "passed_frames": self.passed_frames,
        }

    def report_final(self):
        """
        Provides the following metrics:
        - `total_episodes`: Total number of episodes completed.
        - `average_steps_per_episode`: Average number of steps taken per episode.
        - `max_steps`: Maximum number of steps taken in any episode.
        - `min_steps`: Minimum number of steps taken in any episode.
        - `std_steps`: Standard deviation of steps taken across episodes.
        """
        return self.final_metrics


class OCRegionMetric(MetricGroup, ABC):
    """
    Watch particular screen regions and capture subscreens for OCR when possible. Does not actually perform OCR itself, but makes it easy to capture the relevant regions.
    Children implementing this must define self.kinds in `start()` and then call on `super().start()`.

    Reports:
    - `ocr_regions`: A dictionary mapping kinds to captured regions that had OCR-eligible text detected in them. The keys are kinds of OCR regions, and the values are the stacks of captured screen regions as numpy arrays of shape (num_captures, height, width, channels).
    - `step`: The current step number. Useful for differentiating when multiple OCR texts were found in the same episode. You can typically safely ignore this.

    Final Reports:
    - `ocr_regions`: A list of tuples for all steps where OCR was detected. Is in form: `List[Tuple[int, Dict[str, np.ndarray]]]` where the int is the step number and the Dict maps kinds to a stack of the captured screen region.

    """

    NAME = "ocr"

    def start(self):
        """
        Assumes the child has initialized a dict called self.kinds which tracks the various kinds of OCR that could be done.
                self.kinds should be in the form: {kind: region_name} where region_name is the name of the region to OCR for that kind.
                Will track ocr captured region results in form of list of dictionaries where these kinds are keys.
        """
        super().start()
        if self.NAME != "ocr":
            log_error(
                "OCRMetric subclasses must have NAME equal to 'ocr' for the environment get_info() aggregation step to work.",
                self._parameters,
            )
        if not hasattr(self, "kinds"):
            log_error("OCRMetrics must declare self.kinds dictionary", self._parameters)
        elif not isinstance(self.kinds, dict):
            log_error("self.kinds must be a dictionary", self._parameters)
        self.kinds: dict
        for item in self.kinds:
            if not isinstance(item, str):
                log_error("self.kinds keys must be strings", self._parameters)
            region_info = self.kinds[item]
            if not isinstance(region_info, str):
                log_error(
                    "self.kinds values must be region names (strings)", self._parameters
                )
            if region_info not in self.state_parser.named_screen_regions:
                log_error(
                    f"OCR region name {region_info} not found in state parser named regions. Available options: {self.state_parser.named_screen_regions}",
                    self._parameters,
                )

    @staticmethod
    def can_read_kind(self, frame: np.ndarray, kind: str) -> bool:
        """
        Checks if the frame has text for the given kind.

        Args:
            frame (np.ndarray): The frame to check.
            kind (str): The kind of text to check for.
        """
        raise NotImplementedError

    def reset(self, first=False):
        """
        ocr_regions will track a list of the form List[Tuple[int, Dict[str, np.ndarray]]]
        which is a list of (step_number, {kind: ocr_region}) dictionaries.
        """
        self.ocr_regions = []
        self.steps = 0
        self.prev_has_ocr = False

    def step(self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]):
        all_frames = None
        if recent_frames is not None:
            all_frames = recent_frames  # Current frame is included in recent frames
        else:
            all_frames = np.array([current_frame])
        ocr_dict = {}
        # Aggregate results for all frames and separate per kind.
        for kind in self.kinds.keys():
            captured_frames = []
            for frame in all_frames:
                if self.can_read_kind(frame, kind):
                    captured_frames.append(
                        self.state_parser.capture_named_region(
                            current_frame=frame, name=self.kinds[kind]
                        )
                    )
            true_captured_frames = []  # remove duplicates for efficiency
            # add the later frame in case of overlap detection. This prefers more text for cases where text comes as a stream.
            if len(captured_frames) > 0:
                for i in range(len(captured_frames) - 1):
                    curr_frame = captured_frames[i]
                    next_frame = captured_frames[i + 1]
                    if np.abs(curr_frame - next_frame).mean() > EPSILON:
                        true_captured_frames.append(curr_frame)
                true_captured_frames.append(
                    captured_frames[-1]
                )  # always add the last frame.
                ocr_dict[kind] = np.array(true_captured_frames)
        if len(ocr_dict) > 0:
            self.ocr_regions.append((self.steps, ocr_dict))
            self.prev_has_ocr = True
        else:
            self.prev_has_ocr = False
        self.steps += 1

    def report(self):
        """
        Reports just the previous step's OCR regions if any were found.
        Returns:
            dict: A dictionary containing the captured regions for focused OCR.
        """
        if self.prev_has_ocr:
            return {
                "ocr_regions": self.ocr_regions[-1][1],
                "step": self.ocr_regions[-1][0],
            }
        else:
            return {}

    def report_final(self):
        """
        Reports all the OCR regions extracted in the episode.
        """
        return {"ocr_regions": self.ocr_regions}

    def close(self):
        pass


class SubGoal(ABC):
    """
    Abstract class representing a subgoal for tracking progress towards a test goal. These are intermediate states that must be achieved on the way to the final test goal.
    By convention, the task goal state itself is *not* considered a subgoal, but rather the final goal that the subgoals lead towards.
    """

    NAME = "placeholder"
    """ Name of the subgoal. """

    def __init__(self):
        if self.NAME == "placeholder":
            log_error(
                "Subclasses of SubGoal must set a unique NAME class variable.",
            )
        self.completed = False

    def check_completed(self, frames: np.ndarray, parser: StateParser) -> bool:
        """
        Checks whether the subgoal has been completed based on the given frames and state parser.

        Args:
            frames (np.ndarray): The stack of frames to check for subgoal completion.
            parser (StateParser): The state parser to use for checking subgoal completion.
        Returns:
            bool: True if the subgoal is completed, False otherwise.
        """
        for frame in frames:
            if self._check_completed(frame, parser):
                return True
        return False

    @abstractmethod
    def _check_completed(self, frame: np.ndarray, parser: StateParser) -> bool:
        """
        Checks whether the subgoal has been completed based on a single frame and the state parser.

        Args:
            frames (np.ndarray): A single frame to check for subgoal completion.
            parser (StateParser): The state parser to use for checking subgoal completion.
        Returns:
            bool: True if the subgoal is completed, False otherwise.
        """
        pass


class DummySubGoal(SubGoal):
    """
    A dummy subgoal that is never completed. Useful for testing.
    """

    NAME = "dummy_subgoal"

    def _check_completed(self, frame: np.ndarray, parser: StateParser) -> bool:
        return False


class RegionMatchSubGoal(SubGoal, ABC):
    """
    A subgoal that is completed if a specific region matches a target. Can be used to track subgoals that require specific dialogue boxes to appear, etc.
    """

    NAME = "placeholder"
    _NAMED_REGION: str = None
    _TARGET_NAME: str = None

    def __init__(self):
        super().__init__()
        if self._NAMED_REGION is None or self._TARGET_NAME is None:
            log_error(
                "Subclasses of RegionMatchSubGoal must set _NAMED_REGION and _TARGET_NAME class variables.",
            )

    def _check_completed(self, frame: np.ndarray, parser: StateParser) -> bool:
        matches = parser.named_region_matches_multi_target(
            frame, self._NAMED_REGION, self._TARGET_NAME
        )
        return matches


class AnyRegionMatchSubGoal(SubGoal, ABC):
    """
    A subgoal that is completed if any of a list of specific regions matches their targets.
    """

    NAME = "placeholder"
    _NAMED_REGIONS: List[str] = None
    _TARGET_NAMES: List[str] = None

    def __init__(self):
        super().__init__()
        if (
            self._NAMED_REGIONS is None
            or self._TARGET_NAMES is None
            or len(self._NAMED_REGIONS) != len(self._TARGET_NAMES)
            or len(self._NAMED_REGIONS) == 0
        ):
            log_error(
                "Subclasses of AnyRegionMatchSubGoal must set _NAMED_REGIONS and _TARGET_NAMES class variables, and they must be of the same length non zero.",
            )

    def _check_completed(self, frame: np.ndarray, parser: StateParser) -> bool:
        for named_region, target_name in zip(self._NAMED_REGIONS, self._TARGET_NAMES):
            matches = parser.named_region_matches_multi_target(
                frame, named_region, target_name
            )
            if matches:
                return True
        return False


class SubGoalMetric(MetricGroup, ABC):
    """
    Tracks subgoal based progress towards a specific test goal.
    Subgoals are always sequential, i.e. it is impossible to complete subgoal n+1 without completing subgoal n first.

    Reports:
    - `all`: A list of the names of all subgoals being tracked, regardless of completion status.
    - `completed`: A list of the names of the subgoals that have been completed.

    Final Reports:
    - `reached_subgoals`: List of subgoals that were reached at any point during any episode.
    """

    NAME = "subgoals"
    SUBGOALS: List[SubGoal] = []
    """ List of SubGoal classes representing the subgoals to be tracked. These should be defined in child classes. """

    def start(self):
        if self.NAME != "subgoals":
            log_error(
                f"SubGoalMetric NAME must be 'subgoals', got '{self.NAME}'.",
                self._parameters,
            )
        if len(self.SUBGOALS) == 0:
            log_error(
                "SubGoalMetric requires at least one subgoal to be defined in the SUBGOALS class variable.",
                self._parameters,
            )
        self._subgoals: List[SubGoal] = []
        """ List of SubGoal instances representing the subgoals being tracked. """
        for subgoal_class in self.SUBGOALS:
            subgoal_instance: SubGoal = subgoal_class()
            self._subgoals.append(subgoal_instance)
        self._reached_subgoals: Set[str] = set()
        """ Set of subgoals that were reached at any point during any episode. """
        super().start()

    def close(self):
        pass

    def reset(self, first=False):
        if not first:
            for subgoal in self._subgoals:
                if subgoal.completed:
                    self._reached_subgoals.add(subgoal.NAME)
        for subgoal in self._subgoals:
            subgoal.completed = False

    def step(self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]):
        all_frames = None
        if recent_frames is not None:
            all_frames = recent_frames  # Current frame is included in recent frames
        else:
            all_frames = np.array([current_frame])
        for subgoal in self._subgoals:
            if not subgoal.completed:
                completed = subgoal.check_completed(all_frames, self.state_parser)
                subgoal.completed = completed

    def report(self):
        """
        Reports the names of the subgoals being tracked and which ones have been completed.
        Returns:
            dict: A dictionary containing the list of all subgoals and the list of completed subgoals.
        """
        return {
            "all": [subgoal.NAME for subgoal in self._subgoals],
            "completed": [
                subgoal.NAME for subgoal in self._subgoals if subgoal.completed
            ],
        }

    def report_final(self):
        """
        Reports the names of the subgoals that were reached at any point during any episode.
        Returns:
            dict: A dictionary containing the list of reached subgoals.
        """
        return {"reached_subgoals": list(self._reached_subgoals)}


class DummySubGoalMetric(SubGoalMetric):
    """
    A dummy SubGoalMetric that tracks a single DummySubGoal. Useful for testing.
    """

    SUBGOALS = [DummySubGoal]


def make_subgoal_metric_class(subgoals: List[Type[SubGoal]]) -> Type[SubGoalMetric]:
    """
    Factory function to create a SubGoalMetric class with the given subgoals and name.

    Args:
        subgoals (List[Type[SubGoal]]): The list of SubGoal classes to track.
        name (str): The name of the SubGoalMetric class.

    Returns:
        Type[SubGoalMetric]: A new SubGoalMetric class with the specified subgoals and name.
    """
    if len(subgoals) == 0:
        log_error("Must provide at least one subgoal to create a SubGoalMetric class.")

    class CustomSubGoalMetric(SubGoalMetric):
        SUBGOALS = subgoals

    return CustomSubGoalMetric


class TerminationTruncationMetric(MetricGroup, ABC):
    """
    Tracks whether the environment was terminated or truncated.

    Reports:
    - `terminated`: Whether the environment was terminated.
    - `truncated`: Whether the environment was truncated.

    Final Reports:
    - `episode_end_reason`: List of reasons for episode endings: "terminated", "truncated", or None (None will occur only if there is a bug that leads to a premature reset).
    """

    NAME = "termination_truncation"

    def start(self):
        super().start()
        if self.NAME != "termination_truncation":
            log_error(
                f"TerminationTruncationMetric NAME must be 'termination_truncation', got '{self.NAME}'.",
                self._parameters,
            )
        self.episode_end_reason = []
        """ List of reasons for episode: termination or truncation or None (None will occur only if there is a bug that leads to a premature reset). """
        self.terminated = False
        """ Whether the environment was terminated. """
        self.truncated = False
        """ Whether the environment was truncated. """

    def reset(self, first=False):
        if not first:
            if self.terminated:
                self.episode_end_reason.append("terminated")
            elif self.truncated:
                self.episode_end_reason.append("truncated")
            else:
                self.episode_end_reason.append(None)
        self.terminated = False
        self.truncated = False

    def close(self):
        pass

    @abstractmethod
    def determine_truncated(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ) -> bool:
        """
        Determines whether the environment was truncated.

        :param current_frame: The current frame rendered by the emulator.
        :type current_frame: np.ndarray
        :param recent_frames: The stack of frames that were rendered during the last action. Shape is [n_frames, height, width, channels]. Can be None if rendering is disabled.
        :type recent_frames: Optional[np.ndarray]
        :return: True if the environment was truncated, False otherwise.
        :rtype: bool
        """
        pass

    @abstractmethod
    def determine_terminated(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ) -> bool:
        """
        Determines whether the environment was terminated.

        :param current_frame: The current frame rendered by the emulator.
        :type current_frame: np.ndarray
        :param recent_frames: The stack of frames that were rendered during the last action. Shape is [n_frames, height, width, channels]. Can be None if rendering is disabled.
        :type recent_frames: Optional[np.ndarray]
        :return: True if the environment was terminated, False otherwise.
        :rtype: bool
        """
        pass

    def step(self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]):
        """
        Determines whether the environment was terminated or truncated.
        """
        if self.terminated or self.truncated:
            return  # This should ideally not happen, because the environment should reset after termination or truncation.
        self.truncated = self.determine_truncated(current_frame, recent_frames)
        self.terminated = self.determine_terminated(current_frame, recent_frames)

    def report(self):
        """
        Reports whether the environment was terminated or truncated.
        Returns:
            dict: A dictionary containing the termination and truncation status.
        """
        return {
            "terminated": self.terminated,
            "truncated": self.truncated,
        }

    def report_final(self):
        """
        Reports the reasons for episode endings.
        Returns:
            dict: A dictionary containing the list of episode end reasons.
        """
        return {"episode_end_reason": self.episode_end_reason}


class TerminationMetric(TerminationTruncationMetric, ABC):
    def determine_truncated(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ) -> bool:
        return False


class StateTracker:
    """
    Tracks and provides API access to the game state / metrics over time and across episodes.
    The most hassle-free way to read from the StateTracker is to use the `report()` and `report_final()` methods to get nested dictionaries of all metrics tracked.

    **Example Usage:**

    ```python
    import numpy as np
    from gameboy_worlds import get_pokemon_emulator
    emulator = get_pokemon_emulator(variant="pokemon_red")

    # We can access the StateTracker via the emulator
    state_tracker = emulator.state_tracker

    # Run a random action on the emulator
    emulator.reset()
    allowed_actions = list(LowLevelActions)
    action = np.random.choice(allowed_actions)
    _, _ = emulator.step(action) # also updates the StateTracker internally
    # We can access the current episode metrics via the StateTracker
    episode_metrics = state_tracker.report() # access all of them as a nested dict
    specific_metric = state_tracker.get_episode_metric(("core", "steps")) # access specific metrics

    # If we reset the emulator, the StateTracker will reset its inter-episode metrics as well
    emulator.reset()
    action = np.random.choice(allowed_actions)
    _, _ = emulator.step(action)
    emulator.close() # StateTracker will finalize its metrics internally
    final_metrics = state_tracker.report_final() # access all of them as a nested dict
    specific_final_metric = state_tracker.get_final_metric(("core", "average_steps_per_episode")) # access specific final metrics
    ```
    """

    TERMINATION_TRUNCATION_METRIC: Type[TerminationTruncationMetric] = None
    """ The TerminationTruncationMetric class to use for tracking termination and truncation. If None, no such metric will be tracked. """

    SUBGOAL_METRIC: Type[SubGoalMetric] = None
    """ The SubGoalMetric class to use for tracking subgoal progress. If None, no such metric will be tracked. """

    def __init__(
        self,
        state_parser: StateParser,
        parameters: dict,
    ):
        """
        Initializes the StateTracker.
        Args:
            state_parser (StateParser): An instance of the StateParser to parse game state variables.
            parameters (dict): A dictionary of parameters for configuration.
        """
        verify_parameters(parameters)
        self.state_parser = state_parser
        """ An instance of the StateParser to parse game state variables. """
        self._parameters = parameters
        self.start()
        self.validate()
        if self.metric_classes[0] != CoreMetrics:
            log_error(
                "First metric class must be CoreMetrics. Make sure to call `super().start()` first in child class overrides of `start()`.",
                parameters,
            )
        self.metrics = {}
        """ Dictionary to store MetricGroup instances. """
        for metric_group_class in self.metric_classes:
            metric_group_instance: MetricGroup = metric_group_class(
                state_parser, parameters
            )
            self.metrics[metric_group_instance.NAME] = metric_group_instance
        self.episode_metrics: Dict[str, Dict[str, Any]] = {}
        """ Dictionary to store metrics running during episode. """
        self.final_metrics: Dict[str, Dict[str, Any]] = {}

    def start(self):
        """
        Sets up the metrics for the tracker by creating the list `self.metric_classes`

        Child classes must FIRST call super().start() and THEN set up their own metric classes.
        """
        self.metric_classes: List[Type[MetricGroup]] = [CoreMetrics]
        if self.TERMINATION_TRUNCATION_METRIC is not None:
            if not issubclass(
                self.TERMINATION_TRUNCATION_METRIC, TerminationTruncationMetric
            ):
                log_error(
                    "TERMINATION_TRUNCATION_METRIC must be a subclass of TerminationTruncationMetric.",
                    self._parameters,
                )
            self.metric_classes.append(self.TERMINATION_TRUNCATION_METRIC)
        if self.SUBGOAL_METRIC is not None:
            if not issubclass(self.SUBGOAL_METRIC, SubGoalMetric):
                log_error(
                    "SUBGOAL_METRIC must be a subclass of SubGoalMetric.",
                    self._parameters,
                )
            self.metric_classes.append(self.SUBGOAL_METRIC)

    def validate(self):
        """
        Is meant to be called once after initialization to ensure that the tracker is valid.
        """
        pass

    def reset(self):
        """
        Is called once per environment reset to reset any tracked metrics.
        """
        for metric_group in self.metrics.values():
            metric_group.reset()
        self.step()

    def step(self, recent_frames: Optional[np.ndarray] = None):
        """
        Is called once per environment step to update any tracked metrics.

        Args:
            recent_frames (Optional[np.ndarray]): The stack of frames that were rendered during the last action. Shape is [n_frames, height, width, channels]. Can be None if rendering is disabled.
            epsilon (float, optional): The threshold for considering a frame change.
        """
        current_frame = None
        if recent_frames is None:
            current_frame = self.state_parser.get_current_frame()
        else:
            current_frame = recent_frames[-1]
        self.episode_metrics = {}
        for metric_group in self.metrics.values():
            metric_group.step(current_frame, recent_frames)
            self.episode_metrics[metric_group.NAME] = metric_group.report()

    def close(self):
        """
        Is called once when the environment is closed to finalize any tracked metrics.
        """
        for metric_group in self.metrics.values():
            metric_group.close()
        self.final_metrics = {
            name: mg.report_final() for name, mg in self.metrics.items()
        }

    def report(self) -> Dict[str, Dict[str, Any]]:
        """
        Returns the current episode metrics.

        :return: A nested dictionary containing the current episode metrics.
        :rtype: Dict[str, Dict[str, Any]]
        """
        return self.episode_metrics

    def report_final(self) -> Dict[str, Dict[str, Any]]:
        """
        Returns the final metrics after environment close.

        Returns:
            Dict[str, Dict[str, Any]]: A nested dictionary containing the final metrics.
        """
        return self.final_metrics

    def _get_specific_metric(self, metrics_dict, key: Tuple[str, str]):
        if metrics_dict is None:
            log_error("No metrics available. Have you called step() or close()?")
        metric_group_name, metric_name = key
        if metric_group_name not in metrics_dict:
            log_error(
                f"Metric group {metric_group_name} not found in metrics. Available groups: {list(metrics_dict.keys())}"
            )
        if metric_name not in metrics_dict[metric_group_name]:
            log_error(
                f"Metric {metric_name} not found in metric group {metric_group_name}. Available metrics: {list(metrics_dict[metric_group_name].keys())}"
            )
        return metrics_dict[metric_group_name][metric_name]

    def get_episode_metric(self, key: Tuple[str, str]):
        """
        Returns the metrics for a specific episode and metric group.

        Does not give final metrics at any point.

        :param key: A tuple of the form (metric_group_name, metric_name).
        :type key: Tuple[str, str]
        :return: The requested metric value
        :rtype: Any
        """
        return self._get_specific_metric(self.episode_metrics, key)

    def get_final_metric(self, key: Tuple[str, str]):
        """
        Returns the final metrics for a specific metric group.

        :param key: A tuple of the form (metric_group_name, metric_name).
        :type key: Tuple[str, str]
        :return: The requested final metric value
        :rtype: Any
        """
        return self._get_specific_metric(self.final_metrics, key)

    def __repr__(self) -> str:
        metric_names = [mg.NAME for mg in self.metrics.values()]
        return f"<StateTracker, metrics=({', '.join(metric_names)})>"


class TestTrackerMixin:
    """
    Mixin class for testing trackers.
    Ensures that exactly one of the tracked metrics is a TerminationTruncationMetric.
    """

    def validate(self):
        if not hasattr(self, "_parameters"):
            log_error("Parameters have not been set yet.")
        if self.TERMINATION_TRUNCATION_METRIC is None:
            log_error(
                "TestTrackerMixin requires a TerminationTruncationMetric to be set as TERMINATION_TRUNCATION_METRIC.",
                self._parameters,
            )
        if self.SUBGOAL_METRIC is None:
            log_error(
                "TestTrackerMixin requires a SubGoalMetric to be set as SUBGOAL_METRIC.",
                self._parameters,
            )


class RegionMatchTruncationMetric(TerminationTruncationMetric, ABC):
    """
    Truncates the episode if a specific region matches a target.
    Can be used to truncate episodes when specific dialogue boxes appear, etc.
    """

    _TRUNCATION_NAMED_REGION = None
    _TRUNCATION_TARGET_NAME = None

    def determine_truncated(self, current_frame, recent_frames):
        if (
            self._TRUNCATION_NAMED_REGION is None
            or self._TRUNCATION_TARGET_NAME is None
        ):
            log_error(
                "Must set _TRUNCATION_NAMED_REGION and _TRUNCATION_TARGET_NAME.",
                self._parameters,
            )
        all_frames = [current_frame]
        if recent_frames is not None:
            all_frames = recent_frames
        for frame in all_frames:
            matches = self.state_parser.named_region_matches_multi_target(
                frame,
                self._TRUNCATION_NAMED_REGION,
                self._TRUNCATION_TARGET_NAME,
            )
            if matches:
                return True
        return False


class RegionMatchTerminationMetric(TerminationTruncationMetric, ABC):
    """
    Terminates the episode if a specific region matches a target.
    Can be used to terminate episodes when specific dialogue boxes appear, etc.
    """

    _TERMINATION_NAMED_REGION = None
    _TERMINATION_TARGET_NAME = None

    def determine_terminated(self, current_frame, recent_frames):
        if (
            self._TERMINATION_NAMED_REGION is None
            or self._TERMINATION_TARGET_NAME is None
        ):
            log_error(
                "Must set _TERMINATION_NAMED_REGION and _TERMINATION_TARGET_NAME.",
                self._parameters,
            )
        all_frames = [current_frame]
        if recent_frames is not None:
            all_frames = recent_frames
        for frame in all_frames:
            matches = self.state_parser.named_region_matches_multi_target(
                frame,
                self._TERMINATION_NAMED_REGION,
                self._TERMINATION_TARGET_NAME,
            )
            if matches:
                return True
        return False


class RegionMatchTerminationOnlyMetric(TerminationMetric, ABC):
    """
    RegionMatchTerminationMetric with no truncation.
    No truncation.
    """

    _TERMINATION_NAMED_REGION = None
    _TERMINATION_TARGET_NAME = None

    def determine_terminated(self, current_frame, recent_frames):
        if (
            self._TERMINATION_NAMED_REGION is None
            or self._TERMINATION_TARGET_NAME is None
        ):
            log_error(
                "Must set _TERMINATION_NAMED_REGION and _TERMINATION_TARGET_NAME.",
                self._parameters,
            )
        all_frames = [current_frame]
        if recent_frames is not None:
            all_frames = recent_frames
        for frame in all_frames:
            matches = self.state_parser.named_region_matches_multi_target(
                frame,
                self._TERMINATION_NAMED_REGION,
                self._TERMINATION_TARGET_NAME,
            )
            if matches:
                return True
        return False
