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

class OpenedDashbrdTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_dashbrd"

class ClosedDashbrdTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "closed_dashbrd"

class CheckedNote2TerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "checked_note2"

class CheckedMapTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "checked_map"

class CheckedSnapshotTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "checked_snapshot"

class GoNewsstandTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "in_front_of_newsstand"

class EnteredTaxiTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "entered_taxi"

class TalkedToTaxiDriverTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "talked_to_taxi_driver"

class WenttoWestendTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "went_to_westend"

class PaidTaxiTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "paid_taxi"

class OutsideApartmentTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "outside_apartment"

class EnteredShermanTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "entered_sherman"

class WenttoOfficeTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "stood_in_front_office"

class EnteredWestendTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "entered_westend"

class OpenedElevatorDoorTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_elevator_door"

class EnteredElevatorTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "entered_elevator"

class ClosedElevatorDoorTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "closed_elevator_door"

class CheckedPhotoTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "checked_photo"

class ShotDoorTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "game_screen_area"
    _TERMINATION_TARGET_NAME = "shot_door"

class OpenedDeskTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_desk"

class UnlockedOfficeDoorTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "unlocked_office_door"

class MadeMedicineTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "made_medicine"

class TakenMedicineTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "taken_medicine"

class ShotLockTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "game_screen_area"
    _TERMINATION_TARGET_NAME = "shot_lock"

class OpenedDiaryTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_diary"

class ShotGrimyOfficeDoorTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "game_screen_area"
    _TERMINATION_TARGET_NAME = "shot_door"

class CheckedDeadManTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "checked_dead_man"

class OpenedCabinetTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_cabinet"

class ExitedGrimyOfficeTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "exited_grimy_office"

class OpenedWallSafeTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_wall_safe"

class OpenedCarTrunkTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu1StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_car_trunk"

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

class ReturnedToCashierTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "returned_cashier"

class CashedOutTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "cashed_out"

class OpenedLobbyDoorTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_lobby_door"

class ExitedCasinoTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "exited_casino"

class TalkedInTrainStationTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "talked_in_train_station"

class VisitedCounterTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "visited_counter"

class TakenPamphletTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "taken_pamphlet"

class CheckedTimetableTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "timetable"

class EnteredPlatformTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "game_screen_area"
    _TERMINATION_TARGET_NAME = "on_track6"

class EnteredTrainTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "entered_train"

class BoughtTicketTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "bought_ticket"

class CheckedGirlTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "checked_girl"

class CheckedSignTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "checked_sign"

class ChattedSellerTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "chatted_seller"

class BoughtNewspaperTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "bought_newspaper"

class TakenNewsclip4TerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "taken_newsclip4"

class EnteredChicagoTaxiTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "entered_chicago_taxi"

class ChattedTaxiDriverTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "chatted_taxi_driver"

class EnteredMiddleRoomTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "entered_middle_room"

class LoadedGunTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "loaded_gun"

class OpenedLockTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_lock"

class HitBoardTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "hit_board"

class OpenedTelephoneTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_telephone"

class OpenedBoxTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_box"

class OpenedPocketKnifeTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_pocket_knife"

class OpenedDoorByKnifeTerminationMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = DejaVu2StateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_area"
    _TERMINATION_TARGET_NAME = "opened_door_by_knife"


# subgoal classes
# subgoal classes with multiple region match requirements
class UnlockedMiddleRoomDoorSubGoal(AnyRegionMatchSubGoal):
    NAME = "unlocked_middle_room_door"
    _NAMED_REGIONS = ["dialogue_box_area"]
    _TARGET_NAMES = ["unlocked_middle_door"]

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

class InWallet1MenuSubGoal(AnyRegionMatchSubGoal):
    NAME = "in_wallet1_menu"
    _NAMED_REGIONS = ["menu_title_area"]
    _TARGET_NAMES = ["wallet1_menu"]

class Selected2ChipsSubGoal(AnyRegionMatchSubGoal):
    NAME = "selected_2_chips"
    _NAMED_REGIONS = ["dialogue_box_area"]
    _TARGET_NAMES = ["selected_2_chips"]

class OpenedWestendDoorSubGoal(AnyRegionMatchSubGoal):
    NAME = "opened_westend_door"
    _NAMED_REGIONS = ["dialogue_box_area"]
    _TARGET_NAMES = ["opened_westend_door"]

class OpenedShermanDoorSubGoal(AnyRegionMatchSubGoal):
    NAME = "opened_sherman_door"
    _NAMED_REGIONS = ["dialogue_box_area"]
    _TARGET_NAMES = ["opened_sherman_door"]

# subgoal classes for no action selected
class NoActionInCellarSubGoal(AnyRegionMatchSubGoal):
    NAME = "no_action_in_cellar"
    _NAMED_REGIONS = ["no_action"]
    _TARGET_NAMES = ["in_cellar"]

class NoActionInEmptyRestaurantSubGoal(AnyRegionMatchSubGoal):
    NAME = "no_action_in_empty_restaurant"
    _NAMED_REGIONS = ["no_action"]
    _TARGET_NAMES = ["in_empty_restaurant"]

class NoActionOnPeoriaStSubGoal(AnyRegionMatchSubGoal):
    NAME = "no_action_on_peoria_st"
    _NAMED_REGIONS = ["no_action"]
    _TARGET_NAMES = ["on_peoria_st"]

class NoActionInLobbySubGoal(AnyRegionMatchSubGoal):
    NAME = "no_action_in_lobby"
    _NAMED_REGIONS = ["no_action"]
    _TARGET_NAMES = ["in_lobby"]

class NoActionInShermanLobbySubGoal(AnyRegionMatchSubGoal):
    NAME = "no_action_in_sherman_lobby"
    _NAMED_REGIONS = ["no_action"]
    _TARGET_NAMES = ["in_sherman_lobby"]

class NoActionInWestendLobbySubGoal(AnyRegionMatchSubGoal):
    NAME = "no_action_in_westend_lobby"
    _NAMED_REGIONS = ["no_action"]
    _TARGET_NAMES = ["in_westend_lobby"]

class NoActionInGrimyOfficeSubGoal(AnyRegionMatchSubGoal):
    NAME = "no_action_in_grimy_office"
    _NAMED_REGIONS = ["no_action"]
    _TARGET_NAMES = ["in_grimy_office"]

# subgoal classes with single region match requirement
class UsingKnifeSubGoal(SingleRegionMatchSubGoal):
    NAME = "using_knife"
    _NAMED_REGION = "using_knife_item"

class UsingKey4SubGoal(SingleRegionMatchSubGoal):
    NAME = "using_key4"
    _NAMED_REGION = "using_key4_item"

class UsingNote3SubGoal(SingleRegionMatchSubGoal):
    NAME = "using_note3"
    _NAMED_REGION = "using_note3_item"

class UsingKey2SubGoal(SingleRegionMatchSubGoal):
    NAME = "using_key2"
    _NAMED_REGION = "using_key2_item"

class UsingKey1SubGoal(SingleRegionMatchSubGoal):
    NAME = "using_key1"
    _NAMED_REGION = "using_key1_item"

class UsingCashSubGoal(SingleRegionMatchSubGoal):
    NAME = "using_cash"
    _NAMED_REGION = "using_cash_item"

class UsingBulletSubGoal(SingleRegionMatchSubGoal):
    NAME = "using_bullet"
    _NAMED_REGION = "using_bullet_item"

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

class PointedAt11OnMapSubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_11_on_map"
    _NAMED_REGION = "pointed_at_11_on_map"

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

class PointedAtWestendAddressSubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_westend_address"
    _NAMED_REGION = "selected_westend_address"

class PointedAt25OnMapSubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_25_on_map"
    _NAMED_REGION = "pointed_at_25_on_map"

class PointedAt35OnMapSubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_35_on_map"
    _NAMED_REGION = "pointed_at_35_on_map"

class PointedAt41OnMapSubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_41_on_map"
    _NAMED_REGION = "pointed_at_41_on_map"

class PointedAt45OnMapSubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_45_on_map"
    _NAMED_REGION = "pointed_at_45_on_map"

class PointedAt52OnMapSubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_52_on_map"
    _NAMED_REGION = "pointed_at_52_on_map"

class PointedAt24OnMapSubGoal(SingleRegionMatchSubGoal):
    NAME = "pointed_at_24_on_map"
    _NAMED_REGION = "pointed_at_24_on_map"


# Action selection subgoals in menu and normal have the same target names
# Menu action selection subgoals
# class NoActionSelectedInMenuSubGoal(AnyRegionMatchSubGoal):
#     NAME = "no_action_selected_in_menu"
#     _NAMED_REGIONS = ["action_bar_in_menu"]
#     _TARGET_NAMES = ["no_action_selected"]

class SelectedWatchActionInMenuSubGoal(SingleRegionMatchSubGoal):
    NAME = "selected_watch_action_in_menu"
    _NAMED_REGION = "selected_watch_action_in_menu"

class SelectedUseActionInMenuSubGoal(SingleRegionMatchSubGoal):
    NAME = "selected_use_action_in_menu"
    _NAMED_REGION = "selected_use_action_in_menu"

class SelectedTakeActionInMenuSubGoal(SingleRegionMatchSubGoal):
    NAME = "selected_take_action_in_menu"
    _NAMED_REGION = "selected_take_action_in_menu"

class SelectedOpenActionInMenuSubGoal(SingleRegionMatchSubGoal):
    NAME = "selected_open_action_in_menu"
    _NAMED_REGION = "selected_open_action_in_menu"

class SelectedCloseActionInMenuSubGoal(SingleRegionMatchSubGoal):
    NAME = "selected_close_action_in_menu"
    _NAMED_REGION = "selected_close_action_in_menu"

# Normal action selection subgoals
class SelectedWatchActionInNormalSubGoal(SingleRegionMatchSubGoal):
    NAME = "selected_watch_action_in_normal"
    _NAMED_REGION = "selected_watch_action_in_normal"

class SelectedTakeActionInNormalSubGoal(SingleRegionMatchSubGoal):
    NAME = "selected_take_action_in_normal"
    _NAMED_REGION = "selected_take_action_in_normal"

class SelectedOpenActionInNormalSubGoal(SingleRegionMatchSubGoal):
    NAME = "selected_open_action_in_normal"
    _NAMED_REGION = "selected_open_action_in_normal"

class SelectedCloseActionInNormalSubGoal(SingleRegionMatchSubGoal):
    NAME = "selected_close_action_in_normal"
    _NAMED_REGION = "selected_close_action_in_normal"

class SelectedTalkActionInNormalSubGoal(SingleRegionMatchSubGoal):
    NAME = "selected_talk_action_in_normal"
    _NAMED_REGION = "selected_talk_action_in_normal"

class SelectedHitActionInNormalSubGoal(SingleRegionMatchSubGoal):
    NAME = "selected_hit_action_in_normal"
    _NAMED_REGION = "selected_hit_action_in_normal"