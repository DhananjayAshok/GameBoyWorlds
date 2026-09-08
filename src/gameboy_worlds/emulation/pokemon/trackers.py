from gameboy_worlds.emulation.pokemon.base_metrics import (
    CorePokemonMetrics,
    PokemonOCRMetric,
    PokemonRedLocation,
    PokemonRedStarter,
)
from gameboy_worlds.emulation.pokemon.test_metrics import (
    PokemonCenterTerminateMetric,
    OutsideViridianCenterSubgoal,
    MtMoonTerminateMetric,
    SpeakToBillCompleteTerminateMetric,
    PickupPokeballTerminateMetric,
    ReadTrainersTipsSignTerminateMetric,
    SpeakToCinnabarGymAideCompleteTerminateMetric,
    SpeakToCinnabarMonkTerminateMetric,
    DefeatedBrockTerminateMetric,
    DefeatedLassTerminateMetric,
    CaughtPidgeyTerminateMetric,
    CaughtPikachuTerminateMetric,
    BoughtPotionAtPewterPokemartTerminateMetric,
    UsedPotionOnCharmanderTerminateMetric,
    OpenMapTerminateMetric,
    PokemonRedBoulderBadgeSubGoal,
    PokemonRedCascadeBadgeSubGoal,
    PokemonRedChampionshipTerminateMetric,
    PokemonRedEarthBadgeSubGoal,
    PokemonRedMarshBadgeSubGoal,
    PokemonRedRainbowBadgeSubGoal,
    PokemonRedSoulBadgeSubGoal,
    PokemonRedThunderBadgeSubGoal,
    PokemonRedVolcanoBadgeSubGoal,
    PokemonBrownChampionshipTerminateMetric,
    PokemonBrownEquityBadgeSubGoal,
    PokemonBrownFistBadgeSubGoal,
    PokemonBrownHailBadgeSubGoal,
    PokemonBrownMarineBadgeSubGoal,
    PokemonBrownPsiBadgeSubGoal,
    PokemonBrownSparkyBadgeSubGoal,
    PokemonBrownSproutBadgeSubGoal,
    PokemonBrownStarBadgeSubGoal,
    PokemonCrystalChampionshipTerminateMetric,
    PokemonCrystalFogBadgeSubGoal,
    PokemonCrystalGlacierBadgeSubGoal,
    PokemonCrystalHiveBadgeSubGoal,
    PokemonCrystalMineralBadgeSubGoal,
    PokemonCrystalPlainBadgeSubGoal,
    PokemonCrystalRisingBadgeSubGoal,
    PokemonCrystalStormBadgeSubGoal,
    PokemonCrystalZephyrBadgeSubGoal,
    PokemonPrismChampionshipTerminateMetric,
    PokemonPrismCharmBadgeSubGoal,
    PokemonPrismHazeBadgeSubGoal,
    PokemonPrismMidnightBadgeSubGoal,
    PokemonPrismMuscleBadgeSubGoal,
    PokemonPrismNaljoBadgeSubGoal,
    PokemonPrismNatureBadgeSubGoal,
    PokemonPrismPyreBadgeSubGoal,
    PokemonPrismRaucousBadgeSubGoal,
    UsedNotVeryEffectiveAttackOnSeakingTerminateMetric,
    TriedBuyBikeTerminateMetric,
    ClickVolcanobadgeTerminateMetric,
    OpenedCeruleanHouseMapTerminateMetric,
    SquirtleFaintedTerminateMetric,
    ClickedSwitchTerminateMetric,
    UsedSurfAshTerminateMetric,
    Sold1PsychicTerminateMetric,
    EncounteredGhostTerminateMetric,
    RateMewNameTerminateMetric,
    ReadLetterTerminateMetric,
    SpokeToEliteFourTerminateMetric,
    UsedSuperRodTerminateMetric,
    LookedIntoBinocularsTerminateMetric,
    SpokeToPikachuTerminateMetric,
    OutsideSilfCoTerminateMetric,
    OutsideRobbedHouseBackTerminateMetric,
    GaveMewtwoToDaycareTerminateMetric,
    ReadSaffronSignTerminateMetric,
    MarioGamePlayedTerminateMetric,
    TossedUltraballTerminateMetric,
    OutsideSeafoamIslandsTerminateMetric,
    FlyToPalletTownFromCinnabarTerminateMetric,
    WithdrewStaryuTerminateMetric,
    UsedToxicOnPidgeottoTerminateMetric,
    SwitchedToStaryuTerminateMetric,
    CaughtGoldeenTerminateMetric,
    TriedToTeachStaryuToxicTerminateMetric,
    PlayFluteTerminateMetric,
    OpenedSquirtlePokedexTerminateMetric,
    OpenedBlastoiseStatusTerminateMetric,
    CharizardMovesTerminateMetric,
    SpokeToLeaderTerminateMetric,
    ReachGiovanniAreaTerminateMetric,
    EnteredCherrygroveCentreTerminateMetric,
    WatchedTvTerminateMetric,
    SawMirrorTerminateMetric,
    SpokeToChildTerminateMetric,
    GotBerryTerminateMetric,
    TookDragonairItemTerminateMetric,
    GavePidgeotCleanseTagTerminateMetric,
    OpenedTyphlosionEntryTerminateMetric,
    ExitedMtMortarTerminateMetric,
    GotBiteTerminateMetric,
    ReadElmComputerTerminateMetric,
    SpokeToAideTerminateMetric,
    UsedEscapeRopeTerminateMetric,
    SpokeToVioletGymLeaderTerminateMetric,
    BoughtAntidoteTerminateMetric,
    SoldReviveTerminateMetric,
    PidgeotLearnedToxicTerminateMetric,
    GotAlanNumberTerminateMetric,
    InteractedCutTreeTerminateMetric,
    PickedUpParlzHealTerminateMetric,
    ReadBookTerminateMetric,
    SpokeToMortyTerminateMetric,
    EnteredBurnedTowerTerminateMetric,
    MiltankSadTerminateMetric,
    GotGoodRodTerminateMetric,
    EnteredLighthouseTerminateMetric,
    SpokeToRedHairGirlTerminateMetric,
    ForgotGustTerminateMetric,
    LeftIcePathTerminateMetric,
    IceMazeOtherSideTerminateMetric,
    UsedSuperEffectiveAttackTerminateMetric,
    CaughtDelibirdTerminateMetric,
    EncounteredTangelaTerminateMetric,
    SpokeToSlowpokeTerminateMetric,
    GotCharcoalTerminateMetric,
    SpokeToAzaleaGymTerminateMetric,
    GotFastballTerminateMetric,
    GaveKurtApricotTerminateMetric,
    CantDoThatTerminateMetric,
    UsedHeadbuttTerminateMetric,
    TookSuicunePicTerminateMetric,
    UsedSurfCrystalTerminateMetric,
    SeerSawAlakazamTerminateMetric,
    OpenedMailboxTerminateMetric,
    CalledMomTerminateMetric,
    CaughtPonytaTerminateMetric,
    UsedFlashTerminateMetric,
    BattleTowerExplanationTerminateMetric,
    DefeatedWillTerminateMetric,
    DefeatedKogaTerminateMetric,
)

from gameboy_worlds.emulation.pokemon.base_metrics import (
    PokemonTestMetric,
)
from gameboy_worlds.utils import log_info
from gameboy_worlds.emulation.tracker import (
    StateTracker,
    TestTrackerMixin,
    DummySubGoalMetric,
    make_subgoal_metric_class,
)
from gameboy_worlds.emulation.pokemon.parsers import (
    AgentState,
)
from typing import Optional


class CorePokemonTracker(StateTracker):
    """
    StateTracker for core Pokémon metrics.
    """

    _ADD_GRID_OVERLAY = False
    """ Whether to add the grid overlay drawn by the state parser when the agent is in FREE ROAM. This is useful for VLM based agents may need a coordinate grid overlayed onto the frame, but may cause issues for agents that do not understand that it is not a part of the game. """

    def start(self):
        super().start()
        self.metric_classes.extend([CorePokemonMetrics, PokemonTestMetric])

    def step(self, *args, **kwargs):
        """
        Calls on super().step(), but then modifies the current frame to overlay the grid if the agent is in FREE ROAM.
        """
        super().step(*args, **kwargs)
        if self._ADD_GRID_OVERLAY:
            state = self.episode_metrics["pokemon_core"]["agent_state"]
            # if agent_state is in FREE ROAM, draw the grid, otherwise do not
            if state == AgentState.FREE_ROAM:
                screen = self.episode_metrics["core"]["current_frame"]
                screen = self.state_parser.draw_grid_overlay(current_frame=screen)
                self.episode_metrics["core"]["current_frame"] = screen
                previous_screens = self.episode_metrics["core"]["passed_frames"]
                if previous_screens is not None:
                    self.episode_metrics["core"]["passed_frames"][-1, :] = screen


class PokemonOCRTracker(CorePokemonTracker):
    def start(self):
        super().start()
        self.metric_classes.extend([PokemonOCRMetric])


class PokemonRedStarterTracker(PokemonOCRTracker):
    """
    Example StateTracker that tracks the starter Pokémon chosen in Pokémon Red.
    """

    def start(self):
        super().start()
        self.metric_classes.extend([PokemonRedStarter, PokemonRedLocation])


class PokemonTestTracker(TestTrackerMixin, PokemonOCRTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Pokémon games.
    """

    TERMINATION_TRUNCATION_METRIC = PokemonCenterTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedCenterTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent reaches the entrance to the Viridian City Pokémon Center.
    """

    TERMINATION_TRUNCATION_METRIC = PokemonCenterTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideViridianCenterSubgoal])


class PokemonRedMtMoonTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent reaches the entrance to Mt. Moon.
    """

    TERMINATION_TRUNCATION_METRIC = MtMoonTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedSpeakToBillTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent speaks to Bill.
    """

    TERMINATION_TRUNCATION_METRIC = SpeakToBillCompleteTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedPickupPokeballTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent picks up the Pokéball in Professor Oak's Lab.
    """

    TERMINATION_TRUNCATION_METRIC = PickupPokeballTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedReadTrainersTipsSignTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent reads the Trainer's Tips sign.
    """

    TERMINATION_TRUNCATION_METRIC = ReadTrainersTipsSignTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedSpeakToCinnabarGymAideCompleteTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent speaks to the Cinnabar Gym aide.
    """

    TERMINATION_TRUNCATION_METRIC = SpeakToCinnabarGymAideCompleteTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedSpeakToCinnabarMonkTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent speaks to the Cinnabar Monk.
    """

    TERMINATION_TRUNCATION_METRIC = SpeakToCinnabarMonkTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedDefeatedBrockTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent defeats Brock.
    """

    TERMINATION_TRUNCATION_METRIC = DefeatedBrockTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedDefeatedLassTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent defeats the Lass trainer.
    """

    TERMINATION_TRUNCATION_METRIC = DefeatedLassTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedCaughtPidgeyTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent catches a Pidgey.
    """

    TERMINATION_TRUNCATION_METRIC = CaughtPidgeyTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedCaughtPikachuTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent catches a Pikachu.
    """

    TERMINATION_TRUNCATION_METRIC = CaughtPikachuTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedBoughtPotionAtPewterPokemartTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent buys a Potion at the Pewter City Poké Mart.
    """

    TERMINATION_TRUNCATION_METRIC = BoughtPotionAtPewterPokemartTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedUsedPotionOnCharmanderTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent uses a Potion on Charmander.
    """

    TERMINATION_TRUNCATION_METRIC = UsedPotionOnCharmanderTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedOpenMapTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent opens the map.
    """

    TERMINATION_TRUNCATION_METRIC = OpenMapTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedUsedNotVeryEffectiveAttackOnSeakingTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent uses a not very effective attack on Seaking.
    """

    TERMINATION_TRUNCATION_METRIC = UsedNotVeryEffectiveAttackOnSeakingTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedTriedBuyBikeTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent tries to buy a bike without enough money.
    """

    TERMINATION_TRUNCATION_METRIC = TriedBuyBikeTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedClickVolcanobadgeTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent discovers the secret of the Volcano Badge.
    """

    TERMINATION_TRUNCATION_METRIC = ClickVolcanobadgeTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedOpenedCeruleanHouseMapTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent opens the map on the wall in Cerulean City.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedCeruleanHouseMapTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedSquirtleFaintedTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent defeats Blue at the Cerulean City bridge.
    """

    TERMINATION_TRUNCATION_METRIC = SquirtleFaintedTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedClickedSwitchTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent clicks the secret switch in the Cinnabar Mansion.
    """

    TERMINATION_TRUNCATION_METRIC = ClickedSwitchTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedUsedSurfAshTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent uses Surf to get onto the water.
    """

    TERMINATION_TRUNCATION_METRIC = UsedSurfAshTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedSold1PsychicTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent sells exactly 1 Psychic TM at the Cinnabar Mart.
    """

    TERMINATION_TRUNCATION_METRIC = Sold1PsychicTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedEncounteredGhostTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent encounters a ghost in the Pokémon Tower.
    """

    TERMINATION_TRUNCATION_METRIC = EncounteredGhostTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedRateMewNameTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent gets Mew's nickname rated.
    """

    TERMINATION_TRUNCATION_METRIC = RateMewNameTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedReadLetterTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent reads the letter.
    """

    TERMINATION_TRUNCATION_METRIC = ReadLetterTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedSpokeToEliteFourTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent challenges the Elite Four.
    """

    TERMINATION_TRUNCATION_METRIC = SpokeToEliteFourTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedUsedSuperRodTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent uses the Super Rod properly.
    """

    TERMINATION_TRUNCATION_METRIC = UsedSuperRodTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedLookedIntoBinocularsTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent looks into the binoculars at the border stop.
    """

    TERMINATION_TRUNCATION_METRIC = LookedIntoBinocularsTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedSpokeToPikachuTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent speaks to Pikachu in the Pokémon Fan Club house.
    """

    TERMINATION_TRUNCATION_METRIC = SpokeToPikachuTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedOutsideSilfCoTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent exits Silph Co.
    """

    TERMINATION_TRUNCATION_METRIC = OutsideSilfCoTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedOutsideRobbedHouseBackTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent exits through the backdoor of the robbed house.
    """

    TERMINATION_TRUNCATION_METRIC = OutsideRobbedHouseBackTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedGaveMewtwoToDaycareTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent leaves Mewtwo in the daycare.
    """

    TERMINATION_TRUNCATION_METRIC = GaveMewtwoToDaycareTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedReadSaffronSignTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent reads the sign about Saffron City.
    """

    TERMINATION_TRUNCATION_METRIC = ReadSaffronSignTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedMarioGamePlayedTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent plays the game in the game house.
    """

    TERMINATION_TRUNCATION_METRIC = MarioGamePlayedTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedTossedUltraballTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent tosses an Ultra Ball.
    """

    TERMINATION_TRUNCATION_METRIC = TossedUltraballTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedOutsideSeafoamIslandsTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent exits Seafoam Islands.
    """

    TERMINATION_TRUNCATION_METRIC = OutsideSeafoamIslandsTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedFlyToPalletTownFromCinnabarTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent reaches Pallet Town without using Surf.
    """

    TERMINATION_TRUNCATION_METRIC = FlyToPalletTownFromCinnabarTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedWithdrewStaryuTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent withdraws Staryu from the box.
    """

    TERMINATION_TRUNCATION_METRIC = WithdrewStaryuTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedUsedToxicOnPidgeottoTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent poisons Pidgeotto.
    """

    TERMINATION_TRUNCATION_METRIC = UsedToxicOnPidgeottoTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedSwitchedToStaryuTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent switches to its weakest Pokémon.
    """

    TERMINATION_TRUNCATION_METRIC = SwitchedToStaryuTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedCaughtGoldeenTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent catches a Goldeen.
    """

    TERMINATION_TRUNCATION_METRIC = CaughtGoldeenTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedTriedToTeachStaryuToxicTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent tries to teach Staryu Toxic.
    """

    TERMINATION_TRUNCATION_METRIC = TriedToTeachStaryuToxicTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedPlayFluteTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent plays the Poké Flute.
    """

    TERMINATION_TRUNCATION_METRIC = PlayFluteTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedOpenedSquirtlePokedexTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent opens Squirtle's Pokédex page.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedSquirtlePokedexTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedOpenedBlastoiseStatusTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent opens Blastoise's status page.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedBlastoiseStatusTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedCharizardMovesTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent opens Charizard's move list.
    """

    TERMINATION_TRUNCATION_METRIC = CharizardMovesTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedSpokeToLeaderTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent speaks to the Fuchsia gym leader.
    """

    TERMINATION_TRUNCATION_METRIC = SpokeToLeaderTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedReachGiovanniAreaTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Red that ends an episode when the agent reaches the gym leader in the Viridian Gym.
    """

    TERMINATION_TRUNCATION_METRIC = ReachGiovanniAreaTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalEnteredCherrygroveCentreTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent enters the Cherrygrove Pokémon Center.
    """

    TERMINATION_TRUNCATION_METRIC = EnteredCherrygroveCentreTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalWatchedTvTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent watches TV.
    """

    TERMINATION_TRUNCATION_METRIC = WatchedTvTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalSawMirrorTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent looks into the mirror.
    """

    TERMINATION_TRUNCATION_METRIC = SawMirrorTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalSpokeToChildTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent talks to the child.
    """

    TERMINATION_TRUNCATION_METRIC = SpokeToChildTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalGotBerryTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent obtains a berry.
    """

    TERMINATION_TRUNCATION_METRIC = GotBerryTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalTookDragonairItemTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent takes Dragonair's item back.
    """

    TERMINATION_TRUNCATION_METRIC = TookDragonairItemTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalGavePidgeotCleanseTagTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent makes Pidgeot hold a Cleanse Tag.
    """

    TERMINATION_TRUNCATION_METRIC = GavePidgeotCleanseTagTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalOpenedTyphlosionEntryTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent opens Typhlosion's Pokédex entry.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedTyphlosionEntryTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalExitedMtMortarTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent exits Mt. Mortar.
    """

    TERMINATION_TRUNCATION_METRIC = ExitedMtMortarTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalGotBiteTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent gets a bite while fishing.
    """

    TERMINATION_TRUNCATION_METRIC = GotBiteTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalReadElmComputerTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent reads Elm's computer.
    """

    TERMINATION_TRUNCATION_METRIC = ReadElmComputerTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalSpokeToAideTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent talks to Professor Elm's aide.
    """

    TERMINATION_TRUNCATION_METRIC = SpokeToAideTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalUsedEscapeRopeTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent immediately escapes the Sprout Tower.
    """

    TERMINATION_TRUNCATION_METRIC = UsedEscapeRopeTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalSpokeToVioletGymLeaderTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent talks to the Violet Gym leader.
    """

    TERMINATION_TRUNCATION_METRIC = SpokeToVioletGymLeaderTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalBoughtAntidoteTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent buys one Antidote.
    """

    TERMINATION_TRUNCATION_METRIC = BoughtAntidoteTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalSoldReviveTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent sells one Revive.
    """

    TERMINATION_TRUNCATION_METRIC = SoldReviveTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalPidgeotLearnedToxicTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent teaches Pidgeot Toxic.
    """

    TERMINATION_TRUNCATION_METRIC = PidgeotLearnedToxicTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalGotAlanNumberTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent gets the boy's phone number.
    """

    TERMINATION_TRUNCATION_METRIC = GotAlanNumberTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalInteractedCutTreeTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent interacts with a tree that can be cut.
    """

    TERMINATION_TRUNCATION_METRIC = InteractedCutTreeTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalPickedUpParlzHealTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent picks up the item in the park.
    """

    TERMINATION_TRUNCATION_METRIC = PickedUpParlzHealTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalReadBookTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent reads the book.
    """

    TERMINATION_TRUNCATION_METRIC = ReadBookTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalSpokeToMortyTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent speaks to Morty.
    """

    TERMINATION_TRUNCATION_METRIC = SpokeToMortyTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalEnteredBurnedTowerTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent enters the Burned Tower.
    """

    TERMINATION_TRUNCATION_METRIC = EnteredBurnedTowerTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalMiltankSadTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent refuses to give the Miltank a berry.
    """

    TERMINATION_TRUNCATION_METRIC = MiltankSadTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalGotGoodRodTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent gets a fishing rod.
    """

    TERMINATION_TRUNCATION_METRIC = GotGoodRodTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalEnteredLighthouseTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent enters the lighthouse.
    """

    TERMINATION_TRUNCATION_METRIC = EnteredLighthouseTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalSpokeToRedHairGirlTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent talks to the red haired girl.
    """

    TERMINATION_TRUNCATION_METRIC = SpokeToRedHairGirlTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalForgotGustTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent makes Pidgeot forget Gust.
    """

    TERMINATION_TRUNCATION_METRIC = ForgotGustTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalLeftIcePathTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent exits via the ice path below.
    """

    TERMINATION_TRUNCATION_METRIC = LeftIcePathTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalIceMazeOtherSideTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent reaches the other side of the ice maze.
    """

    TERMINATION_TRUNCATION_METRIC = IceMazeOtherSideTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalUsedSuperEffectiveAttackTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent defeats Golbat with a super effective attack.
    """

    TERMINATION_TRUNCATION_METRIC = UsedSuperEffectiveAttackTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalCaughtDelibirdTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent catches a Delibird.
    """

    TERMINATION_TRUNCATION_METRIC = CaughtDelibirdTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalEncounteredTangelaTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent encounters a Tangela.
    """

    TERMINATION_TRUNCATION_METRIC = EncounteredTangelaTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalSpokeToSlowpokeTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent talks to a Slowpoke.
    """

    TERMINATION_TRUNCATION_METRIC = SpokeToSlowpokeTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalGotCharcoalTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent gets some charcoal from the kiln.
    """

    TERMINATION_TRUNCATION_METRIC = GotCharcoalTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalSpokeToAzaleaGymTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent speaks to the Azalea gym leader.
    """

    TERMINATION_TRUNCATION_METRIC = SpokeToAzaleaGymTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalGotFastballTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent gets a Fast Ball from Kurt.
    """

    TERMINATION_TRUNCATION_METRIC = GotFastballTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalGaveKurtApricotTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent commissions Kurt to make a Poké Ball.
    """

    TERMINATION_TRUNCATION_METRIC = GaveKurtApricotTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalCantDoThatTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent tries to fly out of Ilex Forest.
    """

    TERMINATION_TRUNCATION_METRIC = CantDoThatTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalUsedHeadbuttTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent headbutts a tree.
    """

    TERMINATION_TRUNCATION_METRIC = UsedHeadbuttTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalTookSuicunePicTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent takes a picture of Suicune.
    """

    TERMINATION_TRUNCATION_METRIC = TookSuicunePicTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalUsedSurfTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent surfs onto the water.
    """

    TERMINATION_TRUNCATION_METRIC = UsedSurfCrystalTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalSeerSawAlakazamTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent asks the Poké Seer about Alakazam.
    """

    TERMINATION_TRUNCATION_METRIC = SeerSawAlakazamTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalOpenedMailboxTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent opens the mailbox through the PC.
    """

    TERMINATION_TRUNCATION_METRIC = OpenedMailboxTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalCalledMomTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent calls their mom.
    """

    TERMINATION_TRUNCATION_METRIC = CalledMomTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalCaughtPonytaTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent catches a Ponyta.
    """

    TERMINATION_TRUNCATION_METRIC = CaughtPonytaTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalUsedFlashTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent lights up Silver Cave.
    """

    TERMINATION_TRUNCATION_METRIC = UsedFlashTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalBattleTowerExplanationTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent gets an explanation for the Battle Tower.
    """

    TERMINATION_TRUNCATION_METRIC = BattleTowerExplanationTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalDefeatedWillTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent defeats Will.
    """

    TERMINATION_TRUNCATION_METRIC = DefeatedWillTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonCrystalDefeatedKogaTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokémon Crystal that ends an episode when the agent defeats Koga.
    """

    TERMINATION_TRUNCATION_METRIC = DefeatedKogaTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class PokemonRedChampionshipTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokemon Red that tracks all eight badges and ends an
    episode when the player defeats the Champion Rival.
    """

    TERMINATION_TRUNCATION_METRIC = PokemonRedChampionshipTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class(
        [
            PokemonRedBoulderBadgeSubGoal,
            PokemonRedCascadeBadgeSubGoal,
            PokemonRedThunderBadgeSubGoal,
            PokemonRedRainbowBadgeSubGoal,
            PokemonRedSoulBadgeSubGoal,
            PokemonRedMarshBadgeSubGoal,
            PokemonRedVolcanoBadgeSubGoal,
            PokemonRedEarthBadgeSubGoal,
        ]
    )


class PokemonBrownChampionshipTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokemon Brown that tracks all eight badges and ends an episode
    when the player becomes the Rijon League Champion.
    """

    TERMINATION_TRUNCATION_METRIC = PokemonBrownChampionshipTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class(
        [
            PokemonBrownMarineBadgeSubGoal,
            PokemonBrownHailBadgeSubGoal,
            PokemonBrownSproutBadgeSubGoal,
            PokemonBrownSparkyBadgeSubGoal,
            PokemonBrownFistBadgeSubGoal,
            PokemonBrownEquityBadgeSubGoal,
            PokemonBrownStarBadgeSubGoal,
            PokemonBrownPsiBadgeSubGoal,
        ]
    )


class PokemonCrystalChampionshipTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokemon Crystal that tracks all eight Johto badges and
    ends an episode when the player enters the Hall of Fame.
    """

    TERMINATION_TRUNCATION_METRIC = PokemonCrystalChampionshipTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class(
        [
            PokemonCrystalZephyrBadgeSubGoal,
            PokemonCrystalHiveBadgeSubGoal,
            PokemonCrystalPlainBadgeSubGoal,
            PokemonCrystalFogBadgeSubGoal,
            PokemonCrystalStormBadgeSubGoal,
            PokemonCrystalMineralBadgeSubGoal,
            PokemonCrystalGlacierBadgeSubGoal,
            PokemonCrystalRisingBadgeSubGoal,
        ]
    )


class PokemonPrismChampionshipTestTracker(PokemonTestTracker):
    """
    A TestTracker for Pokemon Prism that tracks all eight badges and ends an episode
    when the player becomes the Rijon League Champion.
    """

    TERMINATION_TRUNCATION_METRIC = PokemonPrismChampionshipTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class(
        [
            PokemonPrismPyreBadgeSubGoal,
            PokemonPrismNatureBadgeSubGoal,
            PokemonPrismCharmBadgeSubGoal,
            PokemonPrismMidnightBadgeSubGoal,
            PokemonPrismMuscleBadgeSubGoal,
            PokemonPrismHazeBadgeSubGoal,
            PokemonPrismRaucousBadgeSubGoal,
            PokemonPrismNaljoBadgeSubGoal,
        ]
    )
