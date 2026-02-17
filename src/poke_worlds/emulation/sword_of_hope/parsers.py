from poke_worlds.utils import verify_parameters, log_error
from poke_worlds.emulation.parser import StateParser


class _BaseSwordOfHopeParser(StateParser):
    """
    Minimal parser scaffold for Sword of Hope variants.

    This only configures rom_data_path so the base StateParser can run.
    """

    VARIANT = ""

    def __init__(self, pyboy, parameters):
        verify_parameters(parameters)
        variant = self.VARIANT
        if f"{variant}_rom_data_path" not in parameters:
            log_error(
                f"ROM data path not found for variant: {variant}. Add {variant}_rom_data_path to config files.",
                parameters,
            )
        self.rom_data_path = parameters[f"{variant}_rom_data_path"]
        super().__init__(pyboy, parameters)

    def __repr__(self) -> str:
        return self.__class__.__name__


class SwordOfHope1Parser(_BaseSwordOfHopeParser):
    VARIANT = "sword_of_hope_1"


class SwordOfHope2Parser(_BaseSwordOfHopeParser):
    VARIANT = "sword_of_hope_2"
