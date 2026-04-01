from typing import Optional

import numpy as np

from gameboy_worlds.emulation.tracker import TerminationMetric
from gameboy_worlds.emulation.legend_of_zelda.parsers import (
    LegendOfZeldaLinksAwakeningParser,
)


class ToronboShorePickupSwordTerminateMetric(TerminationMetric):
    REQUIRED_PARSER = LegendOfZeldaLinksAwakeningParser

    def determine_terminated(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ) -> bool:
        all_frames = [current_frame]
        if recent_frames is not None:
            all_frames = recent_frames

        for frame in all_frames:
            self.state_parser: LegendOfZeldaLinksAwakeningParser
            matched = self.state_parser.named_region_matches_target(
                #frame, "owl_tracker"
                frame, "equipped_action_2"
            )
            #need to change this as is in dialogue is not a good way to check if a task has been done or not
            if matched:
                return True
        return False


class ShieldEquippedTerminateMetric(TerminationMetric):
    REQUIRED_PARSER = LegendOfZeldaLinksAwakeningParser

    def determine_terminated(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ) -> bool:
        all_frames = [current_frame]
        if recent_frames is not None:
            all_frames = recent_frames

        for frame in all_frames:
            self.state_parser: LegendOfZeldaLinksAwakeningParser
            matched = self.state_parser.named_region_matches_target(
                frame, "shield_tracker"
            )
            if matched:
                return True
        return False