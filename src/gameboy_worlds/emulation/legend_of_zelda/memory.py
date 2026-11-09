import os
from typing import Any, Callable, Dict, List, Optional, Tuple

from gameboy_worlds.emulation.game_memory import (
    GameMemory,
    bcd,
    little_endian,
)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory_data")


class ZeldaMemory(GameMemory):
    DATA_DIR = DATA_DIR

    def _signal_groups(self) -> Dict[str, Callable[[], Any]]:
        return {
            "player": self.player,
            "location": self.location,
            "inventory": self.inventory,
            "ui": self.ui,
        }

    def snapshot(self) -> Dict[str, Any]:
        result = {}
        for group, reader in self._signal_groups().items():
            value = reader()
            if value:
                result[group] = value
        return result

    def is_loaded(self) -> bool:
        return self.max_health_units() > 0

    def max_health_units(self) -> int:
        raise NotImplementedError

    def player(self) -> Dict[str, Any]:
        raise NotImplementedError

    def location(self) -> Dict[str, Any]:
        raise NotImplementedError

    def inventory(self) -> Dict[str, Any]:
        raise NotImplementedError

    def ui(self) -> Dict[str, Any]:
        raise NotImplementedError

    def rooms_visited(self) -> int:
        raise NotImplementedError


class LinksAwakeningMemory(ZeldaMemory):
    DATA_FILE = "links_awakening.json"
    ROM_TITLE = b"ZELDA\x00\x00\x00\x00\x00\x00AZLE"
    ROM_GLOBAL_CHECKSUM = 0x0135
    HEALTH_PER_HEART = 8
    FACING = {0: "right", 1: "left", 2: "up", 3: "down"}
    ROOM_VISITED = 0x80
    GAMEPLAY_WORLD = 11
    GAMEPLAY_INVENTORY = 12
    INVENTORY_SLOTS = 12
    INSTRUMENT_OBTAINED = 0x02

    def max_health_units(self) -> int:
        return self.read_byte("wMaxHearts") * self.HEALTH_PER_HEART

    def rupees(self) -> Optional[int]:
        return bcd([self.read_byte("wRupeeCountHigh"), self.read_byte("wRupeeCountLow")])

    def instruments(self) -> int:
        return sum(
            bool(self.read_byte(f"wHasInstrument{index}") & self.INSTRUMENT_OBTAINED)
            for index in range(1, 9)
        )

    def player(self) -> Dict[str, Any]:
        return {
            "health_units": self.read_byte("wHealth"),
            "max_health_units": self.max_health_units(),
            "hearts": self.read_byte("wHealth") / self.HEALTH_PER_HEART,
            "max_hearts": self.read_byte("wMaxHearts"),
            "heart_pieces": self.read_byte("wHeartPiecesCount"),
            "rupees": self.rupees(),
            "deaths": little_endian(self.read_bytes("wDeathCount", 2)),
            "sword_level": self.read_byte("wSwordLevel"),
            "shield_level": self.read_byte("wShieldLevel"),
            "power_bracelet_level": self.read_byte("wPowerBraceletLevel"),
            "bombs": self.read_byte("wBombCount"),
            "arrows": self.read_byte("wArrowCount"),
            "magic_powder": self.read_byte("wMagicPowderCount"),
            "seashells": self.read_byte("wSeashellsCount"),
            "golden_leaves": self.read_byte("wGoldenLeavesCount"),
            "instruments": self.instruments(),
            "ocarina_songs_mask": self.read_byte("wOcarinaSongFlags"),
            "has_flippers": bool(self.read_byte("wHasFlippers")),
            "has_medicine": bool(self.read_byte("wHasMedicine")),
            "trade_item": self.read_byte("wTradeSequenceItem"),
            "keys": {
                "tail": bool(self.read_byte("wHasTailKey")),
                "angler": bool(self.read_byte("wHasAnglerKey")),
                "face": bool(self.read_byte("wHasFaceKey")),
                "bird": bool(self.read_byte("wHasBirdKey")),
            },
        }

    def location(self) -> Dict[str, Any]:
        return {
            "is_indoor": bool(self.read_byte("wIsIndoor")),
            "map_id": self.read_byte("hMapId"),
            "room": self.read_byte("hMapRoom"),
            "x": self.read_byte("hLinkPositionX"),
            "y": self.read_byte("hLinkPositionY"),
            "facing": self.FACING.get(self.read_byte("hLinkDirection")),
            "loaded": self.is_loaded(),
        }

    def inventory(self) -> Dict[str, Any]:
        names = self._data["inventory_items"]
        slots = self.read_bytes("wInventoryItems", self.INVENTORY_SLOTS)
        items = [names.get(str(value), value) for value in slots if value]
        return {
            "b_slot": names.get(str(slots[0]), slots[0]),
            "a_slot": names.get(str(slots[1]), slots[1]),
            "items": items,
            "item_count": len(items),
        }

    def ui(self) -> Dict[str, Any]:
        return {
            "gameplay_type": self.read_byte("wGameplayType"),
            "gameplay_subtype": self.read_byte("wGameplaySubtype"),
            "dialog_state": self.read_byte("wDialogState"),
            "in_world": self.read_byte("wGameplayType") == self.GAMEPLAY_WORLD,
        }

    def rooms_visited(self) -> int:
        return sum(
            bool(value & self.ROOM_VISITED)
            for label in ("wOverworldRoomStatus", "wIndoorARoomStatus", "wIndoorBRoomStatus")
            for value in self.read_bytes(label, 256)
        )


class OracleOfSeasonsMemory(ZeldaMemory):
    DATA_FILE = "oracle_of_seasons.json"
    ROM_TITLE = b"ZELDA DIN\x00\x00AZ7E"
    ROM_GLOBAL_CHECKSUM = 0xFE8F
    HEALTH_PER_HEART = 4
    FACING = {0: "up", 1: "right", 2: "down", 3: "left"}
    ROOM_VISITED = 0x10
    LINK_DIRECTION_OFFSET = 0x08
    LINK_Y_OFFSET = 0x0B
    LINK_X_OFFSET = 0x0D
    SEASONS = ("spring", "summer", "autumn", "winter")
    ROOM_FLAG_GROUPS = ("wGroup0RoomFlags", "wGroup1RoomFlags", "wGroup4RoomFlags", "wGroup5RoomFlags")

    def max_health_units(self) -> int:
        return self.read_byte("wLinkMaxHealth")

    def rupees(self) -> Optional[int]:
        low, high = self.read_bytes("wNumRupees", 2)
        return bcd([high, low])

    def ore_chunks(self) -> Optional[int]:
        low, high = self.read_bytes("wNumOreChunks", 2)
        return bcd([high, low])

    def play_time_frames(self) -> int:
        return little_endian(self.read_bytes("wPlaytimeCounter", 4))

    def player(self) -> Dict[str, Any]:
        seasons = self.read_byte("wObtainedSeasons")
        essences = self.read_byte("wEssencesObtained")
        return {
            "health_units": self.read_byte("wLinkHealth"),
            "max_health_units": self.max_health_units(),
            "hearts": self.read_byte("wLinkHealth") / self.HEALTH_PER_HEART,
            "max_hearts": self.max_health_units() / self.HEALTH_PER_HEART,
            "heart_pieces": self.read_byte("wNumHeartPieces"),
            "rupees": self.rupees(),
            "ore_chunks": self.ore_chunks(),
            "deaths": bcd(list(reversed(self.read_bytes("wDeathCounter", 2)))),
            "enemies_killed": bcd(list(reversed(self.read_bytes("wTotalEnemiesKilled", 2)))),
            "play_time_frames": self.play_time_frames(),
            "sword_level": self.read_byte("wSwordLevel"),
            "shield_level": self.read_byte("wShieldLevel"),
            "bombs": self.read_byte("wNumBombs"),
            "max_bombs": self.read_byte("wMaxBombs"),
            "satchel_level": self.read_byte("wSeedSatchelLevel"),
            "ember_seeds": self.read_byte("wNumEmberSeeds"),
            "scent_seeds": self.read_byte("wNumScentSeeds"),
            "pegasus_seeds": self.read_byte("wNumPegasusSeeds"),
            "gale_seeds": self.read_byte("wNumGaleSeeds"),
            "mystery_seeds": self.read_byte("wNumMysterySeeds"),
            "gasha_seeds": self.read_byte("wNumGashaSeeds"),
            "seasons": [name for bit, name in enumerate(self.SEASONS) if seasons & (1 << bit)],
            "essence_count": bin(essences).count("1"),
            "essences_mask": essences,
        }

    def location(self) -> Dict[str, Any]:
        return {
            "group": self.read_byte("wActiveGroup"),
            "room": self.read_byte("wActiveRoom"),
            "x": self.read_byte("w1Link", self.LINK_X_OFFSET),
            "y": self.read_byte("w1Link", self.LINK_Y_OFFSET),
            "facing": self.FACING.get(self.read_byte("w1Link", self.LINK_DIRECTION_OFFSET)),
            "loaded": self.is_loaded(),
        }

    def inventory(self) -> Dict[str, Any]:
        storage = [value for value in self.read_bytes("wInventoryStorage", 16) if value]
        treasures = sum(bin(value).count("1") for value in self.read_bytes("wObtainedTreasureFlags", 16))
        return {
            "b_slot": self.read_byte("wInventoryB"),
            "a_slot": self.read_byte("wInventoryA"),
            "storage": storage,
            "item_count": len(storage) + bool(self.read_byte("wInventoryA")) + bool(self.read_byte("wInventoryB")),
            "treasures_obtained": treasures,
        }

    def ui(self) -> Dict[str, Any]:
        return {
            "text_active": self.read_byte("wTextIsActive"),
            "menu_disabled": self.read_byte("wMenuDisabled"),
            "objects_disabled": self.read_byte("wDisabledObjects"),
        }

    def rooms_visited(self) -> int:
        return sum(
            bool(value & self.ROOM_VISITED)
            for label in self.ROOM_FLAG_GROUPS
            for value in self.read_bytes(label, 256)
        )
