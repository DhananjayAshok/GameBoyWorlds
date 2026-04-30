from gameboy_worlds.utils import verify_parameters, log_error
from gameboy_worlds.emulation.parser import StateParser, NamedScreenRegion
import os
from typing import List, Tuple, Optional


def _get_proper_regions(
    override_regions: List[Tuple[str, int, int, int, int]],
    base_regions: List[Tuple[str, int, int, int, int]],
) -> List[Tuple[str, int, int, int, int]]:
    if len(override_regions) == 0:
        return base_regions
    proper_regions = override_regions.copy()
    override_names = [region[0] for region in override_regions]
    for region in base_regions:
        if region[0] not in override_names:
            proper_regions.append(region)
    return proper_regions


class BaseLegendOfZeldaParser(StateParser):
    """
    Minimal state parser for Legend of Zelda GameBoy variants.

    This parser only provides the ROM data path required by the base StateParser.
    No custom screen regions or metrics are defined.
    """

    COMMON_REGIONS = [
        ("health_bar", 102, 128, 36, 8),
        ("playable_area", 0, 0, 159, 143),
        ("dialogue_top", 8, 8, 143, 5),
        ("dialogue_bottom", 8, 80, 143, 5),
    ]

    """ List of common named screen regions for Pokémon games.

    - health_bar_top: When the health bar appears at the top, it signifies that the inventory is open.

    - playable_area: The playable region turns white when doors are used.

    - dialogue_top: Dialogues may sometimes appear at the top.

    - dialogue_bottom: Dialogues may sometimes appear at the bottom.
    """

    def __init__(
        self,
        variant: str,
        pyboy,
        parameters,
        override_regions: Optional[List[Tuple[str, int, int, int, int]]] = None,
    ):
        """
        Args:
            variant: Zelda variant string (e.g., legend_of_zelda_links_awakening).
            pyboy: PyBoy emulator instance.
            parameters: Project parameters loaded from configs.
        """
        verify_parameters(parameters)
        if f"{variant}_rom_data_path" not in parameters:
            log_error(
                f"ROM data path not found for variant: {variant}. Add {variant}_rom_data_path to the config files.",
                parameters,
            )
        self.variant = variant
        self.rom_data_path = parameters[f"{variant}_rom_data_path"]
        captures_dir = self.rom_data_path + "/captures/"
        named_screen_regions = []

        if override_regions is None:
            override_regions = []
        regions = _get_proper_regions(
            override_regions=override_regions,
            base_regions=self.COMMON_REGIONS,
        )

        # for region_name, x, y, w, h in self.COMMON_REGIONS:
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

        super().__init__(pyboy, parameters, named_screen_regions)

    def __repr__(self) -> str:
        return f"<BaseLegendOfZeldaParser(variant={self.variant})>"

    def is_in_dialogue(self, current_screen) -> bool:
        """
        Returns True if the game is in dialogue
        """
        in_dialogue_top = self.named_region_matches_target(
            current_screen, "dialogue_top"
        )
        in_dialogue_bottom = self.named_region_matches_target(
            current_screen, "dialogue_bottom"
        )
        return in_dialogue_top or in_dialogue_bottom

    def is_scene_transition(self, current_screen) -> bool:
        """
        Returns True if the game is in dialogue
        """
        transition = self.named_region_matches_target(current_screen, "playable_area")
        return transition

    def is_in_inventory(self, current_screen) -> bool:
        return False

    def is_in_cutscene(self, current_screen) -> bool:
        return False

    def get_agent_state(self, current_screen) -> str:
        if self.is_scene_transition(current_screen):
            return "scene_transition"
        if self.is_in_dialogue(current_screen):
            return "in_dialogue"
        if self.is_in_inventory(current_screen):
            return "in_inventory"
        #if self.is_in_cutscene(current_screen):
        #    return "in_cutscene" 
        #need to fix this as it is giving in cutscene by checking the specfic health bar at that point
        return "free_roam"


class LegendOfZeldaLinksAwakeningParser(BaseLegendOfZeldaParser):
    def __init__(self, pyboy, parameters):
        override_regions = [
            ("health_bar_top", 102, 0, 36, 8),
            ("equipped_action_1", 7, 130, 8, 10),
            ("equipped_action_2", 46, 130, 8, 10),
            ("owl_tracker", 70, 30, 13, 16),
            ("shield_tracker", 106, 54, 7, 8),
            ("outside_tarinhouse_tracker", 122, 20, 5, 10),
            ("kid_screen_tracker", 154, 49, 5, 8),
            ("library", 33, 17, 12, 13),
            ("signboard", 32, 17, 14, 10),
            ("cash_counter_tracker", 94, 84, 15, 10),
            ("shop_signboard_tracker", 57, 73, 30, 5),
            ("call_booth", 76, 50, 20, 12),
            ("telephone_tracker", 81, 76, 13, 9),
            ("telephone_speech_tracker", 25, 16, 53, 7),
            ("bush_outside_forest", 97, 33, 13, 11),
            ("brave_keyword_tracker", 102, 15, 38, 8),
            ("open_chest_tracker", 64, 49, 14, 7),
            ("stone_break_tracker", 49, 35, 12, 40),
            ("bring_keyword_tracker", 24, 86, 56, 10),
            ("skeleton_tracker", 63, 78, 18, 19),
            ("skeleton2_tracker", 63, 32, 18, 14),
            ("no_grass", 79, 36, 14, 8),
            ("diamond_tracker", 47, 65, 17, 10),
            ("house_right_window", 106, 63, 25, 8),
            ("stool", 80, 81, 14, 10),
            ("char_onstairs", 46, 60, 18, 18),
            ("pot", 80, 33, 15, 12),
            ("pond", 55, 39, 51, 31),
            ("signboard_tracker", 28, 30, 21, 18),
            ("witch_tracker", 62, 52, 18, 26),
            ("pots_tracker", 16, 80, 15, 32)
        ]

        """
        - health_bar: Health bar appears at the bottom in legends of zelda link's awakening.
        - equipped_action_1: Action shown on the bottom-left side of the screen (triggered by A).
        - equipped_action_2: Action shown to the right of equipped_action_1 (triggered by S).
        - outside_tarinhouse_tracker: fence outside the house
        - kid_screen_tracker: represents the tree on the right when we can see kids playing
        """
        super().__init__(
            variant="legend_of_zelda_links_awakening",
            pyboy=pyboy,
            parameters=parameters,
            override_regions=override_regions,
        )

    def is_in_cutscene(self, current_screen) -> bool:
        """
        Returns True if the game is in cutscene
        """
        in_cutscence_1 = self.named_region_matches_target(current_screen, "health_bar")
        in_cutscence_2 = self.named_region_matches_target(
            current_screen, "health_bar_top"
        )
        return not (in_cutscence_1 or in_cutscence_2)

    def is_in_inventory(self, current_screen) -> bool:
        """
        Returns True if the game is in inventory
        """
        in_inventory = self.named_region_matches_target(
            current_screen, "health_bar_top"
        )
        return in_inventory


class LegendOfZeldaTheOracleOfSeasonsParser(BaseLegendOfZeldaParser):
    def __init__(self, pyboy, parameters):
        override_regions = [
            ("health_bar", 102, 0, 36, 8),
            # ("dialogue_top", 8, 25, 143, 38),
            # ("dialogue_bottom", 8, 96, 143, 38),
            ("dialogue_top", 8, 25, 8, 37),
            ("dialogue_bottom", 8, 97, 8, 37),
            ("bricks", 152, 24, 7, 100),
            ("beer_guy_tracker", 15, 48, 18, 16),
            ("red_edges", 106, 76, 15, 12),
            ("after_jump", 79, 67, 16, 14),
            ("flowers", 112, 31, 16, 17),
            ("books", 128, 17, 15, 21),
            ("door", 65, 130, 28, 12),
            ("bottom_right_shore", 90, 73, 18, 16),
            ("edge_character", 140, 25, 16, 19),
            ("char_onstairs", 0, 16, 159, 78),
            ("bush", 97, 33, 13, 13),
            ("clocks", 81, 17, 11, 10),
            ("fireplace", 16, 32, 32, 16),
            ("oof_its_heavy", 9, 25, 136, 17),
            ("green_rock_tracker", 79, 47, 16, 14),
            ("rock", 97, 97, 14, 13),
            ("almirah", 80, 17, 31, 12)
        ]
        """
        - bricks: bricks on the right side of the screen, signifying that the inventory is open.
        """
        super().__init__(
            variant="legend_of_zelda_the_oracle_of_seasons",
            pyboy=pyboy,
            parameters=parameters,
            override_regions=override_regions,
        )

    def is_in_cutscene(self, current_screen) -> bool:
        """
        Returns True if the game is in cutscene
        """
        is_in_cutscene = self.named_region_matches_target(current_screen, "health_bar")
        return not is_in_cutscene

    def is_in_inventory(self, current_screen) -> bool:
        """
        Returns True if the game is in inventory
        """
        is_in_inventory = self.named_region_matches_target(current_screen, "bricks")
        return is_in_inventory


class LegendOfZeldaParser(LegendOfZeldaLinksAwakeningParser):
    pass
