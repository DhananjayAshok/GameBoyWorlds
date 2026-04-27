from typing import Optional

import numpy as np

from gameboy_worlds.emulation.tracker import TerminationMetric
from gameboy_worlds.emulation.legend_of_zelda.parsers import (
    LegendOfZeldaLinksAwakeningParser,
    LegendOfZeldaTheOracleOfSeasonsParser
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

class MakeCall2TerminateMetric(ZeldaRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "bring_keyword_tracker"


class SkeletonHouseTerminateMetric(ZeldaRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "skeleton_tracker"


class UndergroundTerminateMetric(ZeldaRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "skeleton2_tracker"


class DiamondKidTalkTerminateMetric(ZeldaRegionAndStateTerminationMetric):
    _TERMINATION_NAMED_REGION = "diamond_tracker"
    _TERMINATION_AGENT_STATE = "in_dialogue"


class InsideHouseTerminateMetric(ZeldaRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "stool"


class PotRoomTerminateMetric(ZeldaRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "char_onstairs"


class PondTerminateMetric(ZeldaRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "pond"


class WeirdTunnelInsideTerminateMetric(ZeldaRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "witch_tracker"


class WitchTalkTerminateMetric(ZeldaRegionAndStateTerminationMetric):
    _TERMINATION_NAMED_REGION = "pots_tracker"
    _TERMINATION_AGENT_STATE = "in_dialogue"


class PotholesSignboardReadTerminateMetric(ZeldaRegionAndStateTerminationMetric):
    _TERMINATION_NAMED_REGION = "signboard_tracker"
    _TERMINATION_AGENT_STATE = "in_dialogue"

#oracle
class OracleRegionMatchTerminationOnlyMetric(ZeldaRegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = LegendOfZeldaTheOracleOfSeasonsParser


class OracleRegionAndStateTerminationMetric(ZeldaRegionAndStateTerminationMetric):
    REQUIRED_PARSER = LegendOfZeldaTheOracleOfSeasonsParser


class OracleAnyRegionAndStateTerminationMetric(TerminationMetric):
    REQUIRED_PARSER = LegendOfZeldaTheOracleOfSeasonsParser
    _TERMINATION_NAMED_REGIONS = []
    _TERMINATION_AGENT_STATE = None

    def determine_terminated(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ) -> bool:
        if len(self._TERMINATION_NAMED_REGIONS) == 0:
            raise ValueError("_TERMINATION_NAMED_REGIONS must be set.")
        if self._TERMINATION_AGENT_STATE is None:
            raise ValueError("_TERMINATION_AGENT_STATE must be set.")

        all_frames = [current_frame]
        if recent_frames is not None:
            all_frames = recent_frames

        for frame in all_frames:
            self.state_parser: LegendOfZeldaTheOracleOfSeasonsParser

            state_matched = (
                self.state_parser.get_agent_state(frame)
                == self._TERMINATION_AGENT_STATE
            )
            if not state_matched:
                continue

            for region_name in self._TERMINATION_NAMED_REGIONS:
                if self.state_parser.named_region_matches_target(frame, region_name):
                    return True

        return False


class OracleOtherPeopleTerminateMetric(OracleRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "beer_guy_tracker"


class OracleGirlTalkTerminateMetric(OracleRegionAndStateTerminationMetric):
    _TERMINATION_NAMED_REGION = "red_edges"
    _TERMINATION_AGENT_STATE = "in_dialogue"


class OracleJumpingTerminateMetric(OracleRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "after_jump"


class OracleFarmerTalkTerminateMetric(OracleRegionAndStateTerminationMetric):
    _TERMINATION_NAMED_REGION = "flowers"
    _TERMINATION_AGENT_STATE = "in_dialogue"


class OracleLibraryTerminateMetric(OracleRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "books"


class OracleParrotTalkTerminateMetric(OracleAnyRegionAndStateTerminationMetric):
    _TERMINATION_NAMED_REGIONS = ["books", "door"]
    _TERMINATION_AGENT_STATE = "in_dialogue"


class OracleFallTerminateMetric(OracleRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "edge_character"


class OracleStairsTerminateMetric(OracleRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "char_onstairs"


class OracleSignboardReadTerminateMetric(OracleRegionAndStateTerminationMetric):
    _TERMINATION_NAMED_REGION = "bush"
    _TERMINATION_AGENT_STATE = "in_dialogue"


class OracleShopInsideTerminateMetric(OracleRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "clocks"


class OracleShopPersonTalkTerminateMetric(OracleRegionAndStateTerminationMetric):
    _TERMINATION_NAMED_REGION = "clocks"
    _TERMINATION_AGENT_STATE = "in_dialogue"


class OracleGirlHouseTerminateMetric(OracleRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "fireplace"


class OraclePotInteractionTerminateMetric(OracleRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "oof_its_heavy"


class OracleInsideTunnelTerminateMetric(OracleRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "green_rock_tracker"


class OracleArtistTalkTerminateMetric(OracleRegionAndStateTerminationMetric):
    _TERMINATION_NAMED_REGION = "rock"
    _TERMINATION_AGENT_STATE = "in_dialogue"


class OracleChickenHouseTerminateMetric(OracleRegionMatchTerminationOnlyMetric):
    _TERMINATION_NAMED_REGION = "almirah"
