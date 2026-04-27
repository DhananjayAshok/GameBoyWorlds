import os
from gameboy_worlds.utils import verify_parameters, log_error
from gameboy_worlds.emulation.parser import StateParser, NamedScreenRegion


class _BaseHarryPotterParser(StateParser):
    """
    Minimal parser scaffold for Harry Potter variants.

    This only configures rom_data_path so the base StateParser can run.
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


class HarryPotterPhilosophersStoneParser(_BaseHarryPotterParser):
    VARIANT = "harrypotter_philosophersstone"

    REGIONS = [
        ("potions_shop_shelf", 7, 26, 105, 21),
    ]

    MULTI_TARGET_REGIONS = [
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
    }
