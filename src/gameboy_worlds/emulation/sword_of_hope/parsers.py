import os
from typing import List, Tuple, Dict

from gameboy_worlds.utils import verify_parameters, log_error
from gameboy_worlds.emulation.parser import StateParser, NamedScreenRegion, _get_proper_regions


class _BaseSwordOfHopeParser(StateParser):
    """
    Base parser for Sword of Hope variants.
    Defines common screen regions for the SoH UI layout:
      - Top stats bar (LV, HP, MP)
      - Game viewport + Gold/EX
      - Status bar (MOVE | ROOM NAME)
      - Command grid (Look/Use/Open/Magic/Hit/Power + directional pad)
    """

    VARIANT = ""

    COMMON_MULTI_TARGET_REGIONS = [
        ("room_label", 48, 72, 104, 16),
        ("game_viewport", 4, 16, 92, 56),
        ("status_bar", 4, 72, 152, 16),
        ("command_area", 4, 88, 152, 56),
        ("battle_full", 4, 16, 152, 128),
        ("battle_viewport", 4, 16, 152, 56),
        ("battle_command", 4, 74, 152, 70),
        ("status_command", 4, 72, 152, 72),
        ("full_screen", 0, 0, 160, 144),
        ("soh2_enemy_viewport", 4, 0, 152, 68),
        ("soh2_battle_command", 4, 68, 152, 19),
        ("soh2_party_stats", 4, 87, 152, 48),
        ("soh2_room_label", 8, 4, 144, 20),
    ]
    """
    - room_label: The room name text on the right side of the MOVE|ROOM status bar. Used for location-based termination.
    - game_viewport: The rendered scene area (top-left quadrant of the screen, below stats).
    - status_bar: The full MOVE | ROOM NAME bar.
    - command_area: The bottom command grid (directional pad + action commands).
    - battle_full: Everything below the LV/HP/MP stats bar (enemy sprites + battle commands). Used for battle detection.
    - battle_viewport: Full-width enemy sprite area (wider than game_viewport to include right side).
    - battle_command: Battle command area including FIGHT/AUTO row + MAGIC/USE/ESCAPE + enemy list.
    - status_command: Status bar + command area combined (y=72 to y=144). Useful for detecting interaction results where text changes span both areas.
    - soh2_enemy_viewport: SoH2 only. Enemy sprite area; SoH2 has no top stats bar so the sprite extends to y=0.
    - soh2_battle_command: SoH2 only. Horizontal command row (CLASH/FLEE/AUTO solo, MAGIC/ITEM/etc with party).
    - soh2_party_stats: SoH2 only. Live LV/HP/MP table at the bottom. Values change per frame so this is mainly for VLM/OCR, not for .npy match termination.
    - soh2_room_label: SoH2 only. The room name header at the TOP of the screen (SoH2 puts the room name above the viewport, not in the bottom MOVE bar like SoH1).
    """

    COMMON_MULTI_TARGETS = {}

    def __init__(
        self,
        pyboy,
        parameters,
        additional_multi_target_regions: List[Tuple[str, int, int, int, int]] = [],
        override_multi_targets: Dict[str, List[str]] = {},
    ):
        verify_parameters(parameters)
        variant = self.VARIANT
        if f"{variant}_rom_data_path" not in parameters:
            log_error(
                f"ROM data path not found for variant: {variant}. Add {variant}_rom_data_path to config files.",
                parameters,
            )
        self.rom_data_path = parameters[f"{variant}_rom_data_path"]
        captures_dir = os.path.join(self.rom_data_path, "captures")

        multi_target_regions = _get_proper_regions(
            override_regions=additional_multi_target_regions,
            base_regions=self.COMMON_MULTI_TARGET_REGIONS,
        )

        multi_targets = {}
        for key, val in self.COMMON_MULTI_TARGETS.items():
            multi_targets[key] = list(val)
        for key in override_multi_targets:
            if key in multi_targets:
                multi_targets[key].extend(override_multi_targets[key])
            else:
                multi_targets[key] = override_multi_targets[key]

        named_screen_regions = []
        for region_name, x, y, w, h in multi_target_regions:
            region_target_paths = {}
            subdir = os.path.join(captures_dir, region_name)
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

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(variant={self.VARIANT})"


class SwordOfHope1Parser(_BaseSwordOfHopeParser):
    VARIANT = "sword_of_hope_1"

    COMMON_MULTI_TARGETS = {
        "room_label": [
            "mill_room",
            "oldman_house",
            "in_forest",
            "shaman_house",
            "shaman_room",
        ],
        "command_area": [
            "dialogue_active",
            "dialogue_cleared",
            "look_selected",
            "exploration_menu",
            "menu_open",
        ],
        "battle_command": [
            "battle_active",
            "battle_won",
            "battle_magic_menu",
            "escape_confirmed",
        ],
        "status_command": [
            "look_target_options",
            "item_found",
            "shop_menu_open",
            "purchase_confirmed",
            "dialogue_visible",
            "dialogue_initiated",
            "dialogue_advanced",
            "magic_menu_open",
            "teleport_result",
            "teleport_dest_cursor",
            "teleport_landed",
        ],
        "battle_full": [
            "mistress_first_dialogue",
            "mistress_second_dialogue",
            "save_prompt_visible",
            "save_confirmed",
            "look_path_target",
            "herb_received",
            "treant_defeated",
            "key_m_selected",
            "gate_opened",
            "in_backroom",
            "scroll_received",
            "grace_selected",
            "charm_received",
        ],
    }


class SwordOfHope2Parser(_BaseSwordOfHopeParser):
    VARIANT = "sword_of_hope_2"

    COMMON_MULTI_TARGETS = {
        "status_command": [
            "dialogue_active",
            "dialogue_cleared",
            "dialogue_initiated",
            "dialogue_advanced",
            "dialogue_visible",
            "battle_won",
            "escape_confirmed",
            "wheat_purchased",
            "motion_result",
            "battle_magic_menu",
            "cpr_sword_purchased",
            "wheat_from_tree",
            "wheat_consumed",
            "cursor_on_power",
            "power_stats_first_page",
            "power_stats_exp_page",
            "cursor_on_look",
            "cursor_on_item",
            "cursor_on_open",
            "cursor_on_magic",
            "cursor_on_hit",
        ],
        "full_screen": [
            "shop_menu_open",
            "magic_menu_open",
            "weapons_shop_menu_open",
            "look_shopkeeper",
            "shop_buy_sell_menu",
            "cursor_on_cpr_sword",
            "hit_tree_target",
            "item_menu_open",
            "use_menu_open",
            "cursor_on_wheat",
        ],
        "command_area": [
            "exploration_menu",
            "power_menu_last_slide",
        ],
        "soh2_room_label": [
            "kings_room",
            "riccar_castle",
        ],
        "soh2_battle_command": [
            "battle_active",
            "cursor_on_auto",
        ],
    }
