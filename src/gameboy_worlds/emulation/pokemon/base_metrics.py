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
from gameboy_worlds.emulation.pokemon.screen import is_fading
from gameboy_worlds.emulation.signal_tracking import MemorySignalsMetric


import numpy as np


class CorePokemonMetrics(MetricGroup):
    """
    Pokémon-specific metrics.

    Reports:
    - agent_state: The AgentState info. Is either Free Roam, In Dialogue, In Menu or In Battle.
    - is_fading: Whether the current screen is blank or one fade step away from the frame before it.
    - passed_fade: Whether any frame that passed during this step was blank or one fade step away from the frame before it (e.g. going through a door).
    - lost_battle: Whether the 'lost battle' dialogue appeared on any frame that passed during this step.
    - n_battles_lost: Number of battles lost so far this episode (counted on the rising edge of the dialogue).

    Final Reports:
    - mean_n_battles_lost_per_episode: Mean number of battles lost per completed episode.


    """

    NAME = "pokemon_core"
    REQUIRED_PARSER = PokemonStateParser

    def start(self):
        self.n_battles_total = []
        self.n_battles_lost_total = []
        super().start()

    def reset(self, first=False):
        if not first:
            self.n_battles_lost_total.append(self.n_battles_lost)
        self.lost_battle = False
        self.n_battles_lost = 0
        self._lost_battle_prev = False
        self.current_state: AgentState = (
            AgentState.IN_DIALOGUE
        )  # Start by default in dialogue because it has the least permissable actions.
        """ The current state of the agent in the game. """
        self._previous_state = self.current_state
        self.is_fading = False
        self.passed_fade = False
        self._last_frame = None

    def close(self):
        self.reset()
        return

    def step(self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]):
        self._previous_state = self.current_state
        current_state = self.state_parser.get_agent_state(current_frame)
        self.current_state = current_state
        if recent_frames is None or len(recent_frames) == 0:
            recent_frames = [current_frame]
        frames = list(recent_frames)
        fading = [
            is_fading(frame, previous)
            for frame, previous in zip(frames, [self._last_frame] + frames[:-1])
        ]
        self.is_fading = fading[-1]
        self.passed_fade = any(fading)
        self._last_frame = current_frame
        self.lost_battle = any(self.state_parser.has_lost_battle(f) for f in frames)
        if self.lost_battle and not self._lost_battle_prev:
            self.n_battles_lost += 1
        self._lost_battle_prev = self.lost_battle

    def report(self) -> dict:
        """
        Reports the current Pokémon core metrics:
        - Agent state
        - Whether the screen is fading, and whether a fade passed during this step
        - Whether the lost battle dialogue appeared this step, and the episode's loss count
        Returns:
            dict: A dictionary containing the current agent state, the fade flags and battle loss info.
        """
        return {
            "agent_state": self.current_state,
            "is_fading": self.is_fading,
            "passed_fade": self.passed_fade,
            "lost_battle": self.lost_battle,
            "n_battles_lost": self.n_battles_lost,
        }

    def report_final(self) -> dict:
        """
        Reports the mean number of battles lost per completed episode.
        """
        if not self.n_battles_lost_total:
            return {}
        return {
            "mean_n_battles_lost_per_episode": float(
                np.mean(self.n_battles_lost_total)
            )
        }


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


class PokemonMemorySignalsMetric(MemorySignalsMetric):
    REQUIRED_PARSER = PokemonStateParser

    def is_ready(self) -> bool:
        return self.state_parser.memory.is_map_loaded()

    def read_clock_seconds(self) -> Optional[float]:
        player = self.state_parser.memory.player()
        clock = player.get("play_time") or player.get("game_time")
        if clock is None:
            return None
        return clock["hours"] * 3600 + clock["minutes"] * 60 + clock["seconds"] + clock["frames"] / 60

    def experience_signal(self) -> Optional[str]:
        return "party_total_experience"

    def _bag(self):
        memory = self.state_parser.memory
        return memory.bag() if hasattr(memory, "bag") else memory.items()

    def read_situational(self) -> dict:
        memory = self.state_parser.memory
        player = memory.player()
        party = memory.party()
        bag = self._bag()
        signals = {
            "money": player.get("money"),
            "bag_kinds": len(bag),
            "bag_total_quantity": sum(item.get("quantity", 1) for item in bag),
            "in_battle": float(memory.is_in_battle()) if memory.has(*self._battle_labels()) else None,
        }
        if party:
            total_hp = sum(mon["hp"] for mon in party)
            total_max = sum(mon["max_hp"] for mon in party)
            signals.update(
                party_hp_total=total_hp,
                party_hp_fraction=total_hp / total_max if total_max else None,
                party_fainted=sum(mon["hp"] == 0 for mon in party),
                party_status_ailments=sum(mon["status"]["raw"] != 0 for mon in party),
            )
        if hasattr(memory, "hidden_objects"):
            hidden = memory.hidden_objects()
            if hidden:
                signals["hidden_objects"] = len(hidden)
        if memory._overlay is None:
            signals["events_raised_all"] = len(memory.events_raised())
        return signals

    def _battle_labels(self) -> tuple:
        return ("wIsInBattle",) if self.state_parser.memory.has("wIsInBattle") else ("wBattleMode",)

    def read_progress(self) -> dict:
        memory = self.state_parser.memory
        player = memory.player()
        party = memory.party()
        signals = {"party_size": len(party)}
        if party:
            levels = [mon["level"] for mon in party]
            signals.update(
                party_total_experience=sum(mon["experience"] for mon in party),
                party_level_sum=sum(levels),
                party_max_level=max(levels),
                party_distinct_moves=len({move["id"] for mon in party for move in mon["moves"]}),
            )
        if "badges" in player:
            signals["badge_count"] = player["badges"]["count"]
        pokedex = memory.pokedex()
        if pokedex:
            signals["pokedex_caught"] = pokedex["owned_count"]
            signals["pokedex_seen"] = pokedex["seen_count"]
        if memory._overlay is None:
            events = memory.events_raised()
            signals["trainers_beaten"] = sum(event.startswith("EVENT_BEAT_") for event in events)
            signals["story_flags_got"] = sum(event.startswith("EVENT_GOT_") for event in events)
        elif hasattr(memory, "event_bits") and memory.has("wEventFlags"):
            signals["event_bits_raw"] = len(memory.event_bits())
        if hasattr(memory, "engine_flags_raised") and memory._overlay is None:
            flags = memory.engine_flags_raised()
            signals["engine_flags"] = len(flags)
            signals["fly_points"] = sum("FLYPOINT" in flag for flag in flags)
        if hasattr(memory, "key_items"):
            signals["key_items"] = len(memory.key_items())
        return signals

    def read_position(self):
        location = self.state_parser.memory.location()
        if "x" not in location or "y" not in location:
            return None
        map_key = location.get("map_id", (location.get("map_group"), location.get("map_number")))
        return map_key, (location["x"], location["y"]), location.get("map_settled")

    def reset_combat(self) -> None:
        self.combat = {
            "battles_started": 0,
            "wild_battles": 0,
            "trainer_battles": 0,
            "battles_won": 0,
            "battles_lost": 0,
            "battles_fled": 0,
            "pokemon_caught_in_battle": 0,
        }
        self._battle_mode = "none"
        self._enemy_hp = None
        self._battle_party_fainted_all = False
        self._caught_at_battle_start = None

    # UNTESTED: battle outcomes have not been validated against real play. They are inferred when
    # the battle ends: all party fainted or Red's "lost" mode is a loss, a dead enemy is a win, a new
    # Pokedex catch is a catch and anything else is fled. Steps are coarser than frames, so a very
    # short battle or the final HP of the enemy can be missed.
    def update_combat(self) -> None:
        memory = self.state_parser.memory
        battle = memory.battle()
        mode = battle.get("mode", "none")
        party = memory.party()
        caught = memory.pokedex().get("owned_count")
        in_battle = mode in ("wild", "trainer")
        was_in_battle = self._battle_mode in ("wild", "trainer")
        if in_battle and not was_in_battle:
            self.combat["battles_started"] += 1
            self.combat[f"{mode}_battles"] += 1
            self._enemy_hp = None
            self._caught_at_battle_start = caught
        if in_battle:
            if "enemy_mon" in battle:
                self._enemy_hp = battle["enemy_mon"]["hp"]
            self._battle_party_fainted_all = bool(party) and all(mon["hp"] == 0 for mon in party)
        if was_in_battle and not in_battle:
            if caught is not None and self._caught_at_battle_start is not None and caught > self._caught_at_battle_start:
                self.combat["pokemon_caught_in_battle"] += 1
            elif mode == "lost" or self._battle_party_fainted_all:
                self.combat["battles_lost"] += 1
            elif self._enemy_hp == 0:
                self.combat["battles_won"] += 1
            else:
                self.combat["battles_fled"] += 1
        self._battle_mode = mode
