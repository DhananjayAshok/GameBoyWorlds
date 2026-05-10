from typing import Optional

from gameboy_worlds.emulation.harry_potter.parsers import (
    HarryPotterPhilosophersStoneParser,
    HarryPotterChamberOfSecretsParser,
)
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


# ============================================================
# Task 14: find_hagrid_vault_test
# ============================================================

class FindHagridVaultTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "vault_entry_cutscene_area"
    _TERMINATION_TARGET_NAME = "vault_entry_cutscene"


class NavigateToHagridSubgoal(RegionMatchSubGoal):
    NAME = "navigate_to_hagrid"
    _NAMED_REGION = "post_boss_hagrid_area"
    _TARGET_NAME = "navigate_to_hagrid"


# ============================================================
# Madam Malkin split tasks
# ============================================================

class EnterMalkinsTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "inside_malkins_area"
    _TERMINATION_TARGET_NAME = "inside_malkins"


class OpenMalkinsBuyMenuTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "robes_menu_area"
    _TERMINATION_TARGET_NAME = "malkins_buy_menu_open"


class SelectRobesTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "robes_menu_area"
    _TERMINATION_TARGET_NAME = "selected_robes"


class ConfirmRobesPurchaseTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "robes_purchase_area"
    _TERMINATION_TARGET_NAME = "confirm_robes_purchase"


class OutsideMalkinsSubgoal(RegionMatchSubGoal):
    NAME = "outside_malkins"
    _NAMED_REGION = "outside_malkins_area"
    _TARGET_NAME = "outside_malkins"


# ============================================================
# Flourish & Blotts split tasks
# ============================================================

class EnterFlourishBlottsTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "inside_flourish_blotts_area"
    _TERMINATION_TARGET_NAME = "inside_flourish_blotts"


class OutsideFlourishBlottsSubgoal(RegionMatchSubGoal):
    NAME = "outside_flourish_blotts"
    _NAMED_REGION = "outside_flourish_blotts_area"
    _TARGET_NAME = "outside_flourish_blotts"


class BuyBooksTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "books_received_area"
    _TERMINATION_TARGET_NAME = "books_received"


class TalkToFlourishClerkSubgoal(RegionMatchSubGoal):
    NAME = "talk_to_flourish_clerk"
    _NAMED_REGION = "dialogue_box_full"
    _TARGET_NAME = "talk_to_flourish_clerk"


# ============================================================
# Apothecary split tasks
# ============================================================

class EnterApothecaryTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "inside_apothecary_area"
    _TERMINATION_TARGET_NAME = "inside_apothecary"


class BuyPotionKitTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "apothecary_purchase_area"
    _TERMINATION_TARGET_NAME = "confirm_apothecary_purchase"


class OutsideApothecarySubgoal(RegionMatchSubGoal):
    NAME = "outside_apothecary"
    _NAMED_REGION = "outside_apothecary_area"
    _TARGET_NAME = "outside_apothecary"


class ApothecaryBuyMenuOpenSubgoal(RegionMatchSubGoal):
    NAME = "apothecary_buy_menu_open"
    _NAMED_REGION = "apothecary_menu_area"
    _TARGET_NAME = "apothecary_buy_menu_open"


# ============================================================
# Cauldron shop tasks
# ============================================================

class EnterCauldronShopTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "inside_cauldron_shop_area"
    _TERMINATION_TARGET_NAME = "inside_cauldron_shop"


class BuyCauldronTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "cauldron_purchase_area"
    _TERMINATION_TARGET_NAME = "confirm_cauldron_purchase"


class OutsideCauldronShopSubgoal(RegionMatchSubGoal):
    NAME = "outside_cauldron_shop"
    _NAMED_REGION = "outside_cauldron_shop_area"
    _TARGET_NAME = "outside_cauldron_shop"


class CauldronBuyMenuOpenSubgoal(RegionMatchSubGoal):
    NAME = "cauldron_buy_menu_open"
    _NAMED_REGION = "cauldron_menu_area"
    _TARGET_NAME = "cauldron_buy_menu_open"


# ============================================================
# Sugarplums Sweets filler tasks
# ============================================================

class EnterSugarplumsTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "inside_sugarplums_area"
    _TERMINATION_TARGET_NAME = "inside_sugarplums"


class OpenSugarplumsBuyMenuTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "sugarplums_menu_area"
    _TERMINATION_TARGET_NAME = "sugarplums_buy_menu_open"


class OutsideSugarplumsSubgoal(RegionMatchSubGoal):
    NAME = "outside_sugarplums"
    _NAMED_REGION = "outside_sugarplums_area"
    _TARGET_NAME = "outside_sugarplums"


# ============================================================
# Talk to Hagrid in Diagon Alley
# ============================================================

class TalkToHagridDiagonTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "dialogue_box_full"
    _TERMINATION_TARGET_NAME = "hagrid_diagon_dialogue"


class InsideMalkinsSubgoal(RegionMatchSubGoal):
    NAME = "inside_malkins"
    _NAMED_REGION = "inside_malkins_area"
    _TARGET_NAME = "inside_malkins"


class SelectedRobesSubgoal(RegionMatchSubGoal):
    NAME = "selected_robes"
    _NAMED_REGION = "robes_menu_area"
    _TARGET_NAME = "selected_robes"


class ConfirmRobesPurchaseSubgoal(RegionMatchSubGoal):
    NAME = "confirm_robes_purchase"
    _NAMED_REGION = "robes_purchase_area"
    _TARGET_NAME = "confirm_robes_purchase"


# ============================================================
# CoS Task 1: find_dobby_test
# ============================================================

class FindDobbyTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "dobby_dialogue_area"
    _TERMINATION_TARGET_NAME = "dobby_dialogue_started"


class FindDobbySubgoal(RegionMatchSubGoal):
    NAME = "find_dobby"
    _NAMED_REGION = "dobby_bed_area"
    _TARGET_NAME = "find_dobby"


# ============================================================
# CoS Task 2: select_card_deck_cos_test
# ============================================================

class SelectCardDeckCosTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "choose_deck_cos_area"
    _TERMINATION_TARGET_NAME = "deck_selected_cos"


# ============================================================
# CoS Task 3: board_flying_car_test
# ============================================================

class BoardFlyingCarTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "flying_car_cutscene_area"
    _TERMINATION_TARGET_NAME = "flying_car_departure"


class TalkToRonCosSubgoal(RegionMatchSubGoal):
    NAME = "talk_to_ron"
    _NAMED_REGION = "talk_to_ron_cos_area"
    _TARGET_NAME = "talk_to_ron"


# ============================================================
# CoS Task 4: enter_burrow_test
# ============================================================

class EnterBurrowTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "mrs_weasley_dialogue_area"
    _TERMINATION_TARGET_NAME = "mrs_weasley_table_dialogue"


class OutsideBurrowAfterCutsceneSubgoal(RegionMatchSubGoal):
    NAME = "outside_burrow_after_cutscene"
    _NAMED_REGION = "burrow_arrival_dialogue_area"
    _TARGET_NAME = "outside_burrow_after_cutscene"


# ============================================================
# CoS Task 5: enter_battle_cos_test
# ============================================================

class EnterBattleCosTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "battle_menu_cos_area"
    _TERMINATION_TARGET_NAME = "in_battle_cos"


# ============================================================
# Burrow room navigation tasks (CoS)
# ============================================================

class EnterPercyRoomTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "percy_room_area"
    _TERMINATION_TARGET_NAME = "inside_percy_room"


class EnterGinnyRoomTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "ginny_room_area"
    _TERMINATION_TARGET_NAME = "inside_ginny_room"


class EnterParentsRoomTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "parents_room_area"
    _TERMINATION_TARGET_NAME = "inside_parents_room"


class EnterFredGeorgeRoomTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "fred_george_room_area"
    _TERMINATION_TARGET_NAME = "inside_fred_george_room"


class EnterRonsRoomTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "rons_room_area"
    _TERMINATION_TARGET_NAME = "inside_rons_room"


class TalkToRonBurrowTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "dialogue_box_full"
    _TERMINATION_TARGET_NAME = "talk_to_ron_burrow"


class EnterKitchenBurrowTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "dialogue_box_full"
    _TERMINATION_TARGET_NAME = "talk_to_mom_kitchen"


class EnterBurrowGardenTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "dialogue_box_full"
    _TERMINATION_TARGET_NAME = "talk_to_ron_garden"


class OutsideGardenDoorSubgoal(RegionMatchSubGoal):
    NAME = "outside_garden_door"
    _NAMED_REGION = "garden_door_area"
    _TARGET_NAME = "outside_garden_door"
