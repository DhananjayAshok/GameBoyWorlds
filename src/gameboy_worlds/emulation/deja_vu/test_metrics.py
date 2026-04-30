import numpy as np

from gameboy_worlds.emulation.deja_vu.parsers import DejaVu1StateParser, DejaVu2StateParser
from gameboy_worlds.emulation.parser import StateParser
from gameboy_worlds.emulation.tracker import (
    RegionMatchTerminationMetric,
    RegionMatchTerminationOnlyMetric,
    SingleRegionMatchSubGoal,
    SubGoal,
    SubGoalMetric,
    TerminationMetric,
    AnyRegionMatchSubGoal
)

# class DejaVuCoatSubGoalMetric(SubGoalMetric):
#     """SubGoalMetric for the take_coat_test task, tracking 'Take' action selection as an intermediate step."""

#     REQUIRED_PARSER = DejaVu1StateParser
#     SUBGOALS = [SelectedTakeActionSubGoal]

# class DejaVuCoatTerminationMetric(RegionMatchTerminationMetric, TerminationMetric):

# deja_vu_1 termination metrics
class TakenCoatTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "took_coat"

class TakenGunTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "took_gun"

class OpenedDoorTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_door"

class ClosedDoorTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "closed_door"

class OpenedPocketTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_pocket"

class OpenedWalletTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_wallet"

class ClosedPocketTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "closed_pocket"

class ClosedWalletTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "closed_wallet"

class CheckedCoatTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "checked_coat"

class CheckedGunTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "checked_gun"

class OpenedSpigotTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_spigot"

class HitBottleTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "hit_bottle"

class EnteredCellarTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "entered_cellar"

class EnteredConnectingRoomTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "entered_connecting_room"

class MadeBetTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "made_bet"

class EnteredEmptyRoomFromMapTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "entered_empty_room"

class UnlockedFrontDoorTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "unlocked_front_door"

class MeetMuggerTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "met_mugger"

class HitMuggerTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "hit_mugger"

class UnlockedCarDoorTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "unlocked_car_door"

# deja_vu_2 termination metrics
class OpenedTrenchCoatPocketTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_trench_coat_pocket"

class OpenedBathroomDoorTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_door"

class TakenGumTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "taken_gum"

class OpenedPantsPocketTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_pants_pocket"

class TakenPantsTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "taken_pants"

class ClosedPantsPocketTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "closed_pants_pocket"

class PutOnTrenchCoatTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "put_on_trench_coat"

class PutOnPantsTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "put_on_pants"

class OpenedWallet1TerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_wallet1"

class TakenNewsclip1TerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "taken_newsclip1"

class TakenLicense1TerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "taken_license1"

class ClosedWallet1TerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "closed_wallet1"

class OpenedColdTapTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_cold_tap"

class ClosedColdTapTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "closed_cold_tap"

class CheckedNewsclip1TerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "checked_newsclip1"

class TakenRing1TerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "taken_ring1"

class OpenedDoorFromMapTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_room_door"

class ClosedDoorFromMapTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "closed_room_door"

class EnteredHallwayTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "entered_hallway"

class Bought2ChipsTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "bought_2_chips"


# subgoal classes
# subgoal classes with multiple region match requirements
class SelectedTakeActionInNormalSubGoal(AnyRegionMatchSubGoal):
    NAME = "selected_take_action"
    _NAMED_REGIONS = ["action_bar_in_normal"]
    _TARGET_NAMES = ["selected_take_action"]

class SelectedOpenActionInNormalSubGoal(AnyRegionMatchSubGoal):
    NAME = "selected_open_action"
    _NAMED_REGIONS = ["action_bar_in_normal"]
    _TARGET_NAMES = ["selected_open_action"]

class SelectedCloseActionInNormalSubGoal(AnyRegionMatchSubGoal):
    NAME = "selected_close_action"
    _NAMED_REGIONS = ["action_bar_in_normal"]
    _TARGET_NAMES = ["selected_close_action"]

class SelectedHitActionInNormalSubGoal(AnyRegionMatchSubGoal):
    NAME = "selected_hit_action_in_normal"
    _NAMED_REGIONS = ["action_bar_in_normal"]
    _TARGET_NAMES = ["selected_hit_action"]

class NoActionSelectedInNormalSubGoal(AnyRegionMatchSubGoal):
    NAME = "no_action_selected"
    _NAMED_REGIONS = ["action_bar_in_normal"]
    _TARGET_NAMES = ["no_action_selected"]

class SelectedTakeActionInMenuSubGoal(AnyRegionMatchSubGoal):
    NAME = "selected_take_action_in_menu"
    _NAMED_REGIONS = ["action_bar_in_menu"]
    _TARGET_NAMES = ["selected_take_action"]

class SelectedOpenActionInMenuSubGoal(AnyRegionMatchSubGoal):
    NAME = "selected_open_action_in_menu"
    _NAMED_REGIONS = ["action_bar_in_menu"]
    _TARGET_NAMES = ["selected_open_action"]

class SelectedCloseActionInMenuSubGoal(AnyRegionMatchSubGoal):
    NAME = "selected_close_action_in_menu"
    _NAMED_REGIONS = ["action_bar_in_menu"]
    _TARGET_NAMES = ["selected_close_action"]

class SelectedWatchActionInMenuSubGoal(AnyRegionMatchSubGoal):
    NAME = "selected_watch_action_in_menu"
    _NAMED_REGIONS = ["action_bar_in_menu"]
    _TARGET_NAMES = ["selected_watch_action"]

class NoActionSelectedInMenuSubGoal(AnyRegionMatchSubGoal):
    NAME = "no_action_selected_in_menu"
    _NAMED_REGIONS = ["action_bar_in_menu"]
    _TARGET_NAMES = ["no_action_selected"]

class InCoatPocketMenuSubGoal(AnyRegionMatchSubGoal):
    NAME = "in_coat_pocket_menu"
    _NAMED_REGIONS = ["menu_title_area"]
    _TARGET_NAMES = ["coat_pocket_menu"]

class InWalletMenuSubGoal(AnyRegionMatchSubGoal):
    NAME = "in_wallet_menu"
    _NAMED_REGIONS = ["menu_title_area"]
    _TARGET_NAMES = ["wallet_menu"]

class InGoodsMenuSubGoal(AnyRegionMatchSubGoal):
    NAME = "in_goods_menu"
    _NAMED_REGIONS = ["menu_title_area"]
    _TARGET_NAMES = ["goods_menu"]

class SockoOnScreenSubGoal(AnyRegionMatchSubGoal):
    NAME = "socko_on_screen"
    _NAMED_REGIONS = ["game_screen_area"]
    _TARGET_NAMES = ["socko_on_screen"]

class OpenedCellarDoorOnScreenSubGoal(AnyRegionMatchSubGoal):
    NAME = "opened_cellar_door_on_screen"
    _NAMED_REGIONS = ["game_screen_area"]
    _TARGET_NAMES = ["opened_cellar_door"]

class InTrenchCoatPocketMenuSubGoal(AnyRegionMatchSubGoal):
    NAME = "in_trench_coat_pocket_menu"
    _NAMED_REGIONS = ["menu_title_area"]
    _TARGET_NAMES = ["trench_coat_pocket_menu"]

class SelectedUseActionInMenuSubGoal(AnyRegionMatchSubGoal):
    NAME = "selected_use_action_in_menu"
    _NAMED_REGIONS = ["action_bar_in_menu"]
    _TARGET_NAMES = ["selected_use_action"]

class InWallet1MenuSubGoal(AnyRegionMatchSubGoal):
    NAME = "in_wallet1_menu"
    _NAMED_REGIONS = ["menu_title_area"]
    _TARGET_NAMES = ["wallet1_menu"]

class Selected2ChipsSubGoal(AnyRegionMatchSubGoal):
    NAME = "selected_2_chips"
    _NAMED_REGIONS = ["dialogue_box_area"]
    _TARGET_NAMES = ["selected_2_chips"]

# subgoal classes with single region match requirement
class PointedAtCoatSubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_coat"
    _NAMED_REGION = "selected_coat_item"

class PointedAtWalletSubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_wallet"
    _NAMED_REGION = "selected_wallet_item"

class PointedAtGumSubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_gum"
    _NAMED_REGION = "selected_gum_item"

class PointedAtPantsSubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_pants"
    _NAMED_REGION = "selected_pants_item"

class PointedAtTrenchCoatSubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_trench_coat"
    _NAMED_REGION = "selected_trench_coat_item"

class SelectedOutfitButtonSubGoal(SingleRegionMatchSubGoal):
    NAME = "selected_outfit_button"
    _NAMED_REGION = "selected_outfit_button"

class PointedAtWallet1SubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_wallet1"
    _NAMED_REGION = "selected_wallet1_item"

class PointedAtNewsclip1SubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_newsclip1"
    _NAMED_REGION = "selected_newsclip1_item"

class PointedAtLicense1SubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_license1"
    _NAMED_REGION = "selected_license1_item"

class PointedAt21OnMapSubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_21_on_map"
    _NAMED_REGION = "pointed_at_21_on_map"

class PointedAt13OnMapSubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_13_on_map"
    _NAMED_REGION = "pointed_at_13_on_map"

class PointedAtCoinSubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_coin"
    _NAMED_REGION = "selected_coin_item"

class UsingCoinSubGoal(SingleRegionMatchSubGoal):
    NAME = "using_coin"
    _NAMED_REGION = "using_coin_item"

class UsingKey3SubGoal(SingleRegionMatchSubGoal):
    NAME = "using_key3"
    _NAMED_REGION = "using_key3_item"

class UsingKey2SubGoal(SingleRegionMatchSubGoal):
    NAME = "using_key2"
    _NAMED_REGION = "using_key2_item"
