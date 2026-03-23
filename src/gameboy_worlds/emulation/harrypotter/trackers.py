from gameboy_worlds.emulation.tracker import (
    StateTracker,
    TestTrackerMixin,
    DummySubGoalMetric,
)
from gameboy_worlds.emulation.harrypotter.test_metrics import (
    PotionsShopTerminateMetric,
)


class HarryPotterTestTracker(TestTrackerMixin, StateTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harry Potter games.
    """

    TERMINATION_TRUNCATION_METRIC = PotionsShopTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PotionsShopTestTracker(HarryPotterTestTracker):
    """
    A TestTracker for Harry Potter Philosopher's Stone that ends an episode when the agent enters the potions shop.
    """

    TERMINATION_TRUNCATION_METRIC = PotionsShopTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric
