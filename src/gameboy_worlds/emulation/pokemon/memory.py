import os
from typing import Any, Callable, Dict, List, Optional, Tuple

from gameboy_worlds.emulation.game_memory import (
    GameMemory,
    SignalUnavailable,
    UnsupportedRom,
    bcd as _bcd,
    big_endian as _big_endian,
    bit_indices as _bit_indices,
)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory_data")
TERMINATOR = 0x50
LIST_END = 0xFF
SCREEN_WIDTH = 20
SCREEN_HEIGHT = 18


def _word(high: int, low: int) -> int:
    return (high << 8) | low


def _dvs(first: int, second: int) -> Dict[str, int]:
    attack, defense = first >> 4, first & 0x0F
    speed, special = second >> 4, second & 0x0F
    hp = ((attack & 1) << 3) | ((defense & 1) << 2) | ((speed & 1) << 1) | (special & 1)
    return {"hp": hp, "attack": attack, "defense": defense, "speed": speed, "special": special}


def _status(value: int) -> Dict[str, Any]:
    return {
        "raw": value,
        "asleep_turns": value & 0x07,
        "poisoned": bool(value & 0x08),
        "burned": bool(value & 0x10),
        "frozen": bool(value & 0x20),
        "paralyzed": bool(value & 0x40),
    }


class PokemonMemory(GameMemory):
    DATA_DIR = DATA_DIR
    POKE_TOKEN: str = "POKé"
    UNVERIFIED_MON_FIELDS: Tuple[str, ...] = ()

    def _verified(self, mon: Dict[str, Any]) -> Dict[str, Any]:
        for field in self.UNVERIFIED_MON_FIELDS:
            mon.pop(field, None)
        return mon

    def __init__(self, pyboy):
        super().__init__(pyboy)
        self._charmap = {int(k): v for k, v in self._data["charmap"].items()}
        self._name_cache: Dict[str, Dict[int, str]] = {}

    def decode_text(self, values: List[int], stop_at_terminator: bool = True) -> str:
        characters = []
        for value in values:
            if stop_at_terminator and value == TERMINATOR:
                break
            characters.append(self._charmap.get(value, "?"))
        return "".join(characters)

    def read_text(self, label: str, length: int = 11, offset: int = 0) -> str:
        return self.decode_text(self.read_bytes(label, length, offset))

    def _rom_table(self) -> Dict[str, dict]:
        if self._overlay is not None:
            return self._overlay["names"]
        return self._data["names"]

    def _read_rom(self, bank: int, address: int) -> int:
        while address >= 0x8000:
            address -= 0x4000
            bank += 1
        return self._memory[bank, address]

    def _load_names(self, table: str) -> Dict[int, str]:
        if table in self._name_cache:
            return self._name_cache[table]
        spec = self._rom_table().get(table)
        names: Dict[int, str] = {}
        if spec is not None:
            bank, address = spec["bank"], spec["addr"]
            count = spec["count"]
            first = spec["first_id"]
            for identifier in range(first, first + count):
                if spec["layout"] == "fixed":
                    values = [self._read_rom(bank, address + i) for i in range(spec["stride"])]
                    address += spec["stride"]
                elif spec["layout"] == "length_prefixed":
                    length = self._read_rom(bank, address) - 1
                    values = [self._read_rom(bank, address + 1 + i) for i in range(length)]
                    address += length + 1
                else:
                    values = []
                    while True:
                        value = self._read_rom(bank, address)
                        address += 1
                        if value == TERMINATOR:
                            break
                        values.append(value)
                text = self.decode_text(values).replace("#", self.POKE_TOKEN).strip()
                if text:
                    names[identifier] = text
        self._name_cache[table] = names
        return names

    def species_name(self, species_id: int) -> Optional[str]:
        return self._load_names("species").get(species_id)

    def move_name(self, move_id: int) -> Optional[str]:
        if move_id == 0:
            return None
        return self._load_names("moves").get(move_id)

    def item_name(self, item_id: int) -> Optional[str]:
        if item_id == 0:
            return None
        name = self._load_names("items").get(item_id)
        if name is not None:
            return name
        if self._overlay is None:
            return self._data["items"].get(str(item_id))
        return None

    def _named_type(self, type_id: int) -> Optional[str]:
        if self._overlay is not None:
            return None
        return self._data["types"].get(str(type_id))

    def _items_list(self, count_label: str, list_label: str, capacity: int, with_quantity: bool) -> List[dict]:
        count = self.read_byte(count_label)
        stride = 2 if with_quantity else 1
        if count > capacity or self.read_byte(list_label, count * stride) != LIST_END:
            return []
        items = []
        for index in range(count):
            item_id = self.read_byte(list_label, index * stride)
            entry: Dict[str, Any] = {"id": item_id, "name": self.item_name(item_id)}
            if with_quantity:
                entry["quantity"] = self.read_byte(list_label, index * stride + 1)
            items.append(entry)
        return items

    def _moves(self, move_ids: List[int], pp_values: List[int]) -> List[dict]:
        moves = []
        for move_id, pp in zip(move_ids, pp_values):
            if move_id == 0:
                continue
            moves.append(
                {
                    "id": move_id,
                    "name": self.move_name(move_id),
                    "pp": pp & 0x3F,
                    "pp_ups": pp >> 6,
                }
            )
        return moves

    def screen_tiles(self) -> List[List[int]]:
        values = self.read_bytes(self.TILEMAP_LABEL, SCREEN_WIDTH * SCREEN_HEIGHT)
        return [
            values[row * SCREEN_WIDTH : (row + 1) * SCREEN_WIDTH]
            for row in range(SCREEN_HEIGHT)
        ]

    def screen_text(self) -> List[str]:
        lines = []
        for row in self.screen_tiles():
            characters = []
            for tile in row:
                character = self._charmap.get(tile)
                printable = (
                    character is not None
                    and tile >= 0x7F
                    and not character.startswith("<")
                )
                characters.append(character if printable else " ")
            lines.append("".join(characters).rstrip())
        return lines

    def snapshot(self) -> Dict[str, Any]:
        result = {}
        for group, reader in self._signal_groups().items():
            value = reader()
            if value:
                result[group] = value
        return result

    def _signal_groups(self) -> Dict[str, Callable[[], Any]]:
        raise NotImplementedError

    TILEMAP_LABEL = ""

    def _optional(self, target: Dict[str, Any], key: str, labels: Tuple[str, ...], reader: Callable[[], Any]) -> None:
        if self.has(*labels):
            target[key] = reader()

    def _drop_unloaded_battle_mons(self, battle: Dict[str, Any]) -> None:
        for key in ("player_mon", "enemy_mon"):
            if key in battle and battle[key]["species_id"] == 0:
                del battle[key]


class Gen1Memory(PokemonMemory):
    DATA_FILE = "pokered.json"
    TILEMAP_LABEL = "wTileMap"
    PARTY_STRUCT_SIZE = 44
    BOX_STRUCT_SIZE = 33
    BATTLE_STRUCT_SIZE = 29
    NAME_LENGTH = 11
    FACING = {1: "right", 2: "left", 4: "down", 8: "up"}
    WALK_STATES = {0: "walking", 1: "biking", 2: "surfing"}
    BATTLE_MODES = {0: "none", 1: "wild", 2: "trainer", 255: "lost"}
    BADGE_NAMES: Optional[Tuple[str, ...]] = None
    NUM_DEX_BYTES = 19
    CONNECTION_BITS = (("north", 3), ("south", 2), ("west", 1), ("east", 0))

    def _signal_groups(self):
        return {
            "player": self.player,
            "location": self.location,
            "party": self.party,
            "bag": self.bag,
            "pc_items": self.pc_items,
            "current_box": self.current_box,
            "pokedex": self.pokedex,
            "battle": self.battle,
            "ui": self.ui,
            "sprites": self.sprites,
            "warps": self.warps,
            "signs": self.signs,
            "wild_encounters": self.wild_encounters,
            "events_raised": self.events_raised,
            "hidden_objects": self.hidden_objects,
            "progress_flags": self.progress_flags,
        }

    def badges(self) -> Dict[str, Any]:
        mask = self.read_byte("wObtainedBadges")
        result: Dict[str, Any] = {"mask": mask, "count": bin(mask).count("1")}
        if self.BADGE_NAMES is not None:
            result["names"] = [
                name for bit, name in enumerate(self.BADGE_NAMES) if mask & (1 << bit)
            ]
        return result

    def player(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        self._optional(result, "name", ("wPlayerName",), lambda: self.read_text("wPlayerName"))
        self._optional(result, "rival_name", ("wRivalName",), lambda: self.read_text("wRivalName"))
        self._optional(result, "money", ("wPlayerMoney",), lambda: _bcd(self.read_bytes("wPlayerMoney", 3)))
        self._optional(result, "coins", ("wPlayerCoins",), lambda: _bcd(self.read_bytes("wPlayerCoins", 2)))
        self._optional(result, "trainer_id", ("wPlayerID",), lambda: self.read_word("wPlayerID"))
        self._optional(result, "badges", ("wObtainedBadges",), self.badges)
        self._optional(
            result,
            "play_time",
            ("wPlayTimeHours", "wPlayTimeMinutes", "wPlayTimeSeconds", "wPlayTimeFrames"),
            lambda: {
                "hours": self.read_byte("wPlayTimeHours"),
                "minutes": self.read_byte("wPlayTimeMinutes"),
                "seconds": self.read_byte("wPlayTimeSeconds"),
                "frames": self.read_byte("wPlayTimeFrames"),
            },
        )
        self._optional(result, "options_raw", ("wOptions",), lambda: self.read_byte("wOptions"))
        self._optional(result, "safari_steps", ("wSafariSteps",), lambda: self.read_word("wSafariSteps"))
        self._optional(result, "safari_balls", ("wNumSafariBalls",), lambda: self.read_byte("wNumSafariBalls"))
        self._optional(result, "repel_steps", ("wRepelRemainingSteps",), lambda: self.read_byte("wRepelRemainingSteps"))
        self._optional(result, "hall_of_fame_teams", ("wNumHoFTeams",), lambda: self.read_byte("wNumHoFTeams"))
        return result

    def map_name(self, map_id: int) -> Optional[str]:
        if self._overlay is not None:
            return None
        entry = self._data["maps"].get(str(map_id))
        return entry["name"] if entry else None

    def is_map_loaded(self) -> bool:
        return self.read_byte("wCurMapWidth") > 0 and self.read_byte("wCurMapHeight") > 0

    def is_map_settled(self) -> Optional[bool]:
        if self._overlay is not None:
            return None
        expected = self._data["maps"].get(str(self.read_byte("wCurMap")))
        if expected is None or expected["width"] is None:
            return None
        return (self.read_byte("wCurMapWidth"), self.read_byte("wCurMapHeight")) == (expected["width"], expected["height"])

    def connections(self) -> Dict[str, Optional[int]]:
        flags = self.read_byte("wCurMapConnections")
        labels = {
            "north": "wNorthConnectedMap",
            "south": "wSouthConnectedMap",
            "west": "wWestConnectedMap",
            "east": "wEastConnectedMap",
        }
        return {
            direction: self.read_byte(labels[direction]) if flags & (1 << bit) else None
            for direction, bit in self.CONNECTION_BITS
        }

    def location(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.has("wCurMap"):
            map_id = self.read_byte("wCurMap")
            result["map_id"] = map_id
            name = self.map_name(map_id)
            if name is not None:
                result["map_name"] = name
        self._optional(result, "x", ("wXCoord",), lambda: self.read_byte("wXCoord"))
        self._optional(result, "y", ("wYCoord",), lambda: self.read_byte("wYCoord"))
        self._optional(result, "block_x", ("wXBlockCoord",), lambda: self.read_byte("wXBlockCoord"))
        self._optional(result, "block_y", ("wYBlockCoord",), lambda: self.read_byte("wYBlockCoord"))
        self._optional(result, "facing", ("wPlayerDirection",), lambda: self.FACING.get(self.read_byte("wPlayerDirection")))
        self._optional(result, "last_map_id", ("wLastMap",), lambda: self.read_byte("wLastMap"))
        self._optional(result, "tileset", ("wCurMapTileset",), lambda: self.read_byte("wCurMapTileset"))
        self._optional(result, "width_blocks", ("wCurMapWidth",), lambda: self.read_byte("wCurMapWidth"))
        self._optional(result, "height_blocks", ("wCurMapHeight",), lambda: self.read_byte("wCurMapHeight"))
        self._optional(result, "map_loaded", ("wCurMapWidth", "wCurMapHeight"), self.is_map_loaded)
        settled = self.is_map_settled() if self._overlay is None else None
        if settled is not None:
            result["map_settled"] = settled
        self._optional(
            result,
            "movement_mode",
            ("wWalkBikeSurfState",),
            lambda: self.WALK_STATES.get(self.read_byte("wWalkBikeSurfState")),
        )
        self._optional(
            result,
            "connections",
            ("wCurMapConnections", "wNorthConnectedMap", "wSouthConnectedMap", "wWestConnectedMap", "wEastConnectedMap"),
            self.connections,
        )
        return result

    def _decode_party_mon(self, raw: List[int]) -> Dict[str, Any]:
        species = raw[0]
        return {
            "species_id": species,
            "species_name": self.species_name(species),
            "hp": _word(raw[1], raw[2]),
            "max_hp": _word(raw[34], raw[35]),
            "level": raw[33],
            "box_level": raw[3],
            "status": _status(raw[4]),
            "types": [raw[5], raw[6]],
            "type_names": [self._named_type(raw[5]), self._named_type(raw[6])],
            "catch_rate": raw[7],
            "moves": self._moves(raw[8:12], raw[29:33]),
            "original_trainer_id": _word(raw[12], raw[13]),
            "experience": _big_endian(raw[14:17]),
            "stat_exp": {
                "hp": _word(raw[17], raw[18]),
                "attack": _word(raw[19], raw[20]),
                "defense": _word(raw[21], raw[22]),
                "speed": _word(raw[23], raw[24]),
                "special": _word(raw[25], raw[26]),
            },
            "dvs": _dvs(raw[27], raw[28]),
            "stats": {
                "attack": _word(raw[36], raw[37]),
                "defense": _word(raw[38], raw[39]),
                "speed": _word(raw[40], raw[41]),
                "special": _word(raw[42], raw[43]),
            },
        }

    def _decode_box_mon(self, raw: List[int]) -> Dict[str, Any]:
        species = raw[0]
        return {
            "species_id": species,
            "species_name": self.species_name(species),
            "hp": _word(raw[1], raw[2]),
            "level": raw[3],
            "status": _status(raw[4]),
            "types": [raw[5], raw[6]],
            "moves": self._moves(raw[8:12], raw[29:33]),
            "original_trainer_id": _word(raw[12], raw[13]),
            "experience": _big_endian(raw[14:17]),
            "dvs": _dvs(raw[27], raw[28]),
        }

    def _roster(self, count_label: str, mons_label: str, ot_label: str, nick_label: str, capacity: int, size: int, decode: Callable) -> List[dict]:
        count = self.read_byte(count_label)
        if count > capacity:
            return []
        members = []
        for slot in range(count):
            mon = self._verified(decode(self.read_bytes(mons_label, size, slot * size)))
            mon["slot"] = slot
            mon["nickname"] = self.read_text(nick_label, self.NAME_LENGTH, slot * self.NAME_LENGTH)
            mon["original_trainer"] = self.read_text(ot_label, self.NAME_LENGTH, slot * self.NAME_LENGTH)
            members.append(mon)
        return members

    def party(self) -> List[dict]:
        if not self.has("wPartyCount", "wPartyMons", "wPartyMonOT", "wPartyMonNicks"):
            return []
        return self._roster("wPartyCount", "wPartyMons", "wPartyMonOT", "wPartyMonNicks", 6, self.PARTY_STRUCT_SIZE, self._decode_party_mon)

    def current_box(self) -> Dict[str, Any]:
        if not self.has("wBoxCount", "wBoxMons", "wBoxMonOT", "wBoxMonNicks"):
            return {}
        return {
            "box_number": self.read_byte("wCurrentBoxNum") & 0x7F if self.has("wCurrentBoxNum") else None,
            "mons": self._roster("wBoxCount", "wBoxMons", "wBoxMonOT", "wBoxMonNicks", 20, self.BOX_STRUCT_SIZE, self._decode_box_mon),
        }

    def bag(self) -> List[dict]:
        if not self.has("wNumBagItems", "wBagItems"):
            return []
        return self._items_list("wNumBagItems", "wBagItems", 20, True)

    def pc_items(self) -> List[dict]:
        if not self.has("wNumBoxItems", "wBoxItems"):
            return []
        return self._items_list("wNumBoxItems", "wBoxItems", 50, True)

    def _species_by_dex(self) -> Dict[int, int]:
        cached = getattr(self, "_dex_cache", None)
        if cached is None:
            bank, address = self._data["pokedex_order"]
            cached = {}
            for species in range(1, 191):
                dex = self._read_rom(bank, address + species - 1)
                if dex:
                    cached[dex] = species
            self._dex_cache = cached
        return cached

    def pokedex(self) -> Dict[str, Any]:
        if not self.has("wPokedexOwned", "wPokedexSeen"):
            return {}
        table = self._species_by_dex()

        def entries(label):
            numbers = [index + 1 for index in _bit_indices(self.read_bytes(label, self.NUM_DEX_BYTES))]
            return [
                {"dex": number, "species_name": self.species_name(table.get(number, 0))}
                for number in numbers
            ]

        owned = entries("wPokedexOwned")
        seen = entries("wPokedexSeen")
        return {"owned_count": len(owned), "seen_count": len(seen), "owned": owned, "seen": seen}

    def _decode_battle_mon(self, raw: List[int]) -> Dict[str, Any]:
        species = raw[0]
        return {
            "species_id": species,
            "species_name": self.species_name(species),
            "hp": _word(raw[1], raw[2]),
            "max_hp": _word(raw[15], raw[16]),
            "level": raw[14],
            "status": _status(raw[4]),
            "types": [raw[5], raw[6]],
            "type_names": [self._named_type(raw[5]), self._named_type(raw[6])],
            "catch_rate": raw[7],
            "moves": self._moves(raw[8:12], raw[25:29]),
            "dvs": _dvs(raw[12], raw[13]),
            "stats": {
                "attack": _word(raw[17], raw[18]),
                "defense": _word(raw[19], raw[20]),
                "speed": _word(raw[21], raw[22]),
                "special": _word(raw[23], raw[24]),
            },
        }

    def _stat_mods(self, label: str) -> Dict[str, int]:
        names = ("attack", "defense", "speed", "special", "accuracy", "evasion")
        return {name: value - 7 for name, value in zip(names, self.read_bytes(label, 6))}

    def is_in_battle(self) -> bool:
        return self.read_byte("wIsInBattle") in (1, 2)

    def battle(self) -> Dict[str, Any]:
        if not self.has("wIsInBattle"):
            return {}
        raw_mode = self.read_byte("wIsInBattle")
        result: Dict[str, Any] = {"mode": self.BATTLE_MODES.get(raw_mode, raw_mode)}
        if raw_mode not in (1, 2):
            return result
        self._optional(result, "battle_type", ("wBattleType",), lambda: self.read_byte("wBattleType"))
        self._optional(result, "player_mon", ("wBattleMon", "wBattleMonNick"), lambda: dict(self._verified(self._decode_battle_mon(self.read_bytes("wBattleMon", self.BATTLE_STRUCT_SIZE))), nickname=self.read_text("wBattleMonNick")))
        self._optional(result, "enemy_mon", ("wEnemyMon", "wEnemyMonNick"), lambda: dict(self._verified(self._decode_battle_mon(self.read_bytes("wEnemyMon", self.BATTLE_STRUCT_SIZE))), nickname=self.read_text("wEnemyMonNick")))
        self._drop_unloaded_battle_mons(result)
        self._optional(result, "player_stat_mods", ("wPlayerMonAttackMod",), lambda: self._stat_mods("wPlayerMonAttackMod"))
        self._optional(result, "enemy_stat_mods", ("wEnemyMonAttackMod",), lambda: self._stat_mods("wEnemyMonAttackMod"))
        self._optional(result, "player_battle_status", ("wPlayerBattleStatus1",), lambda: self.read_bytes("wPlayerBattleStatus1", 3))
        self._optional(result, "enemy_battle_status", ("wEnemyBattleStatus1",), lambda: self.read_bytes("wEnemyBattleStatus1", 3))
        self._optional(result, "player_substitute_hp", ("wPlayerSubstituteHP",), lambda: self.read_byte("wPlayerSubstituteHP"))
        self._optional(result, "enemy_substitute_hp", ("wEnemySubstituteHP",), lambda: self.read_byte("wEnemySubstituteHP"))
        self._optional(result, "player_move_id", ("wPlayerSelectedMove",), lambda: self.read_byte("wPlayerSelectedMove"))
        self._optional(result, "enemy_move_id", ("wEnemySelectedMove",), lambda: self.read_byte("wEnemySelectedMove"))
        self._optional(result, "run_attempts", ("wNumRunAttempts",), lambda: self.read_byte("wNumRunAttempts"))
        if raw_mode == 2:
            self._optional(result, "trainer_class", ("wTrainerClass",), self._trainer_class)
            self._optional(result, "trainer_number", ("wTrainerNo",), lambda: self.read_byte("wTrainerNo"))
            self._optional(result, "enemy_party_species", ("wEnemyPartyCount", "wEnemyPartySpecies"), self._enemy_party_species)
        return result

    def _trainer_class(self) -> Dict[str, Any]:
        class_id = self.read_byte("wTrainerClass")
        name = None
        if self._overlay is None:
            name = self._data["trainer_classes"].get(str(class_id))
        return {"id": class_id, "name": name}

    def _enemy_party_species(self) -> List[dict]:
        count = self.read_byte("wEnemyPartyCount")
        if count > 6:
            return []
        return [
            {"species_id": species, "species_name": self.species_name(species)}
            for species in self.read_bytes("wEnemyPartySpecies", count)
        ]

    def ui(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        self._optional(result, "menu_cursor", ("wCurrentMenuItem",), lambda: self.read_byte("wCurrentMenuItem"))
        self._optional(result, "menu_max_item", ("wMaxMenuItem",), lambda: self.read_byte("wMaxMenuItem"))
        self._optional(result, "menu_top_x", ("wTopMenuItemX",), lambda: self.read_byte("wTopMenuItemX"))
        self._optional(result, "menu_top_y", ("wTopMenuItemY",), lambda: self.read_byte("wTopMenuItemY"))
        self._optional(result, "text_box_id", ("wTextBoxID",), lambda: self.read_byte("wTextBoxID"))
        self._optional(result, "joypad_held", ("hJoyHeld",), lambda: self.read_byte("hJoyHeld"))
        self._optional(result, "joypad_pressed", ("hJoyPressed",), lambda: self.read_byte("hJoyPressed"))
        self._optional(result, "map_music_id", ("wMapMusicSoundID",), lambda: self.read_byte("wMapMusicSoundID"))
        self._optional(result, "last_music_id", ("wLastMusicSoundID",), lambda: self.read_byte("wLastMusicSoundID"))
        return result

    def sprites(self) -> List[dict]:
        if not self.has("wSpriteStateData1", "wSpriteStateData2"):
            return []
        sprites = []
        for index in range(16):
            first = self.read_bytes("wSpriteStateData1", 16, index * 16)
            if first[0] == 0:
                continue
            second = self.read_bytes("wSpriteStateData2", 16, index * 16)
            sprites.append(
                {
                    "index": index,
                    "picture_id": first[0],
                    "movement_status": first[1],
                    "screen_y": first[4],
                    "screen_x": first[6],
                    "facing_raw": first[9],
                    "map_y": second[4] - 4 if index else None,
                    "map_x": second[5] - 4 if index else None,
                }
            )
        return sprites

    def warps(self) -> List[dict]:
        if not self.has("wNumberOfWarps", "wWarpEntries"):
            return []
        count = self.read_byte("wNumberOfWarps")
        if count > 32:
            return []
        warps = []
        for index in range(count):
            y, x, warp_id, destination = self.read_bytes("wWarpEntries", 4, index * 4)
            warps.append({"x": x, "y": y, "destination_warp": warp_id, "destination_map_id": destination})
        return warps

    def signs(self) -> List[dict]:
        if not self.has("wNumSigns", "wSignCoords"):
            return []
        count = self.read_byte("wNumSigns")
        if count > 16:
            return []
        signs = []
        for index in range(count):
            y, x = self.read_bytes("wSignCoords", 2, index * 2)
            signs.append({"x": x, "y": y})
        return signs

    def wild_encounters(self) -> Dict[str, Any]:
        if not self.has("wGrassRate", "wGrassMons", "wWaterRate", "wWaterMons"):
            return {}

        def table(label):
            values = self.read_bytes(label, 20)
            return [
                {"level": values[index], "species_id": values[index + 1], "species_name": self.species_name(values[index + 1])}
                for index in range(0, 20, 2)
            ]

        result: Dict[str, Any] = {
            "grass_rate": self.read_byte("wGrassRate"),
            "water_rate": self.read_byte("wWaterRate"),
        }
        if result["grass_rate"]:
            result["grass"] = table("wGrassMons")
        if result["water_rate"]:
            result["water"] = table("wWaterMons")
        return result

    def event(self, name: str) -> bool:
        if self._overlay is not None:
            raise SignalUnavailable(f"event names are not mapped for {type(self).__name__}")
        return self.read_flag("wEventFlags", self._data["events"][name])

    def event_bits(self) -> List[int]:
        return _bit_indices(self.read_bytes("wEventFlags", 320))

    def events_raised(self) -> List[str]:
        if self._overlay is not None or not self.has("wEventFlags"):
            return []
        names = {index: name for name, index in self._data["events"].items()}
        return sorted(names[bit] for bit in self.event_bits() if bit in names)

    def hidden_objects(self) -> List[str]:
        if self._overlay is not None or not self.has("wToggleableObjectFlags"):
            return []
        names = {index: name for name, index in self._data["toggles"].items()}
        bits = _bit_indices(self.read_bytes("wToggleableObjectFlags", 32))
        return sorted(names[bit] for bit in bits if bit in names)

    def progress_flags(self) -> Dict[str, int]:
        labels = (
            "wStatusFlags1", "wBeatGymFlags", "wStatusFlags2", "wStatusFlags3", "wStatusFlags4",
            "wStatusFlags5", "wStatusFlags6", "wStatusFlags7", "wElite4Flags", "wMovementFlags",
            "wTownVisitedFlag", "wCompletedInGameTradeFlags", "wObtainedHiddenItemsFlags", "wObtainedHiddenCoinsFlags",
        )
        return {label: self.read_word(label) if label in ("wTownVisitedFlag", "wCompletedInGameTradeFlags") else self.read_byte(label) for label in labels if self.has(label)}


class PokemonRedMemory(Gen1Memory):
    ROM_TITLE = b"POKEMON RED"
    ROM_GLOBAL_CHECKSUM = 0x91E6
    BADGE_NAMES = ("boulder", "cascade", "thunder", "rainbow", "soul", "marsh", "volcano", "earth")
    NUM_STORED_BOXES = 12
    STORED_BOX_SIZE = 0x462

    def _signal_groups(self):
        groups = super()._signal_groups()
        groups["stored_boxes"] = self.stored_boxes
        return groups

    def stored_boxes(self) -> List[dict]:
        boxes = []
        for number in range(self.NUM_STORED_BOXES):
            bank, base, _ = self.symbol_info("sBox1" if number < 6 else "sBox7")
            start = base + (number % 6) * self.STORED_BOX_SIZE
            count = self._read(bank, start)
            species = []
            if count <= 20:
                species = [self._read(bank, start + 1 + index) for index in range(count)]
            boxes.append(
                {
                    "box_number": number,
                    "count": count if count <= 20 else None,
                    "species": [
                        {"species_id": value, "species_name": self.species_name(value)}
                        for value in species
                    ],
                }
            )
        return boxes


class PokemonBrownMemory(Gen1Memory):
    OVERLAY_FILE = "pokemon_brown.json"
    ROM_TITLE = b"POKEMON BROWN"
    ROM_GLOBAL_CHECKSUM = 0xEF95
    UNVERIFIED_MON_FIELDS = ("dvs", "stat_exp", "catch_rate", "box_level", "type_names")


class Gen2Memory(PokemonMemory):
    DATA_FILE = "pokecrystal.json"
    TILEMAP_LABEL = "wTilemap"
    PARTY_STRUCT_SIZE = 48
    BOX_STRUCT_SIZE = 32
    BATTLE_STRUCT_SIZE = 32
    NAME_LENGTH = 11
    EGG_SPECIES = 253
    NUM_ITEMS_CAPACITY = 20
    NUM_KEY_ITEMS_CAPACITY = 25
    NUM_BALLS_CAPACITY = 12
    FACING = {0: "down", 1: "up", 2: "left", 3: "right"}
    TIME_OF_DAY = {0: "morning", 1: "day", 2: "night", 3: "darkness"}
    BATTLE_MODES = {0: "none", 1: "wild", 2: "trainer"}
    PLAYER_STATES = {0: "normal", 1: "biking", 4: "surfing", 8: "surfing_pikachu"}
    JOHTO_BADGES = ("zephyr", "hive", "plain", "fog", "mineral", "storm", "glacier", "rising")
    KANTO_BADGES = ("boulder", "cascade", "thunder", "rainbow", "soul", "marsh", "volcano", "earth")

    def _signal_groups(self):
        return {
            "player": self.player,
            "location": self.location,
            "party": self.party,
            "items": self.items,
            "ball_pocket": self.ball_pocket,
            "key_items": self.key_items,
            "tms_hms": self.tms_hms,
            "pc_items": self.pc_items,
            "current_box": self.current_box,
            "pokedex": self.pokedex,
            "battle": self.battle,
            "ui": self.ui,
            "objects": self.objects,
            "day_care": self.day_care,
            "roamers": self.roamers,
            "phone_contacts": self.phone_contacts,
            "events_raised": self.events_raised,
            "engine_flags_raised": self.engine_flags_raised,
        }

    def player(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for key, label in (("name", "wPlayerName"), ("mom_name", "wMomsName"), ("rival_name", "wRivalName"), ("red_name", "wRedsName"), ("green_name", "wGreensName")):
            self._optional(result, key, (label,), lambda label=label: self.read_text(label))
        self._optional(result, "trainer_id", ("wPlayerID",), lambda: self.read_word("wPlayerID"))
        self._optional(result, "money", ("wMoney",), lambda: _big_endian(self.read_bytes("wMoney", 3)))
        self._optional(result, "mom_money", ("wMomsMoney",), lambda: _big_endian(self.read_bytes("wMomsMoney", 3)))
        self._optional(result, "coins", ("wCoins",), lambda: self.read_word("wCoins"))
        self._optional(result, "badges", ("wJohtoBadges", "wKantoBadges"), self.badges)
        self._optional(result, "status_flags", ("wStatusFlags", "wStatusFlags2"), lambda: [self.read_byte("wStatusFlags"), self.read_byte("wStatusFlags2")])
        self._optional(
            result,
            "game_time",
            ("wGameTimeHours", "wGameTimeMinutes", "wGameTimeSeconds", "wGameTimeFrames"),
            lambda: {
                "hours": self.read_word("wGameTimeHours"),
                "minutes": self.read_byte("wGameTimeMinutes"),
                "seconds": self.read_byte("wGameTimeSeconds"),
                "frames": self.read_byte("wGameTimeFrames"),
            },
        )
        self._optional(result, "current_day", ("wCurDay",), lambda: self.read_byte("wCurDay"))
        self._optional(result, "time_of_day", ("wTimeOfDay",), lambda: self.TIME_OF_DAY.get(self.read_byte("wTimeOfDay")))
        self._optional(result, "rtc_clock", ("hHours", "hMinutes", "hSeconds"), lambda: {"hours": self.read_byte("hHours"), "minutes": self.read_byte("hMinutes"), "seconds": self.read_byte("hSeconds")})
        self._optional(result, "player_state", ("wPlayerState",), lambda: self.PLAYER_STATES.get(self.read_byte("wPlayerState"), self.read_byte("wPlayerState")))
        self._optional(result, "repel_steps", ("wRepelEffect",), lambda: self.read_byte("wRepelEffect"))
        self._optional(result, "hall_of_fame_count", ("wHallOfFameCount",), lambda: self.read_byte("wHallOfFameCount"))
        self._optional(result, "options_raw", ("wOptions",), lambda: self.read_byte("wOptions"))
        return result

    def badges(self) -> Dict[str, Any]:
        johto = self.read_byte("wJohtoBadges")
        kanto = self.read_byte("wKantoBadges")
        return {
            "johto_mask": johto,
            "kanto_mask": kanto,
            "count": bin(johto).count("1") + bin(kanto).count("1"),
            "johto": [name for bit, name in enumerate(self.JOHTO_BADGES) if johto & (1 << bit)],
            "kanto": [name for bit, name in enumerate(self.KANTO_BADGES) if kanto & (1 << bit)],
        }

    def map_name(self, group: int, number: int) -> Optional[str]:
        if self._overlay is not None:
            return None
        entry = self._data["maps"].get(f"{group}:{number}")
        return entry["name"] if entry else None

    def is_map_loaded(self) -> bool:
        return self.read_byte("wMapWidth") > 0 and self.read_byte("wMapHeight") > 0

    def is_map_settled(self) -> Optional[bool]:
        if self._overlay is not None:
            return None
        key = f"{self.read_byte('wMapGroup')}:{self.read_byte('wMapNumber')}"
        expected = self._data["maps"].get(key)
        if expected is None or expected["width"] is None:
            return None
        return (self.read_byte("wMapWidth"), self.read_byte("wMapHeight")) == (expected["width"], expected["height"])

    def location(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.has("wMapGroup", "wMapNumber"):
            group, number = self.read_byte("wMapGroup"), self.read_byte("wMapNumber")
            result["map_group"] = group
            result["map_number"] = number
            name = self.map_name(group, number)
            if name is not None:
                result["map_name"] = name
        self._optional(result, "x", ("wXCoord",), lambda: self.read_byte("wXCoord"))
        self._optional(result, "y", ("wYCoord",), lambda: self.read_byte("wYCoord"))
        self._optional(result, "facing", ("wPlayerDirection",), lambda: self.FACING.get(self.read_byte("wPlayerDirection") >> 2))
        self._optional(result, "tileset", ("wMapTileset",), lambda: self.read_byte("wMapTileset"))
        self._optional(result, "width_blocks", ("wMapWidth",), lambda: self.read_byte("wMapWidth"))
        self._optional(result, "height_blocks", ("wMapHeight",), lambda: self.read_byte("wMapHeight"))
        self._optional(result, "map_loaded", ("wMapWidth", "wMapHeight"), self.is_map_loaded)
        settled = self.is_map_settled() if self._overlay is None else None
        if settled is not None:
            result["map_settled"] = settled
        self._optional(result, "warp_number", ("wWarpNumber",), lambda: self.read_byte("wWarpNumber"))
        self._optional(result, "last_spawn_map", ("wLastSpawnMapGroup", "wLastSpawnMapNumber"), lambda: [self.read_byte("wLastSpawnMapGroup"), self.read_byte("wLastSpawnMapNumber")])
        self._optional(result, "visited_spawns_raw", ("wVisitedSpawns",), lambda: self.read_bytes("wVisitedSpawns", 4))
        return result

    def _landmark(self, value: int) -> Optional[str]:
        if self._overlay is not None:
            return None
        return self._data["landmarks"].get(str(value))

    def _decode_box_fields(self, raw: List[int]) -> Dict[str, Any]:
        species = raw[0]
        item = raw[1]
        return {
            "species_id": species,
            "species_name": self.species_name(species),
            "held_item_id": item,
            "held_item_name": self.item_name(item),
            "moves": self._moves(raw[2:6], raw[23:27]),
            "original_trainer_id": _word(raw[6], raw[7]),
            "experience": _big_endian(raw[8:11]),
            "stat_exp": {
                "hp": _word(raw[11], raw[12]),
                "attack": _word(raw[13], raw[14]),
                "defense": _word(raw[15], raw[16]),
                "speed": _word(raw[17], raw[18]),
                "special": _word(raw[19], raw[20]),
            },
            "dvs": _dvs(raw[21], raw[22]),
            "happiness": raw[27],
            "pokerus": raw[28],
            "caught_data_raw": [raw[29], raw[30]],
            "caught_level": raw[29] & 0x3F,
            "caught_time_raw": raw[29] >> 6,
            "caught_location_id": raw[30] & 0x7F,
            "caught_location": self._landmark(raw[30] & 0x7F),
            "level": raw[31],
        }

    def _decode_party_mon(self, raw: List[int]) -> Dict[str, Any]:
        mon = self._decode_box_fields(raw[:32])
        mon.update(
            {
                "status": _status(raw[32]),
                "hp": _word(raw[34], raw[35]),
                "max_hp": _word(raw[36], raw[37]),
                "stats": {
                    "attack": _word(raw[38], raw[39]),
                    "defense": _word(raw[40], raw[41]),
                    "speed": _word(raw[42], raw[43]),
                    "special_attack": _word(raw[44], raw[45]),
                    "special_defense": _word(raw[46], raw[47]),
                },
            }
        )
        return mon

    def party(self) -> List[dict]:
        if not self.has("wPartyCount", "wPartySpecies", "wPartyMons", "wPartyMonOTs", "wPartyMonNicknames"):
            return []
        count = self.read_byte("wPartyCount")
        if count > 6:
            return []
        listed = self.read_bytes("wPartySpecies", count)
        members = []
        for slot in range(count):
            mon = self._verified(self._decode_party_mon(self.read_bytes("wPartyMons", self.PARTY_STRUCT_SIZE, slot * self.PARTY_STRUCT_SIZE)))
            mon["slot"] = slot
            mon["is_egg"] = listed[slot] == self.EGG_SPECIES
            mon["nickname"] = self.read_text("wPartyMonNicknames", self.NAME_LENGTH, slot * self.NAME_LENGTH)
            mon["original_trainer"] = self.read_text("wPartyMonOTs", self.NAME_LENGTH, slot * self.NAME_LENGTH)
            members.append(mon)
        return members

    def items(self) -> List[dict]:
        if not self.has("wNumItems", "wItems"):
            return []
        return self._items_list("wNumItems", "wItems", self.NUM_ITEMS_CAPACITY, True)

    def ball_pocket(self) -> List[dict]:
        if not self.has("wNumBalls", "wBalls"):
            return []
        return self._items_list("wNumBalls", "wBalls", self.NUM_BALLS_CAPACITY, True)

    def key_items(self) -> List[dict]:
        if not self.has("wNumKeyItems", "wKeyItems"):
            return []
        return self._items_list("wNumKeyItems", "wKeyItems", self.NUM_KEY_ITEMS_CAPACITY, False)

    def pc_items(self) -> List[dict]:
        if not self.has("wNumPCItems", "wPCItems"):
            return []
        return self._items_list("wNumPCItems", "wPCItems", 50, True)

    def tms_hms(self) -> List[dict]:
        if not self.has("wTMsHMs"):
            return []
        entries = []
        names = {int(key): value for key, value in self._data["items"].items()}
        machines = sorted(identifier for identifier, name in names.items() if name.startswith(("TM_", "HM_")))
        for index, quantity in enumerate(self.read_bytes("wTMsHMs", 57)):
            if quantity and index < len(machines):
                identifier = machines[index]
                entries.append({"id": identifier, "name": self.item_name(identifier), "quantity": quantity})
        return entries

    def current_box(self) -> Dict[str, Any]:
        if not self.has("sBoxCount", "sBoxSpecies", "sBoxMons", "sBoxMonOTs", "sBoxMonNicknames"):
            return {}
        count = self.read_byte("sBoxCount")
        result: Dict[str, Any] = {"box_number": self.read_byte("wCurBox") if self.has("wCurBox") else None, "mons": []}
        if count > 20:
            return result
        for slot in range(count):
            mon = self._decode_box_fields(self.read_bytes("sBoxMons", self.BOX_STRUCT_SIZE, slot * self.BOX_STRUCT_SIZE))
            mon["slot"] = slot
            mon["nickname"] = self.read_text("sBoxMonNicknames", self.NAME_LENGTH, slot * self.NAME_LENGTH)
            mon["original_trainer"] = self.read_text("sBoxMonOTs", self.NAME_LENGTH, slot * self.NAME_LENGTH)
            result["mons"].append(mon)
        return result

    def pokedex(self) -> Dict[str, Any]:
        if not self.has("wPokedexCaught", "wPokedexSeen"):
            return {}

        def entries(label):
            return [
                {"species_id": index + 1, "species_name": self.species_name(index + 1)}
                for index in _bit_indices(self.read_bytes(label, 32))
            ]

        owned = entries("wPokedexCaught")
        seen = entries("wPokedexSeen")
        return {"owned_count": len(owned), "seen_count": len(seen), "owned": owned, "seen": seen}

    def _decode_battle_mon(self, raw: List[int]) -> Dict[str, Any]:
        species = raw[0]
        return {
            "species_id": species,
            "species_name": self.species_name(species),
            "held_item_id": raw[1],
            "held_item_name": self.item_name(raw[1]),
            "moves": self._moves(raw[2:6], raw[8:12]),
            "dvs": _dvs(raw[6], raw[7]),
            "happiness": raw[12],
            "level": raw[13],
            "status": _status(raw[14]),
            "hp": _word(raw[16], raw[17]),
            "max_hp": _word(raw[18], raw[19]),
            "stats": {
                "attack": _word(raw[20], raw[21]),
                "defense": _word(raw[22], raw[23]),
                "speed": _word(raw[24], raw[25]),
                "special_attack": _word(raw[26], raw[27]),
                "special_defense": _word(raw[28], raw[29]),
            },
            "types": [raw[30], raw[31]],
            "type_names": [self._named_type(raw[30]), self._named_type(raw[31])],
        }

    def _stat_levels(self, label: str) -> Dict[str, int]:
        names = ("attack", "defense", "speed", "special_attack", "special_defense", "accuracy", "evasion")
        return {name: value - 7 for name, value in zip(names, self.read_bytes(label, 7))}

    def is_in_battle(self) -> bool:
        return self.read_byte("wBattleMode") in (1, 2)

    def battle(self) -> Dict[str, Any]:
        if not self.has("wBattleMode"):
            return {}
        raw_mode = self.read_byte("wBattleMode")
        result: Dict[str, Any] = {"mode": self.BATTLE_MODES.get(raw_mode, raw_mode)}
        if raw_mode not in (1, 2):
            return result
        self._optional(result, "battle_type", ("wBattleType",), lambda: self.read_byte("wBattleType"))
        self._optional(result, "player_mon", ("wBattleMon", "wBattleMonNickname"), lambda: dict(self._verified(self._decode_battle_mon(self.read_bytes("wBattleMon", self.BATTLE_STRUCT_SIZE))), nickname=self.read_text("wBattleMonNickname")))
        self._optional(result, "enemy_mon", ("wEnemyMon", "wEnemyMonNickname"), lambda: dict(self._verified(self._decode_battle_mon(self.read_bytes("wEnemyMon", self.BATTLE_STRUCT_SIZE))), nickname=self.read_text("wEnemyMonNickname")))
        self._drop_unloaded_battle_mons(result)
        self._optional(result, "player_stat_levels", ("wPlayerStatLevels",), lambda: self._stat_levels("wPlayerStatLevels"))
        self._optional(result, "enemy_stat_levels", ("wEnemyStatLevels",), lambda: self._stat_levels("wEnemyStatLevels"))
        self._optional(result, "player_substatus", ("wPlayerSubStatus1",), lambda: self.read_bytes("wPlayerSubStatus1", 5))
        self._optional(result, "enemy_substatus", ("wEnemySubStatus1",), lambda: self.read_bytes("wEnemySubStatus1", 5))
        self._optional(result, "active_party_slot", ("wCurBattleMon",), lambda: self.read_byte("wCurBattleMon"))
        if raw_mode == 2:
            self._optional(result, "trainer_class", ("wOtherTrainerClass",), self._trainer_class)
            self._optional(result, "enemy_party_species", ("wOTPartyCount", "wOTPartySpecies"), self._enemy_party_species)
        return result

    def _trainer_class(self) -> Dict[str, Any]:
        class_id = self.read_byte("wOtherTrainerClass")
        name = None
        if self._overlay is None:
            name = self._data["trainer_classes"].get(str(class_id))
        return {"id": class_id, "name": name}

    def _enemy_party_species(self) -> List[dict]:
        count = self.read_byte("wOTPartyCount")
        if count > 6:
            return []
        return [
            {"species_id": species, "species_name": self.species_name(species)}
            for species in self.read_bytes("wOTPartySpecies", count)
        ]

    def ui(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        self._optional(result, "menu_cursor", ("wMenuCursorY",), lambda: self.read_byte("wMenuCursorY"))
        self._optional(result, "joypad_held", ("hJoyDown",), lambda: self.read_byte("hJoyDown"))
        self._optional(result, "joypad_pressed", ("hJoyPressed",), lambda: self.read_byte("hJoyPressed"))
        self._optional(result, "in_menu", ("hInMenu",), lambda: self.read_byte("hInMenu"))
        self._optional(result, "script_running", ("wScriptRunning",), lambda: self.read_byte("wScriptRunning"))
        self._optional(result, "map_music_id", ("wMapMusic",), lambda: self.read_byte("wMapMusic"))
        return result

    def objects(self) -> List[dict]:
        if not self.has("wObjectStructs"):
            return []
        length = 40
        objects = []
        for index in range(13):
            raw = self.read_bytes("wObjectStructs", length, index * length)
            if raw[0] == 0:
                continue
            objects.append(
                {
                    "index": index,
                    "sprite": raw[0],
                    "map_object_index": raw[1],
                    "movement_type": raw[3],
                    "facing": self.FACING.get(raw[8] >> 2),
                    "map_x": raw[16] - 4,
                    "map_y": raw[17] - 4,
                    "screen_x": raw[23],
                    "screen_y": raw[24],
                }
            )
        return objects

    def _breed_mon(self, prefix: str) -> Optional[Dict[str, Any]]:
        species = self.read_byte(f"{prefix}Species")
        if species == 0:
            return None
        return {
            "species_id": species,
            "species_name": self.species_name(species),
            "level": self.read_byte(f"{prefix}Level"),
            "nickname": self.read_text(f"{prefix}Nickname"),
        }

    def day_care(self) -> Dict[str, Any]:
        if not self.has("wDayCareMan", "wDayCareLady", "wBreedMon1Species", "wBreedMon2Species", "wBreedMon1Level", "wBreedMon2Level", "wBreedMon1Nickname", "wBreedMon2Nickname"):
            return {}
        man, lady = self.read_byte("wDayCareMan"), self.read_byte("wDayCareLady")
        result: Dict[str, Any] = {"man_raw": man, "lady_raw": lady}
        if man & 1:
            result["man_mon"] = self._breed_mon("wBreedMon1")
        if lady & 1:
            result["lady_mon"] = self._breed_mon("wBreedMon2")
        return result

    def roamers(self) -> List[dict]:
        if not self.has("wRoamMon1Species", "wRoamMon1Level", "wRoamMon1MapGroup", "wRoamMon1MapNumber", "wRoamMon1HP"):
            return []
        roamers = []
        for index in (1, 2, 3):
            species = self.read_byte(f"wRoamMon{index}Species")
            if species == 0:
                continue
            group = self.read_byte(f"wRoamMon{index}MapGroup")
            number = self.read_byte(f"wRoamMon{index}MapNumber")
            roamers.append(
                {
                    "species_id": species,
                    "species_name": self.species_name(species),
                    "level": self.read_byte(f"wRoamMon{index}Level"),
                    "map_group": group,
                    "map_number": number,
                    "map_name": self.map_name(group, number),
                    "hp": self.read_byte(f"wRoamMon{index}HP"),
                }
            )
        return roamers

    def phone_contacts(self) -> List[int]:
        if not self.has("wPhoneList"):
            return []
        return [value for value in self.read_bytes("wPhoneList", 10) if value]

    def event(self, name: str) -> bool:
        if self._overlay is not None:
            raise SignalUnavailable(f"event names are not mapped for {type(self).__name__}")
        return self.read_flag("wEventFlags", self._data["events"][name])

    def events_raised(self) -> List[str]:
        if self._overlay is not None or not self.has("wEventFlags"):
            return []
        names = {index: name for name, index in self._data["events"].items()}
        raised = _bit_indices(self.read_bytes("wEventFlags", 256))
        return sorted(names[bit] for bit in raised if bit in names)

    def engine_flag(self, name: str) -> bool:
        if self._overlay is not None:
            raise SignalUnavailable(f"engine flags are not mapped for {type(self).__name__}")
        bank, address, bit = self._data["engine_flags"][name]
        return bool(self._read(bank, address) & (1 << bit))

    def engine_flags_raised(self) -> List[str]:
        if self._overlay is not None:
            return []
        return sorted(name for name in self._data["engine_flags"] if self.engine_flag(name))


class PokemonCrystalMemory(Gen2Memory):
    ROM_TITLE = b"PM_CRYSTAL"
    ROM_GLOBAL_CHECKSUM = 0x18D2


class PokemonPrismMemory(Gen2Memory):
    OVERLAY_FILE = "pokemon_prism.json"
    ROM_TITLE = b"PM_PRISM"
    ROM_GLOBAL_CHECKSUM = 0x78E6
    POKE_TOKEN = "Poké"
    UNVERIFIED_MON_FIELDS = (
        "dvs",
        "stat_exp",
        "happiness",
        "pokerus",
        "caught_data_raw",
        "caught_level",
        "caught_time_raw",
        "caught_location_id",
        "caught_location",
        "type_names",
    )
    NUM_ITEMS_CAPACITY = 40
    NUM_KEY_ITEMS_CAPACITY = 50
    NUM_BALLS_CAPACITY = 24
