"""Test metrics for Survival Kids benchmark tasks."""

from gameboy_worlds.emulation.survival_kids.parsers import SurvivalKidsParser
from gameboy_worlds.emulation.tracker import (
    RegionChangedTerminationMetric,
    RegionMatchTerminationMetric,
    TerminationMetric,
)


class StatusBarChangedTerminateMetric(RegionChangedTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _CHANGED_NAMED_REGION = "status_bar"
    _CHANGE_MAE_THRESHOLD = 10


class HpChangedTerminateMetric(RegionChangedTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _CHANGED_NAMED_REGION = "hp_area"
    _CHANGE_MAE_THRESHOLD = 10


class HungerChangedTerminateMetric(RegionChangedTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _CHANGED_NAMED_REGION = "hunger_area"
    _CHANGE_MAE_THRESHOLD = 10


class ResolveHungerTerminateMetric(HungerChangedTerminateMetric):
    pass


class ThirstChangedTerminateMetric(RegionChangedTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _CHANGED_NAMED_REGION = "thirst_area"
    _CHANGE_MAE_THRESHOLD = 10


class DrinkWaterTerminateMetric(ThirstChangedTerminateMetric):
    pass


class StaminaChangedTerminateMetric(RegionChangedTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _CHANGED_NAMED_REGION = "stamina_area"
    _CHANGE_MAE_THRESHOLD = 10


class GameViewportChangedTerminateMetric(
    RegionChangedTerminationMetric, TerminationMetric
):
    REQUIRED_PARSER = SurvivalKidsParser
    _CHANGED_NAMED_REGION = "game_viewport"
    _CHANGE_MAE_THRESHOLD = 10


class AnimalKilledTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "game_viewport"
    _TERMINATION_TARGET_NAME = "animal_killed"


class Chapter1PathClearedTerminateMetric(
    RegionMatchTerminationMetric, TerminationMetric
):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "game_viewport"
    _TERMINATION_TARGET_NAME = "chapter1_path_cleared"


class PathAfterBlockingGrassTerminateMetric(
    RegionMatchTerminationMetric, TerminationMetric
):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "game_viewport"
    _TERMINATION_TARGET_NAME = "path_after_blocking_grass"


class InTheShelterTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "game_viewport"
    _TERMINATION_TARGET_NAME = "in_the_shelter"


class NewPath1FoundTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "game_viewport"
    _TERMINATION_TARGET_NAME = "new_path_1_found"


class NewPath2FoundTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "game_viewport"
    _TERMINATION_TARGET_NAME = "new_path_2_found"


class SharpStoneFoundTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "game_viewport"
    _TERMINATION_TARGET_NAME = "sharp_stone_found"


class DayReferenceTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "day_reference"


class NightReferenceTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "night_reference"


class EnteredShelterTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "entered_shelter"


class FoundRiverTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "found_river"


class WaterMenuOpenTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "water_menu_open"


class AfterFillingWaterTerminateMetric(
    RegionMatchTerminationMetric, TerminationMetric
):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "after_filling_water"


class GotTheWaterTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "got_the_water"


class GotTheStickTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "got_the_stick"


class GotTheTreeBarkTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "got_the_tree_bark"


class GotTheBrdfeatherTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "got_the_brdfeather"


class InventoryOpenTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "menu_area"
    _TERMINATION_TARGET_NAME = "inventory_open"


class PickupItemDialogueTerminateMetric(
    RegionMatchTerminationMetric, TerminationMetric
):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "dialogue_area"
    _TERMINATION_TARGET_NAME = "pickup_item_dialogue"


class CanteenPickupDialogueTerminateMetric(
    RegionMatchTerminationMetric, TerminationMetric
):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "dialogue_area"
    _TERMINATION_TARGET_NAME = "canteen_pickup_dialogue"


class BagIconTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "bag_icon_area"
    _TERMINATION_TARGET_NAME = "bag_icon"


class KnifeEquippedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "equipped_item_area"
    _TERMINATION_TARGET_NAME = "knife_equipped"


class KnifeEquippedScreenTerminateMetric(
    RegionMatchTerminationMetric, TerminationMetric
):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "knife_equipped"


class KnifeChosenTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "choose_item_area"
    _TERMINATION_TARGET_NAME = "knife_chosen"


class MergeMenuTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "merge_menu_area"
    _TERMINATION_TARGET_NAME = "merge_menu"


class MergeConfirmTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "merge_confirm_area"
    _TERMINATION_TARGET_NAME = "merge_confirm"


class CanteenEquippedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "equipped_items_area"
    _TERMINATION_TARGET_NAME = "canteen_equipped"


class CanteenChosenTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "choose_item_area"
    _TERMINATION_TARGET_NAME = "canteen_chosen"


class KindlingMergedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "inventory_select_area"
    _TERMINATION_TARGET_NAME = "kindling_merged"


class SelectKindlingTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "choose_item_area"
    _TERMINATION_TARGET_NAME = "select_kindling"


class UseKindlingTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "equipped_item_area"
    _TERMINATION_TARGET_NAME = "use_kindling"


class FireLitTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "game_viewport"
    _TERMINATION_TARGET_NAME = "fire_lit"


class TakeLeaveMenuTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "item_action_menu_two_options"
    _TERMINATION_TARGET_NAME = "take_leave_menu"


class SelectTakeTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "item_action_menu_two_options"
    _TERMINATION_TARGET_NAME = "select_take"


class CanteenTakeLeaveMenuTerminateMetric(
    RegionMatchTerminationMetric, TerminationMetric
):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "item_action_menu"
    _TERMINATION_TARGET_NAME = "canteen_take_leave_menu"


class CanteenActionMenuTerminateMetric(
    RegionMatchTerminationMetric, TerminationMetric
):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "item_use_menu_area"
    _TERMINATION_TARGET_NAME = "canteen_action_menu"


class CanteenUseSelectedTerminateMetric(
    RegionMatchTerminationMetric, TerminationMetric
):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "item_use_menu_area"
    _TERMINATION_TARGET_NAME = "canteen_use_selected"


class CanteenDrinkSelectedTerminateMetric(
    RegionMatchTerminationMetric, TerminationMetric
):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "item_use_menu_area"
    _TERMINATION_TARGET_NAME = "canteen_drink_selected"


class FeatherTakeLeaveMenuTerminateMetric(
    RegionMatchTerminationMetric, TerminationMetric
):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "item_action_menu_two_options"
    _TERMINATION_TARGET_NAME = "feather_take_leave_menu"


# Condensed tasks not yet in benchmark/tests/survival_kids.csv:
# - Pick up the feather: needs a stable feather pickup dialogue or inventory signal.
# - Select Eat on the meat: needs meat_eat_selected capture.
# - Eat the meat: needs meat_eaten_dialogue capture.
# - Drink from the canteen: needs final drink success/HUD signal, not just menu selection.
# - Clear blocking grass and move forward: needs a tighter grass/path metric or subgoals.
class MeatActionMenuTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "item_action_menu"
    _TERMINATION_TARGET_NAME = "meat_take_eat_leave_menu"


class MeatEatSelectedTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "item_action_menu"
    _TERMINATION_TARGET_NAME = "meat_eat_selected"


class MeatEatenDialogueTerminateMetric(RegionMatchTerminationMetric, TerminationMetric):
    REQUIRED_PARSER = SurvivalKidsParser
    _TERMINATION_NAMED_REGION = "dialogue_area"
    _TERMINATION_TARGET_NAME = "meat_eaten_dialogue"
