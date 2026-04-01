from gameboy_worlds.emulation.legend_of_zelda.base_metrics import (
    CoreLegendOfZeldaMetrics,
)

from gameboy_worlds.emulation.legend_of_zelda.test_metrics import (
    ToronboShorePickupSwordTerminateMetric,
    ShieldEquippedTerminateMetric,
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


#tarian
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