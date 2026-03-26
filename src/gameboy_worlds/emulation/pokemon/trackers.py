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
