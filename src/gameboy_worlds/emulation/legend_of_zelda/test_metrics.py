from typing import Optional

import numpy as np

from gameboy_worlds.emulation.tracker import TerminationMetric
from gameboy_worlds.emulation.legend_of_zelda.parsers import (
    LegendOfZeldaLinksAwakeningParser,
)

class ZeldaRegionMatchTerminationOnlyMetric(TerminationMetric):
    REQUIRED_PARSER = LegendOfZeldaLinksAwakeningParser
    _TERMINATION_NAMED_REGION = None

    def determine_terminated(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ) -> bool:
        if self._TERMINATION_NAMED_REGION is None:
            raise ValueError("_TERMINATION_NAMED_REGION must be set.")

        all_frames = [current_frame]
        if recent_frames is not None:
            all_frames = recent_frames

        for frame in all_frames:
            self.state_parser: LegendOfZeldaLinksAwakeningParser
            matched = self.state_parser.named_region_matches_target(
                frame, self._TERMINATION_NAMED_REGION
            )
            if matched:
                return True
        return False
    
class ZeldaRegionAndStateTerminationMetric(TerminationMetric):
    REQUIRED_PARSER = LegendOfZeldaLinksAwakeningParser
    _TERMINATION_NAMED_REGION = None
    _TERMINATION_AGENT_STATE = None

    def determine_terminated(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ) -> bool:
        if self._TERMINATION_NAMED_REGION is None:
            raise ValueError("_TERMINATION_NAMED_REGION must be set.")
        if self._TERMINATION_AGENT_STATE is None:
            raise ValueError("_TERMINATION_AGENT_STATE must be set.")

        all_frames = [current_frame]
        if recent_frames is not None:
            all_frames = recent_frames

        for frame in all_frames:
            self.state_parser: LegendOfZeldaLinksAwakeningParser
            region_matched = self.state_parser.named_region_matches_target(
                frame, self._TERMINATION_NAMED_REGION
            )
            state_matched = (
                self.state_parser.get_agent_state(frame)
                == self._TERMINATION_AGENT_STATE
            )
            if region_matched and state_matched:
                return True
        return False
    
class ZeldaMultiRegionTerminationOnlyMetric(TerminationMetric):
    REQUIRED_PARSER = LegendOfZeldaLinksAwakeningParser
    _TERMINATION_NAMED_REGIONS = []

    def determine_terminated(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ) -> bool:
        if len(self._TERMINATION_NAMED_REGIONS) == 0:
            raise ValueError("_TERMINATION_NAMED_REGIONS must be set.")

        all_frames = [current_frame]
        if recent_frames is not None:
            all_frames = recent_frames

        for frame in all_frames:
            self.state_parser: LegendOfZeldaLinksAwakeningParser
            all_matched = True

            for region_name in self._TERMINATION_NAMED_REGIONS:
                matched = self.state_parser.named_region_matches_target(
                    frame, region_name
                )
                if not matched:
                    all_matched = False
                    break

            if all_matched:
                return True

        return False
    
class ToronboShorePickupSwordTerminateMetric(ZeldaRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "equipped_action_2"

class ShieldEquippedTerminateMetric(ZeldaRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "shield_tracker"

class OutsideTarinHouseTerminateMetric(ZeldaRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "outside_tarinhouse_tracker"

class OpenInventoryTerminateMetric(ZeldaRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "health_bar_top"

class TalkToKidTerminateMetric(ZeldaRegionAndStateTerminationMetric):
    _TERMINATION_NAMED_REGION = "kid_screen_tracker"
    _TERMINATION_AGENT_STATE = "in_dialogue"

class ReadSignboardTerminateMetric(ZeldaRegionAndStateTerminationMetric):
    _TERMINATION_NAMED_REGION = "signboard"
    _TERMINATION_AGENT_STATE = "in_dialogue"

class GoInsideShopTerminateMetric(ZeldaRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "cash_counter_tracker"

class MakeCallTerminateMetric(ZeldaMultiRegionTerminationOnlyMetric):
    _TERMINATION_NAMED_REGIONS = [
        "telephone_tracker",
        "telephone_speech_tracker",
    ]

class EnterDarkForestTerminateMetric(ZeldaRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "brave_keyword_tracker"


class OpenChestTerminateMetric(ZeldaRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "open_chest_tracker"
