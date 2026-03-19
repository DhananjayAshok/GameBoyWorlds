from gameboy_worlds.utils import verify_parameters, log_error
from gameboy_worlds.emulation.parser import StateParser, NamedScreenRegion
import os


class UltimaRunesOfVirtueParser(StateParser):
    """
    State parser for Ultima: Runes of Virtue.

    Defines screen regions for detecting menu state.

    Screen regions:
    - menu_indicator: A region (y=30-50, x=20-60) that is uniformly white when the
      inventory/status menu is open (triggered by START), and contains game world
      content during normal gameplay.
    """

    VARIANT = "ultima_runes_of_virtue"

    REGIONS = [
        ("menu_indicator", 20, 30, 40, 20),
    ]

    def __init__(self, pyboy, parameters):
        verify_parameters(parameters)
        variant = self.VARIANT
        if f"{variant}_rom_data_path" not in parameters:
            log_error(
                f"ROM data path not found for variant: {variant}. "
                f"Add {variant}_rom_data_path to config files.",
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

        super().__init__(pyboy, parameters, named_screen_regions)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(variant={self.VARIANT})"

    def is_in_menu(self, current_screen) -> bool:
        """Returns True if the game is showing the inventory/status menu."""
        return self.named_region_matches_target(current_screen, "menu_indicator")

    def get_agent_state(self, current_screen) -> str:
        """Returns a string describing the current agent state."""
        if self.is_in_menu(current_screen):
            return "in_menu"
        return "free_roam"
