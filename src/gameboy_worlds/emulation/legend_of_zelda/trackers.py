from gameboy_worlds.emulation.legend_of_zelda.base_metrics import (
    CoreLegendOfZeldaMetrics,
)

from gameboy_worlds.emulation.legend_of_zelda.test_metrics import (
    ToronboShorePickupSwordTerminateMetric,
    ShieldEquippedTerminateMetric,
    OutsideTarinHouseTerminateMetric,
    OpenInventoryTerminateMetric,
    NoWeaponTerminateMetric,
    YesWeaponTerminateMetric,
    TalkToKidTerminateMetric,
    StatueTalkTerminateMetric,
    ReadSignboardTerminateMetric,
    GoInsideShopTerminateMetric,
    MakeCallTerminateMetric,
    EnterDarkForestTerminateMetric,
    InsideTunnelTerminateMetric,
    OpenChestTerminateMetric,
    HeartTakeTerminateMetric,
    ShroomTakeTerminateMetric,
    ShroomSwordTerminateMetric,
    ShroomShieldTerminateMetric,
    SignCheckerTerminateMetric,
    WaterCheckerTerminateMetric,
    MakeCall2TerminateMetric,
    SkeletonHouseTerminateMetric,
    UndergroundTerminateMetric,
    DiamondKidTalkTerminateMetric,
    InsideHouseTerminateMetric,
    PotRoomTerminateMetric,
    PondTerminateMetric,
    WeirdTunnelInsideTerminateMetric,
    WitchTalkTerminateMetric,
    PotholesSignboardReadTerminateMetric,
    PineappleScreenTerminateMetric,
    CallBoothApproachTerminateMetric,
    GrannyCornerTerminateMetric,
    LeaveBaldStoreCarpetTerminateMetric,
    LeaveTrackTerminateMetric,
    ExitFatHouseTerminateMetric,
    BoothHouseUpTerminateMetric,
    ChickHouseBlockTerminateMetric,
    PurplestoneStairsTerminateMetric,
    HeavyStonePushTerminateMetric,
    BoyDialogueExitTerminateMetric,
    DirtPatchTerminateMetric,
    DirtPatchTwoTerminateMetric,
    StonehouseRightTreeTerminateMetric,
    SecondBoyDialogueExitTerminateMetric,
    RailingJumpTerminateMetric,
    PalmtJumpTerminateMetric,
    MonsterDeathTerminateMetric,
    TileslongEscapeTerminateMetric,
    BoardSignApproachTerminateMetric,
    OracleOtherPeopleTerminateMetric,
    OracleGirlTalkTerminateMetric,
    OracleJumpingTerminateMetric,
    OracleFarmerTalkTerminateMetric,
    OracleLibraryTerminateMetric,
    OracleParrotTalkTerminateMetric,
    OracleFallTerminateMetric,
    OracleStairsTerminateMetric,
    OracleSignboardReadTerminateMetric,
    OracleShopInsideTerminateMetric,
    OracleShopPersonTalkTerminateMetric,
    OracleGirlHouseTerminateMetric,
    OraclePotInteractionTerminateMetric,
    OracleInsideTunnelTerminateMetric,
    OracleArtistTalkTerminateMetric,
    OracleChickenHouseTerminateMetric,
    OracleJigglyPathWalkTerminateMetric,
    OracleFairyMeetTerminateMetric,
    OracleThingInteractionTerminateMetric,
    OracleInventoryOpenTerminateMetric,
    OracleClockTowerSignReadTerminateMetric,
    OracleNearStairsTerminateMetric,
    OracleTalkToGirlTerminateMetric,
    OraclePierGoTerminateMetric,
    OracleBoardwalkTerminateMetric,
    OracleCatCheckTerminateMetric,
    OracleCatTalkTerminateMetric,
    OracleOwnerTalkTerminateMetric,
    OracleBridgeWalkTerminateMetric,
    OracleDogTerminateMetric,
    OracleMickeyLeftTerminateMetric,
    OracleStepOffGrassBlockTerminateMetric,
    OracleShopSignPathTerminateMetric,
    OracleClocksUpTerminateMetric,
    OracleJoystickRightTerminateMetric,
    OracleJoystickHouseEntryTerminateMetric,
    OracleApproachRedSnakeTerminateMetric,
    OracleApproachBlueSnakeTerminateMetric,
    OracleRedSnakeTalkTerminateMetric,
    OracleBlueSnakeTalkTerminateMetric,
    OracleBlueBookReadTerminateMetric,
    OracleRedBookReadTerminateMetric,
    OracleLavaFloorTerminateMetric,
    OracleStepOffTrackTerminateMetric,
    OracleGloomyPlaceLeftTerminateMetric,
    OracleGameoverDeathTerminateMetric,
    OracleLeaveGreenCarpetTerminateMetric,
    OracleHolesToTrunkTerminateMetric,
    OracleTrunkToHolesTerminateMetric,
    OracleLeftOfTrunkTerminateMetric,
)

# from gameboy_worlds.emulation.tracker import (
#     StateTracker, 
#     TestTrackerMixin,
#     DummySubGoalMetric
# )

from gameboy_worlds.emulation.tracker import (
    StateTracker,
    TestTrackerMixin,
    SubGoal,
    SubGoalMetric,
    DummySubGoalMetric
)

class CoreLegendOfZeldaTracker(StateTracker):
    """
    StateTracker for core Legend of Zelda metrics.
    """

    def start(self):
        super().start()
        self.metric_classes.extend([CoreLegendOfZeldaMetrics])

# class ZeldaLinksAwakeningOwlTestTracker(
#     TestTrackerMixin, CoreLegendOfZeldaTracker
# ):
#     TERMINATION_TRUNCATION_METRIC = ToronboShorePickupSwordTerminateMetric
#     SUBGOAL_METRIC = DummySubGoalMetric

class OwlTrackerSubGoal(SubGoal):
    NAME = "owl_tracker"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "owl_tracker")


class ZeldaOwlSubGoalMetric(SubGoalMetric):
    SUBGOALS = [OwlTrackerSubGoal]


class ZeldaLinksAwakeningOwlTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = ToronboShorePickupSwordTerminateMetric
    SUBGOAL_METRIC = ZeldaOwlSubGoalMetric


class DialogueSubGoal(SubGoal):
    NAME = "tarian_dialogue"

    def _check_completed(self, frame, parser) -> bool:
        in_dialogue_region = parser.named_region_matches_target(frame, "dialogue_top")
        in_dialogue_state = parser.get_agent_state(frame) == "in_dialogue"
        return in_dialogue_region and in_dialogue_state


class ShieldSubGoalMetric(SubGoalMetric):
    SUBGOALS = [DialogueSubGoal]


class ZeldaLinksAwakeningShieldTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = ShieldEquippedTerminateMetric
    SUBGOAL_METRIC = ShieldSubGoalMetric

class ZeldaLinksAwakeningOutsideTarinHouseTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = OutsideTarinHouseTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric

class ZeldaLinksAwakeningOpenInventoryTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = OpenInventoryTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class InventoryOpenSubGoal(SubGoal):
    NAME = "health_bar_top"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "health_bar_top")


class InventoryOpenSubGoalMetric(SubGoalMetric):
    SUBGOALS = [InventoryOpenSubGoal]


class ZeldaLinksAwakeningWeaponTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = NoWeaponTerminateMetric
    SUBGOAL_METRIC = InventoryOpenSubGoalMetric


class ZeldaLinksAwakeningInventoryWeaponEquipTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = YesWeaponTerminateMetric
    SUBGOAL_METRIC = InventoryOpenSubGoalMetric

class LibrarySubGoal(SubGoal):
    NAME = "library"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "library")
    
class TalkToKidSubGoalMetric(SubGoalMetric):
    SUBGOALS = [LibrarySubGoal]

class ZeldaLinksAwakeningTalkToKidTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = TalkToKidTerminateMetric
    SUBGOAL_METRIC = TalkToKidSubGoalMetric


class ZeldaLinksAwakeningStatueTalkTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = StatueTalkTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric

class SignboardSubGoal(SubGoal):
    NAME = "signboard"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "signboard")

class ReadSignboardSubGoalMetric(SubGoalMetric):
    SUBGOALS = [SignboardSubGoal]

class ZeldaLinksAwakeningReadSignboardTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = ReadSignboardTerminateMetric
    SUBGOAL_METRIC = ReadSignboardSubGoalMetric

class ShopSignboardSubGoal(SubGoal):
    NAME = "shop_signboard"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "shop_signboard_tracker")


class GoInsideShopSubGoalMetric(SubGoalMetric):
    SUBGOALS = [ShopSignboardSubGoal]


class ZeldaLinksAwakeningGoInsideShopTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = GoInsideShopTerminateMetric
    SUBGOAL_METRIC = GoInsideShopSubGoalMetric


class CallBoothSubGoal(SubGoal):
    NAME = "call_booth"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "call_booth")


class MakeCallSubGoalMetric(SubGoalMetric):
    SUBGOALS = [CallBoothSubGoal]


class ZeldaLinksAwakeningMakeCallTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = MakeCallTerminateMetric
    SUBGOAL_METRIC = MakeCallSubGoalMetric

class BushOutsideForestSubGoal(SubGoal):
    NAME = "bush_outside_forest"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "bush_outside_forest")


class EnterDarkForestSubGoalMetric(SubGoalMetric):
    SUBGOALS = [BushOutsideForestSubGoal]


class ZeldaLinksAwakeningEnterDarkForestTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = EnterDarkForestTerminateMetric
    SUBGOAL_METRIC = EnterDarkForestSubGoalMetric


class StoneBreakSubGoal(SubGoal):
    NAME = "stone_break"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "stone_break_tracker")


class OpenChestSubGoalMetric(SubGoalMetric):
    SUBGOALS = [StoneBreakSubGoal]


class ZeldaLinksAwakeningInsideTunnelTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = InsideTunnelTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningOpenChestTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = OpenChestTerminateMetric
    SUBGOAL_METRIC = OpenChestSubGoalMetric


class ZeldaLinksAwakeningChestOpenerTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = OpenChestTerminateMetric
    SUBGOAL_METRIC = OpenChestSubGoalMetric


class ZeldaLinksAwakeningHeartTakeTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = HeartTakeTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningShroomTakeTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = ShroomTakeTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningShroomSwordTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = ShroomSwordTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningShroomShieldTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = ShroomShieldTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningSignCheckerTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = SignCheckerTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningWaterCheckerTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = WaterCheckerTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric

class NoGrassSubGoal(SubGoal):
    NAME = "no_grass"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "no_grass")


class UndergroundSubGoalMetric(SubGoalMetric):
    SUBGOALS = [NoGrassSubGoal]


class HouseRightWindowSubGoal(SubGoal):
    NAME = "house_right_window"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "house_right_window")


class InsideHouseSubGoalMetric(SubGoalMetric):
    SUBGOALS = [HouseRightWindowSubGoal]


class PotSubGoal(SubGoal):
    NAME = "pot"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "pot")


class PotRoomSubGoalMetric(SubGoalMetric):
    SUBGOALS = [PotSubGoal]


class WitchSubGoal(SubGoal):
    NAME = "witch_tracker"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "witch_tracker")


class WitchTalkSubGoalMetric(SubGoalMetric):
    SUBGOALS = [WitchSubGoal]


class PotholesSignboardSubGoal(SubGoal):
    NAME = "signboard_tracker"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "signboard_tracker")


class PotholesSignboardSubGoalMetric(SubGoalMetric):
    SUBGOALS = [PotholesSignboardSubGoal]


class GrannySubGoal(SubGoal):
    NAME = "granny"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "granny")


class GrannySubGoalMetric(SubGoalMetric):
    SUBGOALS = [GrannySubGoal]


class Wood2SubGoal(SubGoal):
    NAME = "wood2"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "wood2")


class Wood2SubGoalMetric(SubGoalMetric):
    SUBGOALS = [Wood2SubGoal]


class TreeSubGoal(SubGoal):
    NAME = "tree"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "tree")


class TreeSubGoalMetric(SubGoalMetric):
    SUBGOALS = [TreeSubGoal]


class TileslongSubGoal(SubGoal):
    NAME = "tileslong"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "tileslong")


class TileslongSubGoalMetric(SubGoalMetric):
    SUBGOALS = [TileslongSubGoal]


class BoardsignSubGoal(SubGoal):
    NAME = "boardsign"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "boardsign")


class BoardsignSubGoalMetric(SubGoalMetric):
    SUBGOALS = [BoardsignSubGoal]


class Boy2ndSubGoal(SubGoal):
    NAME = "boy2nd"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "boy2nd")


class Boy2ndSubGoalMetric(SubGoalMetric):
    SUBGOALS = [Boy2ndSubGoal]


class BoysaySubGoal(SubGoal):
    NAME = "boysay"

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, "boysay")


class BoysaySubGoalMetric(SubGoalMetric):
    SUBGOALS = [BoysaySubGoal]


class ZeldaLinksAwakeningMakeCall2TestTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = MakeCall2TerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningSkeletonTestTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = SkeletonHouseTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningUndergroundTestTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = UndergroundTerminateMetric
    SUBGOAL_METRIC = UndergroundSubGoalMetric


class ZeldaLinksAwakeningKidTalkTestTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = DiamondKidTalkTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningInsideHouseTestTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = InsideHouseTerminateMetric
    SUBGOAL_METRIC = InsideHouseSubGoalMetric


class ZeldaLinksAwakeningPotRoomTestTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = PotRoomTerminateMetric
    SUBGOAL_METRIC = PotRoomSubGoalMetric


class ZeldaLinksAwakeningPondTestTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = PondTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningWeirdTunnelInsideTestTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = WeirdTunnelInsideTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningWitchTalkTestTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = WitchTalkTerminateMetric
    SUBGOAL_METRIC = WitchTalkSubGoalMetric


class ZeldaLinksAwakeningSignboardReaderTestTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = PotholesSignboardReadTerminateMetric
    SUBGOAL_METRIC = PotholesSignboardSubGoalMetric


class ZeldaLinksAwakeningPineappleScreenTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = PineappleScreenTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningCallBoothApproachTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = CallBoothApproachTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningGrannyCornerTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = GrannyCornerTerminateMetric
    SUBGOAL_METRIC = GrannySubGoalMetric


class ZeldaLinksAwakeningLeaveBaldStoreCarpetTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = LeaveBaldStoreCarpetTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningLeaveTrackTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = LeaveTrackTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningExitFatHouseTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = ExitFatHouseTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningBoothHouseUpTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = BoothHouseUpTerminateMetric
    SUBGOAL_METRIC = Wood2SubGoalMetric


class ZeldaLinksAwakeningChickHouseBlockTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = ChickHouseBlockTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningPurplestoneStairsTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = PurplestoneStairsTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningHeavyStonePushTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = HeavyStonePushTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningBoyDialogueExitTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = BoyDialogueExitTerminateMetric
    SUBGOAL_METRIC = Boy2ndSubGoalMetric


class ZeldaLinksAwakeningDirtPatchTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = DirtPatchTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningDirtPatchTwoTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = DirtPatchTwoTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningStonehouseRightTreeTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = StonehouseRightTreeTerminateMetric
    SUBGOAL_METRIC = TreeSubGoalMetric


class ZeldaLinksAwakeningSecondBoyDialogueExitTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = SecondBoyDialogueExitTerminateMetric
    SUBGOAL_METRIC = BoysaySubGoalMetric


class ZeldaLinksAwakeningRailingJumpTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = RailingJumpTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningPalmtJumpTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = PalmtJumpTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningMonsterDeathTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = MonsterDeathTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaLinksAwakeningTileslongEscapeTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = TileslongEscapeTerminateMetric
    SUBGOAL_METRIC = TileslongSubGoalMetric


class ZeldaLinksAwakeningBoardSignApproachTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = BoardSignApproachTerminateMetric
    SUBGOAL_METRIC = BoardsignSubGoalMetric

#oracle

class OracleRegionSubGoal(SubGoal):
    NAME = None
    _NAMED_REGION = None

    def _check_completed(self, frame, parser) -> bool:
        return parser.named_region_matches_target(frame, self._NAMED_REGION)


class OracleFlowersSubGoal(OracleRegionSubGoal):
    NAME = "flowers"
    _NAMED_REGION = "flowers"


class OracleBooksSubGoal(OracleRegionSubGoal):
    NAME = "books"
    _NAMED_REGION = "books"


class OracleBottomRightShoreSubGoal(OracleRegionSubGoal):
    NAME = "bottom_right_shore"
    _NAMED_REGION = "bottom_right_shore"


class OracleClocksSubGoal(OracleRegionSubGoal):
    NAME = "clocks"
    _NAMED_REGION = "clocks"


class OracleTrackemptySubGoal(OracleRegionSubGoal):
    NAME = "trackempty"
    _NAMED_REGION = "trackempty"


class OracleTrunkSubGoal(OracleRegionSubGoal):
    NAME = "trunk"
    _NAMED_REGION = "trunk"


class OracleHolesSubGoal(OracleRegionSubGoal):
    NAME = "holes"
    _NAMED_REGION = "holes"


class OracleFourCySubGoal(OracleRegionSubGoal):
    NAME = "4cy"
    _NAMED_REGION = "4cy"


class OracleFireplaceSubGoal(OracleRegionSubGoal):
    NAME = "fireplace"
    _NAMED_REGION = "fireplace"


class OracleFlowersSubGoalMetric(SubGoalMetric):
    SUBGOALS = [OracleFlowersSubGoal]


class OracleBooksSubGoalMetric(SubGoalMetric):
    SUBGOALS = [OracleBooksSubGoal]


class OracleBottomRightShoreSubGoalMetric(SubGoalMetric):
    SUBGOALS = [OracleBottomRightShoreSubGoal]


class OracleClocksSubGoalMetric(SubGoalMetric):
    SUBGOALS = [OracleClocksSubGoal]


class OracleTrackemptySubGoalMetric(SubGoalMetric):
    SUBGOALS = [OracleTrackemptySubGoal]


class OracleTrunkSubGoalMetric(SubGoalMetric):
    SUBGOALS = [OracleTrunkSubGoal]


class OracleHolesSubGoalMetric(SubGoalMetric):
    SUBGOALS = [OracleHolesSubGoal]


class OracleFourCySubGoalMetric(SubGoalMetric):
    SUBGOALS = [OracleFourCySubGoal]


class OracleFireplaceSubGoalMetric(SubGoalMetric):
    SUBGOALS = [OracleFireplaceSubGoal]


class OracleCatSubGoal(OracleRegionSubGoal):
    NAME = "cat"
    _NAMED_REGION = "cat"


class OracleCatSubGoalMetric(SubGoalMetric):
    SUBGOALS = [OracleCatSubGoal]


class ZeldaOracleOfSeasonsOtherPeopleTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleOtherPeopleTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsGirlTalkTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleGirlTalkTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsJumpingTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleJumpingTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsFarmerTalkTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleFarmerTalkTerminateMetric
    SUBGOAL_METRIC = OracleFlowersSubGoalMetric


class ZeldaOracleOfSeasonsLibraryTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleLibraryTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsParrotTalkTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleParrotTalkTerminateMetric
    SUBGOAL_METRIC = OracleBooksSubGoalMetric


class ZeldaOracleOfSeasonsFallTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleFallTerminateMetric
    SUBGOAL_METRIC = OracleBottomRightShoreSubGoalMetric


class ZeldaOracleOfSeasonsStairsTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleStairsTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsSignboardReadTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleSignboardReadTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsShopInsideTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleShopInsideTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsShopPersonTalkTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleShopPersonTalkTerminateMetric
    SUBGOAL_METRIC = OracleClocksSubGoalMetric


class ZeldaOracleOfSeasonsGirlHouseTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleGirlHouseTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsPotInteractionTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OraclePotInteractionTerminateMetric
    SUBGOAL_METRIC = OracleFireplaceSubGoalMetric


class ZeldaOracleOfSeasonsInsideTunnelTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleInsideTunnelTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsArtistTalkTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleArtistTalkTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsChickenHouseTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleChickenHouseTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsJigglyPathWalkTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleJigglyPathWalkTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsFairyMeetTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleFairyMeetTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsThingInteractionTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleThingInteractionTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsInventoryOpenTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleInventoryOpenTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsClockTowerSignReadTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleClockTowerSignReadTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsNearStairsTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleNearStairsTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsTalkToGirlTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleTalkToGirlTerminateMetric
    SUBGOAL_METRIC = OracleFireplaceSubGoalMetric


class ZeldaOracleOfSeasonsPierGoTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OraclePierGoTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsBoardwalkTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleBoardwalkTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsCatCheckTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleCatCheckTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsCatTalkTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleCatTalkTerminateMetric
    SUBGOAL_METRIC = OracleCatSubGoalMetric


class ZeldaOracleOfSeasonsOwnerTalkTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleOwnerTalkTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsBridgeWalkTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleBridgeWalkTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsDogTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleDogTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsMickeyLeftTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleMickeyLeftTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsStepOffGrassBlockTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleStepOffGrassBlockTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsShopSignPathTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleShopSignPathTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsClocksUpTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleClocksUpTerminateMetric
    SUBGOAL_METRIC = OracleClocksSubGoalMetric


class ZeldaOracleOfSeasonsJoystickRightTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleJoystickRightTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsJoystickHouseEntryTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleJoystickHouseEntryTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsApproachRedSnakeTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleApproachRedSnakeTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsApproachBlueSnakeTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleApproachBlueSnakeTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsRedSnakeTalkTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleRedSnakeTalkTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsBlueSnakeTalkTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleBlueSnakeTalkTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsBlueBookReadTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleBlueBookReadTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsRedBookReadTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleRedBookReadTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsLavaFloorTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleLavaFloorTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsStepOffTrackTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleStepOffTrackTerminateMetric
    SUBGOAL_METRIC = OracleTrackemptySubGoalMetric


class ZeldaOracleOfSeasonsGloomyPlaceLeftTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleGloomyPlaceLeftTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsGameoverDeathTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleGameoverDeathTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsLeaveGreenCarpetTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleLeaveGreenCarpetTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ZeldaOracleOfSeasonsHolesToTrunkTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleHolesToTrunkTerminateMetric
    SUBGOAL_METRIC = OracleTrunkSubGoalMetric


class ZeldaOracleOfSeasonsTrunkToHolesTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleTrunkToHolesTerminateMetric
    SUBGOAL_METRIC = OracleHolesSubGoalMetric


class ZeldaOracleOfSeasonsLeftOfTrunkTracker(TestTrackerMixin, CoreLegendOfZeldaTracker):
    TERMINATION_TRUNCATION_METRIC = OracleLeftOfTrunkTerminateMetric
    SUBGOAL_METRIC = OracleFourCySubGoalMetric
