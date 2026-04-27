from typing import Optional

from gameboy_worlds.emulation.harrypotter.parsers import HarryPotterPhilosophersStoneParser
from gameboy_worlds.emulation.tracker import (
    TerminationMetric,
    RegionMatchTerminationMetric,
    RegionMatchSubGoal,
)
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


class OllivandersInteriorTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "ollivanders_area"
    _TERMINATION_TARGET_NAME = "ollivanders_interior"


class OutsideOllivandersSubgoal(RegionMatchSubGoal):
    NAME = "outside_ollivanders_door"
    _NAMED_REGION = "ollivanders_entrance"
    _TARGET_NAME = "outside_ollivanders_door"


class GetWandTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "wand_received_text"
    _TERMINATION_TARGET_NAME = "wand_received"


class TalkToOllivanderSubgoal(RegionMatchSubGoal):
    NAME = "talk_to_ollivander"
    _NAMED_REGION = "wand_dialogue_area"
    _TARGET_NAME = "talk_to_ollivander"


class ReceiveFolioMagiTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "choose_deck_text"
    _TERMINATION_TARGET_NAME = "choose_deck_shown"


class BoyApproachesSubgoal(RegionMatchSubGoal):
    NAME = "boy_approaches"
    _NAMED_REGION = "folio_boy_area"
    _TARGET_NAME = "boy_approaches"


class SelectCardDeckTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "deck_reward_icon"
    _TERMINATION_TARGET_NAME = "deck_selected"


class CardOptionsShownSubgoal(RegionMatchSubGoal):
    NAME = "card_options_shown"
    _NAMED_REGION = "choose_deck_text"
    _TARGET_NAME = "choose_deck_shown"


class GringottsInteriorTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "gringotts_interior_area"
    _TERMINATION_TARGET_NAME = "gringotts_interior"


class OutsideGringottsSubgoal(RegionMatchSubGoal):
    NAME = "outside_gringotts_door"
    _NAMED_REGION = "gringotts_entrance"
    _TARGET_NAME = "outside_gringotts_door"


class TalkHagridGringottsTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "vault_interior"
    _TERMINATION_TARGET_NAME = "hagrid_vault_dialogue"


class FindHagridGringottsSubgoal(RegionMatchSubGoal):
    NAME = "find_hagrid_gringotts"
    _NAMED_REGION = "hagrid_gringotts_area"
    _TARGET_NAME = "find_hagrid_gringotts"


class GainLevelTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "level_up_text"
    _TERMINATION_TARGET_NAME = "gained_new_level"


class GainSpellTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "spell_level_text"
    _TERMINATION_TARGET_NAME = "gained_new_spell"


class WinBattleTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "battle_reward_bar"
    _TERMINATION_TARGET_NAME = "battle_won"


class FindBossRatSubgoal(RegionMatchSubGoal):
    NAME = "boss_rat_found"
    _NAMED_REGION = "boss_rat_area"
    _TARGET_NAME = "boss_rat_found"
