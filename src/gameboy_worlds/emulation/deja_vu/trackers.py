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
    CheckedCoatTerminationMetric,
    CheckedGunTerminationMetric,
    CheckedNewsclip1TerminationMetric,
    ClosedColdTapTerminationMetric,
    ClosedDoorFromMapTerminationMetric,
    ClosedPantsPocketTerminationMetric,
    ClosedPocketTerminationMetric,
    ClosedWallet1TerminationMetric,
    ClosedWalletTerminationMetric,
    EnteredCellarTerminationMetric,
    EnteredConnectingRoomTerminationMetric,
    EnteredEmptyRoomFromMapTerminationMetric,
    EnteredHallwayTerminationMetric,
    HitBottleTerminationMetric,
    HitMuggerTerminationMetric,
    MadeBetTerminationMetric,
    MeetMuggerTerminationMetric,
    OpenedBathroomDoorTerminationMetric,
    OpenedColdTapTerminationMetric,
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
    NoActionSelectedInNormalSubGoal,
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
class DejaVuCoatTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent takes the coat.
    """

    TERMINATION_TRUNCATION_METRIC = TakenCoatTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedTakeActionInNormalSubGoal])

class DejaVuTakeGunTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent takes the gun.
    """

    TERMINATION_TRUNCATION_METRIC = TakenGunTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedTakeActionInNormalSubGoal])

class DejaVuOpenDoorTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent opens the door.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedDoorTerminationMetric
    SUBGOAL_METRIC = DummySubGoalMetric
    # make_subgoal_metric_class([SelectedOpenActionInNormalSubGoal, NoActionSelectedInNormalSubGoal])

class DejaVuCloseDoorTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent closes the door.
    """

    TERMINATION_TRUNCATION_METRIC = ClosedDoorTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedCloseActionInNormalSubGoal])

class DejaVuOpenPocketTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent opens the pocket.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedPocketTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedOpenActionInMenuSubGoal])

class DejaVuOpenWalletTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent opens the wallet.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedWalletTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedOpenActionInMenuSubGoal])

class DejaVuClosePocketTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent closes the pocket.
    """

    TERMINATION_TRUNCATION_METRIC = ClosedPocketTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        InGoodsMenuSubGoal,
        SelectedCloseActionInMenuSubGoal,
        PointedAtCoatSubGoal,
    ])

class DejaVuCloseWalletTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent closes the wallet.
    """

    TERMINATION_TRUNCATION_METRIC = ClosedWalletTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        InCoatPocketMenuSubGoal,
        SelectedCloseActionInMenuSubGoal,
        PointedAtWalletSubGoal,
    ])

class DejaVuCheckCoatTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent checks the coat.
    """

    TERMINATION_TRUNCATION_METRIC = CheckedCoatTerminationMetric
    SUBGOAL_METRIC = DummySubGoalMetric

class DejaVuCheckGunTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent checks the gun.
    """

    TERMINATION_TRUNCATION_METRIC = CheckedGunTerminationMetric
    SUBGOAL_METRIC = DummySubGoalMetric

class DejaVuOpenSpigotTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent opens the spigot.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedSpigotTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedOpenActionInNormalSubGoal])

class DejaVuHitBottleTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent hits the bottle.
    """

    TERMINATION_TRUNCATION_METRIC = HitBottleTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedHitActionInNormalSubGoal,
        SockoOnScreenSubGoal,
    ])

class DejaVuEnterCellarTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent enters the cellar.
    """

    TERMINATION_TRUNCATION_METRIC = EnteredCellarTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OpenedCellarDoorOnScreenSubGoal])

class DejaVuEnterConnectingRoomTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent enters the connecting room.
    """

    TERMINATION_TRUNCATION_METRIC = EnteredConnectingRoomTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NoActionSelectedInNormalSubGoal])

class DejaVuMakeBetTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent makes a bet in casino.
    """

    TERMINATION_TRUNCATION_METRIC = MadeBetTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedUseActionInMenuSubGoal,
        PointedAtCoinSubGoal,
        UsingCoinSubGoal,
    ])

class DejaVuEnterEmptyRoomFromMapTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent enters an empty room from the map.
    """

    TERMINATION_TRUNCATION_METRIC = EnteredEmptyRoomFromMapTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        NoActionSelectedInNormalSubGoal,
        PointedAt13OnMapSubGoal,
    ])

class DejaVuUnlockFrontDoorTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent unlocks the front door.
    """

    TERMINATION_TRUNCATION_METRIC = UnlockedFrontDoorTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        UsingKey3SubGoal,
        SelectedUseActionInMenuSubGoal,
    ])

class DejaVuMeetMuggerTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent meets the mugger.
    """

    TERMINATION_TRUNCATION_METRIC = MeetMuggerTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NoActionSelectedInNormalSubGoal])

class DejaVuHitMuggerTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent hits the mugger.
    """

    TERMINATION_TRUNCATION_METRIC = HitMuggerTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedHitActionInNormalSubGoal])

class DejaVuUnlockCarDoorTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu games that terminates when the agent unlocks the car door.
    """

    TERMINATION_TRUNCATION_METRIC = UnlockedCarDoorTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([UsingKey2SubGoal])


# deja_vu_2 test trackers
class DejaVuOpenTrenchCoatTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent opens the trench coat pocket.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedTrenchCoatPocketTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedOpenActionInNormalSubGoal])

class DejaVuOpenBathroomDoorTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent opens the bathroom door.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedBathroomDoorTerminationMetric
    SUBGOAL_METRIC = DummySubGoalMetric

class DejaVuTakeGumTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent takes the gum.
    """

    TERMINATION_TRUNCATION_METRIC = TakenGumTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedTakeActionInMenuSubGoal,
        PointedAtGumSubGoal,
        InTrenchCoatPocketMenuSubGoal,
    ])

class DejaVuOpenPantsPocketTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent opens the pants pocket.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedPantsPocketTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedOpenActionInNormalSubGoal])

class DejaVuTakePantsTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent takes the pants.
    """

    TERMINATION_TRUNCATION_METRIC = TakenPantsTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedTakeActionInNormalSubGoal])

class DejaVuClosePantsPocketTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent closes the pants pocket.
    """

    TERMINATION_TRUNCATION_METRIC = ClosedPantsPocketTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        InGoodsMenuSubGoal,
        SelectedCloseActionInMenuSubGoal,
        PointedAtPantsSubGoal,
    ])

class DejaVuPutOnTrenchCoatTestTracker(DejaVuTestTracker):
    """ 
    A TestTracker for Deja Vu 2 that terminates when the agent puts on the trench coat.
    """

    TERMINATION_TRUNCATION_METRIC = PutOnTrenchCoatTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedUseActionInMenuSubGoal,
        PointedAtTrenchCoatSubGoal,
        SelectedOutfitButtonSubGoal,
    ])

class DejaVuPutOnPantsTestTracker(DejaVuTestTracker):
    """ 
    A TestTracker for Deja Vu 2 that terminates when the agent puts on the pants.
    """

    TERMINATION_TRUNCATION_METRIC = PutOnPantsTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedUseActionInMenuSubGoal,
        PointedAtPantsSubGoal,
        SelectedOutfitButtonSubGoal,
    ])

class DejaVuOpenWallet1TestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent open wallet1.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedWallet1TerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        InGoodsMenuSubGoal,
        SelectedOpenActionInMenuSubGoal,
        PointedAtWallet1SubGoal,
    ])

class DejaVuTakeNewsclip1TestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent takes newsclip1.
    """

    TERMINATION_TRUNCATION_METRIC = TakenNewsclip1TerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedTakeActionInMenuSubGoal,
        InWallet1MenuSubGoal,
        PointedAtNewsclip1SubGoal,
    ])

class DejaVuTakeLicense1TestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent takes license1.
    """

    TERMINATION_TRUNCATION_METRIC = TakenLicense1TerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedTakeActionInMenuSubGoal,
        InWallet1MenuSubGoal,
        PointedAtLicense1SubGoal,
    ])

class DejaVuCloseWallet1TestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent closes wallet1.
    """

    TERMINATION_TRUNCATION_METRIC = ClosedWallet1TerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        InGoodsMenuSubGoal,
        SelectedCloseActionInMenuSubGoal,
        PointedAtWallet1SubGoal,
    ])

class DejaVuOpenColdTapTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent opens the cold tap.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedColdTapTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedOpenActionInNormalSubGoal])

class DejaVuCloseColdTapTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent closes the cold tap.
    """

    TERMINATION_TRUNCATION_METRIC = ClosedColdTapTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedCloseActionInNormalSubGoal])

class DejaVuCheckNewsclip1TestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent checks newsclip1.
    """

    TERMINATION_TRUNCATION_METRIC = CheckedNewsclip1TerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        SelectedWatchActionInMenuSubGoal,
        InGoodsMenuSubGoal,
    ])

class DejaVuTakeRing1TestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent takes ring1.
    """

    TERMINATION_TRUNCATION_METRIC = TakenRing1TerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectedTakeActionInNormalSubGoal])

class DejaVuOpenDoorFromMapTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent opens the door from the map.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedDoorFromMapTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([PointedAt21OnMapSubGoal])

class DejaVuCloseDoorFromMapTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent closes the door from the map.
    """

    TERMINATION_TRUNCATION_METRIC = ClosedDoorFromMapTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        PointedAt21OnMapSubGoal,
        SelectedCloseActionInNormalSubGoal,
    ])

class DejaVuEnterHallwayTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent enters the hallway.
    """

    TERMINATION_TRUNCATION_METRIC = EnteredHallwayTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([
        PointedAt21OnMapSubGoal,
        NoActionSelectedInNormalSubGoal,
    ])

class DejaVuBuy2ChipsTestTracker(DejaVuTestTracker):
    """
    A TestTracker for Deja Vu 2 that terminates when the agent buys 2 chips.
    """

    TERMINATION_TRUNCATION_METRIC = Bought2ChipsTerminationMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([Selected2ChipsSubGoal])