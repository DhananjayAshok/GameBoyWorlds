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
