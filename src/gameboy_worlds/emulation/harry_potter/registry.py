from typing import Optional, Union, Type, Dict
from gameboy_worlds.emulation.parser import StateParser
from gameboy_worlds.emulation.tracker import StateTracker
from gameboy_worlds.emulation.emulator import Emulator
from gameboy_worlds.emulation.harry_potter.parsers import (
    HarryPotterPhilosophersStoneParser,
    HarryPotterChamberOfSecretsParser,
)
from gameboy_worlds.emulation.harry_potter.trackers import (
    PotionsShopTestTracker,
    EnterOllivandersTestTracker,
    GetWandTestTracker,
    ReceiveFolioMagiTestTracker,
    SelectCardDeckTestTracker,
    EnterGringottsTestTracker,
    TalkHagridGringottsTestTracker,
    GainLevelTestTracker,
    GainSpellTestTracker,
    WinBattleTestTracker,
    BeatBossRatTestTracker,
    HarryPotterOCRTracker,
    FindHagridVaultTestTracker,
    EnterMalkinsTestTracker,
    OpenMalkinsBuyMenuTestTracker,
    SelectRobesTestTracker,
    ConfirmRobesPurchaseTestTracker,
    FindDobbyTestTracker,
    SelectCardDeckCosTestTracker,
    BoardFlyingCarTestTracker,
    EnterBurrowTestTracker,
    EnterBattleCosTestTracker,
)

GAME_TO_GB_NAME = {
    "harry_potter_philosophers_stone": "HarryPotterPhilosophersStone.gbc",
    "harry_potter_chamber_of_secrets": "HarryPotterChamberOfSecrets.gbc",
}
""" Expected save name for each game. Save the file to <storage_dir_from_config_file>/<game_name>_rom_data/<gb_name>"""

STRONGEST_PARSERS: Dict[str, Type[StateParser]] = {
    "harry_potter_philosophers_stone": HarryPotterPhilosophersStoneParser,
    "harry_potter_chamber_of_secrets": HarryPotterChamberOfSecretsParser,
}
""" Mapping of game names to their corresponding strongest StateParser classes.
Unless you have a very good reason, you should always use the STRONGEST possible parser for a given game.
The parser itself does not affect performance, as for it to perform a read / screen comparison operation , it must be called upon by the state tracker.
This means there is never a reason to use a weaker parser.
"""


AVAILABLE_STATE_TRACKERS: Dict[str, Dict[str, Type[StateTracker]]] = {
    "harry_potter_philosophers_stone": {
        "default": StateTracker,
        "ocr": HarryPotterOCRTracker,
        "potions_shop_test": PotionsShopTestTracker,
        "enter_ollivanders_test": EnterOllivandersTestTracker,
        "get_wand_test": GetWandTestTracker,
        "receive_folio_magi_test": ReceiveFolioMagiTestTracker,
        "select_card_deck_test": SelectCardDeckTestTracker,
        "enter_gringotts_test": EnterGringottsTestTracker,
        "talk_hagrid_gringotts_test": TalkHagridGringottsTestTracker,
        "gain_level_test": GainLevelTestTracker,
        "gain_spell_test": GainSpellTestTracker,
        "win_battle_test": WinBattleTestTracker,
        "beat_boss_rat_test": BeatBossRatTestTracker,
        "find_hagrid_vault_test": FindHagridVaultTestTracker,
        "enter_malkins_test": EnterMalkinsTestTracker,
        "open_malkins_buy_menu_test": OpenMalkinsBuyMenuTestTracker,
        "select_robes_test": SelectRobesTestTracker,
        "confirm_robes_purchase_test": ConfirmRobesPurchaseTestTracker,
    },
    "harry_potter_chamber_of_secrets": {
        "default": StateTracker,
        "ocr": HarryPotterOCRTracker,
        "find_dobby_test": FindDobbyTestTracker,
        "select_card_deck_cos_test": SelectCardDeckCosTestTracker,
        "board_flying_car_test": BoardFlyingCarTestTracker,
        "enter_burrow_test": EnterBurrowTestTracker,
        "enter_battle_cos_test": EnterBattleCosTestTracker,
    },
}
""" Mapping of game names to their available StateTracker classes with string identifiers. """


AVAILABLE_EMULATORS: Dict[str, Dict[str, Type[Emulator]]] = {
    "harry_potter_philosophers_stone": {"default": Emulator},
    "harry_potter_chamber_of_secrets": {"default": Emulator},
}
""" Mapping of game names to their available Emulator classes with string identifiers. """
