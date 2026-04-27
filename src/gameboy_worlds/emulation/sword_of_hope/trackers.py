from gameboy_worlds.emulation.tracker import (
    StateTracker,
    TestTrackerMixin,
    DummySubGoalMetric,
    make_subgoal_metric_class,
)
from gameboy_worlds.emulation.sword_of_hope.test_metrics import (
    MillRoomTerminateMetric,
    ShamanRoomTerminateMetric,
    DialogueClearedTerminateMetric,
    BattleWonTerminateMetric,
    ItemFoundTerminateMetric,
    PurchaseConfirmedTerminateMetric,
    OldmanHouseSubGoal,
    InForestSubGoal,
    ShamanHouseSubGoal,
    DialogueActiveSubGoal,
    BattleActiveSubGoal,
    LookSelectedSubGoal,
    LookTargetOptionsSubGoal,
    ShopMenuOpenSubGoal,
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


class SwordOfHope1ShamanRoomTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent reaches the Shaman's Room.
    Subgoals: in_forest -> shaman_house -> (termination) shaman_room.
    """

    TERMINATION_TRUNCATION_METRIC = ShamanRoomTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OldmanHouseSubGoal, InForestSubGoal, ShamanHouseSubGoal])


class SwordOfHope1DialogueClearTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the dialogue is cleared and control returns to the player.
    Subgoals: dialogue_active -> (termination) dialogue_cleared.
    """

    TERMINATION_TRUNCATION_METRIC = DialogueClearedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([DialogueActiveSubGoal])


class SwordOfHope1BattleWonTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the battle is won.
    Subgoals: battle_active -> (termination) battle_won.
    """

    TERMINATION_TRUNCATION_METRIC = BattleWonTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([BattleActiveSubGoal])


class SwordOfHope1LookItemTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when a hidden item is found by looking at an object.
    Subgoals: look_selected -> look_target_options -> (termination) item_found.
    """

    TERMINATION_TRUNCATION_METRIC = ItemFoundTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([LookSelectedSubGoal, LookTargetOptionsSubGoal])


class SwordOfHope1BuyItemTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when an item is purchased from a shop.
    Subgoals: shop_menu_open -> (termination) purchase_confirmed.
    """

    TERMINATION_TRUNCATION_METRIC = PurchaseConfirmedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([ShopMenuOpenSubGoal])
