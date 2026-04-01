from typing import Optional

from gameboy_worlds.emulation.harrypotter.parsers import HarryPotterPhilosophersStoneParser
from gameboy_worlds.emulation.tracker import TerminationMetric
import numpy as np


class PotionsShopTerminateMetric(TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser

    def determine_terminated(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ) -> bool:
        all_frames = [current_frame]
        if recent_frames is not None:
            all_frames = recent_frames
        for frame in all_frames:
            matches = self.state_parser.named_region_matches_target(
                frame, "potions_shop_shelf"
            )
            if matches:
                return True
        return False
