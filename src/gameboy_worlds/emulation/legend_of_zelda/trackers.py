from gameboy_worlds.emulation.legend_of_zelda.base_metrics import (
    CoreLegendOfZeldaMetrics,
)

from gameboy_worlds.emulation.legend_of_zelda.test_metrics import (
    ToronboShorePickupSwordTerminateMetric,
    ShieldEquippedTerminateMetric,
    OutsideTarinHouseTerminateMetric,
    OpenInventoryTerminateMetric,
    TalkToKidTerminateMetric,
    ReadSignboardTerminateMetric,
    GoInsideShopTerminateMetric,
    MakeCallTerminateMetric,
    EnterDarkForestTerminateMetric,
    OpenChestTerminateMetric,
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


class ZeldaLinksAwakeningOpenChestTestTracker(
    TestTrackerMixin, CoreLegendOfZeldaTracker
):
    TERMINATION_TRUNCATION_METRIC = OpenChestTerminateMetric
    SUBGOAL_METRIC = OpenChestSubGoalMetric

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


class OracleFireplaceSubGoalMetric(SubGoalMetric):
    SUBGOALS = [OracleFireplaceSubGoal]


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
