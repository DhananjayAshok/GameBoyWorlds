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
    RunesOfVirtue1CavernOfHatredEnterFloor5TerminateMetric,
    RunesOfVirtue1CavernOfHatredTalkToKlopFloor5TerminateMetric,
    RunesOfVirtue1CavernOfHatredTalkToKlipFloor5TerminateMetric,
    RunesOfVirtue1CavernOfHatredObtainAxeFloor5TerminateMetric,
    RunesOfVirtue1CavernOfHatredExitedTerminateMetric,
    RunesOfVirtue1CavernOfHatredTerminateMetric,
    RunesOfVirtue1CavernOfCowardiceTerminateMetric,
    RunesOfVirtue1CavernOfCowardiceEnterFloor2TerminateMetric,
    RunesOfVirtue1CavernOfCowardiceEnterFloor3TerminateMetric,
    RunesOfVirtue1CavernOfCowardiceFloor3ChestOpenedTerminateMetric,
    RunesOfVirtue1CavernOfCowardiceEnterFloor4TerminateMetric,
    RunesOfVirtue1CavernOfCowardiceSherryFloor4DialogTerminateMetric,
    RunesOfVirtue1CavernOfCowardiceTakeStewFloor4TerminateMetric,
    RunesOfVirtue1CavernOfCowardiceObtainCoinFloor4TerminateMetric,
    RunesOfVirtue1CavernOfCowardiceEnterFloor5TerminateMetric,
    RunesOfVirtue1CavernOfCowardiceObtainKeyFromDrCatFloor5TerminateMetric,
    RunesOfVirtue1CavernOfCowardiceEnterFloor6TerminateMetric,
    RunesOfVirtue1CavernOfCowardiceEnterSecretDoorFloor6TerminateMetric,
    RunesOfVirtue1CavernOfCowardiceTalkToSherryFloor6TerminateMetric,
    RunesOfVirtue1CavernOfCowardiceTalkToChucklesFloor6TerminateMetric,
    RunesOfVirtue1CavernOfCowardiceObtainMagicRopeFloor6TerminateMetric,
    RunesOfVirtue1CavernOfHatredChestFloor1OpenedTerminateMetric,
    RunesOfVirtue1CavernOfDeceitTerminateMetric,
    RunesOfVirtue1CavernOfDeceitEnterFloor2TerminateMetric,
    RunesOfVirtue1CavernOfDeceitEnterFloor3TerminateMetric,
    RunesOfVirtue1CavernOfDeceitEnterFloor4TerminateMetric,
    RunesOfVirtue1ChucklesDialogTerminateMetric,
    RunesOfVirtue1DeathScreenTerminateMetric,
    RunesOfVirtue1DrCatDialogTerminateMetric,
    RunesOfVirtue1CavernOfDeceitTalkToFinnFloor1TerminateMetric,
    RunesOfVirtue1CavernOfDeceitTalkToKadorFloor3TerminateMetric,
    RunesOfVirtue1CavernOfDeceitTalkToFinnFloor3TerminateMetric,
    RunesOfVirtue1CavernOfDeceitEnterEastDoorFloor1TerminateMetric,
    RunesOfVirtue1DrCatCatsLairDialogTerminateMetric,
    RunesOfVirtue1BuyTwoCakesTerminateMetric,
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
    RunesOfVirtue2CaveOfDishonourLordWhitsaberFloor4TerminateMetric,
    RunesOfVirtue2CaveOfDishonourEquipRodFloor3TerminateMetric,
    RunesOfVirtue2CaveOfDishonourEnterFloor3BlockedTerminateMetric,
    RunesOfVirtue2CaveOfDishonourEnterFloor4TerminateMetric,
    RunesOfVirtue2CaveOfDishonourExitedTerminateMetric,
    RunesOfVirtue2CityOfYewEnteredTerminateMetric,
    RunesOfVirtue2CityOfYewWelcomeSignReadTerminateMetric,
    RunesOfVirtue2MandrakeBardDialogTerminateMetric,
    RunesOfVirtue2CavernOfInjusticeTalkToZoltanFloor4TerminateMetric,
    RunesOfVirtue2CavernOfInjusticeReadHintFloor5TerminateMetric,
    RunesOfVirtue2CavernOfInjusticeTalkToTerryFloor5TerminateMetric,
    RunesOfVirtue2CavernOfInjusticeEnteredTerminateMetric,
    RunesOfVirtue2CavernOfInjusticeEnterFloor2TerminateMetric,
    RunesOfVirtue2CavernOfInjusticeEnterFloor3TerminateMetric,
    RunesOfVirtue2CavernOfInjusticeEnterFloor4TerminateMetric,
    RunesOfVirtue2CavernOfInjusticeEnterFloor5TerminateMetric,
    RunesOfVirtue2CavernOfInjusticeEnterFloor6TerminateMetric,
    RunesOfVirtue2CavernOfInjusticeEnterFloor7TerminateMetric,
    RunesOfVirtue2CavernOfInjusticeEnterEastPortalFloor3TerminateMetric,
    RunesOfVirtue2CaveOfDishonourEnterFloor3TerminateMetric,
    RunesOfVirtue2CaveOfDishonourEnterFloor2TerminateMetric,
    RunesOfVirtue2CaveOfDishonourTerminateMetric,
    RunesOfVirtue2ClimbLadderBehindLockedDoorTerminateMetric,
    RunesOfVirtue2FindLadderBackFromCastleTerminateMetric,
    RunesOfVirtue2FindLadderOutOfCavernOfHatredTerminateMetric,
    RunesOfVirtue2AttendCastleCeremonyTerminateMetric,
    RunesOfVirtue2RuneOfHonourObtainedTerminateMetric,
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


class RunesOfVirtue2CaveOfDishonourLordWhitsaberFloor4TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when Lord Whitsaber's floor 4 dialog is shown in the Cave of Dishonour."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CaveOfDishonourLordWhitsaberFloor4TerminateMetric
    )
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


class RunesOfVirtue2CaveOfDishonourEquipRodFloor3TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player equips the rod on floor 3 in the Cave of Dishonour."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CaveOfDishonourEquipRodFloor3TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CaveOfDishonourEnterFloor3BlockedTestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player reaches the blocked path on floor 3 in the Cave of Dishonour."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CaveOfDishonourEnterFloor3BlockedTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CaveOfDishonourEnterFloor4TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters floor 4 in the Cave of Dishonour."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CaveOfDishonourEnterFloor4TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CaveOfDishonourExitedTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player exits the Cave of Dishonour."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CaveOfDishonourExitedTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CityOfYewEnteredTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player enters the city of Yew."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue2CityOfYewEnteredTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CityOfYewWelcomeSignReadTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player reads the welcome sign in the city of Yew."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CityOfYewWelcomeSignReadTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2MandrakeBardDialogTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when Mandrake the Bard's dialog is shown."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue2MandrakeBardDialogTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfInjusticeTalkToZoltanFloor4TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when Zoltan's floor 4 dialog is shown."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CavernOfInjusticeTalkToZoltanFloor4TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfInjusticeReadHintFloor5TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player reads the floor 5 hint."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CavernOfInjusticeReadHintFloor5TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfInjusticeTalkToTerryFloor5TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when Terry's floor 5 dialog is shown."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CavernOfInjusticeTalkToTerryFloor5TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfInjusticeEnteredTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player enters the Cavern of Injustice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CavernOfInjusticeEnteredTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfInjusticeEnterFloor2TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters floor 2 of the Cavern of Injustice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CavernOfInjusticeEnterFloor2TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfInjusticeEnterFloor3TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters floor 3 of the Cavern of Injustice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CavernOfInjusticeEnterFloor3TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfInjusticeEnterFloor4TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters floor 4 of the Cavern of Injustice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CavernOfInjusticeEnterFloor4TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfInjusticeEnterFloor5TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters floor 5 of the Cavern of Injustice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CavernOfInjusticeEnterFloor5TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfInjusticeEnterFloor6TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters floor 6 of the Cavern of Injustice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CavernOfInjusticeEnterFloor6TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfInjusticeEnterFloor7TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters floor 7 of the Cavern of Injustice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CavernOfInjusticeEnterFloor7TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue2CavernOfInjusticeEnterEastPortalFloor3TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters the east portal on floor 3."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2CavernOfInjusticeEnterEastPortalFloor3TerminateMetric
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


class RunesOfVirtue2RuneOfHonourObtainedTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player obtains the Rune of Honour."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue2RuneOfHonourObtainedTerminateMetric
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


class RunesOfVirtue1CavernOfDeceitEnterFloor2TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters floor 2 of the Cavern of Deceit."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfDeceitEnterFloor2TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfDeceitEnterFloor3TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters floor 3 of the Cavern of Deceit."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfDeceitEnterFloor3TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfDeceitEnterFloor4TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters floor 4 of the Cavern of Deceit."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfDeceitEnterFloor4TerminateMetric
    )
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


class RunesOfVirtue1CavernOfCowardiceEnterFloor5TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters floor 5 of the Cavern of Cowardice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfCowardiceEnterFloor5TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfCowardiceObtainKeyFromDrCatFloor5TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player obtains the key from Dr. Cat on floor 5 of the Cavern of Cowardice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfCowardiceObtainKeyFromDrCatFloor5TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfCowardiceEnterFloor6TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters floor 6 of the Cavern of Cowardice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfCowardiceEnterFloor6TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfCowardiceEnterSecretDoorFloor6TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters the secret door on floor 6 of the Cavern of Cowardice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfCowardiceEnterSecretDoorFloor6TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfCowardiceTalkToSherryFloor6TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player is in dialog with Sherry on floor 6 of the Cavern of Cowardice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfCowardiceTalkToSherryFloor6TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfCowardiceTalkToChucklesFloor6TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player is in dialog with Chuckles on floor 6 of the Cavern of Cowardice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfCowardiceTalkToChucklesFloor6TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfCowardiceObtainMagicRopeFloor6TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player obtains the magic rope on floor 6 of the Cavern of Cowardice."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfCowardiceObtainMagicRopeFloor6TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1DrCatDialogTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player is in dialog with Dr. Cat."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue1DrCatDialogTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfDeceitTalkToFinnFloor1TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player is in dialog with Finn on floor 1 of the Cavern of Deceit."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfDeceitTalkToFinnFloor1TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfDeceitTalkToKadorFloor3TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player is in dialog with Kador on floor 3 of the Cavern of Deceit."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfDeceitTalkToKadorFloor3TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfDeceitTalkToFinnFloor3TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player is in dialog with Finn on floor 3 of the Cavern of Deceit."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfDeceitTalkToFinnFloor3TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfDeceitEnterEastDoorFloor1TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player enters the east door on floor 1 of the Cavern of Deceit."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfDeceitEnterEastDoorFloor1TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1DrCatCatsLairDialogTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player is in dialog with Dr. Cat in the Cat's Lair."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1DrCatCatsLairDialogTerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1BuyTwoCakesTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player buys two cakes."""

    TERMINATION_TRUNCATION_METRIC = RunesOfVirtue1BuyTwoCakesTerminateMetric
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


class RunesOfVirtue1CavernOfHatredEnterFloor5TestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player enters floor 5 of the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfHatredEnterFloor5TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfHatredTalkToKlopFloor5TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player is in dialog with Klop on floor 5 of the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfHatredTalkToKlopFloor5TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfHatredTalkToKlipFloor5TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player is in dialog with Klip on floor 5 of the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfHatredTalkToKlipFloor5TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfHatredObtainAxeFloor5TestTracker(
    RunesOfVirtueTestTracker
):
    """Ends an episode when the player obtains the axe on floor 5 of the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfHatredObtainAxeFloor5TerminateMetric
    )
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1CavernOfHatredExitedTestTracker(RunesOfVirtueTestTracker):
    """Ends an episode when the player exits the Cavern of Hatred."""

    TERMINATION_TRUNCATION_METRIC = (
        RunesOfVirtue1CavernOfHatredExitedTerminateMetric
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
