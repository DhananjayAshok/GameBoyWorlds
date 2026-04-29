from typing import Optional, Union, Type, Dict
from gameboy_worlds.emulation.parser import StateParser
from gameboy_worlds.emulation.tracker import StateTracker
from gameboy_worlds.emulation.emulator import Emulator

from gameboy_worlds.emulation.deja_vu.parsers import (
    DejaVu1StateParser,
    DejaVu2StateParser,
)
from gameboy_worlds.emulation.deja_vu.trackers import (
    DejaVuOCRTracker,
    DejaVu1CheckGunTestTracker,
    DejaVu1CloseDoorTestTracker,
    DejaVu1ClosePocketTestTracker,
    DejaVu1CloseWalletTestTracker,
    DejaVu1CoatTestTracker,
    DejaVu1EnterCellarTestTracker,
    DejaVu1EnterConnectingRoomTestTracker,
    DejaVu1EnterEmptyRoomFromMapTestTracker,
    DejaVu1HitBottleTestTracker,
    DejaVu1HitMuggerTestTracker,
    DejaVu1MeetMuggerTestTracker,
    DejaVu1OpenDoorTestTracker,
    DejaVu1OpenPocketTestTracker,
    DejaVu1OpenSpigotTestTracker,
    DejaVu1OpenWalletTestTracker,
    DejaVu1TakeGunTestTracker,
    DejaVu1CheckCoatTestTracker,
    DejaVu1UnlockCarDoorTestTracker,
    DejaVu1UnlockFrontDoorTestTracker,
    DejaVu2Buy2ChipsTestTracker,
    DejaVu2CheckNewsclip1TestTracker,
    DejaVu2CloseDoorFromMapTestTracker,
    DejaVu2ClosePantsPocketTestTracker,
    DejaVu2CloseWallet1TestTracker,
    DejaVu2EnterHallwayTestTracker,
    DejaVu2OpenBathroomDoorTestTracker,
    DejaVu2OpenDoorFromMapTestTracker,
    DejaVu2OpenPantsPocketTestTracker,
    DejaVu2OpenTrenchCoatTestTracker,
    DejaVu2OpenWallet1TestTracker,
    DejaVu2PutOnPantsTestTracker,
    DejaVu2PutOnTrenchCoatTestTracker,
    DejaVu2TakeGumTestTracker,
    DejaVu2TakeLicense1TestTracker,
    DejaVu2TakeNewsclip1TestTracker,
    DejaVu2TakePantsTestTracker,
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
        "take_coat_test": DejaVu1CoatTestTracker,
        "take_gun_test": DejaVu1TakeGunTestTracker,
        "open_door_test": DejaVu1OpenDoorTestTracker,
        "close_door_test": DejaVu1CloseDoorTestTracker,
        "open_pocket_test": DejaVu1OpenPocketTestTracker,
        "open_wallet_test": DejaVu1OpenWalletTestTracker,
        "close_pocket_test": DejaVu1ClosePocketTestTracker,
        "close_wallet_test": DejaVu1CloseWalletTestTracker,
        "checked_coat_test": DejaVu1CheckCoatTestTracker,
        "checked_gun_test": DejaVu1CheckGunTestTracker,
        "hit_bottle_test": DejaVu1HitBottleTestTracker,
        "open_spigot_test": DejaVu1OpenSpigotTestTracker,
        "enter_cellar_test": DejaVu1EnterCellarTestTracker,
        "enter_connecting_room_test": DejaVu1EnterConnectingRoomTestTracker,
        # "make_bet_test": DejaVu1MakeBetTestTracker,
        "enter_empty_room_from_map_test": DejaVu1EnterEmptyRoomFromMapTestTracker,
        "unlock_front_door_test": DejaVu1UnlockFrontDoorTestTracker,
        "meet_mugger_test": DejaVu1MeetMuggerTestTracker,
        "hit_mugger_test": DejaVu1HitMuggerTestTracker,
        "unlock_car_door_test": DejaVu1UnlockCarDoorTestTracker,
    },
    "deja_vu_2": {
        "default": DejaVuOCRTracker,
        "open_trench_coat_test": DejaVu2OpenTrenchCoatTestTracker,
        "open_bathroom_door_test": DejaVu2OpenBathroomDoorTestTracker,
        "take_gum_test": DejaVu2TakeGumTestTracker,
        "open_pants_pocket_test": DejaVu2OpenPantsPocketTestTracker,
        "close_pants_pocket_test": DejaVu2ClosePantsPocketTestTracker,
        "take_pants_test": DejaVu2TakePantsTestTracker,
        "put_on_trench_coat_test": DejaVu2PutOnTrenchCoatTestTracker,
        "put_on_pants_test": DejaVu2PutOnPantsTestTracker,
        "open_wallet1_test": DejaVu2OpenWallet1TestTracker,
        "take_newsclip1_test": DejaVu2TakeNewsclip1TestTracker,
        "take_license1_test": DejaVu2TakeLicense1TestTracker,
        "close_wallet1_test": DejaVu2CloseWallet1TestTracker,
        # "open_cold_tap_test": DejaVu2OpenColdTapTestTracker,
        # "close_cold_tap_test": DejaVu2CloseColdTapTestTracker,
        "check_newsclip1_test": DejaVu2CheckNewsclip1TestTracker,
        # "take_ring1_test": DejaVu2TakeRing1TestTracker,
        "open_door_from_map_test": DejaVu2OpenDoorFromMapTestTracker,
        "close_door_from_map_test": DejaVu2CloseDoorFromMapTestTracker,
        "enter_hallway_test": DejaVu2EnterHallwayTestTracker,
        "buy_2_chips_test": DejaVu2Buy2ChipsTestTracker,
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
