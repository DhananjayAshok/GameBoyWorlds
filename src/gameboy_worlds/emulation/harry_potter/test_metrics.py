from typing import Optional

from gameboy_worlds.emulation.harry_potter.parsers import (
    HarryPotterPhilosophersStoneParser,
    HarryPotterChamberOfSecretsParser,
)
from gameboy_worlds.emulation.tracker import (
    TerminationMetric,
    RegionMatchTerminationMetric,
    RegionMatchTerminationOnlyMetric,
    RegionMatchSubGoal,
    AnyRegionMatchSubGoal,
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


class ReenterGringottsSubgoal(RegionMatchSubGoal):
    NAME = "reenter_gringotts"
    _NAMED_REGION = "full_screen_area"
    _TARGET_NAME = "reenter_gringotts"


class ExitGringottsTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "full_screen_area"
    _TERMINATION_TARGET_NAME = "exit_gringotts"


class TalkToWeasleysSubgoal(RegionMatchSubGoal):
    NAME = "talk_to_weasleys"
    _NAMED_REGION = "dialogue_box_full"
    _TARGET_NAME = "talk_to_weasleys"


class OnTrainTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "full_screen_area"
    _TERMINATION_TARGET_NAME = "on_train"


class TalkToRonWeasleySubgoal(RegionMatchSubGoal):
    NAME = "talk_to_ron_weasley"
    _NAMED_REGION = "dialogue_box_full"
    _TARGET_NAME = "talk_to_ron_weasley"


class ChocolateFrogs5InventoryTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "chocolate_frogs_5_inventory_area"
    _TERMINATION_TARGET_NAME = "chocolate_frogs_5_inventory"


class SellChocolateFrogSubgoal(RegionMatchSubGoal):
    NAME = "sell_chocolate_frog"
    _NAMED_REGION = "full_screen_area"
    _TARGET_NAME = "sell_chocolate_frog"


class ChocolateFrogs4InventoryTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "chocolate_frogs_5_inventory_area"
    _TERMINATION_TARGET_NAME = "chocolate_frogs_4_inventory"


class StartOfDuelSubgoal(RegionMatchSubGoal):
    NAME = "start_of_duel"
    _NAMED_REGION = "full_screen_area"
    _TARGET_NAME = "start_of_duel"


class LoseDuelTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "full_screen_area"
    _TERMINATION_TARGET_NAME = "lose_duel"


class WinDuelTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "full_screen_area"
    _TERMINATION_TARGET_NAME = "win_duel"


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


class RatKingSpriteSubgoal(RegionMatchSubGoal):
    NAME = "rat_king_sprite"
    _NAMED_REGION = "rat_king_sprite_area"
    _TARGET_NAME = "rat_king_sprite"


class UnableToEscapeSubgoal(RegionMatchSubGoal):
    NAME = "unable_to_escape"
    _NAMED_REGION = "dialogue_box_full"
    _TARGET_NAME = "unable_to_escape"


class RespawnDeathRatTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "full_screen_area"
    _TERMINATION_TARGET_NAME = "respawn_death_rat_screen"


class FullyRestoreMPSubgoal(RegionMatchSubGoal):
    NAME = "fully_restore_your_mp"
    _NAMED_REGION = "mp_points_area"
    _TARGET_NAME = "fully_restore_your_mp"


class UtilizeDeflectCardsSubgoal(RegionMatchSubGoal):
    NAME = "utilize_deflect_cards"
    _NAMED_REGION = "large_dialogue_box"
    _TARGET_NAME = "large_text_content"


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

# ============================================================
# Train walk tasks
# ============================================================

class RightmostTrainCarSubgoal(RegionMatchSubGoal):
    NAME = "rightmost_train_car"
    _NAMED_REGION = "rightmost_train_car"
    _TARGET_NAME = "rightmost_train_car_capture"


class LeftmostTrainCarSubgoal(RegionMatchSubGoal):
    NAME = "leftmost_train_car"
    _NAMED_REGION = "leftmost_train_car"
    _TARGET_NAME = "leftmost_train_car_capture"


class LeftmostTrainCarTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "leftmost_train_car"
    _TERMINATION_TARGET_NAME = "leftmost_train_car_capture"


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


class NavigateToCarTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "car_area"
    _TERMINATION_TARGET_NAME = "next_to_car"


class DiagonAlleySubgoal(RegionMatchSubGoal):
    NAME = "diagon_alley"
    _NAMED_REGION = "find_location"
    _TARGET_NAME = "diagon_alley"


class StartMenuTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "menu"
    _TERMINATION_TARGET_NAME = "start_menu"


class PumpkinPastySubgoal(RegionMatchSubGoal):
    NAME = "pumpkin_pasties"
    _NAMED_REGION = "last_item"
    _TARGET_NAME = "pumpkin_pasties"


class EatPumpkinPastyTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "item_consumption"
    _TERMINATION_TARGET_NAME = "ate_pumpkin_pasties"


class EquippedPointedHatSubgoal(RegionMatchSubGoal):
    NAME = "equipped_pointed_hat"
    _NAMED_REGION = "equip_screen"
    _TARGET_NAME = "equipped_pointed_hat"


class EquippedPointedHatPlainWorkRobeTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "equip_screen"
    _TERMINATION_TARGET_NAME = "equipped_pointed_hat_plain_work_robe"


class RemoveHatSubgoal(RegionMatchSubGoal):
    NAME = "remove_hat"
    _NAMED_REGION = "equip_screen"
    _TARGET_NAME = "remove_hat"


class RemoveRobeSubgoal(RegionMatchSubGoal):
    NAME = "remove_robe"
    _NAMED_REGION = "equip_screen"
    _TARGET_NAME = "remove_robe"


class EmptyEquipCursorRobeTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "equip_screen"
    _TERMINATION_TARGET_NAME = "empty_equip_cursor_robe"


# ============================================================
# Boat Battle tasks
# ============================================================

class TalkToHagridBeforeBoatSubgoal(RegionMatchSubGoal):
    NAME = "talk_with_hagrid_before_boat"
    _NAMED_REGION = "dialogue_box_full"
    _TARGET_NAME = "talk_with_hagrid_before_boat"


class BoatBattleTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "boat_battle"
    _TERMINATION_TARGET_NAME = "boat_battle_target"


# ============================================================
# Die task
# ============================================================

class WeakenedHealthBarSubgoal(RegionMatchSubGoal):
    NAME = "weakened_health_bar"
    _NAMED_REGION = "large_dialogue_box"
    _TARGET_NAME = "weakened_health_bar"


class RestoredFullHealthTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "large_dialogue_box"
    _TERMINATION_TARGET_NAME = "restored_full_health"


# ============================================================
# Yellow Rat then Big Yellow Monster task
# ============================================================

class FightYellowRatSubgoal(RegionMatchSubGoal):
    NAME = "fight_yellow_rat"
    _NAMED_REGION = "top_left_battle"
    _TARGET_NAME = "yellow_rat"


class FightBigYellowMonsterTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "top_left_battle"
    _TERMINATION_TARGET_NAME = "big_yellow_monster"


# ============================================================
# Bat then Big Yellow Monster (middle) task
# ============================================================

class FightBatMiddleSubgoal(RegionMatchSubGoal):
    NAME = "fight_bat_middle"
    _NAMED_REGION = "middle_fight_area"
    _TARGET_NAME = "bat"


class FightBigYellowMonsterMiddleTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "middle_fight_area"
    _TERMINATION_TARGET_NAME = "big_yellow_monster"


# ============================================================
# Find stone gargoyles on the wall task
# ============================================================

class FindFirstStoneGargoylesSubgoal(RegionMatchSubGoal):
    NAME = "find_first_stone_gargoyles"
    _NAMED_REGION = "stone_gargoyles_wall"
    _TARGET_NAME = "two_stone_gargoyles"


class TalkingWithHagridDungeonSubgoal(RegionMatchSubGoal):
    NAME = "talking_with_hagrid_dungeon"
    _NAMED_REGION = "full_screen_area"
    _TARGET_NAME = "talking_with_hagrid_dungeon"


class GreenDungeonRoomTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "full_screen_area"
    _TERMINATION_TARGET_NAME = "green_dungeon_room"


# ============================================================
# Hogwarts hourglass room tasks
# ============================================================

class LockedDoorSubgoal(RegionMatchSubGoal):
    NAME = "locked_door"
    _NAMED_REGION = "dialogue_box_full"
    _TARGET_NAME = "locked_door"


class StayDownThereTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "dialogue_box_full"
    _TERMINATION_TARGET_NAME = "stay_down_there"


class AnyHourglassSubgoal(AnyRegionMatchSubGoal):
    NAME = "any_hourglass"
    _NAMED_REGIONS = ["center_right", "center_right"]
    _TARGET_NAMES = ["hourglass_1", "hourglass_2"]


class HousePointsTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "full_screen_area"
    _TERMINATION_TARGET_NAME = "house_points"


class Hourglass1Subgoal(RegionMatchSubGoal):
    NAME = "hourglass_1"
    _NAMED_REGION = "center_right"
    _TARGET_NAME = "hourglass_1"


class Hourglass2TerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "center_right"
    _TERMINATION_TARGET_NAME = "hourglass_2"


class BottomRoomSubgoal(RegionMatchSubGoal):
    NAME = "bottom_room"
    _NAMED_REGION = "bottom_fifth"
    _TARGET_NAME = "bottom_room"


class BetweenGargoylesSubgoal(RegionMatchSubGoal):
    NAME = "between_gargoyles"
    _NAMED_REGION = "left_vertical_strip"
    _TARGET_NAME = "between_gargoyles"


class StandingOnSealFacingUpTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "center_half"
    _TERMINATION_TARGET_NAME = "standing_on_seal_facing_up"


# ============================================================
# Purple room stone boss tasks
# ============================================================

class BossPurpleStartSubgoal(RegionMatchSubGoal):
    NAME = "boss_purple_start"
    _NAMED_REGION = "top_left_quarter"
    _TARGET_NAME = "boss_purple_start"


class BossPurpleWinTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "full_screen_area"
    _TERMINATION_TARGET_NAME = "boss_purple_win"


class FindThirdStoneGargoylesSubgoal(RegionMatchSubGoal):
    NAME = "find_third_stone_gargoyles"
    _NAMED_REGION = "stone_gargoyles_wall"
    _TARGET_NAME = "two_stone_gargoyles_3"


class FindSecondStoneGargoylesTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterPhilosophersStoneParser
    _TERMINATION_NAMED_REGION = "stone_gargoyles_wall"
    _TERMINATION_TARGET_NAME = "two_stone_gargoyles_2"


# ============================================================
# Chamber of Secrets: spell learning and battle action tasks
# ============================================================

class TalkGlassesGuySubgoal(RegionMatchSubGoal):
    NAME = "talk_glasses_guy"
    _NAMED_REGION = "dialogue_box_full"
    _TARGET_NAME = "talk_glasses_guy"


class SpellLearnedTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "dialogue_box_full"
    _TERMINATION_TARGET_NAME = "spell_learned"


class SelectCastSpellTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "battle_action_area"
    _TERMINATION_TARGET_NAME = "cast_spell"


class SelectCardAttackTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "battle_action_area"
    _TERMINATION_TARGET_NAME = "card_attack"


class SelectUseItemTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "battle_action_area"
    _TERMINATION_TARGET_NAME = "use_item"


class SelectFleeTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "battle_action_area"
    _TERMINATION_TARGET_NAME = "flee"


class SelectFolioBrutiTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "battle_action_area"
    _TERMINATION_TARGET_NAME = "folio_bruti"


class RestoreAllMagicTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "dialogue_box_full"
    _TERMINATION_TARGET_NAME = "restore_all_magic"


class BroomDoomTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "dialogue_box_full"
    _TERMINATION_TARGET_NAME = "broom_doom"


class UseCardAttackTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "full_screen_area"
    _TERMINATION_TARGET_NAME = "use_card_attack"


# ============================================================
# Chamber of Secrets: garden battle opponents and Diagon Alley
# ============================================================

class SprinklerLeadTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "opponent_lead_area"
    _TERMINATION_TARGET_NAME = "sprinkler_lead"


class GreenRatLeadTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "opponent_lead_area"
    _TERMINATION_TARGET_NAME = "green_rat_lead"


class GnomeTopLeftTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "opponent_top_left_area"
    _TERMINATION_TARGET_NAME = "gnome"


class GreyHoseTopLeftTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "opponent_top_left_area"
    _TERMINATION_TARGET_NAME = "grey_hose"


class ReachedDiagonAlleyTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "dialogue_box_full"
    _TERMINATION_TARGET_NAME = "reached_diagon_alley"


# ============================================================
# Chamber of Secrets: Fred and George's room tasks
# ============================================================

class TalkToFredGeorgeFirstTimeTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "dialogue_box_full"
    _TERMINATION_TARGET_NAME = "talk_to_fred_george_first_time"


class TalkToFredGeorgeSecondTimeTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "dialogue_box_full"
    _TERMINATION_TARGET_NAME = "talk_to_fred_george_second_time"


class TalkToGreenStatueTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = HarryPotterChamberOfSecretsParser
    _TERMINATION_NAMED_REGION = "dialogue_box_full"
    _TERMINATION_TARGET_NAME = "talk_to_green_statue"
