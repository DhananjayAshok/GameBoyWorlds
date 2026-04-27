from typing import Optional, Union, Type, Dict
from gameboy_worlds.emulation.parser import StateParser
from gameboy_worlds.emulation.tracker import StateTracker
from gameboy_worlds.emulation.emulator import Emulator

from gameboy_worlds.emulation.deja_vu.parsers import (
    DejaVu1StateParser,
    DejaVu2StateParser,
)
from gameboy_worlds.emulation.deja_vu.trackers import (
    DejaVuBuy2ChipsTestTracker,
    DejaVuCheckNewsclip1TestTracker,
    DejaVuCloseColdTapTestTracker,
    DejaVuCloseDoorFromMapTestTracker,
    DejaVuCloseWallet1TestTracker,
    DejaVuEnterConnectingRoomTestTracker,
    DejaVuEnterHallwayTestTracker,
    DejaVuHitMuggerTestTracker,
    DejaVuMakeBetTestTracker,
    DejaVuMeetMuggerTestTracker,
    DejaVuOCRTracker,
    DejaVuClosePantsPocketTestTracker,
    DejaVuCoatTestTracker,
    DejaVuEnterCellarTestTracker,
    DejaVuOpenBathroomDoorTestTracker,
    DejaVuOpenColdTapTestTracker,
    DejaVuOpenDoorFromMapTestTracker,
    DejaVuOpenPantsPocketTestTracker,
    DejaVuOpenSpigotTestTracker,
    DejaVuOpenTrenchCoatTestTracker,
    DejaVuOpenWallet1TestTracker,
    DejaVuPutOnPantsTestTracker,
    DejaVuPutOnTrenchCoatTestTracker,
    DejaVuTakeGumTestTracker,
    DejaVuTakeGunTestTracker,
    DejaVuOpenDoorTestTracker,
    DejaVuCloseDoorTestTracker,
    DejaVuOpenPocketTestTracker,
    DejaVuOpenWalletTestTracker,
    DejaVuClosePocketTestTracker,
    DejaVuCloseWalletTestTracker,
    DejaVuCheckCoatTestTracker,
    DejaVuCheckGunTestTracker,
    DejaVuHitBottleTestTracker,
    DejaVuTakeLicense1TestTracker,
    DejaVuTakeNewsclip1TestTracker,
    DejaVuTakePantsTestTracker,
    DejaVuTakeRing1TestTracker,
    DejaVuEnterEmptyRoomFromMapTestTracker,
    DejaVuUnlockCarDoorTestTracker,
    DejaVuUnlockFrontDoorTestTracker,
)
from gameboy_worlds.emulation.deja_vu.emulators import DejaVuEmulator

GAME_TO_GB_NAME = {
    "deja_vu_1": "DejaVu.gbc",
    "deja_vu_2": "DejaVu.gbc",
}
""" Expected save name for each game. Save the file to <storage_dir_from_config_file>/<game_name>_rom_data/<gb_name>"""

STRONGEST_PARSERS: Dict[str, Type[StateParser]] = {
    "deja_vu_1": DejaVu1StateParser,
    "deja_vu_2": DejaVu2StateParser,
}
""" Mapping of game names to their corresponding strongest StateParser classes. 
Unless you have a very good reason, you should always use the STRONGEST possible parser for a given game. 
The parser itself does not affect performance, as for it to perform a read / screen comparison operation , it must be called upon by the state tracker.
This means there is never a reason to use a weaker parser. 
"""


AVAILABLE_STATE_TRACKERS: Dict[str, Dict[str, Type[StateTracker]]] = {
    "deja_vu_1": {
        "default": DejaVuOCRTracker,
        "take_coat_test": DejaVuCoatTestTracker,
        "take_gun_test": DejaVuTakeGunTestTracker,
        "open_door_test": DejaVuOpenDoorTestTracker,
        "close_door_test": DejaVuCloseDoorTestTracker,
        "open_pocket_test": DejaVuOpenPocketTestTracker,
        "open_wallet_test": DejaVuOpenWalletTestTracker,
        "close_pocket_test": DejaVuClosePocketTestTracker,
        "close_wallet_test": DejaVuCloseWalletTestTracker,
        "checked_coat_test": DejaVuCheckCoatTestTracker,
        "checked_gun_test": DejaVuCheckGunTestTracker,
        "hit_bottle_test": DejaVuHitBottleTestTracker,
        "open_spigot_test": DejaVuOpenSpigotTestTracker,
        "enter_cellar_test": DejaVuEnterCellarTestTracker,
        "enter_connecting_room_test": DejaVuEnterConnectingRoomTestTracker,
        "make_bet_test": DejaVuMakeBetTestTracker,
        "enter_empty_room_from_map_test": DejaVuEnterEmptyRoomFromMapTestTracker,
        "unlock_front_door_test": DejaVuUnlockFrontDoorTestTracker,
        "meet_mugger_test": DejaVuMeetMuggerTestTracker,
        "hit_mugger_test": DejaVuHitMuggerTestTracker,
        "unlock_car_door_test": DejaVuUnlockCarDoorTestTracker,
    },
    "deja_vu_2": {
        "default": DejaVuOCRTracker,
        "open_trench_coat_test": DejaVuOpenTrenchCoatTestTracker,
        "open_bathroom_door_test": DejaVuOpenBathroomDoorTestTracker,
        "take_gum_test": DejaVuTakeGumTestTracker,
        "open_pants_pocket_test": DejaVuOpenPantsPocketTestTracker,
        "close_pants_pocket_test": DejaVuClosePantsPocketTestTracker,
        "take_pants_test": DejaVuTakePantsTestTracker,
        "put_on_trench_coat_test": DejaVuPutOnTrenchCoatTestTracker,
        "put_on_pants_test": DejaVuPutOnPantsTestTracker,
        "open_wallet1_test": DejaVuOpenWallet1TestTracker,
        "take_newsclip1_test": DejaVuTakeNewsclip1TestTracker,
        "take_license1_test": DejaVuTakeLicense1TestTracker,
        "close_wallet1_test": DejaVuCloseWallet1TestTracker,
        "open_cold_tap_test": DejaVuOpenColdTapTestTracker,
        "close_cold_tap_test": DejaVuCloseColdTapTestTracker,
        "check_newsclip1_test": DejaVuCheckNewsclip1TestTracker,
        "take_ring1_test": DejaVuTakeRing1TestTracker,
        "open_door_from_map_test": DejaVuOpenDoorFromMapTestTracker,
        "close_door_from_map_test": DejaVuCloseDoorFromMapTestTracker,
        "enter_hallway_test": DejaVuEnterHallwayTestTracker,
        "buy_2_chips_test": DejaVuBuy2ChipsTestTracker,
    },
}
""" Mapping of game names to their available StateTracker classes with string identifiers. """


AVAILABLE_EMULATORS: Dict[str, Dict[str, Type[Emulator]]] = {
    "deja_vu_1": {
        "default": DejaVuEmulator,
    },
    "deja_vu_2": {
        "default": DejaVuEmulator,
    },
}
""" Mapping of game names to their available Emulator classes with string identifiers. """
