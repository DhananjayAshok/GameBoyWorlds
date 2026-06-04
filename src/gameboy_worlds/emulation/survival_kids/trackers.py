"""State trackers for Survival Kids."""

from gameboy_worlds.emulation.tracker import StateTracker
from gameboy_worlds.emulation.tracker import DummySubGoalMetric, TestTrackerMixin
from gameboy_worlds.emulation.survival_kids.base_metrics import (
    CoreSurvivalKidsMetrics,
    SurvivalKidsExploreMetrics,
    SurvivalKidsHudMetrics,
    SurvivalKidsOCRMetric,
    SurvivalKidsVitalMetrics,
)
from gameboy_worlds.emulation.survival_kids.test_metrics import (
    AfterFillingWaterTerminateMetric,
    BagIconTerminateMetric,
    AnimalKilledTerminateMetric,
    CanteenActionMenuTerminateMetric,
    CanteenChosenTerminateMetric,
    CanteenDrinkSelectedTerminateMetric,
    CanteenPickupDialogueTerminateMetric,
    CanteenTakeLeaveMenuTerminateMetric,
    CanteenUseSelectedTerminateMetric,
    Chapter1PathClearedTerminateMetric,
    DayReferenceTerminateMetric,
    DrinkWaterTerminateMetric,
    EnteredShelterTerminateMetric,
    FeatherTakeLeaveMenuTerminateMetric,
    FireLitTerminateMetric,
    FoundRiverTerminateMetric,
    GameViewportChangedTerminateMetric,
    GotTheBrdfeatherTerminateMetric,
    GotTheStickTerminateMetric,
    GotTheTreeBarkTerminateMetric,
    GotTheWaterTerminateMetric,
    HpChangedTerminateMetric,
    HungerChangedTerminateMetric,
    InTheShelterTerminateMetric,
    InventoryOpenTerminateMetric,
    KindlingMergedTerminateMetric,
    KnifeEquippedScreenTerminateMetric,
    KnifeChosenTerminateMetric,
    KnifeEquippedTerminateMetric,
    MergeConfirmTerminateMetric,
    MergeMenuTerminateMetric,
    MeatActionMenuTerminateMetric,
    MeatEatenDialogueTerminateMetric,
    MeatEatSelectedTerminateMetric,
    NightReferenceTerminateMetric,
    PickupItemDialogueTerminateMetric,
    PathAfterBlockingGrassTerminateMetric,
    ResolveHungerTerminateMetric,
    SelectKindlingTerminateMetric,
    SelectTakeTerminateMetric,
    StaminaChangedTerminateMetric,
    StatusBarChangedTerminateMetric,
    TakeLeaveMenuTerminateMetric,
    ThirstChangedTerminateMetric,
    UseKindlingTerminateMetric,
    WaterMenuOpenTerminateMetric,
)


class SurvivalKidsTracker(StateTracker):
    def start(self):
        super().start()
        self.metric_classes.extend([CoreSurvivalKidsMetrics, SurvivalKidsExploreMetrics])


class SurvivalKidsVitalsTracker(SurvivalKidsTracker):
    def start(self):
        super().start()
        self.metric_classes.extend([SurvivalKidsVitalMetrics])


class SurvivalKidsHudTracker(SurvivalKidsTracker):
    def start(self):
        super().start()
        self.metric_classes.extend([SurvivalKidsHudMetrics])


class SurvivalKidsOCRTracker(SurvivalKidsHudTracker):
    def start(self):
        super().start()
        self.metric_classes.extend([SurvivalKidsOCRMetric])


class SurvivalKidsTestTracker(TestTrackerMixin, SurvivalKidsOCRTracker):
    TERMINATION_TRUNCATION_METRIC = StatusBarChangedTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SurvivalKidsStatusBarChangedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = StatusBarChangedTerminateMetric


class SurvivalKidsHpChangedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = HpChangedTerminateMetric


class SurvivalKidsHungerChangedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = HungerChangedTerminateMetric


class SurvivalKidsResolveHungerTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = ResolveHungerTerminateMetric


class SurvivalKidsThirstChangedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = ThirstChangedTerminateMetric


class SurvivalKidsDrinkWaterTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = DrinkWaterTerminateMetric


class SurvivalKidsStaminaChangedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = StaminaChangedTerminateMetric


class SurvivalKidsGameViewportChangedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GameViewportChangedTerminateMetric


class SurvivalKidsInventoryOpenTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = InventoryOpenTerminateMetric


class SurvivalKidsPickupItemDialogueTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = PickupItemDialogueTerminateMetric


class SurvivalKidsCanteenPickupDialogueTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = CanteenPickupDialogueTerminateMetric


class SurvivalKidsBagIconTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = BagIconTerminateMetric


class SurvivalKidsKnifeEquippedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = KnifeEquippedTerminateMetric


class SurvivalKidsKnifeEquippedScreenTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = KnifeEquippedScreenTerminateMetric


class SurvivalKidsKnifeChosenTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = KnifeChosenTerminateMetric


class SurvivalKidsMergeMenuTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = MergeMenuTerminateMetric


class SurvivalKidsMergeConfirmTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = MergeConfirmTerminateMetric


class SurvivalKidsCanteenChosenTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = CanteenChosenTerminateMetric


class SurvivalKidsKindlingMergedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = KindlingMergedTerminateMetric


class SurvivalKidsTakeLeaveMenuTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = TakeLeaveMenuTerminateMetric


class SurvivalKidsSelectTakeTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = SelectTakeTerminateMetric


class SurvivalKidsCanteenTakeLeaveMenuTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = CanteenTakeLeaveMenuTerminateMetric


class SurvivalKidsCanteenActionMenuTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = CanteenActionMenuTerminateMetric


class SurvivalKidsCanteenUseSelectedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = CanteenUseSelectedTerminateMetric


class SurvivalKidsCanteenDrinkSelectedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = CanteenDrinkSelectedTerminateMetric


class SurvivalKidsAnimalKilledTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = AnimalKilledTerminateMetric


class SurvivalKidsChapter1PathClearedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = Chapter1PathClearedTerminateMetric


class SurvivalKidsPathAfterBlockingGrassTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = PathAfterBlockingGrassTerminateMetric


class SurvivalKidsInTheShelterTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = InTheShelterTerminateMetric


class SurvivalKidsNewPath1FoundTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = NewPath1FoundTerminateMetric


class SurvivalKidsNewPath2FoundTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = NewPath2FoundTerminateMetric


class SurvivalKidsSharpStoneFoundTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = SharpStoneFoundTerminateMetric


class SurvivalKidsDayReferenceTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = DayReferenceTerminateMetric


class SurvivalKidsNightReferenceTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = NightReferenceTerminateMetric


class SurvivalKidsEnteredShelterTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnteredShelterTerminateMetric


class SurvivalKidsFoundRiverTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = FoundRiverTerminateMetric


class SurvivalKidsWaterMenuOpenTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = WaterMenuOpenTerminateMetric


class SurvivalKidsAfterFillingWaterTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = AfterFillingWaterTerminateMetric


class SurvivalKidsGotTheWaterTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GotTheWaterTerminateMetric


class SurvivalKidsGotTheStickTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GotTheStickTerminateMetric


class SurvivalKidsGotTheTreeBarkTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GotTheTreeBarkTerminateMetric


class SurvivalKidsGotTheBrdfeatherTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = GotTheBrdfeatherTerminateMetric


class SurvivalKidsSelectKindlingTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = SelectKindlingTerminateMetric


class SurvivalKidsUseKindlingTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = UseKindlingTerminateMetric


class SurvivalKidsFireLitTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = FireLitTerminateMetric


class SurvivalKidsFeatherTakeLeaveMenuTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = FeatherTakeLeaveMenuTerminateMetric


class SurvivalKidsMeatActionMenuTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = MeatActionMenuTerminateMetric


class SurvivalKidsMeatEatSelectedTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = MeatEatSelectedTerminateMetric


class SurvivalKidsMeatEatenDialogueTracker(SurvivalKidsTestTracker):
    TERMINATION_TRUNCATION_METRIC = MeatEatenDialogueTerminateMetric
