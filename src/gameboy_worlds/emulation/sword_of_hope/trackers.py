from gameboy_worlds.emulation.tracker import (
    StateTracker,
    TestTrackerMixin,
    DummySubGoalMetric,
)
from gameboy_worlds.emulation.sword_of_hope.test_metrics import (
    MillRoomTerminateMetric,
)


class SwordOfHope1TestTracker(TestTrackerMixin, StateTracker):
    """
    Base TestTracker for Sword of Hope 1.
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create task-specific trackers.
    """

    TERMINATION_TRUNCATION_METRIC = MillRoomTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope1MillRoomTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent reaches the Mill Room (first adjacent room from start).
    """

    TERMINATION_TRUNCATION_METRIC = MillRoomTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric
