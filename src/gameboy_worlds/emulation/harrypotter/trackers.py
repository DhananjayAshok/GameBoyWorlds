from gameboy_worlds.emulation.tracker import (
    StateTracker,
    TestTrackerMixin,
    DummySubGoalMetric,
    make_subgoal_metric_class,
)
from gameboy_worlds.emulation.harrypotter.test_metrics import (
    PotionsShopTerminateMetric,
    OllivandersInteriorTerminateMetric,
    OutsideOllivandersSubgoal,
    GetWandTerminateMetric,
    TalkToOllivanderSubgoal,
    ReceiveFolioMagiTerminateMetric,
    BoyApproachesSubgoal,
    SelectCardDeckTerminateMetric,
    CardOptionsShownSubgoal,
    GringottsInteriorTerminateMetric,
    OutsideGringottsSubgoal,
    TalkHagridGringottsTerminateMetric,
    FindHagridGringottsSubgoal,
    GainLevelTerminateMetric,
    GainSpellTerminateMetric,
    WinBattleTerminateMetric,
    FindBossRatSubgoal,
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


class EnterOllivandersTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = OllivandersInteriorTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideOllivandersSubgoal])


class GetWandTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = GetWandTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([TalkToOllivanderSubgoal])


class ReceiveFolioMagiTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = ReceiveFolioMagiTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([BoyApproachesSubgoal])


class SelectCardDeckTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = SelectCardDeckTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([CardOptionsShownSubgoal])


class EnterGringottsTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = GringottsInteriorTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideGringottsSubgoal])


class TalkHagridGringottsTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = TalkHagridGringottsTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([FindHagridGringottsSubgoal])


class GainLevelTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = GainLevelTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class GainSpellTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = GainSpellTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class WinBattleTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = WinBattleTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class BeatBossRatTestTracker(HarryPotterTestTracker):
    """Boss fight — termination TBD, subgoal is finding the boss rat."""
    TERMINATION_TRUNCATION_METRIC = WinBattleTerminateMetric  # placeholder until boss-specific termination
    SUBGOAL_METRIC = make_subgoal_metric_class([FindBossRatSubgoal])
