from typing import Optional

import numpy as np

from gameboy_worlds.emulation.runes_of_virtue_1.parsers import RunesOfVirtue1Parser
from gameboy_worlds.emulation.tracker import TerminationMetric


class OpenMenuTerminateMetric(TerminationMetric):
    """Terminates the episode when the player opens the inventory menu."""

    REQUIRED_PARSER = RunesOfVirtue1Parser

    def determine_terminated(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ) -> bool:
        all_frames = [current_frame]
        if recent_frames is not None:
            all_frames = recent_frames
        for frame in all_frames:
            self.state_parser: RunesOfVirtue1Parser
            in_menu = self.state_parser.named_region_matches_target(
                frame, "menu_indicator"
            )
            if in_menu:
                return True
        return False
