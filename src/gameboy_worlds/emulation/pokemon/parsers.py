"""
Pokemon specific game state parser implementations for both PokemonRed and PokemonCrystal.
While this code base started from: https://github.com/PWhiddy/PokemonRedExperiments/ (v2) and was initially read from memory states https://github.com/thatguy11325/pokemonred_puffer/blob/main/pokemonred_puffer/global_map.py, this is no longer the case as we have moved to visual based state parsing.
This decision was primarily made to facilitate easier extension to other games and rom hacks in the future, as well as to avoid reliance on specific memory addresses which may vary between different versions of the game.

However, the code base supports reading from memory addresses to extract game state information, which can be useful for incorporating domain knowledge into reward structures or other aspects of the environment. See the MemoryBasedPokemonRedStateParser class for examples of how to read game state information from memory addresses.

WARNING: The screen capture mechanisms of the parsers rely on a SPECIFIC FRAME being used in the game. This is not a concern with Gen I games, but Gen II games have options for frames. All states and captures in this repo assume a particular choice of frame, and often it is NOT the default Frame 1.
Ensure that your agents DO NOT change the frame settings in the game, or the state parsing will fail.

CORE DESIGN PRINCIPLE: Never branch the parser subclasses for a given variant. The inheritance tree for a parser after the game variant parser should always be a tree with only one child per layer.
This is to ensure that we don't double effort, any capability added to a parser will always be valid for that game variant.
If this principle is followed, any state tracker can always use the STRONGEST (lowest level) parser for a given variant without concern for missing functionality.
"""

from gameboy_worlds.emulation.parser import NamedScreenRegion
from gameboy_worlds.utils import (
    log_warn,
    log_info,
    log_error,
    load_parameters,
    verify_parameters,
)
from gameboy_worlds.emulation.parser import StateParser, _get_proper_regions

from typing import Set, List, Type, Dict, Optional, Tuple
import os
from abc import ABC, abstractmethod
from enum import Enum

from pyboy import PyBoy

import json
import numpy as np
from bidict import bidict


class AgentState(Enum):
    """
    0. FREE_ROAM: The agent is freely roaming the game world.
    1. IN_DIALOGUE: The agent is currently in a dialogue state. (including reading signs, talking to NPCs, etc.)
    2. IN_MENU: The agent is currently in a menu state. (including PC, Name Entry, Pokedex, etc.)
    3. IN_BATTLE: The agent is currently in a battle state.
    """

    FREE_ROAM = 0
    IN_DIALOGUE = 1
    IN_MENU = 2
    IN_BATTLE = 3


class PokemonStateParser(StateParser, ABC):
    """
    Base class for Pokemon game state parsers. Uses visual screen regions to parse game state.
    Defines common named screen regions and methods for determining game states such as being in battle, menu, or dialogue.

    Can be used to determine the exact AgentState
    """

    COMMON_REGIONS = [
        ("dialogue_bottom_right", 153, 135, 10, 10),
        ("menu_top_right", 152, 1, 6, 6),
        ("pc_top_left", 0, 0, 6, 6),
        ("battle_enemy_hp_text", 15, 17, 10, 5),
        ("battle_player_hp_text", 80, 73, 10, 5),
        ("battle_base_menu_top_left", 65, 96, 5, 5),
        ("battle_fight_options_top_right", 80, 64, 5, 5),
        ("battle_fight_options_cursor_on_top", 40, 103, 3, 3),
        ("dialogue_choice_bottom_right", 153, 87, 6, 6),
        ("name_entity_top_left", 0, 32, 6, 6),
        ("player_card_middle", 56, 70, 6, 6),
        ("map_bottom_right", 140, 130, 10, 10),
    ]
    """ List of common named screen regions for Pokemon games. 
    - dialogue_bottom_right: Bottom right of dialogue box when interacting with NPCs, signs, etc. Speak to an NPC to capture this.
    
    - menu_top_right: Top right of the screen when the player start menu is open. Open the start menu to capture this.
    
    - pc_top_left: Top left of the screen when the PC is open. Open the PC to capture this.
    
    - battle_enemy_hp_text: Region showing the text 'HP' for the enemy Pokémon in battle. Engage in a battle to capture this.
    
    - battle_player_hp_text: Region showing the text 'HP' for the player's Pokémon in battle. Engage in a battle to capture this.
    
    - battle_base_menu_top_left: Top left of the battle base menu. Engage in a battle to capture this.

    - battle_fight_options_top_right: Top right of the fight options menu in battle. Engage in a battle and open the fight options to capture this.

    - battle_fight_options_cursor_on_top: Region showing the cursor on the top attack option in the fight options menu. Engage in a battle, open the fight options and move the cursor to the top option to capture this.
    
    - dialogue_choice_bottom_right: Bottom right of the choice dialogue box when answering choice questions (e.g. Yes/No prompts). Trigger a choice dialogue to capture this (e.g. confirmation of starter choice)
    
    - name_entity_top_left: Top left of the screen when naming a character or Pokémon. Catch a pokemon and give it a nickname to capture this.
    
    - player_card_middle: Middle of the player card screen. Go to this from start menu -> player name
    
    - map_bottom_right: Bottom right of the map screen when the town map is open.  Open the town map to capture this.
    """

    COMMON_MULTI_TARGET_REGIONS = [
        ("screen", 0, 0, 150, 140),
        ("dialogue_box_middle", 10, 105, 120, 30),
        ("dialogue_box_full", 5, 100, 150, 40),
        ("screen_bottom_half", 5, 70, 150, 70),
        ("screen_quadrant_1", 85, 0, 60, 60),
        ("screen_quadrant_2", 0, 0, 60, 60),
        ("screen_quadrant_3", 0, 70, 60, 70),
        ("screen_quadrant_4", 85, 70, 60, 70),
        ("screen_middle", 65, 55, 20, 20),
    ]
    """ List of common multi-target named screen regions for Pokemon games.
    
    - screen: Most of the screen except for the very edges. Useful for general state parsing.
    - dialogue_box_middle: Middle of the dialogue box, but not on that spot where the blinking arrow cursor appears. Useful for catching particular dialogues.
    - dialogue_box_full: Full dialogue box area, is useful to capture for OCR purposes.
    - screen_bottom_half: Bottom half of the screen, useful for OCR of dialogue and other text.
    - screen_quadrant_1: Top right quadrant of the screen.
    - screen_quadrant_2: Top left quadrant of the screen.
    - screen_quadrant_3: Bottom left quadrant of the screen.
    - screen_quadrant_4: Bottom right quadrant of the screen.
    - screen_middle: Middle of the screen.
    """

    COMMON_MULTI_TARGETS = {
        "dialogue_box_middle": [
            "got_away_safely",
            "cannot_escape",
            "cannot_run_from_trainer",
            "no_pp_for_move",
        ],
        "menu_box_strip": ["cursor_on_options", "cursor_on_pokedex"],
    }
    """ Common multi-targets for the common multi-target named screen regions. 
    - dialogue_box_middle:
        - got_away_safely: Run successfully from a wild battle.
        - cannot_escape: Fail to run from a wild Pokemon
        - cannot_run_from_trainer: Try to run from a trainer battle and get an error message
        - no_pp_for_move: Try to use a move with no PP remaining.
    - menu_box_strip:
        - cursor_on_options: Cursor is on the options in the start menu. This is vital to prevent agents from changing the text frame option. 
        - cursor_on_pokedex: Cursor is on the Pokedex in the start menu.

    """

    def __init__(
        self,
        variant: str,
        pyboy: PyBoy,
        parameters: dict,
        additional_named_screen_region_details: List[
            Tuple[str, int, int, int, int]
        ] = [],
        additional_multi_target_named_screen_region_details: List[
            Tuple[str, int, int, int, int]
        ] = [],
        override_multi_targets: Dict[str, List[str]] = {},
    ):
        """
        Initializes the PokemonStateParser.
        Args:
            variant (str): The variant of the Pokemon game.
            pyboy (PyBoy): The PyBoy emulator instance.
            parameters (dict): Configuration parameters for the emulator.
            additional_named_screen_region_details (List[Tuple[str, int, int, int, int]]): Parameters associated with additional named screen regions to include.
            additional_multi_target_named_screen_region_details (List[Tuple[str, int, int, int, int]]): Parameters associated with additional multi-target named screen regions to include.
            override_multi_targets (Dict[str, List[str]]): Dictionary mapping region names to lists of target names for multi-target regions.
        """
        verify_parameters(parameters)
        regions = _get_proper_regions(
            override_regions=additional_named_screen_region_details,
            base_regions=self.COMMON_REGIONS,
        )
        self.variant = variant
        if f"{variant}_rom_data_path" not in parameters:
            log_error(
                f"ROM data path not found for variant: {variant}. Add {variant}_rom_data_path to the config files. See configs/pokemon_red_vars.yaml for an example",
                parameters,
            )
        self.rom_data_path = parameters[f"{variant}_rom_data_path"]
        """ Path to the ROM data directory for the specific Pokemon variant."""
        captures_dir = self.rom_data_path + "/captures/"
        named_screen_regions = []
        for region_name, x, y, w, h in regions:
            region = NamedScreenRegion(
                region_name,
                x,
                y,
                w,
                h,
                parameters=parameters,
                target_path=os.path.join(captures_dir, region_name),
            )
            named_screen_regions.append(region)
        multi_target_regions = _get_proper_regions(
            override_regions=additional_multi_target_named_screen_region_details,
            base_regions=self.COMMON_MULTI_TARGET_REGIONS,
        )
        multi_target_region_names = [region[0] for region in multi_target_regions]
        multi_targets = self.COMMON_MULTI_TARGETS.copy()
        for key in override_multi_targets:
            if key in multi_targets:
                multi_targets[key].extend(override_multi_targets[key])
            else:
                multi_targets[key] = override_multi_targets[key]
        multi_target_provided_region_names = list(multi_targets.keys())
        if not set(multi_target_provided_region_names).issubset(
            set(multi_target_region_names)
        ):
            log_error(
                f"Multi-target regions provided in multi_targets do not match the defined multi-target regions. Provided: {multi_target_provided_region_names}, Defined: {multi_target_region_names}",
                parameters,
            )
        for region_name, x, y, w, h in multi_target_regions:
            region_target_paths = {}
            subdir = captures_dir + f"/{region_name}/"
            for target_name in multi_targets.get(region_name, []):
                region_target_paths[target_name] = os.path.join(subdir, target_name)
            region = NamedScreenRegion(
                region_name,
                x,
                y,
                w,
                h,
                parameters=parameters,
                multi_target_paths=region_target_paths,
            )
            named_screen_regions.append(region)
        super().__init__(pyboy, parameters, named_screen_regions)

    @abstractmethod
    def is_in_pokedex(self, current_screen: np.ndarray) -> bool:
        """
        Determines if the Pokedex is currently open.
        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.

        Returns:
            bool: True if the Pokedex is open, False otherwise.
        """
        raise NotImplementedError

    @staticmethod
    def is_in_pokemon_menu(self, current_screen: np.ndarray) -> bool:
        """
        Determines if the Pokemon menu is currently open.
        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.
        Returns:
            bool: True if the Pokemon menu is open, False otherwise.
        """
        raise NotImplementedError

    def is_hovering_over_options_in_menu(self, current_screen: np.ndarray) -> bool:
        """
        Determines if the cursor is currently hovering over options in the menu. Typically we force the agent off this state.

        # TODO: This method currently only has one multi_target screen checked, cursor_on_options, which is screen captured AFTER the player gets the pokedex
        The problem is the menu layout is slightly different before the pokedex is acquired, making the check useless before that point.
        To fix this, we need to capture another target for the same multi_target region (e.g. cursor_on_options_no_pokedex) and check for both here.
        But I am lazy, and so will hope this is not needed.

        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.

        Returns:
            bool: True if hovering over options, False otherwise.
        """
        return self.named_region_matches_multi_target(
            current_screen, "menu_box_strip", "cursor_on_options"
        )

    def is_in_battle(self, current_screen: np.ndarray) -> bool:
        """
        Determines if the player is currently in a battle by checking for battle HP text regions.

        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.

        Returns:
            bool: True if in battle, False otherwise.
        """
        if self.is_in_fight_bag(current_screen):
            return False  # Then, is in menu
        enemy_hp_match = self.named_region_matches_target(
            current_screen, "battle_enemy_hp_text"
        )
        player_hp_match = self.named_region_matches_target(
            current_screen, "battle_player_hp_text"
        )
        return enemy_hp_match or player_hp_match

    def is_in_base_battle_menu(self, current_screen: np.ndarray) -> bool:
        """
        Determines if the player is currently in the base battle menu by checking for the battle base menu top left region.

        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.
        Returns:
            bool: True if in the base battle menu, False otherwise.
        """
        return self.named_region_matches_target(
            current_screen, "battle_base_menu_top_left"
        )

    def is_in_run_screen(self, current_screen: np.ndarray) -> bool:
        """
        Determines if the player is currently in the run screen by checking for the battle base menu top left region.
        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.
        Returns:
            bool: True if in the run screen, False otherwise.
        """
        got_away_safely = self.named_region_matches_multi_target(
            current_screen, "dialogue_box_middle", "got_away_safely"
        )
        cannot_escape = self.named_region_matches_multi_target(
            current_screen, "dialogue_box_middle", "cannot_escape"
        )
        cannot_run_from_trainer = self.named_region_matches_multi_target(
            current_screen, "dialogue_box_middle", "cannot_run_from_trainer"
        )
        return got_away_safely or cannot_escape or cannot_run_from_trainer

    def is_in_fight_options_menu(self, current_screen: np.ndarray) -> bool:
        """
        Determines if the player is currently in the fight options menu by checking for the battle fight options top right region.

        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.
        Returns:
            bool: True if in the fight options menu, False otherwise.
        """
        return self.named_region_matches_target(
            current_screen, "battle_fight_options_top_right"
        )

    def is_on_top_attack_option(self, current_screen: np.ndarray) -> bool:
        """
        Determines if the cursor is currently on the top attack option in the fight options menu.

        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.
        Returns:
            bool: True if the cursor is on the top attack option, False otherwise.
        """
        return self.named_region_matches_target(
            current_screen, "battle_fight_options_cursor_on_top"
        )

    def tried_no_pp_move(self, current_screen: np.ndarray) -> bool:
        """
        Determines if the player tried to use a move with no PP by checking for the no_pp_for_move target in the dialogue box middle region.

        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.
        Returns:
            bool: True if the player tried to use a move with no PP, False otherwise.
        """
        return self.named_region_matches_multi_target(
            current_screen, "dialogue_box_middle", "no_pp_for_move"
        )

    @abstractmethod
    def is_in_fight_bag(self, current_screen: np.ndarray) -> bool:
        raise NotImplementedError

    def is_on_top_menu_option(self, current_screen: np.ndarray) -> bool:
        """
        Determines if the cursor is currently on the top option in the start menu.

        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.
        Returns:
            bool: True if the cursor is on the top menu option, False otherwise.
        """
        return self.named_region_matches_multi_target(
            current_screen, "menu_box_strip", "cursor_on_pokedex"
        )

    def is_in_menu(
        self, current_screen: np.ndarray, trust_previous: bool = False
    ) -> bool:
        """
        Determines if any form of menu (or choice dialogue) is currently open by checking a variety of screen regions.

        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.
            trust_previous (bool): If True, trusts that checks for other states like is_in_battle have been done and can be skipped.

        Returns:
            bool: True if the menu is open, False otherwise.
        """
        any_match_regions = [
            "menu_top_right",
            "dialogue_choice_bottom_right",
            "pc_top_left",
            "name_entity_top_left",
            "player_card_middle",
            "map_bottom_right",
            "pokemon_list_hp_text",  # This one is defined in each subclass as the position varies slightly between games
        ]
        if not trust_previous:
            if self.is_in_battle(current_screen):
                return False
        if self.is_in_fight_bag(current_screen):
            return True
        if self.is_in_pokedex(current_screen):
            return True
        if self.is_in_pokemon_menu(current_screen):
            return True
        for region_name in any_match_regions:
            if self.named_region_matches_target(current_screen, region_name):
                return True
        return False

    def dialogue_box_open(self, current_screen: np.ndarray) -> bool:
        """
        Determines if a dialogue box is currently open by checking the dialogue bottom right region.
        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.
        Returns:
            bool: True if a dialogue box is open, False otherwise.
        """
        return self.named_region_matches_target(current_screen, "dialogue_bottom_right")

    def dialogue_box_empty(self, current_screen: np.ndarray) -> bool:
        box = self.capture_named_region(
            current_frame=current_screen, name="dialogue_box_full"
        )
        perc_lt_255 = np.mean(box < 255)
        if perc_lt_255 < 0.082:  # Empirical threshold
            return True
        return False

    def is_in_dialogue(
        self, current_screen: np.ndarray, trust_previous: bool = False
    ) -> bool:
        """
        Determines if the player is currently in a dialogue state or reading text from a sign, interacting with an object etc.
        Essentially anything that causes text to appear at the bottom of the screen that isn't a battle, pc or menu.

        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.
            trust_previous (bool): If True, trusts that checks for other states like is_in_battle have been done and can be skipped.

        Returns:
            bool: True if in dialogue, False otherwise.
        """
        if trust_previous:
            return self.named_region_matches_target(
                current_screen, "dialogue_bottom_right"
            )
        if self.is_in_battle(current_screen):
            return False
        elif self.is_in_menu(current_screen):
            return False
        else:
            return self.dialogue_box_open(current_screen)

    def get_agent_state(self, current_screen: np.ndarray) -> AgentState:
        """
        Determines the current agent state based on the screen.

        Uses trust_previous to optimize checks.

        Args:
            current_screen (np.ndarray): The current screen frame from the emulator.

        Returns:
            AgentState: The current agent state.
        """
        if self.is_in_battle(current_screen):
            return AgentState.IN_BATTLE
        elif self.is_in_menu(current_screen, trust_previous=True):
            return AgentState.IN_MENU
        elif self.is_in_dialogue(current_screen, trust_previous=True):
            return AgentState.IN_DIALOGUE
        else:
            return AgentState.FREE_ROAM


class BasePokemonRedStateParser(PokemonStateParser, ABC):
    """
    Game state parser for all PokemonRed-based games.
    """

    REGIONS = [
        ("pokedex_top_left", 7, 6, 12, 6),
        ("pokedex_info_mid_left", 6, 71, 6, 6),
        ("pokemon_list_hp_text", 32, 9, 10, 5),
        ("pokemon_stats_line", 66, 55, 5, 5),
        ("battle_bag_options_bottom_left", 32, 96, 5, 5),
    ]
    """ Additional named screen regions specific to Pokemon Red games.
    - pokedex_top_left: Top left of the screen when the Pokedex is open. Open the Pokedex to capture this.
    - pokedex_info_mid_left: Middle left of the screen when viewing a Pokémon's info in the Pokedex. Open a Pokémon's info in the Pokedex to capture this.
    - pokemon_list_hp_text: Region showing the text 'HP' for the player's Pokémon in the Pokémon list. Open the Pokémon list from the start menu to capture this.
    - pokemon_stats_line: A line in the Pokémon stats screen. Open a Pokémon's stats from the start menu -> pokemon menu to capture this.
    - battle_bag_options_bottom_left: The bottom left part of the menu when you open the items option from the battle menu. 
    """

    MULTI_TARGET_REGIONS = [
        ("menu_box_strip", 89, 13, 5, 100),
    ]
    """ Additional multi-target named screen regions specific to Pokemon Red games. 
    - menu_box_strip: Strip of the menu box when the start menu is open. Open the start menu to capture this. The margins are adjusted to avoiding capturing the player name, as this may change across sav files and states. 
    """

    def __init__(
        self,
        pyboy: PyBoy,
        variant: str,
        parameters: dict,
        override_regions: List[Tuple[str, int, int, int, int]] = [],
        override_multi_target_regions: List[Tuple[str, int, int, int, int]] = [],
        override_multi_targets: Dict[str, List[str]] = {},
    ):
        self.REGIONS = _get_proper_regions(
            override_regions=override_regions, base_regions=self.REGIONS
        )
        self.MULTI_TARGET_REGIONS = _get_proper_regions(
            override_regions=override_multi_target_regions,
            base_regions=self.MULTI_TARGET_REGIONS,
        )
        super().__init__(
            variant=variant,
            pyboy=pyboy,
            parameters=parameters,
            additional_named_screen_region_details=self.REGIONS,
            additional_multi_target_named_screen_region_details=self.MULTI_TARGET_REGIONS,
            override_multi_targets=override_multi_targets,
        )

    def is_in_pokedex(self, current_screen: np.ndarray) -> bool:
        return self.named_region_matches_target(
            current_screen, "pokedex_top_left"
        ) or self.named_region_matches_target(current_screen, "pokedex_info_mid_left")

    def is_in_pokemon_menu(self, current_screen: np.ndarray) -> bool:
        return self.named_region_matches_target(
            current_screen, "pokemon_list_hp_text"
        ) or self.named_region_matches_target(current_screen, "pokemon_stats_line")

    def is_in_fight_bag(self, current_screen: np.ndarray) -> bool:
        return self.named_region_matches_target(
            current_screen, "battle_bag_options_bottom_left"
        )

    def __repr__(self):
        return f"<PokemonRedParser(variant={self.variant})>"


class BasePokemonCrystalStateParser(PokemonStateParser, ABC):
    """
    Game state parser for all PokemonCrystal-based games.

    TODO: The map screenshot for crystal assumes a Jhoto map. Must do a similar process for Kanto. To add Kanto we should add another named screen region called map_bottom_right_kanto with same boundary as player_card_middle and then recapture it.
    Without this fix, the is_in_menu check may fail when in Kanto as the map_bottom_right region will not match.
    """

    REGIONS = [
        ("pokemon_list_hp_text", 87, 16, 10, 5),
        ("pokedex_seen_text", 3, 88, 5, 5),
        ("pokedex_info_height_text", 69, 57, 5, 5),
        ("pokegear_top_left", 0, 0, 6, 6),
        ("pokemon_stats_lvl_text", 113, 0, 5, 5),
        ("bag_text", 18, 0, 6, 6),
    ]
    """ Additional named screen regions specific to Pokemon Crystal games.
    - pokemon_list_hp_text: Region showing the text 'HP' for the player's Pokémon in the Pokémon list. Open the Pokémon list from the start menu to capture this.
    - pokedex_seen_text: Region showing the 'SEEN' text in the Pokedex. Open the Pokedex to capture this.
    - pokedex_info_height_text: Region showing the 'HEIGHT' text in the Pokedex info screen. Open a Pokémon's info in the Pokedex to capture this.
    - pokegear_top_left: Top left of the screen when the Pokegear is open. Open the Pokegear to capture this.
    - pokemon_stats_lvl_text: Region showing the 'LV' text in the Pokémon stats screen. Open a Pokémon's stats from the start menu -> pokemon menu to capture this.
    - bag_text: Top left of the screen when the Bag is open. Open the Bag to capture this.
    """

    MULTI_TARGET_REGIONS = [
        ("menu_box_strip", 89, 13, 5, 120),
    ]
    """ Additional multi-target named screen regions specific to Pokemon Crystal games. 
    - menu_box_strip: Strip of the menu box when the start menu is open. Open the start menu to capture this. The margins are adjusted to avoiding capturing the player name, as this may change across sav files and states. 
    """

    def __init__(
        self,
        pyboy: PyBoy,
        variant: str,
        parameters: dict,
        override_regions: List[Tuple[str, int, int, int, int]] = [],
        override_multi_target_regions: List[Tuple[str, int, int, int, int]] = [],
        override_multi_targets: Dict[str, List[str]] = {},
    ):
        self.REGIONS = _get_proper_regions(
            override_regions=override_regions, base_regions=self.REGIONS
        )
        self.MULTI_TARGET_REGIONS = _get_proper_regions(
            override_regions=override_multi_target_regions,
            base_regions=self.MULTI_TARGET_REGIONS,
        )
        super().__init__(
            variant=variant,
            pyboy=pyboy,
            parameters=parameters,
            additional_named_screen_region_details=self.REGIONS,
            additional_multi_target_named_screen_region_details=self.MULTI_TARGET_REGIONS,
            override_multi_targets=override_multi_targets,
        )

    def is_in_bag(self, current_screen: np.ndarray) -> bool:
        """
        Determines if the Bag is currently open.
        """
        return self.named_region_matches_target(current_screen, "bag_text")

    def is_in_fight_bag(self, current_screen: np.ndarray) -> bool:
        """
        For PokemonCrystal, this is just the same as in bag.
        """
        return self.is_in_bag(current_screen)

    def is_in_pokegear(self, current_screen: np.ndarray) -> bool:
        """
        Determines if the Pokegear is currently open.
        """
        return self.named_region_matches_target(current_screen, "pokegear_top_left")

    def is_in_pokedex(self, current_screen):
        return self.named_region_matches_target(
            current_screen, "pokedex_seen_text"
        ) or self.named_region_matches_target(
            current_screen, "pokedex_info_height_text"
        )

    def is_in_pokemon_menu(self, current_screen: np.ndarray) -> bool:
        return self.named_region_matches_target(
            current_screen, "pokemon_stats_lvl_text"
        ) or self.named_region_matches_target(current_screen, "pokemon_list_hp_text")

    def is_in_menu(
        self, current_screen: np.ndarray, trust_previous: bool = False
    ) -> bool:
        # This technically mistakenly also flags when someone calls you on the pokegear, but that's probably fine for now.
        # Could change by adding special region for pokegear_call_top_left and overriding is_in_menu and is_in_dialogue.
        result = super().is_in_menu(current_screen, trust_previous=trust_previous)
        if result:
            return True
        if self.is_in_bag(current_screen):
            return True
        if self.is_in_pokegear(current_screen):
            return True
        # Finally, when transitioning to PC screens, maps etc, the screen goes white. Catch that here.
        # print(f"Checking for white screen... Pixel stats: {np.min(current_screen)}, {np.max(current_screen)}, {np.mean(current_screen)}") # I get 248, 248, 248.0
        # The following doesn't catch all white screens (e.g town maps), but does catch some important ones like PC screens.
        if np.mean(current_screen) > 245 and np.min(current_screen) > 245:
            return True
        elif np.mean(current_screen) > 210:  # screen coming down from full white
            return True
        else:
            return False

    def __repr__(self):
        return f"<PokemonCrystalParser(variant={self.variant})>"


class PokemonRedStateParser(BasePokemonRedStateParser):
    def __init__(self, pyboy, parameters):
        override_multi_targets = {
            "dialogue_box_middle": [
                "picked_charmander",
                "picked_bulbasaur",
                "picked_squirtle",
                "talk_bill_complete",
                "pick_up_pokeball_starting",  # is tied to player character name being You
                "trainers_tips_sign",
                "cinnabar_gym_aid_complete",
                "talk_cinnabar_monk",
                "defeated_brock",
                "defeated_lass",
                "caught_pidgey",
                "caught_pikachu",
                "used_potion_on_charmander",
            ],
            "screen_bottom_half": [
                "viridian_pokemon_center_entrance",
                "mt_moon_entrance",
                "bought_potion_at_pewter_pokemart",
            ],
            "screen_middle": [
                "outside_viridian_center_from_left",
                "outside_viridian_center_from_right",
            ],
        }
        super().__init__(
            pyboy,
            variant="pokemon_red",
            parameters=parameters,
            override_multi_targets=override_multi_targets,
        )


class PokemonBrownStateParser(BasePokemonRedStateParser):
    def __init__(self, pyboy, parameters):
        super().__init__(pyboy, variant="pokemon_brown", parameters=parameters)


class PokemonStarBeastsStateParser(BasePokemonRedStateParser):
    def __init__(self, pyboy, parameters):
        override_regions = [
            ("pokemon_list_hp_text", 33, 10, 4, 4),
            ("battle_enemy_hp_text", 6, 15, 5, 5),
            ("battle_player_hp_text", 88, 72, 5, 5),
        ]
        super().__init__(
            pyboy,
            variant="pokemon_starbeasts",
            parameters=parameters,
            override_regions=override_regions,
        )


class PokemonCrystalStateParser(BasePokemonCrystalStateParser):
    def __init__(self, pyboy, parameters):
        super().__init__(pyboy, variant="pokemon_crystal", parameters=parameters)


class PokemonPrismStateParser(BasePokemonCrystalStateParser):
    def __init__(self, pyboy, parameters):
        override_regions = [("player_card_middle", 25, 58, 5, 5)]
        super().__init__(
            pyboy,
            variant="pokemon_prism",
            parameters=parameters,
            override_regions=override_regions,
        )


class PokemonFoolsGoldStateParser(BasePokemonCrystalStateParser):
    def __init__(self, pyboy, parameters):
        override_regions = [("pokedex_info_height_text", 66, 65, 5, 5)]
        super().__init__(
            pyboy,
            variant="pokemon_fools_gold",
            parameters=parameters,
            override_regions=override_regions,
        )


"""
The below code shows how to add domain information into the game state parser and read from memory addresses to get descriptive state information. 

This is not actually used in any of the current environments, but is left here to show that if you want to bake in more domain knowledge and create explicit reward schedules etc., you can read the information required to do so in this class. 
"""


class MemoryBasedPokemonRedStateParser(PokemonRedStateParser):
    """
    Game state parser for Pokemon Red. Uses memory addresses to parse game state.
    Can be used to reproduce https://github.com/PWhiddy/PokemonRedExperiments/ (v2) and facilitates reward engineering based on memory states.
    """

    _PAD = 20
    _GLOBAL_MAP_SHAPE = (444 + _PAD * 2, 436 + _PAD * 2)
    _MAP_ROW_OFFSET = _PAD
    _MAP_COL_OFFSET = _PAD

    def __init__(self, pyboy, parameters):
        """
        Initializes the Pokemon Red game state parser.

        Args:
            pyboy: An instance of the PyBoy emulator.
            parameters: A dictionary of parameters for configuration.
        """
        super().__init__(pyboy, parameters=parameters)
        events_location = parameters["pokemon_red_rom_data_path"] + "/events.json"
        with open(events_location) as f:
            event_slots = json.load(f)
        event_slots = event_slots
        event_names = {v: k for k, v in event_slots.items() if not v[0].isdigit()}
        beat_opponent_events = bidict()

        def _pop(d, keys):
            for key in keys:
                if key in d:
                    d.pop(key, None)

        pop_queue = []
        for name, slot in event_names.items():
            if name.startswith("Beat "):
                beat_opponent_events[name.replace("Beat ", "")] = slot
                pop_queue.append(name)
        _pop(event_names, pop_queue)
        self.defeated_opponent_events = beat_opponent_events
        """Events related to beating specific opponents. E.g. Beat Brock"""
        tms_obtained_events = bidict()
        pop_queue = []
        for name, slot in event_names.items():
            if name.startswith("Got Tm"):
                tms_obtained_events[name.replace("Got ", "").strip()] = slot
                pop_queue.append(name)
        _pop(event_names, pop_queue)
        self.tms_obtained_events = tms_obtained_events
        """Events related to obtaining specific TMs. E.g. Got Tm01"""
        hm_obtained_events = bidict()
        pop_queue = []
        for name, slot in event_names.items():
            if name.startswith("Got Hm"):
                hm_obtained_events[name.replace("Got ", "").strip()] = slot
                pop_queue.append(name)
        _pop(event_names, pop_queue)
        self.hm_obtained_events = hm_obtained_events
        """Events related to obtaining specific HMs. E.g. Got Hm01"""
        passed_badge_check_events = bidict()
        pop_queue = []
        for name, slot in event_names.items():
            if name.startswith("Passed ") and "badge" in name:
                passed_badge_check_events[
                    name.replace("Passed ", "").replace(" Check", "").strip()
                ] = slot
                pop_queue.append(name)
        _pop(event_names, pop_queue)
        self.passed_badge_check_events = passed_badge_check_events
        """Events related to passing badge checks. E.g. Passed Boulder badge check. These will only be relevant to enter Victory Road."""
        self.key_items_obtained_events = bidict()
        """Events related to obtaining key items. E.g. Got Bicycle"""
        pop_queue = []
        for name, slot in event_names.items():
            if name.startswith("Got "):
                self.key_items_obtained_events[name.replace("Got ", "").strip()] = slot
                pop_queue.append(name)
        _pop(event_names, pop_queue)
        self.map_events = {
            "Cinnabar Gym": bidict(),
            "Victory Road": bidict(),
            "Silph Co": bidict(),
            "Seafoam Islands": bidict(),
        }
        """Events related to specific map events like unlocking gates or moving boulders."""
        for name, slot in event_names.items():
            if name.startswith("Cinnabar Gym Gate") and name.endswith("Unlocked"):
                self.map_events["Cinnabar Gym"][name] = slot
                pop_queue.append(name)
            elif name.startswith("Victory Road") and "Boulder On" in name:
                self.map_events["Victory Road"][name] = slot
                pop_queue.append(name)
            elif name.startswith("Silph Co") and "Unlocked" in name:
                self.map_events["Silph Co"][name] = slot
                pop_queue.append(name)
            elif name.startswith("Seafoam"):
                self.map_events["Seafoam Islands"][name] = slot
                pop_queue.append(name)
        _pop(event_names, pop_queue)
        self.cutscene_events = bidict()
        """ Flags for cutscene based events (I think, lol). """

        cutscenes = [
            "Event 001",
            "Daisy Walking",
            "Pokemon Tower Rival On Left",
            "Seel Fan Boast",
            "Pikachu Fan Boast",
            "Lab Handing Over Fossil Mon",
            "Route22 Rival Wants Battle",
        ]  # my best guess, need to verify, Silph Co Receptionist At Desk? Autowalks?
        pop_queue = []
        for name, slot in event_names.items():
            if name in cutscenes:
                self.cutscene_events[name] = slot
                pop_queue.append(name)
        _pop(event_names, pop_queue)
        self.special_events = bidict(event_names)
        """ All other events not categorized elsewhere."""

        MAP_PATH = parameters["pokemon_red_rom_data_path"] + "/map_data.json"
        with open(MAP_PATH) as map_data:
            MAP_DATA = json.load(map_data)["regions"]
        self._MAP_DATA = {int(e["id"]): e for e in MAP_DATA}

    def get_map_name(self, map_n: int) -> Optional[str]:
        """
        Gets the name of the map given its identifier.
        Args:
            map_n (int): Map identifier.
        Returns:
            Optional[str]: Name of the map if found, None otherwise.
        """
        try:
            return self._MAP_DATA[map_n]["name"]
        except KeyError:
            return None

    def local_to_global(self, r: int, c: int, map_n: int) -> Tuple[int, int]:
        """
        Converts local map coordinates to global map coordinates.
        Args:
            r (int): Local row coordinate.
            c (int): Local column coordinate.
            map_n (int): Map identifier.
        Returns:
            (int, int): Global (row, column) coordinates.
        """
        try:
            (
                map_x,
                map_y,
            ) = self._MAP_DATA[
                map_n
            ]["coordinates"]
            gy = r + map_y + self._MAP_ROW_OFFSET
            gx = c + map_x + self._MAP_COL_OFFSET
            if (
                0 <= gy < self._GLOBAL_MAP_SHAPE[0]
                and 0 <= gx < self._GLOBAL_MAP_SHAPE[1]
            ):
                return gy, gx
            print(
                f"coord out of bounds! global: ({gx}, {gy}) game: ({r}, {c}, {map_n})"
            )
            return self._GLOBAL_MAP_SHAPE[0] // 2, self._GLOBAL_MAP_SHAPE[1] // 2
        except KeyError:
            print(f"Map id {map_n} not found in map_data.json.")
            return self._GLOBAL_MAP_SHAPE[0] // 2, self._GLOBAL_MAP_SHAPE[1] // 2

    def get_opponents_defeated(self) -> Set[str]:
        """
        Returns a set of all defeated opponents. This function isn't actually used in any current environments, but is left here to show how to read game state information.
        Similar functions can be created to read obtained TMs, HMs, key items, passed badge checks, etc.

        Returns:
            Set[str]: A set of names of defeated opponents.
        """
        return self.get_raised_flags(self.defeated_opponent_events)

    def get_facing_direction(self) -> Tuple[int, int]:
        """
        Gets the direction the player is facing.
        Returns:
            (int, int): Tuple representing the direction vector (dy, dx).
        """
        direction = self.read_m(0xD52A)
        if direction == 1:
            return (0, 1)  # Right
        elif direction == 2:
            return (0, -1)  # Left
        elif direction == 4:
            return (1, 0)  # Down
        else:
            return (-1, 0)  # Up

    def get_local_coords(self) -> Tuple[int, int, int]:
        """
        Gets the local game coordinates (x, y, map number).
        Returns:
            (int, int, int): Tuple containing (x, y, map number).
        """
        return (self.read_m(0xD362), self.read_m(0xD361), self.read_m(0xD35E))

    def get_global_coords(self):
        """
        Gets the global coordinates of the player.
        Returns:
            (int, int): Tuple containing (global y, global x) coordinates.
        """
        x_pos, y_pos, map_n = self.get_local_coords()
        return self.local_to_global(y_pos, x_pos, map_n)

    def get_badges(self) -> np.array:
        """
        Gets the player's badges as a binary array.
        Returns:
            np.array: Array of 8 binary values representing whether the player has obtained each of the badges.
        """
        # or  self.bit_count(self.read_m(0xD356))
        return np.array(
            [int(bit) for bit in f"{self.read_m(0xD356):08b}"], dtype=np.int8
        )
