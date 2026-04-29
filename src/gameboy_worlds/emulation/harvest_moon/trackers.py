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
    StorageTerminateMetric,
    OutsideStorageSubgoal,
    PickupWaterCanTerminateMetric,
    NextToWaterCanSubgoal,
    PickupSickleTerminateMetric,
    NextToSickleSubgoal,
    PickupHoeTerminateMetric,
    NextToHoeSubgoal,
    PickupHammerTerminateMetric,
    NextToHammerSubgoal,
    PickupGrassSeedTerminateMetric,
    NextToGrassSeedSubgoal,
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
    BuyCroissantTerminateMetric,
    SelectCroissantSubgoal,
    BuyCroissantOptionSubgoal,
    BuyCakeTerminateMetric,
    SelectCakeSubgoal,
    BuyCakeOptionSubgoal,
    GoToChurchPrayTerminateMetric,
    OutsideChurchSubgoal,
    InsideChurchSubgoal,
    PrayOptionSubgoal,
    OpenStorageListTerminateMetric,
    NextToStorageListSubgoal,
    FindLostBirdTerminateMetric,
    NextToLostBirdSubgoal,
    SpeakToBlueHairGirlTerminateMetric,
    NextToBlueHairGirlSubgoal,
    SpeakToGoldenHairGirlTerminateMetric,
    NextToGoldenHairGirlSubgoal,
    SpeakToPinkHairGirlTerminateMetric,
    NextToPinkHairGirlSubgoal,
    FillChickenFodderBlock1TerminateMetric,
    NextToChickenSiloSubgoal,
    PickupChickenFodderSubgoal,
    NextToChickenFodderBlock1Subgoal,
    ReadVillageSignTerminateMetric,
    NextToVillageSignSubgoal,
    ReadFarmSignTerminateMetric,
    NextToFarmSignSubgoal,
    ReadSecretGardenSignTerminateMetric,
    NextToSecretGardenSignSubgoal,
    
    # HM2
    FlowerShopEntranceTerminateMetric,
    OutsideFlowerShop2Subgoal,
    SelectPotatoSeeds2Subgoal,
    SelectPotatoSeedsOnePortion2Subgoal,
    BuyAsparagusSeedsTerminateMetric,
    SelectAsparagusSeeds2Subgoal,
    SelectAsparagusSeedsOnePortion2Subgoal,
    RestaurantEntranceTerminateMetric,
    OutsideRestaurant2Subgoal,
    BuyLunchSetTerminateMetric,
    SelectLunchSetSubgoal,
    BuyLunchSetOptionSubgoal,
    BuyBeverageSetTerminateMetric,
    SelectBeverageSetSubgoal,
    BuyBeverageSetOptionSubgoal,
    BuyTodaysSpecialTerminateMetric,
    SelectTodaysSpecialSubgoal,
    BuyTodaysSpecialOptionSubgoal,
    
    # HM2 TO DO
    OpenMenuTerminateMetric,
    ReadNoticeBoardTerminateMetric,
    NextToNoticeBoardSubgoal,
    ReadCropFieldSignTerminateMetric,
    NextToCropFieldSignSubgoal,
    NextToDiarySubgoal,
    DiaryOptionSubgoal,
    
    ## HM3
    NextToSecretGardenSign3Subgoal,
    BuyPotatoSeeds3TerminateMetric,
    NextToPotatoSeeds3Subgoal,
    NextToTurnipSeeds3Subgoal,
    SelectPotatoSeeds3Subgoal,
    SelectPotatoSeedsOnePortion3Subgoal,
    BuyTurnipSeeds3TerminateMetric,
    SelectTurnipSeeds3Subgoal,
    SelectTurnipSeedsOnePortion3Subgoal,
    SpeakToLukiaTerminateMetric,
    NextToLukiaSubgoal,
    SpeakToLucusTerminateMetric,
    NextToLucusSubgoal,
    SpeakToLylaTerminateMetric,
    NextToLylaSubgoal,
    BuyMealSetTerminateMetric,
    NextToMealSetSubgoal,
    SelectMealSetSubgoal,
    BuyCoffeeTerminateMetric,
    NextToCoffeeSubgoal,
    SelectCoffeeSubgoal,
    ShoppingMallEntranceTerminateMetric,
    NearShoppingMallSubgoal,
    FarmersUnionEntranceTerminateMetric,
    NearFarmersUnionSubgoal,
    AquariumEntranceTerminateMetric,
    NearAquariumSubgoal,
    TheatreEntranceTerminateMetric,
    NearTheatreSubgoal,
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

class HarvestMoonStorageTracker(HarvestMoonTestTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = StorageTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideStorageSubgoal])

class HarvestMoonPickupWaterCanTracker(HarvestMoonTestTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = PickupWaterCanTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToWaterCanSubgoal])

class HarvestMoonPickupSickleTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = PickupSickleTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToSickleSubgoal])

class HarvestMoonPickupHoeTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = PickupHoeTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToHoeSubgoal])

class HarvestMoonPickupHammerTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = PickupHammerTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToHammerSubgoal])

class HarvestMoonPickupGrassSeedTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = PickupGrassSeedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToGrassSeedSubgoal])

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

class HarvestMoonBuyCroissantTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = BuyCroissantTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideRestaurantSubgoal, ShopForFoodSubgoal, SelectCroissantSubgoal, BuyCroissantOptionSubgoal])

class HarvestMoonBuyCakeTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = BuyCakeTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideRestaurantSubgoal, ShopForFoodSubgoal, SelectCakeSubgoal, BuyCakeOptionSubgoal])

class HarvestMoonGoToChurchPrayTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = GoToChurchPrayTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideChurchSubgoal, InsideChurchSubgoal, PrayOptionSubgoal])

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

class HarvestMoonSpeakToGoldenHairGirlTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = SpeakToGoldenHairGirlTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToGoldenHairGirlSubgoal])

class HarvestMoonSpeakToPinkHairGirlTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = SpeakToPinkHairGirlTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToPinkHairGirlSubgoal])

class HarvestMoonFillChickenFodderTracker(HarvestMoonTestTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = FillChickenFodderBlock1TerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToChickenSiloSubgoal, PickupChickenFodderSubgoal, NextToChickenFodderBlock1Subgoal])



class HarvestMoonOpenMenuTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = OpenMenuTerminateMetric

# HM2
class HarvestMoon2FlowerShopEntranceTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = FlowerShopEntranceTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideFlowerShop2Subgoal])

class HarvestMoon2BuyPotatoSeedsTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = BuyPotatoSeedsTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectPotatoSeeds2Subgoal, SelectPotatoSeedsOnePortion2Subgoal])

class HarvestMoon2BuyAsparagusSeedsTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = BuyAsparagusSeedsTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectAsparagusSeeds2Subgoal, SelectAsparagusSeedsOnePortion2Subgoal])

class HarvestMoon2RestaurantEntranceTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = RestaurantEntranceTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideRestaurant2Subgoal])

class HarvestMoon2BuyLunchSetTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = BuyLunchSetTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectLunchSetSubgoal, BuyLunchSetOptionSubgoal])

class HarvestMoon2BuyBeverageSetTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = BuyBeverageSetTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectBeverageSetSubgoal, BuyBeverageSetOptionSubgoal])

class HarvestMoon2BuyTodaysSpecialTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = BuyTodaysSpecialTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SelectTodaysSpecialSubgoal, BuyTodaysSpecialOptionSubgoal])

class HarvestMoon2WriteDiaryAndSleepTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = GoToSleepTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToDiarySubgoal, DiaryOptionSubgoal])

class HarvestMoon2ReadSecretGardenSignTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = ReadSecretGardenSignTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToSecretGardenSignSubgoal])

class HarvestMoon2ReadCropFieldSignTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = ReadCropFieldSignTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToCropFieldSignSubgoal])
    
## TO DO
class HarvestMoonReadNoticeBoardTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = ReadNoticeBoardTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToNoticeBoardSubgoal])

class HarvestMoonReadVillageSignTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = ReadVillageSignTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToVillageSignSubgoal])

class HarvestMoonReadFarmSignTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = ReadFarmSignTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToFarmSignSubgoal])


# class HarvestMoonCleanRockTracker(HarvestMoonTestTracker):
#     """
#     Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
#     """

#     TERMINATION_TRUNCATION_METRIC = PickupWaterCanTerminateMetric
#     SUBGOAL_METRIC = make_subgoal_metric_class([NextToWaterCanSubgoal])


## HM3
class HarvestMoon3ReadSecretGardenSignTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = ReadSecretGardenSignTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToSecretGardenSign3Subgoal])

class HarvestMoon3BuyPotatoSeedsTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = BuyPotatoSeeds3TerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToPotatoSeeds3Subgoal, SelectPotatoSeeds3Subgoal, SelectPotatoSeedsOnePortion3Subgoal])

class HarvestMoon3BuyTurnipSeedsTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = BuyTurnipSeeds3TerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToTurnipSeeds3Subgoal, SelectTurnipSeeds3Subgoal, SelectTurnipSeedsOnePortion3Subgoal])

class HarvestMoon3SpeakToLukiaTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = SpeakToLukiaTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToLukiaSubgoal])

class HarvestMoon3SpeakToLucusTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = SpeakToLucusTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToLucusSubgoal])

class HarvestMoon3SpeakToLylaTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = SpeakToLylaTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToLylaSubgoal])

class HarvestMoon3BuyMealSetTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = BuyMealSetTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToMealSetSubgoal, SelectMealSetSubgoal])

class HarvestMoon3BuyCoffeeTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = BuyCoffeeTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NextToCoffeeSubgoal, SelectCoffeeSubgoal])

class HarvestMoon3ShoppingMallEntranceTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = ShoppingMallEntranceTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NearShoppingMallSubgoal])

class HarvestMoon3FarmersUnionEntranceTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = FarmersUnionEntranceTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NearFarmersUnionSubgoal])

class HarvestMoon3AquariumEntranceTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = AquariumEntranceTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NearAquariumSubgoal])

class HarvestMoon3TheatreEntranceTracker(HarvestMoonTestTracker):
    TERMINATION_TRUNCATION_METRIC = TheatreEntranceTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NearTheatreSubgoal])