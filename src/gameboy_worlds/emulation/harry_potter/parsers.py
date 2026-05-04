import os
import numpy as np
from gameboy_worlds.utils import verify_parameters, log_error
from gameboy_worlds.emulation.parser import StateParser, NamedScreenRegion


class _BaseHarryPotterParser(StateParser):
    """
    Minimal parser scaffold for Harry Potter variants.

    This only configures rom_data_path so the base StateParser can run.
    Includes dialogue detection methods used by HarryPotterOCRMetric.
    """

    VARIANT = ""
    REGIONS = []
    MULTI_TARGET_REGIONS = []
    MULTI_TARGETS = {}

    def __init__(self, pyboy, parameters):
        verify_parameters(parameters)
        variant = self.VARIANT
        if f"{variant}_rom_data_path" not in parameters:
            log_error(
                f"ROM data path not found for variant: {variant}. Add {variant}_rom_data_path to config files.",
                parameters,
            )
        self.rom_data_path = parameters[f"{variant}_rom_data_path"]
        captures_dir = os.path.join(self.rom_data_path, "captures")
        named_screen_regions = []
        for region_name, x, y, w, h in self.REGIONS:
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
        for region_name, x, y, w, h in self.MULTI_TARGET_REGIONS:
            target_names = self.MULTI_TARGETS.get(region_name, [])
            multi_target_paths = {
                t: os.path.join(captures_dir, region_name, t)
                for t in target_names
            }
            region = NamedScreenRegion(
                region_name,
                x,
                y,
                w,
                h,
                parameters=parameters,
                multi_target_paths=multi_target_paths if multi_target_paths else None,
            )
            named_screen_regions.append(region)
        super().__init__(pyboy, parameters, named_screen_regions)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(variant={self.VARIANT})"

    # -- Dialogue detection methods (used by HarryPotterOCRMetric) --
    # These require "dialogue_box_full" (MULTI_TARGET_REGIONS) to be defined
    # in the child parser. No separate indicator region needed — detection
    # works by analyzing the dialogue area content directly.

    def _dialogue_box_content_ratio(self, current_screen: np.ndarray) -> float:
        """Returns the fraction of non-white pixels in the dialogue box area."""
        box = self.capture_named_region(
            current_frame=current_screen, name="dialogue_box_full"
        )
        return float(np.mean(box < 255))

    def dialogue_box_open(self, current_screen: np.ndarray) -> bool:
        """
        Checks if a dialogue box is currently displayed by analyzing pixel
        content in the dialogue_box_full region. If enough non-white pixels
        are present, dialogue is considered active.
        """
        return self._dialogue_box_content_ratio(current_screen) >= 0.08

    def dialogue_box_empty(self, current_screen: np.ndarray) -> bool:
        """
        Checks if the dialogue box area contains no meaningful text.
        """
        return self._dialogue_box_content_ratio(current_screen) < 0.08

    def is_in_dialogue(self, current_screen: np.ndarray) -> bool:
        """Checks if the player is actively reading dialogue text."""
        return self.dialogue_box_open(current_screen)


class HarryPotterChamberOfSecretsParser(_BaseHarryPotterParser):
    VARIANT = "harry_potter_chamber_of_secrets"
    DIALOGUE_BOX_REGION = (0, 112, 155, 7)
    """Shared CoS dialogue box coordinates in (x, y, width, height) form."""

    REGIONS = []

    MULTI_TARGET_REGIONS = [
        ("dialogue_box_full", *DIALOGUE_BOX_REGION),
        ("dobby_bed_area", 96, 71, 40, 48),
        ("dobby_dialogue_area", *DIALOGUE_BOX_REGION),
        ("choose_deck_cos_area", 41, 95, 78, 9),
        ("talk_to_ron_cos_area", *DIALOGUE_BOX_REGION),
        ("flying_car_cutscene_area", 0, 0, 158, 56),
        ("burrow_arrival_dialogue_area", *DIALOGUE_BOX_REGION),
        ("mrs_weasley_dialogue_area", *DIALOGUE_BOX_REGION),
        ("battle_menu_cos_area", 102, 120, 57, 23),
    ]

    MULTI_TARGETS = {
        "dobby_bed_area": [
            "find_dobby",
        ],
        "dobby_dialogue_area": [
            "dobby_dialogue_started",
        ],
        "choose_deck_cos_area": [
            "deck_selected_cos",
        ],
        "talk_to_ron_cos_area": [
            "talk_to_ron",
        ],
        "flying_car_cutscene_area": [
            "flying_car_departure",
        ],
        "burrow_arrival_dialogue_area": [
            "outside_burrow_after_cutscene",
        ],
        "mrs_weasley_dialogue_area": [
            "mrs_weasley_table_dialogue",
        ],
        "battle_menu_cos_area": [
            "in_battle_cos",
        ],
    }


class HarryPotterPhilosophersStoneParser(_BaseHarryPotterParser):
    VARIANT = "harry_potter_philosophers_stone"

    REGIONS = [
        ("potions_shop_shelf", 7, 26, 105, 21),
    ]

    MULTI_TARGET_REGIONS = [
        ("dialogue_box_full", 31, 111, 129, 10),
        ("ollivanders_area", 80, 16, 63, 40),
        ("ollivanders_entrance", 70, 21, 23, 21),
        ("wand_dialogue_area", 19, 43, 31, 46),
        ("wand_received_text", 7, 80, 144, 8),
        ("folio_boy_area", 0, 63, 105, 54),
        ("choose_deck_text", 42, 86, 77, 10),
        ("deck_reward_icon", 68, 129, 16, 14),
        ("gringotts_entrance", 65, 3, 30, 11),
        ("gringotts_interior_area", 62, 112, 31, 15),
        ("hagrid_gringotts_area", 49, 33, 31, 21),
        ("vault_interior", 0, 49, 117, 69),
        ("level_up_text", 33, 47, 94, 9),
        ("boss_rat_area", 44, 40, 12, 15),
        ("spell_level_text", 34, 48, 92, 16),
        ("battle_reward_bar", 39, 25, 77, 6),
        # -- Task 14: find_hagrid_vault_test --
        # The subgoal uses the Hagrid dialogue box screen state rather than
        # Hagrid's sprite, since dialogue is more stable than character art.
        ("post_boss_hagrid_area", 31, 111, 129, 10),   # subgoal: navigate_to_hagrid (capture the Hagrid dialogue box state)
        ("vault_entry_cutscene_area", 55, 32, 75, 39), # termination: vault_entry_cutscene
        # -- Madam Malkin split-task assets --
        ("outside_malkins_area", 19, 4, 21, 17),       # subgoal: outside_malkins
        ("inside_malkins_area", 121, 29, 16, 16),      # termination: inside_malkins
        ("robes_menu_area", 0, 0, 143, 29),            # termination: malkins_buy_menu_open
        ("robes_purchase_area", 31, 25, 80, 6),        # confirmation prompt: confirm_robes_purchase
    ]

    MULTI_TARGETS = {
        "ollivanders_area": [
            "ollivanders_interior",
        ],
        "ollivanders_entrance": [
            "outside_ollivanders_door",
        ],
        "wand_dialogue_area": [
            "talk_to_ollivander",
        ],
        "wand_received_text": [
            "wand_received",
        ],
        "folio_boy_area": [
            "boy_approaches",
        ],
        "choose_deck_text": [
            "choose_deck_shown",
        ],
        "deck_reward_icon": [
            "deck_selected",
        ],
        "gringotts_entrance": [
            "outside_gringotts_door",
        ],
        "gringotts_interior_area": [
            "gringotts_interior",
        ],
        "hagrid_gringotts_area": [
            "find_hagrid_gringotts",
        ],
        "vault_interior": [
            "hagrid_vault_dialogue",
        ],
        "level_up_text": [
            "gained_new_level",
        ],
        "boss_rat_area": [
            "boss_rat_found",
        ],
        "spell_level_text": [
            "gained_new_spell",
        ],
        "battle_reward_bar": [
            "battle_won",
        ],
        # -- Task 14 --
        "post_boss_hagrid_area": [
            "navigate_to_hagrid",
        ],
        "vault_entry_cutscene_area": [
            "vault_entry_cutscene",
        ],
        # -- Madam Malkin split-task assets --
        "outside_malkins_area": [
            "outside_malkins",
        ],
        "inside_malkins_area": [
            "inside_malkins",
        ],
        "robes_menu_area": [
            "malkins_buy_menu_open",
            "selected_robes",
        ],
        "robes_purchase_area": [
            "confirm_robes_purchase",
        ],
    }
