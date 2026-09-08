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
    RunesOfVirtue1BasementChestOpenedTestTracker,
    RunesOfVirtue1BasementLadderUnlockedTestTracker,
    RunesOfVirtue1CavernOfHatredEnterFloor2TestTracker,
    RunesOfVirtue1CavernOfHatredSherryFloor2DialogTestTracker,
    RunesOfVirtue1CavernOfHatredChooseDoorWithSherryTestTracker,
    RunesOfVirtue1CavernOfHatredChooseRightDoorMelissaDialogTestTracker,
    RunesOfVirtue1CavernOfHatredEnterFloor3TestTracker,
    RunesOfVirtue1CavernOfHatredEnterFloor4TestTracker,
    RunesOfVirtue1CavernOfHatredEnterFloor5TestTracker,
    RunesOfVirtue1CavernOfHatredTalkToKlopFloor5TestTracker,
    RunesOfVirtue1CavernOfHatredTalkToKlipFloor5TestTracker,
    RunesOfVirtue1CavernOfHatredObtainAxeFloor5TestTracker,
    RunesOfVirtue1CavernOfHatredExitedTestTracker,
    RunesOfVirtue1CavernOfHatredChestFloor1OpenedTestTracker,
    RunesOfVirtue1CavernOfHatredTestTracker,
    RunesOfVirtue1CavernOfCowardiceTestTracker,
    RunesOfVirtue1CavernOfCowardiceEnterFloor2TestTracker,
    RunesOfVirtue1CavernOfCowardiceEnterFloor3TestTracker,
    RunesOfVirtue1CavernOfCowardiceFloor3ChestOpenedTestTracker,
    RunesOfVirtue1CavernOfCowardiceEnterFloor4TestTracker,
    RunesOfVirtue1CavernOfCowardiceSherryFloor4DialogTestTracker,
    RunesOfVirtue1CavernOfCowardiceTakeStewFloor4TestTracker,
    RunesOfVirtue1CavernOfCowardiceObtainCoinFloor4TestTracker,
    RunesOfVirtue1CavernOfCowardiceEnterFloor5TestTracker,
    RunesOfVirtue1CavernOfCowardiceObtainKeyFromDrCatFloor5TestTracker,
    RunesOfVirtue1CavernOfCowardiceEnterFloor6TestTracker,
    RunesOfVirtue1CavernOfCowardiceEnterSecretDoorFloor6TestTracker,
    RunesOfVirtue1CavernOfCowardiceTalkToSherryFloor6TestTracker,
    RunesOfVirtue1CavernOfCowardiceTalkToChucklesFloor6TestTracker,
    RunesOfVirtue1CavernOfCowardiceObtainMagicRopeFloor6TestTracker,
    RunesOfVirtue1CavernOfDeceitTestTracker,
    RunesOfVirtue1CavernOfDeceitEnterFloor2TestTracker,
    RunesOfVirtue1CavernOfDeceitEnterFloor3TestTracker,
    RunesOfVirtue1CavernOfDeceitEnterFloor4TestTracker,
    RunesOfVirtue1ChucklesDialogTestTracker,
    RunesOfVirtue1DeathScreenTestTracker,
    RunesOfVirtue1DrCatDialogTestTracker,
    RunesOfVirtue1CavernOfDeceitTalkToFinnFloor1TestTracker,
    RunesOfVirtue1CavernOfDeceitTalkToKadorFloor3TestTracker,
    RunesOfVirtue1CavernOfDeceitTalkToFinnFloor3TestTracker,
    RunesOfVirtue1CavernOfDeceitEnterEastDoorFloor1TestTracker,
    RunesOfVirtue1DrCatCatsLairDialogTestTracker,
    RunesOfVirtue1BuyTwoCakesTestTracker,
    RunesOfVirtue1GnuGnu1DialogTestTracker,
    RunesOfVirtue1GnuGnu2DialogTestTracker,
    RunesOfVirtue1KingDialogTestTracker,
    RunesOfVirtue1OpenMenuTestTracker,
    RunesOfVirtue1SherryDialogTestTracker,
    RunesOfVirtue1ShipRiddenTestTracker,
    RunesOfVirtue1TelescopeViewTestTracker,
    RunesOfVirtue2BlacksmithFailBuyShieldTestTracker,
    RunesOfVirtue2BlockedRoomEnteredTestTracker,
    RunesOfVirtue2BringTholdenBackToKingTestTracker,
    RunesOfVirtue2CaveOfDishonourEquipRodFloor3TestTracker,
    RunesOfVirtue2CaveOfDishonourEnterFloor3BlockedTestTracker,
    RunesOfVirtue2CaveOfDishonourEnterFloor4TestTracker,
    RunesOfVirtue2CaveOfDishonourExitedTestTracker,
    RunesOfVirtue2CityOfYewEnteredTestTracker,
    RunesOfVirtue2CityOfYewWelcomeSignReadTestTracker,
    RunesOfVirtue2MandrakeBardDialogTestTracker,
    RunesOfVirtue2CavernOfInjusticeTalkToZoltanFloor4TestTracker,
    RunesOfVirtue2CavernOfInjusticeReadHintFloor5TestTracker,
    RunesOfVirtue2CavernOfInjusticeTalkToTerryFloor5TestTracker,
    RunesOfVirtue2CavernOfInjusticeEnteredTestTracker,
    RunesOfVirtue2CavernOfInjusticeEnterFloor2TestTracker,
    RunesOfVirtue2CavernOfInjusticeEnterFloor3TestTracker,
    RunesOfVirtue2CavernOfInjusticeEnterFloor4TestTracker,
    RunesOfVirtue2CavernOfInjusticeEnterFloor5TestTracker,
    RunesOfVirtue2CavernOfInjusticeEnterFloor6TestTracker,
    RunesOfVirtue2CavernOfInjusticeEnterFloor7TestTracker,
    RunesOfVirtue2CavernOfInjusticeEnterEastPortalFloor3TestTracker,
    RunesOfVirtue2CaveOfDishonourEnterFloor3TestTracker,
    RunesOfVirtue2CaveOfDishonourEnterFloor2TestTracker,
    RunesOfVirtue2CaveOfDishonourTestTracker,
    RunesOfVirtue2ClimbLadderBehindLockedDoorTestTracker,
    RunesOfVirtue2FindLadderBackFromCastleTestTracker,
    RunesOfVirtue2FindLadderOutOfCavernOfHatredTestTracker,
    RunesOfVirtue2AttendCastleCeremonyTestTracker,
    RunesOfVirtue2RuneOfHonourObtainedTestTracker,
    RunesOfVirtue2GiveCheeseToSherryTestTracker,
    RunesOfVirtue2GrabCheeseFromKitchenTestTracker,
    RunesOfVirtue2InteractWithMapOnTableTestTracker,
    RunesOfVirtue2CavernOfHatredEnterFloor4TestTracker,
    RunesOfVirtue2CavernOfHatredEnterFloor5TestTracker,
    RunesOfVirtue2CavernOfHatredEnterFloor6TestTracker,
    RunesOfVirtue2CavernOfHatredEnterFloor7TestTracker,
    RunesOfVirtue2CavernOfHatredGate1UnlockedTestTracker,
    RunesOfVirtue2CavernOfHatredGrabKeyTestTracker,
    RunesOfVirtue2CavernOfHatredLadder2TestTracker,
    RunesOfVirtue2CavernOfHatredLadderRoom2TestTracker,
    RunesOfVirtue2CavernOfHatredTestTracker,
    RunesOfVirtue2DeathScreenTestTracker,
    RunesOfVirtue2CaveOfDishonourLordWhitsaberFloor4TestTracker,
    RunesOfVirtue2LordWhitsaberDialogTestTracker,
    RunesOfVirtue2NystulDialogTestTracker,
    RunesOfVirtue2OpenMenuTestTracker,
    RunesOfVirtue2ReadBookTestTracker,
    RunesOfVirtue2SandyCookDialogTestTracker,
    RunesOfVirtue2SherryMouseDialogTestTracker,
    RunesOfVirtue2UnlockDoorAndSaveTholdenTestTracker,
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
        "cavern_of_hatred_test": RunesOfVirtue1CavernOfHatredTestTracker,
        "cavern_of_cowardice_test": RunesOfVirtue1CavernOfCowardiceTestTracker,
        "cavern_of_cowardice_enter_floor_2_test": (
            RunesOfVirtue1CavernOfCowardiceEnterFloor2TestTracker
        ),
        "cavern_of_cowardice_enter_floor_3_test": (
            RunesOfVirtue1CavernOfCowardiceEnterFloor3TestTracker
        ),
        "cavern_of_cowardice_floor_3_chest_opened_test": (
            RunesOfVirtue1CavernOfCowardiceFloor3ChestOpenedTestTracker
        ),
        "cavern_of_cowardice_enter_floor_4_test": (
            RunesOfVirtue1CavernOfCowardiceEnterFloor4TestTracker
        ),
        "cavern_of_cowardice_sherry_floor_4_dialog_test": (
            RunesOfVirtue1CavernOfCowardiceSherryFloor4DialogTestTracker
        ),
        "cavern_of_cowardice_take_stew_floor_4_test": (
            RunesOfVirtue1CavernOfCowardiceTakeStewFloor4TestTracker
        ),
        "cavern_of_cowardice_obtain_coin_floor_4_test": (
            RunesOfVirtue1CavernOfCowardiceObtainCoinFloor4TestTracker
        ),
        "cavern_of_cowardice_enter_floor_5_test": (
            RunesOfVirtue1CavernOfCowardiceEnterFloor5TestTracker
        ),
        "cavern_of_cowardice_obtain_key_from_dr_cat_floor_5_test": (
            RunesOfVirtue1CavernOfCowardiceObtainKeyFromDrCatFloor5TestTracker
        ),
        "cavern_of_cowardice_enter_floor_6_test": (
            RunesOfVirtue1CavernOfCowardiceEnterFloor6TestTracker
        ),
        "cavern_of_cowardice_enter_secret_door_floor_6_test": (
            RunesOfVirtue1CavernOfCowardiceEnterSecretDoorFloor6TestTracker
        ),
        "cavern_of_cowardice_talk_to_sherry_floor_6_test": (
            RunesOfVirtue1CavernOfCowardiceTalkToSherryFloor6TestTracker
        ),
        "cavern_of_cowardice_talk_to_chuckles_floor_6_test": (
            RunesOfVirtue1CavernOfCowardiceTalkToChucklesFloor6TestTracker
        ),
        "cavern_of_cowardice_obtain_magic_rope_floor_6_test": (
            RunesOfVirtue1CavernOfCowardiceObtainMagicRopeFloor6TestTracker
        ),
        "cavern_of_deceit_test": RunesOfVirtue1CavernOfDeceitTestTracker,
        "cavern_of_deceit_enter_floor_2_test": (
            RunesOfVirtue1CavernOfDeceitEnterFloor2TestTracker
        ),
        "cavern_of_deceit_enter_floor_3_test": (
            RunesOfVirtue1CavernOfDeceitEnterFloor3TestTracker
        ),
        "cavern_of_deceit_enter_floor_4_test": (
            RunesOfVirtue1CavernOfDeceitEnterFloor4TestTracker
        ),
        "dr_cat_dialog_test": RunesOfVirtue1DrCatDialogTestTracker,
        "cavern_of_deceit_talk_to_finn_floor_1_test": (
            RunesOfVirtue1CavernOfDeceitTalkToFinnFloor1TestTracker
        ),
        "cavern_of_deceit_talk_to_kador_floor_3_test": (
            RunesOfVirtue1CavernOfDeceitTalkToKadorFloor3TestTracker
        ),
        "cavern_of_deceit_talk_to_finn_floor_3_test": (
            RunesOfVirtue1CavernOfDeceitTalkToFinnFloor3TestTracker
        ),
        "cavern_of_deceit_enter_east_door_floor_1_test": (
            RunesOfVirtue1CavernOfDeceitEnterEastDoorFloor1TestTracker
        ),
        "dr_cat_cats_lair_dialog_test": (
            RunesOfVirtue1DrCatCatsLairDialogTestTracker
        ),
        "buy_two_cakes_test": RunesOfVirtue1BuyTwoCakesTestTracker,
        "ship_ridden_test": RunesOfVirtue1ShipRiddenTestTracker,
        "basement_ladder_unlocked_test": (
            RunesOfVirtue1BasementLadderUnlockedTestTracker
        ),
        "basement_chest_opened_test": RunesOfVirtue1BasementChestOpenedTestTracker,
        "cavern_of_hatred_enter_floor_2_test": (
            RunesOfVirtue1CavernOfHatredEnterFloor2TestTracker
        ),
        "cavern_of_hatred_sherry_floor_2_dialog_test": (
            RunesOfVirtue1CavernOfHatredSherryFloor2DialogTestTracker
        ),
        "cavern_of_hatred_choose_door_with_sherry_test": (
            RunesOfVirtue1CavernOfHatredChooseDoorWithSherryTestTracker
        ),
        "cavern_of_hatred_choose_right_door_melissa_dialog_test": (
            RunesOfVirtue1CavernOfHatredChooseRightDoorMelissaDialogTestTracker
        ),
        "cavern_of_hatred_enter_floor_3_test": (
            RunesOfVirtue1CavernOfHatredEnterFloor3TestTracker
        ),
        "cavern_of_hatred_enter_floor_4_test": (
            RunesOfVirtue1CavernOfHatredEnterFloor4TestTracker
        ),
        "cavern_of_hatred_enter_floor_5_test": (
            RunesOfVirtue1CavernOfHatredEnterFloor5TestTracker
        ),
        "cavern_of_hatred_talk_to_klop_floor_5_test": (
            RunesOfVirtue1CavernOfHatredTalkToKlopFloor5TestTracker
        ),
        "cavern_of_hatred_talk_to_klip_floor_5_test": (
            RunesOfVirtue1CavernOfHatredTalkToKlipFloor5TestTracker
        ),
        "cavern_of_hatred_obtain_axe_floor_5_test": (
            RunesOfVirtue1CavernOfHatredObtainAxeFloor5TestTracker
        ),
        "cavern_of_hatred_exited_test": (
            RunesOfVirtue1CavernOfHatredExitedTestTracker
        ),
        "cavern_of_hatred_chest_floor_1_opened_test": (
            RunesOfVirtue1CavernOfHatredChestFloor1OpenedTestTracker
        ),
        "telescope_view_test": RunesOfVirtue1TelescopeViewTestTracker,
        "death_screen_test": RunesOfVirtue1DeathScreenTestTracker,
    },
    "runes_of_virtue_2": {
        "default": RunesOfVirtueOCRTracker,
        "basic": CoreRunesOfVirtueTracker,
        "open_menu_test": RunesOfVirtue2OpenMenuTestTracker,
        "read_book_test": RunesOfVirtue2ReadBookTestTracker,
        "blocked_room_entered_test": RunesOfVirtue2BlockedRoomEnteredTestTracker,
        "nystul_dialog_test": RunesOfVirtue2NystulDialogTestTracker,
        "blacksmith_fail_buy_shield_test": (
            RunesOfVirtue2BlacksmithFailBuyShieldTestTracker
        ),
        "sherry_mouse_dialog_test": RunesOfVirtue2SherryMouseDialogTestTracker,
        "sandy_cook_dialog_test": RunesOfVirtue2SandyCookDialogTestTracker,
        "lord_whitsaber_dialog_test": RunesOfVirtue2LordWhitsaberDialogTestTracker,
        "cave_of_dishonour_lord_whitsaber_floor_4_test": (
            RunesOfVirtue2CaveOfDishonourLordWhitsaberFloor4TestTracker
        ),
        "cave_of_dishonour_test": RunesOfVirtue2CaveOfDishonourTestTracker,
        "cavern_of_hatred_test": RunesOfVirtue2CavernOfHatredTestTracker,
        "cave_of_dishonour_enter_floor_2_test": (
            RunesOfVirtue2CaveOfDishonourEnterFloor2TestTracker
        ),
        "cave_of_dishonour_enter_floor_3_test": (
            RunesOfVirtue2CaveOfDishonourEnterFloor3TestTracker
        ),
        "cave_of_dishonour_equip_rod_floor_3_test": (
            RunesOfVirtue2CaveOfDishonourEquipRodFloor3TestTracker
        ),
        "cave_of_dishonour_enter_floor_3_blocked_test": (
            RunesOfVirtue2CaveOfDishonourEnterFloor3BlockedTestTracker
        ),
        "cave_of_dishonour_enter_floor_4_test": (
            RunesOfVirtue2CaveOfDishonourEnterFloor4TestTracker
        ),
        "cave_of_dishonour_exited_test": (
            RunesOfVirtue2CaveOfDishonourExitedTestTracker
        ),
        "city_of_yew_entered_test": RunesOfVirtue2CityOfYewEnteredTestTracker,
        "city_of_yew_welcome_sign_read_test": (
            RunesOfVirtue2CityOfYewWelcomeSignReadTestTracker
        ),
        "mandrake_bard_dialog_test": RunesOfVirtue2MandrakeBardDialogTestTracker,
        "cavern_of_injustice_talk_to_zoltan_floor_4_test": (
            RunesOfVirtue2CavernOfInjusticeTalkToZoltanFloor4TestTracker
        ),
        "cavern_of_injustice_read_hint_floor_5_test": (
            RunesOfVirtue2CavernOfInjusticeReadHintFloor5TestTracker
        ),
        "cavern_of_injustice_talk_to_terry_floor_5_test": (
            RunesOfVirtue2CavernOfInjusticeTalkToTerryFloor5TestTracker
        ),
        "cavern_of_injustice_entered_test": (
            RunesOfVirtue2CavernOfInjusticeEnteredTestTracker
        ),
        "cavern_of_injustice_enter_floor_2_test": (
            RunesOfVirtue2CavernOfInjusticeEnterFloor2TestTracker
        ),
        "cavern_of_injustice_enter_floor_3_test": (
            RunesOfVirtue2CavernOfInjusticeEnterFloor3TestTracker
        ),
        "cavern_of_injustice_enter_floor_4_test": (
            RunesOfVirtue2CavernOfInjusticeEnterFloor4TestTracker
        ),
        "cavern_of_injustice_enter_floor_5_test": (
            RunesOfVirtue2CavernOfInjusticeEnterFloor5TestTracker
        ),
        "cavern_of_injustice_enter_floor_6_test": (
            RunesOfVirtue2CavernOfInjusticeEnterFloor6TestTracker
        ),
        "cavern_of_injustice_enter_floor_7_test": (
            RunesOfVirtue2CavernOfInjusticeEnterFloor7TestTracker
        ),
        "cavern_of_injustice_enter_east_portal_floor_3_test": (
            RunesOfVirtue2CavernOfInjusticeEnterEastPortalFloor3TestTracker
        ),
        "grab_cheese_from_kitchen_test": (
            RunesOfVirtue2GrabCheeseFromKitchenTestTracker
        ),
        "give_cheese_to_sherry_test": RunesOfVirtue2GiveCheeseToSherryTestTracker,
        "climb_ladder_behind_locked_door_test": (
            RunesOfVirtue2ClimbLadderBehindLockedDoorTestTracker
        ),
        "interact_with_map_on_table_test": (
            RunesOfVirtue2InteractWithMapOnTableTestTracker
        ),
        "find_ladder_back_from_castle_test": (
            RunesOfVirtue2FindLadderBackFromCastleTestTracker
        ),
        "unlock_door_and_save_tholden_test": (
            RunesOfVirtue2UnlockDoorAndSaveTholdenTestTracker
        ),
        "find_ladder_out_of_cavern_of_hatred_test": (
            RunesOfVirtue2FindLadderOutOfCavernOfHatredTestTracker
        ),
        "bring_tholden_back_to_king_test": (
            RunesOfVirtue2BringTholdenBackToKingTestTracker
        ),
        "attend_castle_ceremony_test": (
            RunesOfVirtue2AttendCastleCeremonyTestTracker
        ),
        "rune_of_honour_obtained_test": (
            RunesOfVirtue2RuneOfHonourObtainedTestTracker
        ),
        "cavern_of_hatred_gate_1_unlocked_test": (
            RunesOfVirtue2CavernOfHatredGate1UnlockedTestTracker
        ),
        "cavern_of_hatred_ladder_room_2_test": (
            RunesOfVirtue2CavernOfHatredLadderRoom2TestTracker
        ),
        "cavern_of_hatred_ladder_2_test": (
            RunesOfVirtue2CavernOfHatredLadder2TestTracker
        ),
        "cavern_of_hatred_grab_key_test": (
            RunesOfVirtue2CavernOfHatredGrabKeyTestTracker
        ),
        "cavern_of_hatred_enter_floor_4_test": (
            RunesOfVirtue2CavernOfHatredEnterFloor4TestTracker
        ),
        "cavern_of_hatred_enter_floor_5_test": (
            RunesOfVirtue2CavernOfHatredEnterFloor5TestTracker
        ),
        "cavern_of_hatred_enter_floor_6_test": (
            RunesOfVirtue2CavernOfHatredEnterFloor6TestTracker
        ),
        "cavern_of_hatred_enter_floor_7_test": (
            RunesOfVirtue2CavernOfHatredEnterFloor7TestTracker
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
