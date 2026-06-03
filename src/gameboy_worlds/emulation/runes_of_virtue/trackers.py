from gameboy_worlds.emulation.runes_of_virtue.base_metrics import (
    CoreRunesOfVirtueMetrics,
    RunesOfVirtueOCRMetric,
)
from gameboy_worlds.emulation.runes_of_virtue.test_metrics import (
    RunesOfVirtue1BasementChestOpenedTerminateMetric,
    RunesOfVirtue1BasementLadderUnlockedTerminateMetric,
    RunesOfVirtue1CavernOfHatredEnterFloor2TerminateMetric,
    RunesOfVirtue1CavernOfHatredSherryFloor2DialogTerminateMetric,
    RunesOfVirtue1CavernOfHatredChooseDoorWithSherryTerminateMetric,
    RunesOfVirtue1CavernOfHatredChooseRightDoorMelissaDialogTerminateMetric,
    RunesOfVirtue1CavernOfHatredEnterFloor3TerminateMetric,
    RunesOfVirtue1CavernOfHatredEnterFloor4TerminateMetric,
    RunesOfVirtue1CavernOfHatredTerminateMetric,
    RunesOfVirtue1CavernOfCowardiceTerminateMetric,
    RunesOfVirtue1CavernOfCowardiceEnterFloor2TerminateMetric,
    RunesOfVirtue1CavernOfCowardiceEnterFloor3TerminateMetric,
    RunesOfVirtue1CavernOfCowardiceFloor3ChestOpenedTerminateMetric,
    RunesOfVirtue1CavernOfCowardiceEnterFloor4TerminateMetric,
    RunesOfVirtue1CavernOfCowardiceSherryFloor4DialogTerminateMetric,
    RunesOfVirtue1CavernOfCowardiceTakeStewFloor4TerminateMetric,
    RunesOfVirtue1CavernOfCowardiceObtainCoinFloor4TerminateMetric,
    RunesOfVirtue1CavernOfHatredChestFloor1OpenedTerminateMetric,
    RunesOfVirtue1CavernOfDeceitTerminateMetric,
    RunesOfVirtue1ChucklesDialogTerminateMetric,
    RunesOfVirtue1DeathScreenTerminateMetric,
    RunesOfVirtue1DrCatDialogTerminateMetric,
    RunesOfVirtue1DrCatCatsLairDialogTerminateMetric,
    RunesOfVirtue1GnuGnu1DialogTerminateMetric,
    RunesOfVirtue1GnuGnu2DialogTerminateMetric,
    RunesOfVirtue1KingDialogTerminateMetric,
    RunesOfVirtue1OpenMenuTerminateMetric,
    RunesOfVirtue1SherryDialogTerminateMetric,
    RunesOfVirtue1ShipRiddenTerminateMetric,
    RunesOfVirtue1TelescopeViewTerminateMetric,
    RunesOfVirtue2BlacksmithFailBuyShieldTerminateMetric,
    RunesOfVirtue2BlockedRoomEnteredTerminateMetric,
    RunesOfVirtue2BringTholdenBackToKingTerminateMetric,
    RunesOfVirtue2CaveOfDishonourEnterFloor3TerminateMetric,
    RunesOfVirtue2CaveOfDishonourEnterFloor2TerminateMetric,
    RunesOfVirtue2CaveOfDishonourTerminateMetric,
    RunesOfVirtue2ClimbLadderBehindLockedDoorTerminateMetric,
    RunesOfVirtue2FindLadderBackFromCastleTerminateMetric,
    RunesOfVirtue2FindLadderOutOfCavernOfHatredTerminateMetric,
    RunesOfVirtue2AttendCastleCeremonyTerminateMetric,
    RunesOfVirtue2GiveCheeseToSherryTerminateMetric,
    RunesOfVirtue2GrabCheeseFromKitchenTerminateMetric,
    RunesOfVirtue2InteractWithMapOnTableTerminateMetric,
    RunesOfVirtue2CavernOfHatredEnterFloor4TerminateMetric,
    RunesOfVirtue2CavernOfHatredEnterFloor5TerminateMetric,
    RunesOfVirtue2CavernOfHatredEnterFloor6TerminateMetric,
    RunesOfVirtue2CavernOfHatredEnterFloor7TerminateMetric,
    RunesOfVirtue2CavernOfHatredGate1UnlockedTerminateMetric,
    RunesOfVirtue2CavernOfHatredGrabKeyTerminateMetric,
    RunesOfVirtue2CavernOfHatredLadder2TerminateMetric,
    RunesOfVirtue2CavernOfHatredLadderRoom2TerminateMetric,
    RunesOfVirtue2CavernOfHatredTerminateMetric,
    RunesOfVirtue2DeathScreenTerminateMetric,
    RunesOfVirtue2LordWhitsaberDialogTerminateMetric,
    RunesOfVirtue2NystulDialogTerminateMetric,
    RunesOfVirtue2OpenMenuTerminateMetric,
    RunesOfVirtue2ReadBookTerminateMetric,
    RunesOfVirtue2SandyCookDialogTerminateMetric,
    RunesOfVirtue2SherryMouseDialogTerminateMetric,
    RunesOfVirtue2UnlockDoorAndSaveTholdenTerminateMetric,
)
from gameboy_worlds.emulation.tracker import (
    DummySubGoalMetric,
    StateTracker,
    TestTrackerMixin,
)


class CoreRunesOfVirtueTracker(StateTracker):
    """
    StateTracker for core Runes of Virtue metrics.
    """

    def start(self):
        super().start()
        self.metric_classes.extend([CoreRunesOfVirtueMetrics])


class RunesOfVirtueOCRTracker(CoreRunesOfVirtueTracker):
    """
    StateTracker for core Runes of Virtue metrics and OCR region captures.
    """

    def start(self):
        super().start()
        self.metric_classes.extend([RunesOfVirtueOCRMetric])


class RunesOfVirtueTestTracker(TestTrackerMixin, RunesOfVirtueOCRTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Runes of Virtue games.
    """

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue1OpenMenuTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1OpenMenuTestTracker(RunesOfVirtueTestTracker):
    """
    A TestTracker for Runes of Virtue 1 that ends an episode when the player opens the inventory menu.
    """

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue1OpenMenuTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2OpenMenuTestTracker(RunesOfVirtueTestTracker):
    """
    A TestTracker for Runes of Virtue 2 that ends an episode when the player opens the inventory menu.
    """

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue2OpenMenuTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2ReadBookTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player opens a book."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue2ReadBookTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2BlockedRoomEnteredTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player has entered the blocked room."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue2BlockedRoomEnteredTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2NystulDialogTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player is in dialog with Nystul."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue2NystulDialogTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2BlacksmithFailBuyShieldTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the blacksmith's failed shield purchase dialog is shown."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2BlacksmithFailBuyShieldTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2SherryMouseDialogTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when Sherry the mouse's dialog is shown."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue2SherryMouseDialogTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2SandyCookDialogTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when Sandy the cook's dialog is shown."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue2SandyCookDialogTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2LordWhitsaberDialogTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when Lord Whitsaber's dialog is shown."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue2LordWhitsaberDialogTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CaveOfDishonourTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player has entered the Cave of Dishonour."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue2CaveOfDishonourTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfHatredTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player has entered the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue2CavernOfHatredTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CaveOfDishonourEnterFloor2TestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player enters floor 2 in the Cave of Dishonour."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CaveOfDishonourEnterFloor2TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CaveOfDishonourEnterFloor3TestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player enters floor 3 in the Cave of Dishonour."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CaveOfDishonourEnterFloor3TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2GrabCheeseFromKitchenTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player grabs the cheese from the kitchen."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2GrabCheeseFromKitchenTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2GiveCheeseToSherryTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player gives the cheese to Sherry."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2GiveCheeseToSherryTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2ClimbLadderBehindLockedDoorTestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player climbs the ladder behind the locked door."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2ClimbLadderBehindLockedDoorTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2InteractWithMapOnTableTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player interacts with the map on the table."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2InteractWithMapOnTableTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2FindLadderBackFromCastleTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player finds a ladder back from the castle."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2FindLadderBackFromCastleTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2UnlockDoorAndSaveTholdenTestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player unlocks the door and saves Tholden."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2UnlockDoorAndSaveTholdenTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2FindLadderOutOfCavernOfHatredTestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player finds a ladder out of the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2FindLadderOutOfCavernOfHatredTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2BringTholdenBackToKingTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player brings Tholden back to the king."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2BringTholdenBackToKingTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2AttendCastleCeremonyTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player attends the ceremony in the castle."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2AttendCastleCeremonyTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfHatredGate1UnlockedTestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the first Cavern of Hatred gate is unlocked."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CavernOfHatredGate1UnlockedTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfHatredLadderRoom2TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters the second ladder room in the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CavernOfHatredLadderRoom2TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfHatredLadder2TestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player reaches the second ladder in the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue2CavernOfHatredLadder2TerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfHatredGrabKeyTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player grabs the key in the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue2CavernOfHatredGrabKeyTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfHatredEnterFloor4TestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player enters floor 4 in the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CavernOfHatredEnterFloor4TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfHatredEnterFloor5TestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player enters floor 5 in the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CavernOfHatredEnterFloor5TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfHatredEnterFloor6TestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player enters floor 6 in the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CavernOfHatredEnterFloor6TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfHatredEnterFloor7TestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player enters floor 7 in the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CavernOfHatredEnterFloor7TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2DeathScreenTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the death / game over screen is shown."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue2DeathScreenTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1KingDialogTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player is in dialog with the king."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue1KingDialogTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1ChucklesDialogTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player is in dialog with Chuckles."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue1ChucklesDialogTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1GnuGnu1DialogTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player is in dialog with Gnu Gnu at his 1st store."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue1GnuGnu1DialogTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1GnuGnu2DialogTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player is in dialog with Gnu Gnu at his 2nd store."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue1GnuGnu2DialogTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1SherryDialogTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player is in dialog with Sherry."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue1SherryDialogTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfHatredTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player has entered the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue1CavernOfHatredTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfDeceitTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player has entered the Cavern of Deceit."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue1CavernOfDeceitTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfCowardiceTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player has entered the Cavern of Cowardice."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue1CavernOfCowardiceTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfCowardiceEnterFloor2TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters floor 2 of the Cavern of Cowardice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfCowardiceEnterFloor2TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfCowardiceEnterFloor3TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters floor 3 of the Cavern of Cowardice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfCowardiceEnterFloor3TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfCowardiceFloor3ChestOpenedTestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player opens the floor 3 chest in the Cavern of Cowardice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfCowardiceFloor3ChestOpenedTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfCowardiceEnterFloor4TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters floor 4 of the Cavern of Cowardice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfCowardiceEnterFloor4TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfCowardiceSherryFloor4DialogTestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player is in dialog with Sherry on floor 4 of the Cavern of Cowardice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfCowardiceSherryFloor4DialogTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfCowardiceTakeStewFloor4TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player takes stew on floor 4 of the Cavern of Cowardice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfCowardiceTakeStewFloor4TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfCowardiceObtainCoinFloor4TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player obtains the coin on floor 4 of the Cavern of Cowardice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfCowardiceObtainCoinFloor4TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1DrCatDialogTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player is in dialog with Dr. Cat."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue1DrCatDialogTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1DrCatCatsLairDialogTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player is in dialog with Dr. Cat in the Cat's Lair."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1DrCatCatsLairDialogTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1ShipRiddenTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player rides the ship."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue1ShipRiddenTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1BasementLadderUnlockedTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player unlocks the basement ladder."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue1BasementLadderUnlockedTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1BasementChestOpenedTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player opens the basement chest."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue1BasementChestOpenedTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfHatredEnterFloor2TestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player enters floor 2 of the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfHatredEnterFloor2TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfHatredSherryFloor2DialogTestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when Sherry's floor 2 dialog is on screen in the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfHatredSherryFloor2DialogTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfHatredChooseDoorWithSherryTestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when Sherry asks the player to choose a door in the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfHatredChooseDoorWithSherryTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfHatredChooseRightDoorMelissaDialogTestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when Melissa's dialog is on screen after choosing the right door."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfHatredChooseRightDoorMelissaDialogTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfHatredEnterFloor3TestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player enters floor 3 of the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfHatredEnterFloor3TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfHatredEnterFloor4TestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player enters floor 4 of the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfHatredEnterFloor4TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfHatredChestFloor1OpenedTestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player opens the floor 1 chest in the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfHatredChestFloor1OpenedTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1TelescopeViewTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player is looking through the telescope."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue1TelescopeViewTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1DeathScreenTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the death / game over screen is shown."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue1DeathScreenTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric
