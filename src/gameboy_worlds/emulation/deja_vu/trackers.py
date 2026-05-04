from gameboy_worlds.utils import log_info
from gameboy_worlds.emulation.tracker import (
    DummySubGoalMetric,
    StateTracker,
    TestTrackerMixin,
    make_subgoal_metric_class,
)
from gameboy_worlds.emulation.deja_vu.parsers import AgentState
from gameboy_worlds.emulation.deja_vu.base_metrics import (
    DejaVuTestMetric,
    CoreDejaVuMetrics,
    DejaVuOCRMetric,
)
# import metrics for the test trackers
from gameboy_worlds.emulation.deja_vu.test_metrics import (
    Bought2ChipsTerminationMetric,
    BoughtTicketTerminationMetric,
    CashedOutTerminationMetric,
    CheckedCoatTerminationMetric,
    CheckedGirlTerminationMetric,
    CheckedGunTerminationMetric,
    CheckedMapTerminationMetric,
    CheckedNewsclip1TerminationMetric,
    CheckedNote2TerminationMetric,
    CheckedSignTerminationMetric,
    CheckedSnapshotTerminationMetric,
    CheckedTimetableTerminationMetric,
    ClosedColdTapTerminationMetric,
    ClosedDashbrdTerminationMetric,
    ClosedDoorFromMapTerminationMetric,
    ClosedPantsPocketTerminationMetric,
    ClosedPocketTerminationMetric,
    ClosedWallet1TerminationMetric,
    ClosedWalletTerminationMetric,
    EnteredCellarTerminationMetric,
    EnteredConnectingRoomTerminationMetric,
    EnteredEmptyRoomFromMapTerminationMetric,
    EnteredHallwayTerminationMetric,
    EnteredPlatformTerminationMetric,
    EnteredTaxiTerminationMetric,
    EnteredTrainTerminationMetric,
    ExitedCasinoTerminationMetric,
    GoNewsstandTerminationMetric,
    OpenedLobbyDoorTerminationMetric,
    OutsideApartmentTerminationMetric,
    PaidTaxiTerminationMetric,
    ReturnedToCashierTerminationMetric,
    TakenPamphletTerminationMetric,
    TalkedInTrainStationTerminationMetric,
    VisitedCounterTerminationMetric,
    WenttoWestendTerminationMetric,
    HitBottleTerminationMetric,
    HitMuggerTerminationMetric,
    MadeBetTerminationMetric,
    MeetMuggerTerminationMetric,
    OpenedBathroomDoorTerminationMetric,
    OpenedColdTapTerminationMetric,
    OpenedDashbrdTerminationMetric,
    OpenedDoorFromMapTerminationMetric,
    OpenedDoorTerminationMetric,
    OpenedPantsPocketTerminationMetric,
    OpenedPocketTerminationMetric,
    OpenedSpigotTerminationMetric,
    OpenedTrenchCoatPocketTerminationMetric,
    OpenedWallet1TerminationMetric,
    OpenedWalletTerminationMetric,
    PutOnPantsTerminationMetric,
    PutOnTrenchCoatTerminationMetric,
    TakenCoatTerminationMetric,
    TakenGumTerminationMetric,
    TakenGunTerminationMetric,
    ClosedDoorTerminationMetric,
    TakenLicense1TerminationMetric,
    TakenNewsclip1TerminationMetric,
    TakenPantsTerminationMetric,
    TakenRing1TerminationMetric,
    TalkedToTaxiDriverTerminationMetric,
    UnlockedCarDoorTerminationMetric,
    UnlockedFrontDoorTerminationMetric,
)
# import subgoal classes for the subgoal metrics
from gameboy_worlds.emulation.deja_vu.test_metrics import (
    InWallet1MenuSubGoal,
    PointedAtPantsSubGoal,
    SelectedOpenActionInMenuSubGoal,
    SelectedOpenActionInNormalSubGoal,
    SelectedTakeActionInNormalSubGoal,
    SelectedCloseActionInNormalSubGoal,
    SelectedCloseActionInMenuSubGoal,
    InCoatPocketMenuSubGoal,
    InWalletMenuSubGoal,
    PointedAtCoatSubGoal,
    PointedAtWalletSubGoal,
    InGoodsMenuSubGoal,
    SelectedHitActionInNormalSubGoal,
    SockoOnScreenSubGoal,
    OpenedCellarDoorOnScreenSubGoal,
    PointedAtGumSubGoal,
    SelectedTakeActionInMenuSubGoal,
    InTrenchCoatPocketMenuSubGoal,
    SelectedOutfitButtonSubGoal,
    SelectedUseActionInMenuSubGoal,
    PointedAtTrenchCoatSubGoal,
    PointedAtWallet1SubGoal,
    PointedAtNewsclip1SubGoal,
    PointedAtLicense1SubGoal,
    SelectedWatchActionInMenuSubGoal,
    PointedAt21OnMapSubGoal,
    Selected2ChipsSubGoal,
    PointedAtCoinSubGoal,
    UsingCoinSubGoal,
    PointedAt13OnMapSubGoal,
    UsingKey3SubGoal,
    UsingKey2SubGoal,
    PointedAt11OnMapSubGoal,
    SelectedTalkActionInNormalSubGoal,
    PointedAtWestendAddressSubGoal,
    NoActionInCellarSubGoal,
    NoActionInEmptyRestaurantSubGoal,
    NoActionOnPeoriaStSubGoal,
    PointedAt25OnMapSubGoal,
    PointedAt35OnMapSubGoal,
    NoActionInLobbySubGoal,
    SelectedWatchActionInNormalSubGoal,
    PointedAt45OnMapSubGoal,
    PointedAt52OnMapSubGoal,
    PointedAt41OnMapSubGoal,
)


class CoreDejaVuTracker(StateTracker):
    """
    StateTracker for core Deja Vu metrics.
    """

    _REMOVE_GRID_OVERLAY = False
    """ Whether to remove the grid overlay drawn by the state parser when the agent is in FREE ROAM. This is useful for VLM based agents may need a coordinate grid overlayed onto the frame, but may cause issues for agents that do not understand that it is not a part of the game. """

    def start(self):
        super().start()
        self.metric_classes.extend([CoreDejaVuMetrics, DejaVuTestMetric])

    def step(self, *args, **kwargs):
        """
        Calls on super().step(), but then modifies the current frame to overlay the grid if the agent is in FREE ROAM.
        """
        super().step(*args, **kwargs)

        if self._REMOVE_GRID_OVERLAY:
            state = self.episode_metrics["dejavu_core"]["agent_state"]
            # if agent_state is in FREE ROAM, draw the grid, otherwise do not
            if state == AgentState.FREE_ROAM:
                screen = self.episode_metrics["core"]["current_frame"]
                screen = self.state_parser.draw_grid_overlay(current_frame=screen)
                self.episode_metrics["core"]["current_frame"] = screen
                previous_screens = self.episode_metrics["core"]["passed_frames"]
                if previous_screens is not None:
                    self.episode_metrics["core"]["passed_frames"][-1, :] = screen


class DejaVuOCRTracker(CoreDejaVuTracker):
    def start(self):
        super().start()
        self.metric_classes.extend([DejaVuOCRMetric])


class DejaVuTestTracker(TestTrackerMixin, DejaVuOCRTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Deja Vu games.
    """

    TERMINATION_TRUNCATION_METRIC = TakenCoatTerminationMetric
    SUBGOAL_METRIC = DummySubGoalMetric

# deja_vu_1 test trackers
class DejaVu1CoatTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent takes the coat.
    """

    TERMINATION_TRUNCATION_METRIC = TakenCoatTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedTakeActionInNormalSubGoal])

class DejaVu1TakeGunTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent takes the gun.
    """

    TERMINATION_TRUNCATION_METRIC = TakenGunTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedTakeActionInNormalSubGoal])

class DejaVu1OpenDoorTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent opens the door.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedDoorTerminationMetric
    SUBGOAL_METRIC = DummySubGoalMetric
    # make_subgoal_metric_class([SelectedOpenActionInNormalSubGoal, NoActionSelectedInNormalSubGoal])

class DejaVu1CloseDoorTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent closes the door.
    """

    TERMINATION_TRUNCATION_METRIC = ClosedDoorTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedCloseActionInNormalSubGoal])

class DejaVu1OpenPocketTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent opens the pocket.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedPocketTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedOpenActionInMenuSubGoal])

class DejaVu1OpenWalletTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent opens the wallet.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedWalletTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedOpenActionInMenuSubGoal])

class DejaVu1ClosePocketTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent closes the pocket.
    """

    TERMINATION_TRUNCATION_METRIC = ClosedPocketTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        InGoodsMenuSubGoal,
        SelectedCloseActionInMenuSubGoal,
        PointedAtCoatSubGoal,
    ])

class DejaVu1CloseWalletTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent closes the wallet.
    """

    TERMINATION_TRUNCATION_METRIC = ClosedWalletTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        InCoatPocketMenuSubGoal,
        SelectedCloseActionInMenuSubGoal,
        PointedAtWalletSubGoal,
    ])

class DejaVu1CheckCoatTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent checks the coat.
    """

    TERMINATION_TRUNCATION_METRIC = CheckedCoatTerminationMetric
    SUBGOAL_METRIC = DummySubGoalMetric

class DejaVu1CheckGunTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent checks the gun.
    """

    TERMINATION_TRUNCATION_METRIC = CheckedGunTerminationMetric
    SUBGOAL_METRIC = DummySubGoalMetric

class DejaVu1OpenSpigotTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent opens the spigot.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedSpigotTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedOpenActionInNormalSubGoal])

class DejaVu1HitBottleTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent hits the bottle.
    """

    TERMINATION_TRUNCATION_METRIC = HitBottleTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedHitActionInNormalSubGoal,
        SockoOnScreenSubGoal,
    ])

class DejaVu1EnterCellarTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent enters the cellar.
    """

    TERMINATION_TRUNCATION_METRIC = EnteredCellarTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OpenedCellarDoorOnScreenSubGoal])

class DejaVu1EnterConnectingRoomTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent enters the connecting room.
    """

    TERMINATION_TRUNCATION_METRIC = EnteredConnectingRoomTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NoActionInCellarSubGoal])

class DejaVu1MakeBetTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent makes a bet in casino.
    """

    TERMINATION_TRUNCATION_METRIC = MadeBetTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedUseActionInMenuSubGoal,
        PointedAtCoinSubGoal,
        UsingCoinSubGoal,
    ])

class DejaVu1EnterEmptyRoomFromMapTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent enters an empty room from the map.
    """

    TERMINATION_TRUNCATION_METRIC = EnteredEmptyRoomFromMapTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([PointedAt13OnMapSubGoal])

class DejaVu1UnlockFrontDoorTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent unlocks the front door.
    """

    TERMINATION_TRUNCATION_METRIC = UnlockedFrontDoorTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        UsingKey3SubGoal,
        SelectedUseActionInMenuSubGoal,
    ])

class DejaVu1MeetMuggerTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent meets the mugger.
    """

    TERMINATION_TRUNCATION_METRIC = MeetMuggerTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NoActionInEmptyRestaurantSubGoal])

class DejaVu1HitMuggerTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent hits the mugger.
    """

    TERMINATION_TRUNCATION_METRIC = HitMuggerTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedHitActionInNormalSubGoal])

class DejaVu1UnlockCarDoorTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent unlocks the car door.
    """

    TERMINATION_TRUNCATION_METRIC = UnlockedCarDoorTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([UsingKey2SubGoal])

class DejaVu1OpenDashbrdTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent opens the car dashboard.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedDashbrdTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedOpenActionInNormalSubGoal])

class DejaVu1CloseDashbrdTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent closes the car dashboard.
    """

    TERMINATION_TRUNCATION_METRIC = ClosedDashbrdTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedCloseActionInNormalSubGoal])

class DejaVu1CheckedNote2TestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent checks note 2.
    """

    TERMINATION_TRUNCATION_METRIC = CheckedNote2TerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedWatchActionInMenuSubGoal,
        InGoodsMenuSubGoal,
    ])

class DejaVu1CheckedMapTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent checks the map.
    """

    TERMINATION_TRUNCATION_METRIC = CheckedMapTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedWatchActionInMenuSubGoal,
        InGoodsMenuSubGoal,
    ])

class DejaVu1CheckedSnapshotTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent checks the snapshot.
    """

    TERMINATION_TRUNCATION_METRIC = CheckedSnapshotTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedWatchActionInMenuSubGoal,
        InGoodsMenuSubGoal,
    ])

class DejaVu1GoNewsstandTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent goes to the newsstand.
    """

    TERMINATION_TRUNCATION_METRIC = GoNewsstandTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([PointedAt11OnMapSubGoal])

class DejaVu1EnterTaxiTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent enters the taxi.
    """

    TERMINATION_TRUNCATION_METRIC = EnteredTaxiTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NoActionOnPeoriaStSubGoal])

class DejaVu1TalkToTaxiDriverTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent talks to the taxi driver.
    """

    TERMINATION_TRUNCATION_METRIC = TalkedToTaxiDriverTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedTalkActionInNormalSubGoal])

class DejaVu1GotoWestendTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent goes to westend.
    """

    TERMINATION_TRUNCATION_METRIC = WenttoWestendTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([PointedAtWestendAddressSubGoal])

class DejaVu1PayTaxiTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent pays the taxi fare.
    """

    TERMINATION_TRUNCATION_METRIC = PaidTaxiTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedUseActionInMenuSubGoal])

class DejaVu1GotoApartmentTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent goes to the apartment.
    """

    TERMINATION_TRUNCATION_METRIC = OutsideApartmentTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([PointedAt25OnMapSubGoal])


# deja_vu_2 test trackers
class DejaVu2OpenTrenchCoatTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent opens the trench coat pocket.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedTrenchCoatPocketTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedOpenActionInNormalSubGoal])

class DejaVu2OpenBathroomDoorTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent opens the bathroom door.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedBathroomDoorTerminationMetric
    SUBGOAL_METRIC = DummySubGoalMetric

class DejaVu2TakeGumTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent takes the gum.
    """

    TERMINATION_TRUNCATION_METRIC = TakenGumTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedTakeActionInMenuSubGoal,
        PointedAtGumSubGoal,
        InTrenchCoatPocketMenuSubGoal,
    ])

class DejaVu2OpenPantsPocketTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent opens the pants pocket.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedPantsPocketTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedOpenActionInNormalSubGoal])

class DejaVu2TakePantsTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent takes the pants.
    """

    TERMINATION_TRUNCATION_METRIC = TakenPantsTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedTakeActionInNormalSubGoal])

class DejaVu2ClosePantsPocketTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent closes the pants pocket.
    """

    TERMINATION_TRUNCATION_METRIC = ClosedPantsPocketTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        InGoodsMenuSubGoal,
        SelectedCloseActionInMenuSubGoal,
        PointedAtPantsSubGoal,
    ])

class DejaVu2PutOnTrenchCoatTestTracker(DejaVuTestTracker):
    """ 
    A TestTracker for Deja Vu 2 that terminates when the agent puts on the trench coat.
    """

    TERMINATION_TRUNCATION_METRIC = PutOnTrenchCoatTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedUseActionInMenuSubGoal,
        PointedAtTrenchCoatSubGoal,
        SelectedOutfitButtonSubGoal,
    ])

class DejaVu2PutOnPantsTestTracker(DejaVuTestTracker):
    """ 
    A TestTracker for Deja Vu 2 that terminates when the agent puts on the pants.
    """

    TERMINATION_TRUNCATION_METRIC = PutOnPantsTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedUseActionInMenuSubGoal,
        PointedAtPantsSubGoal,
        SelectedOutfitButtonSubGoal,
    ])

class DejaVu2OpenWallet1TestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent open wallet1.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedWallet1TerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        InGoodsMenuSubGoal,
        SelectedOpenActionInMenuSubGoal,
        PointedAtWallet1SubGoal,
    ])

class DejaVu2TakeNewsclip1TestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent takes newsclip1.
    """

    TERMINATION_TRUNCATION_METRIC = TakenNewsclip1TerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedTakeActionInMenuSubGoal,
        InWallet1MenuSubGoal,
        PointedAtNewsclip1SubGoal,
    ])

class DejaVu2TakeLicense1TestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent takes license1.
    """

    TERMINATION_TRUNCATION_METRIC = TakenLicense1TerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedTakeActionInMenuSubGoal,
        InWallet1MenuSubGoal,
        PointedAtLicense1SubGoal,
    ])

class DejaVu2CloseWallet1TestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent closes wallet1.
    """

    TERMINATION_TRUNCATION_METRIC = ClosedWallet1TerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        InGoodsMenuSubGoal,
        SelectedCloseActionInMenuSubGoal,
        PointedAtWallet1SubGoal,
    ])

class DejaVu2OpenColdTapTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent opens the cold tap.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedColdTapTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedOpenActionInNormalSubGoal])

class DejaVu2CloseColdTapTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent closes the cold tap.
    """

    TERMINATION_TRUNCATION_METRIC = ClosedColdTapTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedCloseActionInNormalSubGoal])

class DejaVu2CheckNewsclip1TestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent checks newsclip1.
    """

    TERMINATION_TRUNCATION_METRIC = CheckedNewsclip1TerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedWatchActionInMenuSubGoal,
        InGoodsMenuSubGoal,
    ])

class DejaVu2TakeRing1TestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent takes ring1.
    """

    TERMINATION_TRUNCATION_METRIC = TakenRing1TerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedTakeActionInNormalSubGoal])

class DejaVu2OpenDoorFromMapTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent opens the door from the map.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedDoorFromMapTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([PointedAt21OnMapSubGoal])

class DejaVu2CloseDoorFromMapTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent closes the door from the map.
    """

    TERMINATION_TRUNCATION_METRIC = ClosedDoorFromMapTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        PointedAt21OnMapSubGoal,
        SelectedCloseActionInNormalSubGoal,
    ])

class DejaVu2EnterHallwayTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent enters the hallway.
    """

    TERMINATION_TRUNCATION_METRIC = EnteredHallwayTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([PointedAt21OnMapSubGoal])

class DejaVu2Buy2ChipsTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent buys 2 chips.
    """

    TERMINATION_TRUNCATION_METRIC = Bought2ChipsTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([Selected2ChipsSubGoal])

class DejaVu2ReturnToCashierTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent returns to the cashier after buying chips.
    """

    TERMINATION_TRUNCATION_METRIC = ReturnedToCashierTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([PointedAt35OnMapSubGoal])

class DejaVu2CashOutTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent cashes out in the casino.
    """

    TERMINATION_TRUNCATION_METRIC = CashedOutTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedUseActionInMenuSubGoal])

class DejaVu2OpenLobbyDoorTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent opens the locked door in the casino.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedLobbyDoorTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedOpenActionInNormalSubGoal,
        PointedAt13OnMapSubGoal,
    ])

class DejaVu2ExitCasinoTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent exits the casino.
    """

    TERMINATION_TRUNCATION_METRIC = ExitedCasinoTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NoActionInLobbySubGoal])

class DejaVu2TalkInTrainStationTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent talks to the person in the train station.
    """

    TERMINATION_TRUNCATION_METRIC = TalkedInTrainStationTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedTalkActionInNormalSubGoal])

class DejaVu2VisitCounterTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent visits the counter in the casino.
    """

    TERMINATION_TRUNCATION_METRIC = VisitedCounterTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([PointedAt25OnMapSubGoal])

class DejaVu2TakePamphletTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent takes the pamphlet in the casino.
    """

    TERMINATION_TRUNCATION_METRIC = TakenPamphletTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedTakeActionInNormalSubGoal])

class DejaVu2CheckTimetableTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent checks the timetable in the train station.
    """

    TERMINATION_TRUNCATION_METRIC = CheckedTimetableTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedWatchActionInNormalSubGoal])

class DejaVu2EnterPlatformTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent enters the platform.
    """

    TERMINATION_TRUNCATION_METRIC = EnteredPlatformTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([PointedAt41OnMapSubGoal])

class DejaVu2EnterTrainTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent enters the train.
    """

    TERMINATION_TRUNCATION_METRIC = EnteredTrainTerminationMetric
    SUBGOAL_METRIC = DummySubGoalMetric

class DejaVu2BuyTicketTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent buys a ticket for the train.
    """

    TERMINATION_TRUNCATION_METRIC = BoughtTicketTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedUseActionInMenuSubGoal])

class DejaVu2CheckGirlTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent checks the girl in the train station.
    """

    TERMINATION_TRUNCATION_METRIC = CheckedGirlTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedWatchActionInNormalSubGoal])

class DejaVu2CheckSignTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent checks the sign in the train station.
    """

    TERMINATION_TRUNCATION_METRIC = CheckedSignTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedWatchActionInNormalSubGoal])