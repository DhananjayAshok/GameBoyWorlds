from typing import Optional
from abc import ABC
from gameboy_worlds.emulation.pokemon.parsers import (
    AgentState,
    MemoryBasedPokemonRedStateParser,
    PokemonRedStateParser,
    PokemonStateParser,
)
from gameboy_worlds.emulation.tracker import (
    MetricGroup,
    OCRegionMetric,
    TerminationTruncationMetric,
)


import numpy as np


class CorePokemonMetrics(MetricGroup):
    """
    Pokémon-specific metrics.

    Reports:
    - agent_state: The AgentState info. Is either Free Roam, In Dialogue, In Menu or In Battle.

    Final Reports:
    - None


    """

    NAME = "pokemon_core"
    REQUIRED_PARSER = PokemonStateParser

    def start(self):
        self.n_battles_total = []
        super().start()

    def reset(self, first=False):
        if not first:
            pass
        self.current_state: AgentState = (
            AgentState.IN_DIALOGUE
        )  # Start by default in dialogue because it has the least permissable actions.
        """ The current state of the agent in the game. """
        self._previous_state = self.current_state

    def close(self):
        self.reset()
        return

    def step(self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]):
        self._previous_state = self.current_state
        current_state = self.state_parser.get_agent_state(current_frame)
        self.current_state = current_state

    def report(self) -> dict:
        """
        Reports the current Pokémon core metrics:
        - Agent state
        Returns:
            dict: A dictionary containing the current agent state.
        """
        return {
            "agent_state": self.current_state
        }

    def report_final(self) -> dict:
        """
        Reports nothing:
        """
        return {}


class PokemonRedTeamInfoMetric(MetricGroup):
    """Keeps the latest live Pokémon Red party-list image crops.

    The parser runs on every emulator step.  Outside the party screen those
    crops are simply ignored; ``GetTeamInfoAction`` only returns them after its
    START-menu flow has established that the party screen opened.

    The arrays live in this metric's ``team_info`` dictionary and are attached
    to the HLA result only after a successful open.  ``report()`` intentionally
    exposes only the capture step, otherwise every ordinary movement state log
    would print all of the raw image arrays.

    Reports:
    - ``captured_at_step``: tracker step at which the live arrays were taken.
    """

    NAME = "pokemon_team_info"
    REQUIRED_PARSER = PokemonStateParser

    def reset(self, first=False):
        self.steps = 0
        self.team_info = None
        self.captured_at_step = None

    def step(self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]):
        self.steps += 1
        # PokemonOCRTracker is shared by the other Pokémon games.  Keep the
        # metric harmless there while making it available for Pokémon Red.
        if isinstance(self.state_parser, PokemonRedStateParser):
            self.team_info = self.state_parser.get_team_info(current_frame)
            self.captured_at_step = self.steps
        else:
            self.team_info = None
            self.captured_at_step = None

    def report(self) -> dict:
        return {
            "captured_at_step": self.captured_at_step,
        }

    def report_final(self) -> dict:
        return {}

    def close(self):
        pass


class PokemonOCRMetric(OCRegionMetric):
    REQUIRED_PARSER = PokemonStateParser

    def reset(self, first=False):
        super().reset(first)
        self.prev_was_in_fight_options = False

    def start(self):
        self.kinds = {
            "dialogue": "dialogue_box_full",
            "battle_attack_options": "screen_bottom_half",
        }
        super().start()

    def can_read_kind(self, current_frame: np.ndarray, kind: str) -> bool:
        self.state_parser: PokemonStateParser
        if kind == "dialogue":
            in_dialogue = self.state_parser.dialogue_box_open(
                current_screen=current_frame
            )
            dialogue_empty = self.state_parser.dialogue_box_empty(
                current_screen=current_frame
            )
            in_battle_menu = self.state_parser.is_in_base_battle_menu(
                current_screen=current_frame
            )
            in_fight_options = self.state_parser.is_in_fight_options_menu(
                current_screen=current_frame
            )
            in_bag = self.state_parser.is_in_fight_bag(current_screen=current_frame)
            return (
                in_dialogue
                and not dialogue_empty
                and not in_battle_menu
                and not in_fight_options
                and not in_bag
            )
        if kind == "battle_attack_options":
            in_fight_options = self.state_parser.is_in_fight_options_menu(
                current_screen=current_frame
            )
            if in_fight_options:
                if self.prev_was_in_fight_options:
                    self.prev_was_in_fight_options = True
                    return False
                else:
                    self.prev_was_in_fight_options = True
                    return True
            else:
                self.prev_was_in_fight_options = False
                return False
        return False


class PokemonExitBattleTruncationMetric(TerminationTruncationMetric, ABC):
    """
    Truncates the episode if the agent exits a battle (enters into free roam)
    Implement this class to test scenarios where the task can be completed entirely within a battle.
    """

    def determine_truncated(self, current_frame, recent_frames):
        self.state_parser: PokemonStateParser
        current_state = self.state_parser.get_agent_state(current_frame)
        if current_state == AgentState.FREE_ROAM:
            return True
        return False


class PokemonRedStarter(MetricGroup):
    """
    Specific tracking for choice of starter Pokémon in Pokémon Red.

    Reports:
    - current_starter: The starter Pokémon chosen in the current episode.

    Final Reports:
    - starter_choices: A dictionary with the total number of times each starter Pokémon was chosen across all episodes.
    """

    NAME = "pokemon_red_starter"
    REQUIRED_PARSER = PokemonRedStateParser

    def start(self):
        self.starters_chosen = []
        super().start()

    def reset(self, first=False):
        if not first:
            self.starters_chosen.append(self.current_starter)
        self.current_starter = None
        """ The starter Pokémon chosen in the current episode. """

    def step(self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]):
        if self.current_starter is not None:
            return
        if recent_frames is not None:
            all_frames = recent_frames
        else:
            all_frames = np.array([current_frame])
        for frame in all_frames:
            chose_charmander = self.state_parser.named_region_matches_multi_target(
                frame, "dialogue_box_middle", "picked_charmander"
            )
            if chose_charmander:
                self.current_starter = "charmander"
                return
            chose_bulbasaur = self.state_parser.named_region_matches_multi_target(
                frame, "dialogue_box_middle", "picked_bulbasaur"
            )
            if chose_bulbasaur:
                self.current_starter = "bulbasaur"
                return
            chose_squirtle = self.state_parser.named_region_matches_multi_target(
                frame, "dialogue_box_middle", "picked_squirtle"
            )
            if chose_squirtle:
                self.current_starter = "squirtle"
                return
        return

    def report(self) -> dict:
        """
        Reports the current starter Pokémon chosen in the episode.

        Returns:
            dict: A dictionary containing the current starter Pokémon.
        """
        return {"current_starter": self.current_starter}

    def close(self):
        self.reset()
        starter_choices = {"charmander": 0, "bulbasaur": 0, "squirtle": 0, None: 0}
        for choice in self.starters_chosen:
            starter_choices[choice] += 1
        starter_choices["None"] = starter_choices.pop(None)
        self.starter_choices = starter_choices

    def report_final(self):
        """
        Reports the total number of times each starter Pokémon was chosen across all episodes.
        """
        return self.starter_choices


class PokemonRedLocation(MetricGroup):
    """
    Reads from memory states to determine the player's current location in Pokemon Red.

    Reports:
    - direction: The direction the player is facing
    - has_moved: Whether the player has moved since the last step
    - current_global_location: (x, y)
    - current_local_location: (x, y, map_name)
    - n_walk_steps: Number of walk steps taken in the current episode
    - unique_locations: List of unique locations visited in the current episode
    - n_of_unique_locations: Number of unique locations visited in the current episode

    Final Reports:
    - mean_n_walk_steps_per_episode: Mean number of walk steps taken per episode
    - mean_n_unique_locations_per_episode: Mean number of unique locations visited per episode
    - std_n_walk_steps_per_episode: Standard deviation of walk steps taken per episode
    - std_n_unique_locations_per_episode: Standard deviation of unique locations visited per episode
    - max_n_walk_steps_per_episode: Maximum number of walk steps taken in a single episode
    - max_n_unique_locations_per_episode: Maximum number of unique locations visited in a single episode


    """

    NAME = "pokemon_red_location"
    REQUIRED_PARSER = MemoryBasedPokemonRedStateParser

    def start(self):
        self.total_n_walk_steps = []
        self.total_n_of_unique_locations = []
        super().start()

    def reset(self, first=False):
        if not first:
            self.total_n_of_unique_locations.append(len(self.unique_locations))
            self.total_n_walk_steps.append(self.n_walk_steps)
        else:
            self.direction = None
            self.current_local_location = None
            self.current_global_location = None
            self.has_moved = False
            self.n_walk_steps = 0
            self.unique_locations = set()

    def step(self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]):
        self.state_parser: MemoryBasedPokemonRedStateParser
        self.direction = self.state_parser.get_facing_direction()
        current_local_position = self.state_parser.get_local_coords()
        current_global_position = self.state_parser.get_global_coords()
        x, y, map_number = current_local_position
        map_name = self.state_parser.get_map_name(map_number)
        if self.current_local_location is None:
            self.current_local_location = (x, y, map_name)
            self.current_global_location = current_global_position
            self.unique_locations.add(map_name)
        else:
            if (
                self.current_local_location[0] != x
                or self.current_local_location[1] != y
                or self.current_local_location[2] != map_name
            ):
                self.has_moved = True
                if map_name == self.current_local_location[2]:
                    initial_coord = np.array(self.current_local_location[0:2])
                    new_coord = np.array(current_local_position[0:2])
                    manhattan_distance = np.sum(np.abs(initial_coord - new_coord))
                    self.n_walk_steps += manhattan_distance
                else:
                    # use global coords to estimate distance moved
                    initial_coord = np.array(self.current_global_location)
                    new_coord = np.array(current_global_position)
                    manhattan_distance = np.sum(np.abs(initial_coord - new_coord))
                    self.n_walk_steps += manhattan_distance
                    self.unique_locations.add(map_name)
            else:
                self.has_moved = False
            self.current_global_location = current_global_position
            self.current_local_location = (x, y, map_number)

    def report(self) -> dict:
        """
        Reports the current location metrics:
        - direction: The direction the player is facing
        - has_moved: Whether the player has moved since the last step
        - current_global_location: (x, y)
        - current_local_location: (x, y, map_name)
        - n_walk_steps: Number of walk steps taken in the current episode
        - unique_locations: List of unique locations visited in the current episode
        - n_of_unique_locations: Number of unique locations visited in the current episode

        Returns:
            dict: A dictionary containing the current location metrics.
        """
        return {
            "direction": self.direction,
            "has_moved": self.has_moved,
            "current_global_location": self.current_global_location,
            "current_local_location": self.current_local_location,
            "n_walk_steps": self.n_walk_steps,
            "unique_locations": list(self.unique_locations),
            "n_of_unique_locations": len(self.unique_locations),
        }

    def report_final(self):
        return {
            "mean_n_walk_steps_per_episode": float(np.mean(self.total_n_walk_steps)),
            "mean_n_unique_locations_per_episode": float(
                np.mean(self.total_n_of_unique_locations)
            ),
            "std_n_walk_steps_per_episode": float(np.std(self.total_n_walk_steps)),
            "std_n_unique_locations_per_episode": float(
                np.std(self.total_n_of_unique_locations)
            ),
            "max_n_walk_steps_per_episode": int(np.max(self.total_n_walk_steps)),
            "max_n_unique_locations_per_episode": int(
                np.max(self.total_n_of_unique_locations)
            ),
        }

    def close(self):
        pass


class PokemonTestMetric(MetricGroup):
    NAME = "pokemon_test"
    REQUIRED_PARSER = PokemonStateParser

    def start(self):
        super().start()

    def reset(self, first=False):
        if not first:
            pass
        self.prev_was_fight = False
        self.is_in_fight = False
        self.is_got_away_safely = False

    def close(self):
        self.reset()
        return

    def step(self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]):
        self.state_parser: PokemonStateParser
        is_fight = False
        self.is_got_away_safely = self.state_parser.named_region_matches_multi_target(
            current_frame, "dialogue_box_middle", "got_away_safely"
        )
        # is_fight = self.state_parser.is_in_fight_options_menu(current_screen=current_frame)
        self.prev_was_fight = self.is_in_fight
        self.is_in_fight = is_fight

    def report(self) -> dict:
        return {
            "is_in_fight": self.is_in_fight,
            "is_got_away_safely": self.is_got_away_safely,
            "was_in_fight_last_step": self.prev_was_fight,
        }

    def report_final(self) -> dict:
        return {}
