from poke_worlds.emulation.emulator import Emulator, LowLevelActions
from poke_worlds.emulation.deja_vu.parsers import DejaVuStateParser, AgentState
from poke_worlds.emulation.deja_vu.trackers import CoreDejaVuTracker
from poke_worlds.utils import log_error
from typing import Tuple
import numpy as np


class DejaVuEmulator(Emulator):
    """
    Deja Vu-specific emulator adapter.
    
    Handles Deja Vu game-specific logic:
    - Menu navigation and investigation system
    - Dialogue and clue collection
    - Puzzle-solving phases
    """

    REQUIRED_STATE_PARSER = DejaVuStateParser
    REQUIRED_STATE_TRACKER = CoreDejaVuTracker
    _MAXIMUM_DIALOGUE_PRESSES = 2000  # For now set a crazy high value
    """ Maximum number of times the agent will click B to get through a dialogue. """
    _SKIP_DIALOGUE = False
    """ Whether to auto skip dialogue by clicking B repeatedly until we are no longer in dialogue."""

    def step(self, action=None) -> Tuple[np.ndarray, bool]:
        """
        Execute one game step with Deja Vu-specific handling.
        
        Handles dialogue auto-skip to speed up gameplay while preserving investigation mechanics.
        
        Args:
            action: The action to execute (can be None for no action)
            
        Returns:
            Tuple of (frames, done): frames from the step, and whether episode ended
        """
        frames, done = super().step(action)
        self.state_parser: DejaVuStateParser
        current_frame = self.get_current_frame()
        
        all_next_frames = [frames]
        if self._SKIP_DIALOGUE:
            # Auto-skip dialogue to accelerate game progression
            # This allows the agent to move through story elements faster
            # For Deja Vu, dialogue is critical to story progression and investigations, so we initialize the auto-skip action to false
            current_state = self.state_parser.get_agent_state(current_frame)
            n_clicks = 0
            # Clicks through any dialogue popups
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
