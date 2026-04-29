from typing import Optional, Union, Type, Dict
from gameboy_worlds.emulation.parser import StateParser
from gameboy_worlds.emulation.tracker import StateTracker
from gameboy_worlds.emulation.emulator import Emulator
from gameboy_worlds.emulation.sword_of_hope.parsers import (
    SwordOfHope1Parser,
    SwordOfHope2Parser,
)
from gameboy_worlds.emulation.sword_of_hope.trackers import (
    SwordOfHopeOCRTracker,
    SwordOfHope1MillRoomTestTracker,
    SwordOfHope1ShamanRoomTestTracker,
    SwordOfHope1DialogueClearTestTracker,
    SwordOfHope1BattleWonTestTracker,
    SwordOfHope1LookItemTestTracker,
    SwordOfHope1BuyItemTestTracker,
    SwordOfHope1OverworldFromDefaultTestTracker,
    SwordOfHope1TalkToNpcTestTracker,
    SwordOfHope1MenuOpenCloseTestTracker,
    SwordOfHope1BattleMagicCommandTestTracker,
    SwordOfHope1CastTeleportTestTracker,
    SwordOfHope1TalkToNpcMultipleTestTracker,
    SwordOfHope1BinaryChoiceSaveTestTracker,
    SwordOfHope1LookSurroundHerbTestTracker,
    SwordOfHope1HitTreantItemTestTracker,
    SwordOfHope1DefeatTreantTestTracker,
    SwordOfHope1HitWallPassageTestTracker,
    SwordOfHope1UseKeyUnlockTestTracker,
    SwordOfHope1CollectScrollGraceTestTracker,
    SwordOfHope1CastGraceAltarTestTracker,
    SwordOfHope1CompleteTeleportTestTracker,
    SwordOfHope1EscapeBattleTestTracker,
    SwordOfHope2DialogueClearTestTracker,
    SwordOfHope2TalkToNpcTestTracker,
    SwordOfHope2MenuOpenCloseTestTracker,
    SwordOfHope2FirstAdjacentRoomTestTracker,
    SwordOfHope2OverworldFromDefaultTestTracker,
)

GAME_TO_GB_NAME = {
    "sword_of_hope_1": "SwordofHope.gb",
    "sword_of_hope_2": "SwordofHope2.gb",
}
""" Expected save name for each game. Save the file to <storage_dir_from_config_file>/<game_name>_rom_data/<gb_name>"""

STRONGEST_PARSERS: Dict[str, Type[StateParser]] = {
    "sword_of_hope_1": SwordOfHope1Parser,
    "sword_of_hope_2": SwordOfHope2Parser,
}
""" Mapping of game names to their corresponding strongest StateParser classes. 
Unless you have a very good reason, you should always use the STRONGEST possible parser for a given game. 
The parser itself does not affect performance, as for it to perform a read / screen comparison operation , it must be called upon by the state tracker.
This means there is never a reason to use a weaker parser. 
"""


AVAILABLE_STATE_TRACKERS: Dict[str, Dict[str, Type[StateTracker]]] = {
    "sword_of_hope_1": {
        "default": SwordOfHopeOCRTracker,
        "mill_room_test": SwordOfHope1MillRoomTestTracker,
        "shaman_room_test": SwordOfHope1ShamanRoomTestTracker,
        "dialogue_clear_test": SwordOfHope1DialogueClearTestTracker,
        "battle_won_test": SwordOfHope1BattleWonTestTracker,
        "look_item_test": SwordOfHope1LookItemTestTracker,
        "buy_item_test": SwordOfHope1BuyItemTestTracker,
        "overworld_from_default_test": SwordOfHope1OverworldFromDefaultTestTracker,
        "talk_to_npc_test": SwordOfHope1TalkToNpcTestTracker,
        "menu_open_close_test": SwordOfHope1MenuOpenCloseTestTracker,
        "battle_magic_command_test": SwordOfHope1BattleMagicCommandTestTracker,
        "cast_teleport_test": SwordOfHope1CastTeleportTestTracker,
        "talk_to_npc_multiple_test": SwordOfHope1TalkToNpcMultipleTestTracker,
        "binary_choice_save_test": SwordOfHope1BinaryChoiceSaveTestTracker,
        "look_surround_herb_test": SwordOfHope1LookSurroundHerbTestTracker,
        "hit_treant_item_test": SwordOfHope1HitTreantItemTestTracker,
        "defeat_treant_test": SwordOfHope1DefeatTreantTestTracker,
        "hit_wall_passage_test": SwordOfHope1HitWallPassageTestTracker,
        "use_key_unlock_test": SwordOfHope1UseKeyUnlockTestTracker,
        "collect_scroll_grace_test": SwordOfHope1CollectScrollGraceTestTracker,
        "cast_grace_altar_test": SwordOfHope1CastGraceAltarTestTracker,
        "complete_teleport_test": SwordOfHope1CompleteTeleportTestTracker,
        "escape_battle_test": SwordOfHope1EscapeBattleTestTracker,
    },
    "sword_of_hope_2": {
        "default": SwordOfHopeOCRTracker,
        "dialogue_clear_test": SwordOfHope2DialogueClearTestTracker,
        "talk_to_npc_test": SwordOfHope2TalkToNpcTestTracker,
        "menu_open_close_test": SwordOfHope2MenuOpenCloseTestTracker,
        "first_adjacent_room_test": SwordOfHope2FirstAdjacentRoomTestTracker,
        "overworld_from_default_test": SwordOfHope2OverworldFromDefaultTestTracker,
    },
}
""" Mapping of game names to their available StateTracker classes with string identifiers. """


AVAILABLE_EMULATORS: Dict[str, Dict[str, Type[Emulator]]] = {
    "sword_of_hope_1": {"default": Emulator},
    "sword_of_hope_2": {"default": Emulator},
}
""" Mapping of game names to their available Emulator classes with string identifiers. """
