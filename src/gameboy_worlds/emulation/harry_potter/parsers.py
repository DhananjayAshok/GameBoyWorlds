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
        # -- Burrow room navigation tasks --
        ("percy_room_area", 16, 0, 52, 80),         # termination: inside_percy_room
        ("ginny_room_area", 74, 0, 36, 57),         # termination: inside_ginny_room
        ("parents_room_area", 97, 0, 60, 65),       # termination: inside_parents_room
        ("fred_george_room_area", 16, 32, 16, 84),  # termination: inside_fred_george_room
        ("rons_room_area", 137, 0, 22, 71),         # termination: inside_rons_room
        # -- Burrow kitchen / garden quest tasks --
        ("garden_door_area", 80, 24, 10, 8),        # subgoal: outside_garden_door
        ("car_area", 80, 65, 55, 70),
        # Battle action list: bottom fifth of the screen, left three fifths.
        ("battle_action_area", 0, 115, 96, 29),
        ("full_screen_area", 0, 0, 160, 144),
        # Front (lead) slot of the opponents box in battle.
        ("opponent_lead_area", 0, 40, 48, 32),
        # Top-left battle slot, directly above the lead slot.
        ("opponent_top_left_area", 0, 0, 48, 40),
    ]

    MULTI_TARGETS = {
        "dobby_bed_area": [
            "find_dobby",
        ],
        "dialogue_box_full": [
            "talk_to_ron_burrow",
            "talk_to_mom_kitchen",
            "talk_to_ron_garden",
            "talk_glasses_guy",
            "spell_learned",
            "restore_all_magic",
            "broom_doom",
            "reached_diagon_alley",
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
        "battle_action_area": [
            "cast_spell",
            "card_attack",
            "use_item",
            "flee",
            "folio_bruti",
        ],
        "full_screen_area": [
            "use_card_attack",
        ],
        "opponent_lead_area": [
            "sprinkler_lead",
            "green_rat_lead",
        ],
        "opponent_top_left_area": [
            "gnome",
            "grey_hose",
        ],
        # -- Burrow room navigation tasks --
        "percy_room_area": [
            "inside_percy_room",
        ],
        "ginny_room_area": [
            "inside_ginny_room",
        ],
        "parents_room_area": [
            "inside_parents_room",
        ],
        "fred_george_room_area": [
            "inside_fred_george_room",
        ],
        "rons_room_area": [
            "inside_rons_room",
        ],
        "garden_door_area": [
            "outside_garden_door",
        ],
        "car_area": ["next_to_car"],
    }


class HarryPotterPhilosophersStoneParser(_BaseHarryPotterParser):
    VARIANT = "harry_potter_philosophers_stone"
    DIALOGUE_BOX_REGION = (0, 112, 158, 8)
    """Shared PS dialogue box coordinates in (x, y, width, height) form."""

    REGIONS = [
        ("potions_shop_shelf", 7, 26, 105, 21),
    ]

    MULTI_TARGET_REGIONS = [
        ("dialogue_box_full", *DIALOGUE_BOX_REGION),
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
        # -- Flourish & Blotts split-task assets --
        ("outside_flourish_blotts_area", 93, 21, 21, 19),  # subgoal: outside_flourish_blotts
        ("inside_flourish_blotts_area", 54, 16, 91, 49),   # termination: inside_flourish_blotts
        ("books_received_area", 45, 110, 68, 32),          # termination: books_received
        # -- Apothecary split-task assets --
        ("outside_apothecary_area", 95, 31, 20, 18),    # subgoal: outside_apothecary
        ("inside_apothecary_area", 94, 14, 49, 20),     # termination: inside_apothecary
        ("apothecary_menu_area", 0, 0, 157, 30),    # terminations: apothecary_buy_menu_open, selected_apothecary_item
        ("apothecary_purchase_area", 16, 0, 131, 86),   # termination: confirm_apothecary_purchase
        # -- Cauldron shop assets --
        ("outside_cauldron_shop_area", 57, 20, 22, 20),     # subgoal: outside_cauldron_shop
        ("inside_cauldron_shop_area", 17, 2, 54, 20),      # termination: inside_cauldron_shop
        ("cauldron_menu_area", 0, 0, 115, 32),          # subgoal: cauldron_buy_menu_open
        ("cauldron_purchase_area", 31, 24, 78, 7),      # termination: confirm_cauldron_purchase
        # -- Sugarplums Sweets filler tasks --
        ("outside_sugarplums_area", 55, 22, 22, 20),    # subgoal: outside_sugarplums
        ("inside_sugarplums_area", 25, 30, 75, 35),     # termination: inside_sugarplums
        ("sugarplums_menu_area", 0, 0, 130, 30),        # termination: sugarplums_buy_menu_open
        ("find_location", 0, 100, 160, 44),
        ("menu", 0, 0, 90, 120),
        ("last_item", 0, 105, 160, 30),
        ("item_consumption", 0, 30, 160, 110),
        ("equip_screen", 0, 25, 160, 119),
        ("rat_king_sprite_area", 0, 0, 60, 100),
        ("full_screen_area", 0, 0, 160, 144),
        ("mp_points_area", 60, 120, 60, 10),
        ("large_dialogue_box", 0, 112, 160, 32),
        ("chocolate_frogs_5_inventory_area", 0, 60, 160, 20),
        ("leftmost_train_car", 0, 0, 90, 90),
        ("rightmost_train_car", 75, 0, 85, 90),
        ("boat_battle", 100, 60, 60, 20),
        ("top_left_battle", 0, 0, 40, 40),
        ("middle_fight_area", 35, 35, 25, 30),
        # Gargoyles sit on the wall band y 0-25; the pair can appear anywhere
        # across x 20-100, so this is the capture box for the x=62 case.
        ("stone_gargoyles_wall", 62, 0, 20, 25),
        ("top_left_quarter", 0, 0, 80, 72),
        ("center_right", 80, 36, 80, 72),
        # Dead center, extending halfway toward each of the 4 screen edges.
        ("center_half", 40, 36, 80, 72),
        # Full-height vertical strip spanning x 20-50.
        ("left_vertical_strip", 20, 0, 30, 144),
        # Bottom fifth of the screen (144 / 5 ~= 29px).
        ("bottom_fifth", 0, 115, 160, 29),
    ]

    MULTI_TARGETS = {
        "large_dialogue_box": [
            "large_text_content",
            "weakened_health_bar",
            "restored_full_health",
        ],
        "top_left_battle": [
            "yellow_rat",
            "big_yellow_monster",
        ],
        "middle_fight_area": [
            "bat",
            "big_yellow_monster",
        ],
        "stone_gargoyles_wall": [
            "two_stone_gargoyles",
            "two_stone_gargoyles_2",
            "two_stone_gargoyles_3",
        ],
        "chocolate_frogs_5_inventory_area": [
            "chocolate_frogs_5_inventory",
            "chocolate_frogs_4_inventory",
        ],
        "mp_points_area": [
            "fully_restore_your_mp",
        ],
        "find_location": [
            "diagon_alley",
        ],
        "full_screen_area": [
            "respawn_death_rat_screen",
            "reenter_gringotts",
            "exit_gringotts",
            "on_train",
            "sell_chocolate_frog",
            "start_of_duel",
            "win_duel",
            "lose_duel",
            "green_dungeon_room",
            "talking_with_hagrid_dungeon",
            "boss_purple_win",
            "house_points",
        ],
        "top_left_quarter": [
            "boss_purple_start",
        ],
        "center_right": [
            "hourglass_1",
            "hourglass_2",
        ],
        "center_half": [
            "standing_on_seal_facing_up",
        ],
        "left_vertical_strip": [
            "between_gargoyles",
        ],
        "bottom_fifth": [
            "bottom_room",
        ],
        "leftmost_train_car": ["leftmost_train_car_capture"],
        "rightmost_train_car": ["rightmost_train_car_capture"],
        "menu": [
            "start_menu",
        ],
        "rat_king_sprite_area": [
            "rat_king_sprite",
        ],
        "last_item": [
            "pumpkin_pasties",
        ],
        "item_consumption": [
            "ate_pumpkin_pasties",
        ],
        "equip_screen": [
            "nothing_equipped",
            "equipped_pointed_hat",
            "equipped_pointed_hat_plain_work_robe",
            "remove_hat",
            "remove_robe",
            "empty_equip_cursor_robe",
        ],
        "dialogue_box_full": [
            "talk_to_flourish_clerk",
            "hagrid_diagon_dialogue",
            "unable_to_escape",
            "talk_to_weasleys",
            "talk_to_ron_weasley",
            "talk_with_hagrid_before_boat",
            "locked_door",
            "stay_down_there",
        ],
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
        # -- Flourish & Blotts split-task assets --
        "outside_flourish_blotts_area": [
            "outside_flourish_blotts",
        ],
        "inside_flourish_blotts_area": [
            "inside_flourish_blotts",
        ],
        "books_received_area": [
            "books_received",
        ],
        # -- Apothecary split-task assets --
        "outside_apothecary_area": [
            "outside_apothecary",
        ],
        "inside_apothecary_area": [
            "inside_apothecary",
        ],
        "apothecary_menu_area": [
            "apothecary_buy_menu_open",
        ],
        "apothecary_purchase_area": [
            "confirm_apothecary_purchase",
        ],
        # -- Cauldron shop assets --
        "outside_cauldron_shop_area": [
            "outside_cauldron_shop",
        ],
        "inside_cauldron_shop_area": [
            "inside_cauldron_shop",
        ],
        "cauldron_menu_area": [
            "cauldron_buy_menu_open",
        ],
        "cauldron_purchase_area": [
            "confirm_cauldron_purchase",
        ],
        # -- Sugarplums Sweets filler tasks --
        "outside_sugarplums_area": [
            "outside_sugarplums",
        ],
        "inside_sugarplums_area": [
            "inside_sugarplums",
        ],
        "sugarplums_menu_area": [
            "sugarplums_buy_menu_open",
        ],
        "boat_battle": [
            "boat_battle_target",
        ],
    }
