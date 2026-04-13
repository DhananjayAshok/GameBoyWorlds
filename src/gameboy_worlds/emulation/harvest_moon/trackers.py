from gameboy_worlds.emulation.harvest_moon.base_metrics import (
    CoreHarvestMoonMetrics,
    HarvestMoonOCRMetric,
    HarvestMoonTestMetric,
)
from gameboy_worlds.emulation.harvest_moon.test_metrics import (
    CowBarnTerminateMetric,
    OutsideCowBarnSubgoal,
    ChickenCoopTerminateMetric,
    OutsideChickenCoopSubgoal,
    PickupWaterCanTerminateMetric,
    NextToWaterCanSubgoal,
    GoToSleepTerminateMetric,
    SleepOptionSubgoal,
    FeedSpiritTerminateMetric,
    NextToSpiritSubgoal,
    WaterTurnipTerminateMetric,
    NextToTurnipSubgoal,
    BuyPotatoSeedsTerminateMetric,
    OutsideFlowerShopSubgoal,
    ShopForSeedsSubgoal,
    SelectPotatoSeedsSubgoal,
    SelectPotatoSeedsOnePortionSubgoal,
    BuyTurnipSeedsTerminateMetric,
    SelectTurnipSeedsSubgoal,
    SelectTurnipSeedsOnePortionSubgoal,
    BuyRiceBallTerminateMetric,
    OutsideRestaurantSubgoal,
    ShopForFoodSubgoal,
    SelectRiceBallSubgoal,
    BuyRiceBallOptionSubgoal,
    OpenStorageListTerminateMetric,
    NextToStorageListSubgoal,
    FindLostBirdTerminateMetric,
    NextToLostBirdSubgoal,
    SpeakToBlueHairGirlTerminateMetric,
    NextToBlueHairGirlSubgoal,
    FillChickenFodderBlock1TerminateMetric,
    NextToChickenSiloSubgoal,
    PickupChickenFodderSubgoal,
    NextToChickenFodderBlock1Subgoal,
)
from gameboy_worlds.utils import log_info
from gameboy_worlds.emulation.tracker import (
    StateTracker,
    TestTrackerMixin,
    DummySubGoalMetric,
    make_subgoal_metric_class,
)
from gameboy_worlds.emulation.harvest_moon.parsers import (
    AgentState,
)
from typing import Optional


class CoreHarvestMoonTracker(StateTracker):
    """
    StateTracker for core Harvest Moon metrics.
    """

    _REMOVE_GRID_OVERLAY = False
    """ Whether to remove the grid overlay drawn by the state parser when the agent is in FREE ROAM. This is useful for VLM based agents may need a coordinate grid overlayed onto the frame, but may cause issues for agents that do not understand that it is not a part of the game. """

    def start(self):
        super().start()
        self.metric_classes.extend([CoreHarvestMoonMetrics, HarvestMoonTestMetric])

    def step(self, *args, **kwargs):
        """
        Calls on super().step(), but then modifies the current frame to overlay the grid if the agent is in FREE ROAM.
        """
        super().step(*args, **kwargs)
        if self._REMOVE_GRID_OVERLAY:
            state = self.episode_metrics["harvest_moon_core"]["agent_state"]
            # if agent_state is in FREE ROAM, draw the grid, otherwise do not
            if state == AgentState.FREE_ROAM:
                screen = self.episode_metrics["core"]["current_frame"]
                screen = self.state_parser.draw_grid_overlay(current_frame=screen)
                self.episode_metrics["core"]["current_frame"] = screen
                previous_screens = self.episode_metrics["core"]["passed_frames"]
                if previous_screens is not None:
                    self.episode_metrics["core"]["passed_frames"][-1, :] = screen


class HarvestMoonOCRTracker(CoreHarvestMoonTracker):
    def start(self):
        super().start()
        self.metric_classes.extend([HarvestMoonOCRMetric])
        
class HarvestMoonTestTracker(TestTrackerMixin, HarvestMoonOCRTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = CowBarnTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric

class HarvestMoonCowBarnTracker(HarvestMoonTestTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = CowBarnTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideCowBarnSubgoal])
    
class HarvestMoonChickenCoopTracker(HarvestMoonTestTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = ChickenCoopTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideChickenCoopSubgoal])

class HarvestMoonPickupWaterCanTracker(HarvestMoonTestTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = PickupWaterCanTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToWaterCanSubgoal])

class HarvestMoonGoToSleepTracker(HarvestMoonTestTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = GoToSleepTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SleepOptionSubgoal])
    
class HarvestMoonFeedSpiritTracker(HarvestMoonTestTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = FeedSpiritTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToSpiritSubgoal])

class HarvestMoonWaterTurnipTracker(HarvestMoonTestTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = WaterTurnipTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToTurnipSubgoal])

class HarvestMoonBuyPotatoSeedsTracker(HarvestMoonTestTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = BuyPotatoSeedsTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideFlowerShopSubgoal, ShopForSeedsSubgoal, SelectPotatoSeedsSubgoal, SelectPotatoSeedsOnePortionSubgoal])

class HarvestMoonBuyTurnipSeedsTracker(HarvestMoonTestTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = BuyTurnipSeedsTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideFlowerShopSubgoal,ShopForSeedsSubgoal, SelectTurnipSeedsSubgoal, SelectTurnipSeedsOnePortionSubgoal])

class HarvestMoonBuyRiceBallTracker(HarvestMoonTestTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = BuyRiceBallTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideRestaurantSubgoal, ShopForFoodSubgoal, SelectRiceBallSubgoal, BuyRiceBallOptionSubgoal])

class HarvestMoonOpenStorageListTracker(HarvestMoonTestTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = OpenStorageListTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToStorageListSubgoal])

class HarvestMoonFindLostBirdTracker(HarvestMoonTestTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = FindLostBirdTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToLostBirdSubgoal])

class HarvestMoonSpeakToBlueHairGirlTracker(HarvestMoonTestTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = SpeakToBlueHairGirlTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToBlueHairGirlSubgoal])

class HarvestMoonFillChickenFodderTracker(HarvestMoonTestTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = FillChickenFodderBlock1TerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToChickenSiloSubgoal, PickupChickenFodderSubgoal, NextToChickenFodderBlock1Subgoal])

# class HarvestMoonCleanRockTracker(HarvestMoonTestTracker):
#     """
#     Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
#     """

#     TERMINATION_TRUNCATION_METRIC = PickupWaterCanTerminateMetric
#     SUBGOAL_METRIC = make_subgoal_metric_class([NextToWaterCanSubgoal])