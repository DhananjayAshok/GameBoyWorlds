from typing import Dict, Type

from gameboy_worlds.emulation.emulator import Emulator
from gameboy_worlds.emulation.parser import StateParser
from gameboy_worlds.emulation.runes_of_virtue.parsers import (
    RunesOfVirtue1StateParser,
    RunesOfVirtue2StateParser,
)
from gameboy_worlds.emulation.runes_of_virtue.emulators import RunesOfVirtueEmulator
from gameboy_worlds.emulation.runes_of_virtue.trackers import (
    CoreRunesOfVirtueTracker,
    RunesOfVirtueOCRTracker,
    RunesOfVirtue1CaveOfDeceitTestTracker,
    RunesOfVirtue1ChucklesDialogTestTracker,
    RunesOfVirtue1DeathScreenTestTracker,
    RunesOfVirtue1GnuGnu1DialogTestTracker,
    RunesOfVirtue1GnuGnu2DialogTestTracker,
    RunesOfVirtue1KingDialogTestTracker,
    RunesOfVirtue1OpenMenuTestTracker,
    RunesOfVirtue1SherryDialogTestTracker,
    RunesOfVirtue1TelescopeViewTestTracker,
    RunesOfVirtue2BlacksmithFailBuyShieldTestTracker,
    RunesOfVirtue2CaveOfDishonourLadder1TestTracker,
    RunesOfVirtue2CavernOfHatredTestTracker,
    RunesOfVirtue2CaveOfDishonourTestTracker,
    RunesOfVirtue2DeathScreenTestTracker,
    RunesOfVirtue2LordWhitsaberDialogTestTracker,
    RunesOfVirtue2NystulDialogTestTracker,
    RunesOfVirtue2OpenMenuTestTracker,
    RunesOfVirtue2ReadBookTestTracker,
    RunesOfVirtue2SandyCookDialogTestTracker,
    RunesOfVirtue2SherryMouseDialogTestTracker,
)
from gameboy_worlds.emulation.tracker import StateTracker


GAME_TO_GB_NAME = {
    "runes_of_virtue_1": "RunesOfVirtue1.gb",
    "runes_of_virtue_2": "RunesOfVirtue2.gb",
}
""" Expected save name for each game. Save the file to <storage_dir_from_config_file>/<game_name>_rom_data/<gb_name>"""


STRONGEST_PARSERS: Dict[str, Type[StateParser]] = {
    "runes_of_virtue_1": RunesOfVirtue1StateParser,
    "runes_of_virtue_2": RunesOfVirtue2StateParser,
}
""" Mapping of game names to their corresponding strongest StateParser classes. """


AVAILABLE_STATE_TRACKERS: Dict[str, Dict[str, Type[StateTracker]]] = {
    "runes_of_virtue_1": {
        "default": RunesOfVirtueOCRTracker,
        "basic": CoreRunesOfVirtueTracker,
        "open_menu_test": RunesOfVirtue1OpenMenuTestTracker,
        "king_dialog_test": RunesOfVirtue1KingDialogTestTracker,
        "chuckles_dialog_test": RunesOfVirtue1ChucklesDialogTestTracker,
        "gnu_gnu_1_dialog_test": RunesOfVirtue1GnuGnu1DialogTestTracker,
        "gnu_gnu_2_dialog_test": RunesOfVirtue1GnuGnu2DialogTestTracker,
        "sherry_dialog_test": RunesOfVirtue1SherryDialogTestTracker,
        "cave_of_deceit_test": RunesOfVirtue1CaveOfDeceitTestTracker,
        "telescope_view_test": RunesOfVirtue1TelescopeViewTestTracker,
        "death_screen_test": RunesOfVirtue1DeathScreenTestTracker,
    },
    "runes_of_virtue_2": {
        "default": RunesOfVirtueOCRTracker,
        "basic": CoreRunesOfVirtueTracker,
        "open_menu_test": RunesOfVirtue2OpenMenuTestTracker,
        "read_book_test": RunesOfVirtue2ReadBookTestTracker,
        "nystul_dialog_test": RunesOfVirtue2NystulDialogTestTracker,
        "blacksmith_fail_buy_shield_test": (
            RunesOfVirtue2BlacksmithFailBuyShieldTestTracker
        ),
        "sherry_mouse_dialog_test": RunesOfVirtue2SherryMouseDialogTestTracker,
        "sandy_cook_dialog_test": RunesOfVirtue2SandyCookDialogTestTracker,
        "lord_whitsaber_dialog_test": RunesOfVirtue2LordWhitsaberDialogTestTracker,
        "cave_of_dishonour_test": RunesOfVirtue2CaveOfDishonourTestTracker,
        "cavern_of_hatred_test": RunesOfVirtue2CavernOfHatredTestTracker,
        "cave_of_dishonour_ladder_1_test": (
            RunesOfVirtue2CaveOfDishonourLadder1TestTracker
        ),
        "death_screen_test": RunesOfVirtue2DeathScreenTestTracker,
    },
}
""" Mapping of game names to their available StateTracker classes with string identifiers. """


AVAILABLE_EMULATORS: Dict[str, Dict[str, Type[Emulator]]] = {
    "runes_of_virtue_1": {"default": RunesOfVirtueEmulator},
    "runes_of_virtue_2": {"default": RunesOfVirtueEmulator},
}
""" Mapping of game names to their available Emulator classes with string identifiers. """
