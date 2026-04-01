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
        super().__init__(pyboy, parameters, named_screen_regions)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(variant={self.VARIANT})"


class HarryPotterPhilosophersStoneParser(_BaseHarryPotterParser):
    VARIANT = "harrypotter_philosophersstone"

    REGIONS = [
        ("potions_shop_shelf", 7, 26, 105, 21),
    ]
