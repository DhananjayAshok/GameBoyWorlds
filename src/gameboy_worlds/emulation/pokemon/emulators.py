from gameboy_worlds.emulation.emulator import Emulator, LowLevelActions
from gameboy_worlds.emulation.pokemon.parsers import PokemonStateParser, AgentState
from gameboy_worlds.emulation.pokemon.trackers import CorePokemonTracker
from gameboy_worlds.emulation.pokemon.screen import is_blank, is_fading
from gameboy_worlds.utils import log_error
from typing import Optional, Tuple
import numpy as np


class PokemonEmulator(Emulator):
    """
    Almost the exact same as Emulator, but forces the agent to not mess with the menu options cursor. Also auto skips naming screens, and waits out screen fades so that no action ends on a blank or half-faded screen.
    """

    REQUIRED_STATE_PARSER = PokemonStateParser
    REQUIRED_STATE_TRACKER = CorePokemonTracker
    _MAXIMUM_DIALOGUE_PRESSES = 2000  # For now set a crazy high value
    """ Maximum number of times the agent will click B to get through a dialogue. """
    _SKIP_DIALOGUE = False
    """ Whether to auto skip dialogue by clicking B repeatedly until we are no longer in dialogue."""
    _FADE_CHECK_TICKS = 4
    """ Ticks between frames while waiting out a fade. """
    _FADE_CALM_CHECKS = 3
    """ A fade is over once this many checks in a row see neither a blank screen nor a fade step. A fade holds each shade for up to ~8 ticks, so these checks must span longer than that. """
    _FADE_MAX_TICKS = 240
    """ Maximum number of ticks to wait for a fade to end. """
    _last_frame: Optional[np.ndarray] = None
    """ The last frame returned by run_action_on_emulator, to compare the next action's first frame against. """

    def reset(self, new_init_state: str = None):
        super().reset(new_init_state)
        self._last_frame = None

    def run_action_on_emulator(
        self, action: LowLevelActions = None
    ) -> Optional[np.ndarray]:
        """
        Performs the action as Emulator does. If the screen is then in a fade, keeps the emulator running with no buttons pressed until the fade is over.

        Args:
            action (LowLevelActions): Lowest level action to perform on the emulator.
        Returns:
            Optional[np.ndarray]: The stack of frames that passed while performing the action and waiting out any fade.
        """
        frames = super().run_action_on_emulator(action)
        before = frames[-2] if len(frames) > 1 else self._last_frame
        if is_fading(frames[-1], before) or (before is not None and is_blank(before)):
            waited = self._wait_out_fade(frames[-1])
            if self.save_video and self.video_writer.video_running:
                self.video_writer.add_video_frames(waited)
            frames = np.concatenate([frames, waited], axis=0)
        self._last_frame = frames[-1]
        return frames

    def _wait_out_fade(self, last_frame: np.ndarray) -> np.ndarray:
        waited, calm, previous = [], 0, last_frame
        for _ in range(self._FADE_MAX_TICKS // self._FADE_CHECK_TICKS):
            self._pyboy.tick(self._FADE_CHECK_TICKS, True)
            current = self.get_current_frame()
            waited.append(current)
            fading = is_blank(previous) or is_fading(current, previous)
            calm = 0 if fading else calm + 1
            if calm >= self._FADE_CALM_CHECKS:
                break
            previous = current
        return np.stack(waited)

    def step(self, action=None) -> Tuple[np.ndarray, bool]:
        frames, done = super().step(action)
        self.state_parser: PokemonStateParser
        current_frame = self.get_current_frame()
        if self.state_parser.is_hovering_over_options_in_menu(current_frame):
            # WARNING: see the state parser method for details, but this currently does not work before the agent gets the pokedex
            # force the agent to click the up button to get off the options
            self.run_action_on_emulator(LowLevelActions.PRESS_ARROW_UP)
        all_next_frames = [frames]
        # If we are on a naming screen, just don't pick a name and get out.
        if self.state_parser.named_region_matches_target(
            current_frame, name="name_entity_top_left"
        ):
            # then enter and get out
            next_frames = self.run_action_on_emulator(
                LowLevelActions.PRESS_BUTTON_START
            )
            all_next_frames.append(next_frames)
            next_frames = self.run_action_on_emulator(LowLevelActions.PRESS_BUTTON_A)
            all_next_frames.append(next_frames)
        if (
            self._SKIP_DIALOGUE
        ):  # Make this True to auto skip dialogue and accumilate it into the frames returned.
            current_state = self.state_parser.get_agent_state(current_frame)
            n_clicks = 0
            # Clicks through any dialogue popups.
            while (
                n_clicks < self._MAXIMUM_DIALOGUE_PRESSES
            ) and current_state == AgentState.IN_DIALOGUE:
                next_frames = self.run_action_on_emulator(
                    LowLevelActions.PRESS_BUTTON_B
                )
                current_state = self.state_parser.get_agent_state(next_frames[-1])
                all_next_frames.append(next_frames)
                n_clicks += 1
        if len(all_next_frames) > 1:
            frames = np.concatenate(all_next_frames)
            self._update_listeners_after_actions(
                self._get_unique_frames(frames[1:])
            )  # Skip the first frame as that is already counted
            frames = self._get_unique_frames(frames)
        return frames, done

    def _open_to_first_state(self):
        self._pyboy.tick(10000, False)  # get to opening menu
        self.run_action_on_emulator(
            LowLevelActions.PRESS_BUTTON_A
        )  # press A to get past opening menu
        self._pyboy.tick(1000, False)  # wait for load
        self.run_action_on_emulator(
            LowLevelActions.PRESS_BUTTON_A
        )  # press A to load game
        self._pyboy.tick(1000, False)  # wait for file select
        self.run_action_on_emulator(
            LowLevelActions.PRESS_BUTTON_A
        )  # press A to confirm load
        self._pyboy.tick(5000, False)  # wait for game to load
