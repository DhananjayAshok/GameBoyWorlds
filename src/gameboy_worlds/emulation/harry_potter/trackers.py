from gameboy_worlds.emulation.tracker import (
    StateTracker,
    TestTrackerMixin,
    DummySubGoalMetric,
    make_subgoal_metric_class,
)
from gameboy_worlds.emulation.harry_potter.base_metrics import HarryPotterOCRMetric
from gameboy_worlds.emulation.harry_potter.test_metrics import (
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
    # Task 14
    FindHagridVaultTerminateMetric,
    NavigateToHagridSubgoal,
    # Madam Malkin split tasks
    EnterMalkinsTerminateMetric,
    OpenMalkinsBuyMenuTerminateMetric,
    SelectRobesTerminateMetric,
    ConfirmRobesPurchaseTerminateMetric,
    OutsideMalkinsSubgoal,
    # Flourish & Blotts split tasks
    EnterFlourishBlottsTerminateMetric,
    OutsideFlourishBlottsSubgoal,
    BuyBooksTerminateMetric,
    TalkToFlourishClerkSubgoal,
    # Apothecary tasks
    EnterApothecaryTerminateMetric,
    BuyPotionKitTerminateMetric,
    OutsideApothecarySubgoal,
    ApothecaryBuyMenuOpenSubgoal,
    # Cauldron shop tasks
    EnterCauldronShopTerminateMetric,
    BuyCauldronTerminateMetric,
    OutsideCauldronShopSubgoal,
    CauldronBuyMenuOpenSubgoal,
    # Sugarplums Sweets filler tasks
    EnterSugarplumsTerminateMetric,
    OpenSugarplumsBuyMenuTerminateMetric,
    OutsideSugarplumsSubgoal,
    # Talk to Hagrid in Diagon Alley
    TalkToHagridDiagonTerminateMetric,
    # CoS Task 1
    FindDobbyTerminateMetric,
    FindDobbySubgoal,
    # CoS Task 2
    SelectCardDeckCosTerminateMetric,
    # CoS Task 3
    BoardFlyingCarTerminateMetric,
    TalkToRonCosSubgoal,
    # CoS Task 4
    EnterBurrowTerminateMetric,
    OutsideBurrowAfterCutsceneSubgoal,
    # CoS Task 5
    EnterBattleCosTerminateMetric,
    # Burrow room navigation tasks (CoS)
    EnterPercyRoomTerminateMetric,
    EnterGinnyRoomTerminateMetric,
    EnterParentsRoomTerminateMetric,
    EnterFredGeorgeRoomTerminateMetric,
    EnterRonsRoomTerminateMetric,
    TalkToRonBurrowTerminateMetric,
    EnterKitchenBurrowTerminateMetric,
    EnterBurrowGardenTerminateMetric,
    OutsideGardenDoorSubgoal,
)


class HarryPotterOCRTracker(StateTracker):
    """
    Base tracker that adds OCR dialogue capture support for Harry Potter games.
    Requires the parser to have a "dialogue_box_full" region defined.
    """

    def start(self):
        super().start()
        self.metric_classes.extend([HarryPotterOCRMetric])


class HarryPotterTestTracker(TestTrackerMixin, HarryPotterOCRTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harry Potter games.
    All test trackers get OCR dialogue capture support via HarryPotterOCRTracker.
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


# Task 14
class FindHagridVaultTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = FindHagridVaultTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([NavigateToHagridSubgoal])


# Madam Malkin split tasks (Task 15a/b/c/d)
class EnterMalkinsTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterMalkinsTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideMalkinsSubgoal])


class OpenMalkinsBuyMenuTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = OpenMalkinsBuyMenuTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SelectRobesTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = SelectRobesTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class ConfirmRobesPurchaseTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = ConfirmRobesPurchaseTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


# Flourish & Blotts split tasks
class EnterFlourishBlottsTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterFlourishBlottsTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideFlourishBlottsSubgoal])


class BuyBooksTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = BuyBooksTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([TalkToFlourishClerkSubgoal])


# Apothecary tasks
class EnterApothecaryTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterApothecaryTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideApothecarySubgoal])


class BuyPotionKitTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = BuyPotionKitTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([ApothecaryBuyMenuOpenSubgoal])


# Cauldron shop tasks
class EnterCauldronShopTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterCauldronShopTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideCauldronShopSubgoal])


class BuyCauldronTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = BuyCauldronTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([CauldronBuyMenuOpenSubgoal])


# Sugarplums Sweets filler tasks
class EnterSugarplumsTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterSugarplumsTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideSugarplumsSubgoal])


class OpenSugarplumsBuyMenuTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = OpenSugarplumsBuyMenuTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


# Talk to Hagrid in Diagon Alley
class TalkToHagridDiagonTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = TalkToHagridDiagonTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


# CoS Task 1
class FindDobbyTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = FindDobbyTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([FindDobbySubgoal])


# CoS Task 2
class SelectCardDeckCosTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = SelectCardDeckCosTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


# CoS Task 3
class BoardFlyingCarTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = BoardFlyingCarTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([TalkToRonCosSubgoal])


# CoS Task 4
class EnterBurrowTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterBurrowTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideBurrowAfterCutsceneSubgoal])


# CoS Task 5
class EnterBattleCosTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterBattleCosTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


# Burrow room navigation tasks (CoS)
class EnterPercyRoomTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterPercyRoomTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class EnterGinnyRoomTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterGinnyRoomTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class EnterParentsRoomTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterParentsRoomTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class EnterFredGeorgeRoomTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterFredGeorgeRoomTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class EnterRonsRoomTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterRonsRoomTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class TalkToRonBurrowTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = TalkToRonBurrowTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class EnterKitchenBurrowTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterKitchenBurrowTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class EnterBurrowGardenTestTracker(HarryPotterTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterBurrowGardenTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideGardenDoorSubgoal])
