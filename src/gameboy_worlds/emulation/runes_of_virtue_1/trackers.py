from gameboy_worlds.emulation.runes_of_virtue_1.base_metrics import CoreRunesOfVirtue1Metrics
from gameboy_worlds.emulation.runes_of_virtue_1.test_metrics import OpenMenuTerminateMetric
from gameboy_worlds.emulation.tracker import StateTracker, TestTrackerMixin, DummySubGoalMetric


class CoreRunesOfVirtue1Tracker(StateTracker):
    """
    StateTracker for Ultima: Runes of Virtue.

    Tracks agent_state (in_menu vs free_roam) via CoreRunesOfVirtue1Metrics.
    """

    def start(self):
        super().start()
        self.metric_classes.extend([CoreRunesOfVirtue1Metrics])


class RunesOfVirtue1TestTracker(TestTrackerMixin, CoreRunesOfVirtue1Tracker):
    """
    Base test tracker for Runes of Virtue 1.
    Inherit and set TERMINATION_TRUNCATION_METRIC for specific tasks.
    """

    TERMINATION_TRUNCATION_METRIC = OpenMenuTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class RunesOfVirtue1OpenMenuTestTracker(RunesOfVirtue1TestTracker):
    """
    Test tracker that ends an episode when the player opens the inventory menu.
    """

    TERMINATION_TRUNCATION_METRIC = OpenMenuTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric
