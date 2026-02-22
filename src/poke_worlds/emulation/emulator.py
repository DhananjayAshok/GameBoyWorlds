from enum import Enum
from typing import Type, Optional, Tuple


import os
import re
from time import perf_counter
import sys
import shutil
import uuid
from poke_worlds.emulation.parser import StateParser
from poke_worlds.emulation.tracker import StateTracker
from poke_worlds.utils import (
    load_parameters,
    log_error,
    log_warn,
    file_makedir,
    log_info,
    is_none_str,
    verify_parameters,
    log_dict,
)


import cv2

from pyboy import PyBoy
from pyboy.utils import WindowEvent
from matplotlib import pyplot as plt
from skimage.transform import downscale_local_mean
import numpy as np
from tqdm import tqdm


class LowLevelActions(Enum):
    """
    Enum for low-level actions that can be performed on the GameBoy emulator.
    """

    PRESS_ARROW_DOWN = WindowEvent.PRESS_ARROW_DOWN
    PRESS_ARROW_LEFT = WindowEvent.PRESS_ARROW_LEFT
    PRESS_ARROW_RIGHT = WindowEvent.PRESS_ARROW_RIGHT
    PRESS_ARROW_UP = WindowEvent.PRESS_ARROW_UP
    PRESS_BUTTON_A = WindowEvent.PRESS_BUTTON_A
    PRESS_BUTTON_B = WindowEvent.PRESS_BUTTON_B
    PRESS_BUTTON_START = WindowEvent.PRESS_BUTTON_START


class ReleaseActions(Enum):
    """
    Enum for release actions corresponding to low-level actions.
    """

    release_actions = {
        LowLevelActions.PRESS_ARROW_DOWN: WindowEvent.RELEASE_ARROW_DOWN,
        LowLevelActions.PRESS_ARROW_LEFT: WindowEvent.RELEASE_ARROW_LEFT,
        LowLevelActions.PRESS_ARROW_RIGHT: WindowEvent.RELEASE_ARROW_RIGHT,
        LowLevelActions.PRESS_ARROW_UP: WindowEvent.RELEASE_ARROW_UP,
        LowLevelActions.PRESS_BUTTON_A: WindowEvent.RELEASE_BUTTON_A,
        LowLevelActions.PRESS_BUTTON_B: WindowEvent.RELEASE_BUTTON_B,
        LowLevelActions.PRESS_BUTTON_START: WindowEvent.RELEASE_BUTTON_START,
    }


class IDPathCreator:
    """
    Handles the creation of IDs and paths for saving emulator artifacts.
    """

    def __init__(self, parameters: dict):
        verify_parameters(parameters)
        self._parameters = parameters

    def _get_numbered_instance_id(self, path: str, instance_id: str = None) -> int:
        """
        Looks at the given path and returns <next_number>_<instance_id> where next_number is 1 + the highest existing numbered instance ID in the path.

        :param path: Path to look for existing instances.
        :type path: str
        :param instance_id: Instance ID pattern to match. If None, counts all instances.
        :type instance_id: str
        :return: Number of existing instances matching the pattern.
        """
        # instance_id = str(uuid.uuid4())[:8]
        if not os.path.exists(path):
            if instance_id is None:
                instance_id = str(uuid.uuid4())[:8]
            return f"0_{instance_id}"
        if instance_id is None:
            instance_id = str(uuid.uuid4())[:8]
            n_existing = os.listdir(path)
            return f"{len(n_existing)}_{instance_id}"
        # must find the pattern <number>_<instance_id>
        pattern = re.compile(r"(\d+)_" + re.escape(instance_id))
        existing_instances = [d for d in os.listdir(path) if pattern.match(d)]
        if len(existing_instances) == 0:
            return f"0_{instance_id}"
        else:
            return f"{len(existing_instances)}_{instance_id}"

    def get_session_path(
        self,
        session_name: Optional[str],
        instance_id: Optional[str],
        environment_variant: str,
    ) -> str:
        if session_name is None:
            session_name = "tmp_sessions"
            log_warn(
                f"Saving a temporary session. If you run poke_worlds.clear_tmp_sessions(), it will be deleted. To make it permanent, pass in a `session_name` to the emulator constructor kwargs."
            )
        elif not isinstance(session_name, str) or session_name == "":
            log_error(
                f"session_name must be a non-empty string. Recieved {session_name}",
                self._parameters,
            )
        storage_dir = self._parameters["storage_dir"]
        session_path = os.path.join(
            storage_dir, "sessions", environment_variant, session_name
        )
        if instance_id is not None:
            if not isinstance(instance_id, str) or instance_id == "":
                log_error(
                    f"instance_id must be a non-empty string. Recieved {instance_id}",
                    self._parameters,
                )
            session_path = os.path.join(session_path, "named_instances")
        instance_id = self._get_numbered_instance_id(session_path, instance_id)
        full_session_path = os.path.join(session_path, instance_id)
        os.makedirs(full_session_path, exist_ok=True)
        return full_session_path

    def clear_tmp_sessions(self):
        """
        Clears the tmp_sessions directory for ALL game variants.
        """
        storage_dir = self._parameters["storage_dir"]
        session_path = os.path.join(storage_dir, "sessions")
        if not os.path.exists(session_path):
            return
        existing_variants = os.listdir(session_path)
        cleared_sessions = {}
        for variant in existing_variants:
            tmp_sessions_path = os.path.join(session_path, variant, "tmp_sessions")
            if not os.path.exists(tmp_sessions_path):
                continue
            n_sessions = os.listdir(tmp_sessions_path)
            shutil.rmtree(tmp_sessions_path)
            cleared_sessions[variant] = len(n_sessions)
        log_info(
            f"Cleared temporary sessions, statistics:",
            self._parameters,
        )
        log_dict(cleared_sessions, parameters=self._parameters)


class Emulator:
    """
    Handles the running of the GameBoy emulator, including loading ROMs, managing state, performing low level actions and calling the tracker.
    Subclasses will likely only be needed to manually force the execution of specific button sequences when certain states are detected. (e.g. short-circuiting specific menus, etc.)

    Can be used to access the `state_parser` and `state_tracker` instances for the running game instance.
    """

    REQUIRED_STATE_PARSER = StateParser
    """ The minimal functionality StateParser needed for this emulator to run """

    REQUIRED_STATE_TRACKER = StateTracker
    """ The minimal functionality StateTracker needed for this emulator to run """

    def __init__(
        self,
        game: str,
        gb_path: str,
        state_parser_class: Type[StateParser],
        state_tracker_class: Type[StateTracker],
        init_state: str,
        parameters: dict,
        *,
        headless: bool = True,
        max_steps: int = None,
        save_video: bool = None,
        session_name: str = None,
        instance_id: str = None,
    ):
        """
        Start the GameBoy emulator with the given ROM file and initial state.

        Args:
            game (str): Name of game variant being emulated.
            gb_path (str): Path to the GameBoy ROM file.
            state_parser_class (Type[StateParser]): A class that inherits from StateParser to parse game state variables.
            state_tracker_class (Type[StateTracker]): A class that inherits from StateTracker to track game state metrics.
            init_state (str): Path to the initial state file to load.
            parameters (dict): Dictionary of parameters for the environment.
            headless (bool, optional): Whether to run the environment in headless mode.
            max_steps (int, optional): Maximum number of steps per episode.
            save_video (bool, optional): Whether to save video of the episodes.
            session_name (str, optional): Name of the session. If None, a new session name will be allocated. This is the broad category you want to save files to
            instance_id (str, optional): Unique identifier for this environment instance. If None, a new UUID will be generated. The instance ID is useful for distinguishing multiple environments running in parallel with the same session name.
        """
        verify_parameters(parameters)
        self._parameters = parameters
        if game is None or game == "":
            log_error(
                "You must provide a name for the game variant being emulated.",
                self._parameters,
            )
        if gb_path is None:
            log_error(
                "You must provide a path to the GameBoy ROM file.", self._parameters
            )
        if not issubclass(state_parser_class, self.REQUIRED_STATE_PARSER):
            log_error(
                f"state_parser_class must be a subclass of {self.REQUIRED_STATE_PARSER.__name__}, got {state_parser_class_.__name__}.",
                self._parameters,
            )
        if not issubclass(state_tracker_class, self.REQUIRED_STATE_TRACKER):
            log_error(
                f"state_tracker_class must be a subclass of {self.REQUIRED_STATE_TRACKER.__name__}, got {state_tracker_class.__name__}.",
                self._parameters,
            )
        if init_state is None:
            log_error(
                "You must provide an initial state file to load.", self._parameters
            )
        if headless not in [True, False]:
            log_error("headless must be a boolean.", self._parameters)
        self.game = game
        """ Name of game variant being emulated. """
        self._gb_path = gb_path
        self._set_init_state(init_state)
        # validate init_state exists and ends with .state
        if not os.path.exists(self._gb_path):
            log_error(
                f"GameBoy ROM file {self._gb_path} does not exist. You must obtain a ROM through official means, and then place it in the path: {self._gb_path}",
                self._parameters,
            )
        if not self._gb_path.endswith(".gb") and not self._gb_path.endswith(".gbc"):
            log_error(
                f"GameBoy ROM file {self._gb_path} is not a .gb or .gbc file.",
                self._parameters,
            )
        self.headless = headless
        """ Whether to run the environment in headless mode."""
        if max_steps is None:
            max_steps = self._parameters["gameboy_max_steps"]
        if max_steps > self._parameters["gameboy_hard_max_steps"]:
            log_warn(
                f"max_steps {max_steps} exceeds gameboy_hard_max_steps {self._parameters['gameboy_hard_max_steps']}. Setting to hard max.",
                self._parameters,
            )
            max_steps = self._parameters["gameboy_hard_max_steps"]
        self.max_steps = max_steps
        """ Maximum number of steps per episode. """
        if save_video is None:
            save_video = self._parameters["gameboy_default_save_video"]
        self.save_video = save_video
        """ Whether to save video of the episodes. """
        self._video_text = None
        """ Text to place in the bottom left corner of the video, if any. Can be overriden by an environment. """
        id_path_creator = IDPathCreator(self._parameters)
        self.session_path = id_path_creator.get_session_path(
            session_name=session_name,
            instance_id=instance_id,
            environment_variant=self.get_env_variant(),
        )
        """ Path to the session directory. This is where all artifacts for this session are saved. """
        self.act_freq = parameters["gameboy_action_freq"]
        """ Number of emulator ticks per action. Defaults to value specified in config files. """
        self.press_step = parameters["gameboy_press_step"]
        """ Number of emulator ticks to hold down a button press. Defaults to value specified in config files. """
        self.render_headless = parameters["gameboy_headless_render"]
        """ Whether to render the emulator screen even in headless mode. This must be true for methods that rely on image observations (e.g. VLMs) to access the screen. Defaults to value specified in config files. """
        if not self.render_headless:
            log_error(
                "render_headless cannot be set to False. In the Pokemon environments, screen captures are used aggressively to determine state. ",
                self._parameters,
            )

        self._full_frame_writer = None
        self._model_frame_writer = None
        self.reset_count = 0
        """ Number of times the environment has been reset. """
        self.step_count = 0
        """ Number of steps taken in the current episode. """
        self._reduce_video_resolution = parameters["gameboy_reduce_video_resolution"]
        pokemon_frame_size = (
            160,
            144,
        )  # Confirm this is universal if you want other GB games.
        self.screen_shape = (pokemon_frame_size[0], pokemon_frame_size[1], 1)
        """ Resolution of the rendered game screen """
        if self._reduce_video_resolution:
            self.output_shape = (pokemon_frame_size[0] // 2, pokemon_frame_size[1] // 2)
        else:
            self.output_shape = (pokemon_frame_size[0], pokemon_frame_size[1])
            """ Shape of the output observations. This is the resolution of the rendered screen. """

        head = "null" if self.headless else "SDL2"

        self._pyboy = PyBoy(
            self._gb_path,
            window=head,
        )
        self.state_parser = state_parser_class(self._pyboy, self._parameters)
        """ Instance of the StateParser to parse game state variables. """

        self.state_tracker = state_tracker_class(
            self.state_parser,
            self._parameters,
        )
        """ Instance of the StateTracker to track game state metrics. """

        # self.screen = self.pyboy.botsupport_manager().screen()

        if not self.headless:
            if not is_none_str(self._parameters["gameboy_headed_emulation_speed"]):
                self._pyboy.set_emulation_speed(
                    int(self._parameters["gameboy_headed_emulation_speed"])
                )
        self.reset()

    @staticmethod
    def create_first_state(gb_path: str, state_path: str):
        """
        Creates a basic state for the emulator. This can be used to create an initial, default state file for a new game.

        Warning: This method uses parameter free logging, so if you override the log_file with a command prompt argument, it will be ignored here.

        Args:
            gb_path (str): Path to the GameBoy ROM file.
            state_path (str): Path to save the initial state file.
        """
        # error out if gb_path does not exist or is not a .gb or .gbc file
        if not os.path.exists(gb_path):
            log_error(
                f"GameBoy ROM file {gb_path} does not exist. You must obtain a ROM through official means, and then place it in the path: {gb_path}"
            )
        if not gb_path.endswith(".gb") and not gb_path.endswith(".gbc"):
            log_error(f"GameBoy ROM file {gb_path} is not a .gb or .gbc file.")
        if not state_path.endswith(".state"):
            state_path = state_path + ".state"
        if os.path.exists(state_path):
            log_error(f"State file {state_path} already exists. Will not overwrite...")
        file_makedir(state_path)
        pyboy = PyBoy(
            gb_path,
            window="null",
        )
        with open(state_path, "wb") as f:
            pyboy.save_state(f)
        pyboy.stop()
        log_info(f"Created initial state file at {state_path}")
        sys.exit(0)

    def set_init_state(self, init_state: str):
        """Sets a new initial state file for the environment. and resets the environment.

        Args:
            init_state (str): Path to the new initial state file.
        """
        self._set_init_state(init_state)
        self.reset()

    def _set_init_state(self, init_state: str):
        """
        Sets a new initial state file for the environment to eventually load.
        Does not reset the environment.

        Args:
            init_state (str): Path to the new initial state file.
        """
        if init_state is None:
            # log_warn(f"No initial state file provided. Using default initial state.", self._parameters)
            return
        if not init_state.endswith(".state"):
            init_state = init_state + ".state"
        states_path = self._parameters[f"{self.game}_rom_data_path"] + "/states/"
        if not os.path.exists(init_state):
            if states_path in init_state:
                log_error(
                    f"Initial state file {init_state} does not exist.", self._parameters
                )
            # try to resolve.
            potential_path = os.path.join(states_path, init_state)
            if os.path.exists(potential_path):
                init_state = potential_path
            else:
                log_error(
                    f"Initial state file {init_state} does not exist.", self._parameters
                )
        self.init_state = init_state
        log_info(f"Set new initial state file to {self.init_state}", self._parameters)

    def reset(self, new_init_state: str = None):
        """
        Resets the environment to the initial state. Optionally loads a new initial state file.

        Args:
            new_init_state (str, optional): Path to a new initial state file to load.
        """
        # validate the new_init_state if provided
        if new_init_state is not None:
            self._set_init_state(new_init_state)
        # restart game, skipping to init_state
        with open(self.init_state, "rb") as f:
            self._pyboy.load_state(f)

        self.reset_count += 1
        self.step_count = 0
        self.state_tracker.reset()
        self.close_video()
        self._video_text = None
        return

    def get_current_frame(self) -> np.ndarray:
        """
        Renders the currently rendered screen of the emulator and returns it as a numpy array.

        Returns:
            np.ndarray: The rendered image as a numpy array.
        """
        return self.state_parser.get_current_frame()

    def _update_listeners_after_actions(self, frames: np.ndarray):
        """
        Updates the video and state tracker after a batch of actions are run on the emulator without step()

        You should *not* call this method when implementing HighLevelActions, instead call step(), track the states at each step, and return the list of transition states.

        Args:
            frames (np.ndarray): Frames of shape [n_frames, H, W, C] that contain the frames which elapsed during the run of the actions outside step
        """
        if self.save_video and self.video_running:
            self.add_video_frames(frames)
        self.state_tracker.step(frames)

    def _get_unique_frames(self, frames: np.ndarray) -> np.ndarray:
        """
        Removes duplicate frames from a stack of frames.

        Args:
            frames (np.ndarray): Stack of frames of shape [n_frames, H, W, C].
        Returns:
            np.ndarray: Stack of frames with duplicates removed. Shape is [n_unique_frames, H, W, C].
        """
        unique_frames = []
        for frame in frames:
            if len(unique_frames) == 0:
                unique_frames.append(frame)
            else:
                if not np.array_equal(frame, unique_frames[-1]):
                    unique_frames.append(frame)
        unique_frames = np.stack(unique_frames, axis=0)
        return unique_frames

    def step(self, action: LowLevelActions = None) -> Tuple[Optional[np.ndarray], bool]:
        """
        Takes a step in the environment by performing the given action on the emulator. If saving video, starts the video recording on the first step.

        :param action: Lowest level action to perform on the emulator.
        :type action: LowLevelActions
        :return:
            - The stack of frames that passed while performing the action, if rendering is enabled. Is of shape [n_frames (3 right now), height, width, channels]. Otherwise, None.

            - Is max steps reached.
        :rtype: Tuple[Optional[np.ndarray], bool]
        """
        if action is not None:
            if action not in LowLevelActions:
                log_error(
                    f"Invalid action {action}. Must be one of {list(LowLevelActions)} or None",
                    self._parameters,
                )
        if self.step_count >= self.max_steps:
            log_warn(
                "Step called after max_steps reached. Please reset the environment.",
                self._parameters,
            )
            # This does not exit because some HighLevelActions may call step() multiple times in their execution.
            # It is not the best practice to allow this to happen, but it is easier to not error out here than check in every HighLevelAction, and this won't advantage the agent too much.
            # One consequence, however, is that max_steps then becomes a soft limit rather than a hard limit.

        if self.save_video and self.step_count == 0:
            self.start_video()

        frames = self.run_action_on_emulator(action)
        self.step_count += 1
        frames = self._get_unique_frames(frames)
        self._update_listeners_after_actions(frames)
        return frames, self.check_if_done()

    def get_state_parser(self) -> StateParser:
        """
        Returns the current game state parser instance.

        Returns:
            StateParser: The current game state parser.
        """
        return self.state_parser

    def run_action_on_emulator(
        self, action: LowLevelActions = None
    ) -> Optional[np.ndarray]:
        """

        Performs the given action on the emulator by pressing and releasing the corresponding button.

        Args:
            action (LowLevelActions): Lowest level action to perform on the emulator.
        Returns:
            Optional[np.ndarray]: The stack of frames that passed while performing the actions. Is of shape [n_frames (3 right now), height, width, channels]. Otherwise, None.
        """
        frames = None
        if action is not None:
            frames = []
            self._pyboy.send_input(action.value)
            press_step = self.press_step
            self._pyboy.tick(press_step, True)
            frames.append(self.get_current_frame())
            self._pyboy.send_input(ReleaseActions.release_actions.value[action])
            self._pyboy.tick(self.act_freq - press_step - 1, True)
            frames.append(self.get_current_frame())
            self._pyboy.tick(1, True)
            frames.append(self.get_current_frame())
            frames = np.stack(frames, axis=0)
        else:
            self._pyboy.tick(self.act_freq, True)
            frames = [self.get_current_frame()]
            frames = np.array(frames)
        return frames

    def reduce_resolution(self, frame: np.ndarray) -> np.ndarray:
        """
        Reduces the resolution of the given frame by a factor of 2 using local mean downscaling.
        Args:
            frame (np.ndarray): The frame to reduce the resolution of.
        Returns:
            np.ndarray: The reduced resolution frame.
        """
        reduced = (downscale_local_mean(frame, (2, 2, 1))).astype(np.uint8)
        return reduced

    def save_render(self, reduce_res: bool = None):
        """
        Saves the current rendered screen of the emulator as a JPEG image in the renders directory.

        Args:
            reduce_res (bool, optional): Whether to reduce the resolution of the saved image.
                If None, uses the default setting from the config files.
        """
        render_path = os.path.join(
            self.session_path, "renders", f"step_{self.step_count}.jpeg"
        )
        file_makedir(render_path)
        if reduce_res is None:
            reduce_res = self._reduce_video_resolution
        current_frame = self.get_current_frame()
        if reduce_res:
            current_frame = self.reduce_resolution(current_frame)
        plt.imsave(render_path, current_frame[:, :, 0])

    def get_free_video_id(self) -> str:
        """
        Returns a new unique video ID for saving video files.

        Returns:
            str: A new unique video ID.
        """
        base_dir = os.path.join(self.session_path, "videos")
        videos = os.listdir(base_dir) if os.path.exists(base_dir) else []
        # all will be something.mp4, if its int.mp4, get the int
        video_ints = []
        for video in videos:
            if video.endswith(".mp4"):
                video_name = video[:-4]
                if video_name.isdigit():
                    video_ints.append(int(video_name))
        if len(video_ints) == 0:
            return "0.mp4"
        return str(max(video_ints) + 1) + ".mp4"

    def start_video(self, video_id: str = None):
        """
        Starts recording video of the emulator's screen.
        Args:
            video_id (str, optional): Name of the video file to save. If None, a new unique name will be generated.
        """
        if video_id is not None:
            if not isinstance(video_id, str):
                log_error(
                    "video_id must be a string (not digits) if provided.",
                    self._parameters,
                )
            if not video_id.endswith(".mp4"):
                log_error("video_id must end with .mp4 if provided.", self._parameters)
            if os.path.exists(os.path.join(self.session_path, "videos", video_id)):
                log_warn(
                    f"video_id {video_id} already exists. Overwriting...",
                    self._parameters,
                )
        else:
            video_id = self.get_free_video_id()
        base_dir = os.path.join(self.session_path, "videos")
        os.makedirs(base_dir, exist_ok=True)
        video_path = os.path.join(base_dir, f"{video_id}")
        self.close_video()
        self.frame_writer = cv2.VideoWriter(
            video_path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            60,
            (self.output_shape[0], self.output_shape[1]),
            isColor=False,
        )
        self.video_running = True
        log_info(f"\nStarted recording video to: {video_path}\n", self._parameters)

    def check_text_bounds(self, image, text, org, font_face, font_scale, thickness):
        img_h, img_w = image.shape[:2]
        x, y = org

        # Get the width and height of the text box
        # retval is (width, height), baseLine is the y-offset from the bottom
        (text_w, text_h), baseline = cv2.getTextSize(
            text, font_face, font_scale, thickness
        )

        # Check right and top/bottom bounds
        # Note: org (x,y) is the bottom-left corner of the text
        is_within_x = (x + text_w) <= img_w and x >= 0
        is_within_y = (y - text_h) >= 0 and y <= img_h
        return is_within_x and is_within_y, (text_w, text_h)

    def _add_video_text(self, frame: np.ndarray) -> np.ndarray:
        if self._video_text is None:
            return frame
        if self._video_text.strip() == "":
            return frame
        frame = frame.copy()
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottom_left_corner_of_text = (5, frame.shape[0] - 10)
        # check if that section of the frame is too bright, and if so, use black text instead of white
        region = frame[frame.shape[0] - 20 : frame.shape[0], 0:100]
        if np.mean(region) > 200:
            font_color = (0, 0, 0)  # Black color for bright backgrounds
        else:
            font_color = (255, 255, 255)  # White color for dark backgrounds
        scale = 0.5
        fits = self.check_text_bounds(
            frame, self._video_text, bottom_left_corner_of_text, font, scale, 1
        )[0]
        while not fits and scale > 0.05:
            scale -= 0.1
            fits = self.check_text_bounds(
                frame, self._video_text, bottom_left_corner_of_text, font, scale, 1
            )[0]
        line_type = 1
        cv2.putText(
            frame,
            self._video_text,
            bottom_left_corner_of_text,
            font,
            scale,
            font_color,
            line_type,
        )
        return frame

    def add_video_frames(self, frames: np.ndarray):
        """
        Adds a list of frame from the emulator to the video being recorded.
        If video_text is set, it will be added to the bottom left corner of each frame.

        Args:
            frames (np.ndarray): A stack of frames to add to the video. Shape is [n_frames, height, width, channels].
        """

        # frame_size = (current_frame.shape[1], current_frame.shape[0]) # Width, Height, should be equal to self.output_shape
        # Create VideoWriter object
        for frame in frames:
            if self._reduce_video_resolution:
                frame = self.reduce_resolution(frame)
            frame = self._add_video_text(frame)
            self.frame_writer.write(frame)
        return

    def check_if_done(self):
        """
        Checks if the max_steps limit has been reached.
        """
        done = self.step_count >= self.max_steps - 1
        return done

    def close_video(self):
        """
        Closes the video writer and stops recording video.
        """
        if self._full_frame_writer is not None:
            self._full_frame_writer.release()
            self._full_frame_writer = None
        if self._model_frame_writer is not None:
            self._model_frame_writer.release()
            self._model_frame_writer = None
        self.video_running = False

    def close(self) -> StateTracker:
        """
        Closes the emulator and any associated resources.
        If the session directory is empty after closing, it will be deleted.
        """
        self.state_tracker.close()
        self._pyboy.stop(save=False)
        self.close_video()
        self.state_tracker.close()
        # check if session directory is empty, and if so delete it
        if (
            os.path.exists(self.session_path)
            and len(os.listdir(self.session_path)) == 0
        ):
            os.rmdir(self.session_path)
        return self.state_tracker

    def human_play(self, max_steps: int = None):
        """
        Allows a human to play the emulator using keyboard inputs.
        Args:
            max_steps (int, optional): Maximum number of steps to play. Defaults to gameboy_hard_max_steps in configs.
        """
        if max_steps is None:
            max_steps = self._parameters["gameboy_hard_max_steps"]
        log_info(
            "Starting human play mode. Use arrow keys and A(a)/B(s)/Start(enter) buttons to play. Close the window to exit.",
            self._parameters,
        )
        if self.headless:
            log_error(
                "Human play mode requires headless=False. Change the initialization",
                self._parameters,
            )
        self.reset()
        while True:
            self._pyboy.tick(1, True)
            self.state_tracker.step()
            if self.step_count >= max_steps:
                break
        self.close()

    def random_play(self, max_steps: int = None):
        """
        Allows the emulator to play itself using (sort of) random actions.
        Args:
            max_steps (int, optional): Maximum number of steps to play. Defaults to gameboy_hard_max_steps in configs.
        """
        if max_steps is None:
            max_steps = self._parameters["gameboy_random_play_max_steps"]
        log_info("Starting random play mode.", self._parameters)
        self.reset()
        pbar = tqdm(total=max_steps, desc="Random Play Steps")
        allowed_actions = list(LowLevelActions)
        # remove the Start and Select actions from allowed actions to avoid menu spamming.
        allowed_actions.remove(LowLevelActions.PRESS_BUTTON_START)
        while self.step_count < max_steps:
            action = np.random.choice(allowed_actions)
            frames, done = self.step(action)
            pbar.update(1)
            if done:
                break
        pbar.close()
        self.close()
        log_info("Random play mode ended.", self._parameters)

    def _dev_play(self, max_steps: int = None):
        """
        Allows a human to play the emulator using keyboard inputs. Does not route through step function.
        This function continuously reads from the parameters in the configs directory and if it detects a change in the `gameboy_dev_play_stop` parameter, will enter a breakpoint

        Args:
            max_steps (int, optional): Maximum number of steps to play. Defaults to gameboy_hard_max_steps in configs.
        """
        if not hasattr(self.state_parser, "rom_data_path"):
            log_error(
                "Development play mode requires a StateParser with rom_data_path attribute.",
                self._parameters,
            )
        if max_steps is None:
            max_steps = self._parameters["gameboy_hard_max_steps"]
        log_info(
            "Starting human play mode. Use arrow keys and A(a)/B(s)/Start(enter) buttons to play. Close the window to exit. Open configs/gameboy_vars.yaml and set gameboy_dev_play_stop to true to enable development mode.",
            self._parameters,
        )
        if self.headless:
            log_error(
                "Human play mode requires headless=False. Change the initialization",
                self._parameters,
            )
        self.reset()
        valid_regions = []
        unassigned_regions = []
        for region_name, region in self.state_parser.named_screen_regions.items():
            valid_regions.append(region_name)
            if region.multi_targets is None:
                if region.target is None:
                    unassigned_regions.append(region_name)
            else:
                for target_name in region.multi_targets.keys():
                    if region.multi_targets[target_name] is None:
                        unassigned_regions.append((region_name, target_name))
        if len(unassigned_regions) > 0:
            log_warn(
                f"Unassigned regions (target array not set) are: {unassigned_regions}",
                self._parameters,
            )
        while True:
            self._parameters = load_parameters()
            if not self._parameters["gameboy_dev_play_stop"]:
                self._pyboy.tick(1, True)
                self.state_tracker.step()
            else:
                tracker_report = self.state_tracker.report()
                tracker_report["core"].pop("current_frame", None)
                tracker_report["core"].pop("passed_frames", None)
                dev_instructions = f"""
                In development mode.
                Enter 'e' to close the emulator.
                Enter '' to re-enter normal play mode (remember to change gameboy_dev_play_stop back to false in configs or it'll stop again). 
                Enter 'p' to print the current state.
                Enter 'w' to pass a single tick without any action.
                Enter 's <state_name>' to save the current state as a .state file.
                Enter 'l <state_name>' to load a .state file.
                Enter 'c <region_name> <save_name / None if region.target_path is set>' to capture a named region and save it as a .npy file. To enter a multi-target region use the format "c <region_name>,<target_name> <save_name>" (no spaces in between region and target name)
                Enter 'd <None / region_name>' to draw a named region and display the current screen with the region drawn.
                Enter 'b' to enter a breakpoint.
                Valid region names are: {valid_regions}
                Initially unassigned regions (target array not set) were: {unassigned_regions}\n\t Note: This list does not update as you assign targets during this session.
                Current State: 
                """
                log_info(dev_instructions, self._parameters)
                tracker_report.pop("ocr", None)
                log_dict(tracker_report, parameters=self._parameters)
                user_input = input("Dev mode input: ")
                user_input = user_input.lower().strip()
                first_char = user_input[0] if len(user_input) > 0 else ""
                allowed_inputs = ["e", "", "p", "w", "c", "s", "l", "d", "b"]
                if first_char not in allowed_inputs:
                    log_warn(
                        f"Invalid input {user_input}. Valid inputs are: {allowed_inputs}",
                        self._parameters,
                    )
                    continue
                if first_char == "e":
                    log_info("Exiting human play mode.", self._parameters)
                    break
                elif first_char == "":
                    log_info(
                        "Exiting development mode. Resuming normal play.",
                        self._parameters,
                    )
                    continue
                elif first_char == "p":
                    log_info(
                        f"Current State:\n{str(self.state_tracker)}", self._parameters
                    )
                    continue
                elif first_char == "w":
                    self._pyboy.tick(1, True)
                    self.state_tracker.step()
                    continue
                elif first_char == "s" or first_char == "l":
                    parts = user_input.split(" ")
                    if len(parts) != 2:
                        log_warn(f"Invalid input {user_input}.", self._parameters)
                        continue
                    state_name = parts[1]
                    if not state_name.endswith(".state"):
                        state_name = state_name + ".state"
                    state_path = os.path.join(
                        self.state_parser.rom_data_path, "states", state_name
                    )
                    if first_char == "s":
                        if os.path.exists(state_path):
                            confirm_input = input(
                                f"State file {state_path} already exists. Overwrite? (y/n): "
                            )
                            if confirm_input.lower().strip() != "y":
                                log_info("Aborting save state.", self._parameters)
                                continue
                        self.save_state(state_path)
                    else:
                        if not os.path.exists(state_path):
                            log_warn(
                                f"State file {state_path} does not exist. Cannot load.",
                                self._parameters,
                            )
                            continue
                        self.set_init_state(state_path)
                elif first_char == "b":
                    grid_cells = self.state_parser.capture_grid_cells(
                        current_frame=self.get_current_frame(), y_offset=0
                    )
                    breakpoint()
                else:
                    current_frame = self.get_current_frame()
                    # draw it even if c, so we can see what we're capturing
                    save_path = None
                    if first_char == "c":
                        parts = user_input.split(" ")
                        if len(parts) != 3:
                            if len(parts) != 2:
                                log_warn(
                                    f"Invalid input {user_input}.", self._parameters
                                )
                                continue
                            else:
                                region_name = parts[1].split(",")[0]
                                region = self.state_parser.named_screen_regions[
                                    region_name
                                ]
                                if region.multi_targets is None:
                                    save_path = region.target_path
                                else:
                                    if "," not in parts[1]:
                                        log_warn(
                                            f"Region {region_name} is a multi-target region. Specify target",
                                            self._parameters,
                                        )
                                        continue
                                    target_name = parts[1].split(",")[1]
                                    if target_name not in region.multi_target_paths:
                                        log_warn(
                                            f"Target name {target_name} not found in region {region_name} with targets {region.multi_targets.keys()}.",
                                            self._parameters,
                                        )
                                        continue
                                    save_path = region.multi_target_paths[target_name]
                                if save_path is None:
                                    log_warn(
                                        f"Region {region_name} does not have a target path specified. Please provide a save name.",
                                        self._parameters,
                                    )
                                    continue
                        else:
                            save_name = parts[2]
                            if not save_name.endswith(".npy"):
                                save_name = save_name + ".npy"
                                save_path = os.path.join(
                                    self.state_parser.rom_data_path,
                                    "captures",
                                    save_name,
                                )
                        file_makedir(save_path)
                    elif first_char == "d":
                        parts = user_input.split(" ")
                        if len(parts) == 2:
                            region_name = parts[1].split(",")[
                                0
                            ]  # Shouldn't need but anyway.
                        elif len(parts) == 1:
                            region_name = "Full Screen"
                        else:
                            log_warn(f"Invalid input {user_input}.", self._parameters)
                            continue
                    if region_name == "Full Screen":
                        drawn_frame = current_frame  # self.state_parser.draw_grid_overlay(current_frame)
                    else:
                        drawn_frame = self.state_parser.draw_named_region(
                            current_frame, region_name
                        )
                    plt.imshow(drawn_frame[:, :, 0], cmap="gray")
                    plt.title(f"Region: {region_name}")
                    plt.show()
                    if first_char == "c":
                        captured_region = self.state_parser.capture_named_region(
                            current_frame, region_name
                        )
                        plt.imshow(captured_region[:, :, 0], cmap="gray")
                        plt.title(f"Captured Region: {region_name}")
                        plt.show()
                        existing_file = os.path.exists(save_path)
                        existing_str = (
                            ""
                            if not existing_file
                            else " (will overwrite existing file)"
                        )
                        confirmation_input = input(
                            f"Save captured region {region_name} to {save_path}? (y/n) {existing_str}: "
                        )
                        if confirmation_input.lower().strip() != "y":
                            log_info("Aborting capture region.", self._parameters)
                            continue
                        np.save(save_path, captured_region)
                        log_info(
                            f"Saved captured region {region_name} to {save_path}",
                            self._parameters,
                        )
            if self.step_count >= max_steps:
                break
        tracker = self.close()
        log_info("Human play mode ended.", self._parameters)
        # log_dict(tracker.report_final(), parameters=self._parameters)

    def save_state(self, state_path: str):
        """
        Saves the current state of the emulator to a .state file.
        Args:
            state_path (str): Path to save the .state file.

        """
        if not state_path.endswith(".state"):
            state_path = state_path + ".state"
        file_makedir(state_path)
        with open(state_path, "wb") as f:
            self._pyboy.save_state(f)
        log_info(f"Saved state to {state_path}", self._parameters)

    def _sav_to_state(self, sav_file: Optional[str], state_file: str):
        """
        Loads a .sav file into the emulator and saves the corresponding .state file.
        Use this if you want to manually create .sav files and convert them to .state files for use as initial states.
        Requires `_open_to_first_state` to be implemented in the subclass to get past opening menus.

        Args:
            save_file (str or None): Path to the .sav file to load. If None, looks for a .sav file in the same directory as the ROM with the same base name.
            state_file (str): Path to save the .state file
        """
        log_info(
            "Trying to find .sav file and convert to .state file. This is a breaking operation, so the program will terminate after its completion.",
            self._parameters,
        )
        if sav_file is not None:
            expected_sav = sav_file
        else:
            if ".gbc" in self._gb_path:
                expected_sav = self._gb_path.replace(".gbc", ".sav")
            else:
                expected_sav = self._gb_path.replace(".gb", ".sav")
        if not os.path.exists(expected_sav):
            log_error(
                f"Expected .sav file at {expected_sav} to convert to .state file, but it does not exist.",
                self._parameters,
            )
        if state_file is None or state_file == "":
            log_error(
                "You must provide a state_file to save the .state file.",
                self._parameters,
            )
        if not state_file.endswith(".state"):
            state_file = state_file + ".state"
        if os.path.exists(state_file):
            log_error(
                f"state_file {state_file} already exists. Please provide a new path to avoid overwriting.",
                self._parameters,
            )
        file_makedir(state_file)
        # copy the .sav file to self._gb_path.gb.ram file
        save_destination = self._gb_path.replace(".gb", ".gb.ram")
        shutil.copyfile(expected_sav, save_destination)
        self.close()
        self._pyboy = PyBoy(
            self._gb_path,
            window="null",
        )
        self._pyboy.set_emulation_speed(0)
        self._open_to_first_state()
        self.save_state(state_file)
        self._pyboy.stop(save=False)
        log_info(
            "State saved successfully. Exiting now to avoid issues ...",
            self._parameters,
        )
        # remove the .gb.ram file
        if os.path.exists(save_destination):
            os.remove(save_destination)
        sys.exit(0)

    def _open_to_first_state(self):
        """
        Presses buttons on the emulator to get past the opening menus and into the game itself.
        You don't really need to implement this method, but if you do, you can use _sav_to_state to create state files from mGBA sav files.
        """
        raise NotImplementedError

    def get_env_variant(self) -> str:
        """
        Returns a string identifier for the particular environment variant being used.

        :return: string name identifier of the particular env e.g. PokemonRed
        """
        return self.game


def bytes_to_padded_hex_string(integer_value):
    """
    Converts a bytes object into a padded, '0x'-prefixed hexadecimal string.
    """
    # 1. Convert the bytes object back into an integer
    # Assumes big-endian order for the example '0x00a' -> 10
    # 2. Format the integer into a string with padding and the '0x' prefix
    # The 'x' specifier for hex, '#' adds '0x', '04' pads to 4 hex characters total
    # (not including the '0x' prefix for simple formatters like this, but managing width)

    # A robust approach to match your exact output '0x00a':
    # You generally want enough width for your bytes. b'\n' is 1 byte, 2 hex chars.

    return f"0x{integer_value:04x}"  # {0:04x} pads to 4 digits specifically
