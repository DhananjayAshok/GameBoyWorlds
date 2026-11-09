import json
import os
from functools import lru_cache
from typing import Dict, List, Optional, Set, Tuple


class SignalUnavailable(KeyError):
    pass


class UnsupportedRom(ValueError):
    pass


@lru_cache(maxsize=None)
def load_memory_data(path: str) -> dict:
    with open(path) as handle:
        return json.load(handle)


def big_endian(values: List[int]) -> int:
    total = 0
    for value in values:
        total = (total << 8) | value
    return total


def little_endian(values: List[int]) -> int:
    return big_endian(list(reversed(values)))


def bcd(values: List[int]) -> Optional[int]:
    total = 0
    for value in values:
        high, low = value >> 4, value & 0x0F
        if high > 9 or low > 9:
            return None
        total = total * 100 + high * 10 + low
    return total


def bit_indices(values: List[int]) -> List[int]:
    return [
        index * 8 + bit
        for index, value in enumerate(values)
        for bit in range(8)
        if value & (1 << bit)
    ]


class GameMemory:
    DATA_DIR: str = ""
    DATA_FILE: str = ""
    OVERLAY_FILE: Optional[str] = None
    ROM_TITLE: bytes = b""
    ROM_GLOBAL_CHECKSUM: int = 0

    def __init__(self, pyboy):
        self._memory = pyboy.memory
        self._data = load_memory_data(os.path.join(self.DATA_DIR, self.DATA_FILE))
        self._symbols: Dict[str, List[int]] = self._data["symbols"]
        self._overlay = (
            load_memory_data(os.path.join(self.DATA_DIR, self.OVERLAY_FILE))
            if self.OVERLAY_FILE
            else None
        )
        self._allowed: Optional[Set[str]] = None
        if self._overlay is not None:
            self._allowed = set(self._overlay["labels"])
            self._symbols = dict(self._symbols)
            for label, entry in self._overlay["relocated"].items():
                self._symbols[label] = entry["symbol"]
        header = [self._memory[0, address] for address in range(0x134, 0x150)]
        self._cgb = header[0x143 - 0x134] in (0x80, 0xC0)
        self._verify_rom(header)

    def _verify_rom(self, header: List[int]) -> None:
        title = bytes(header[: len(self.ROM_TITLE)])
        checksum = big_endian(header[0x14E - 0x134 : 0x150 - 0x134])
        if title != self.ROM_TITLE or checksum != self.ROM_GLOBAL_CHECKSUM:
            raise UnsupportedRom(
                f"{type(self).__name__} expects title {self.ROM_TITLE!r} with global checksum "
                f"{self.ROM_GLOBAL_CHECKSUM:#06x}, loaded ROM has {title!r} with {checksum:#06x}. "
                "The memory map is only valid for that exact build."
            )

    def has(self, *labels: str) -> bool:
        for label in labels:
            if label not in self._symbols:
                return False
            if self._allowed is not None and label not in self._allowed:
                return False
        return True

    def available_symbols(self) -> List[str]:
        if self._allowed is not None:
            return sorted(self._allowed)
        return sorted(self._symbols)

    def symbol_info(self, label: str) -> Tuple[int, int, int]:
        if not self.has(label):
            raise SignalUnavailable(f"{label} is not mapped for {type(self).__name__}")
        bank, address, size = self._symbols[label]
        return bank, address, size

    def _read(self, bank: int, address: int) -> int:
        if 0xA000 <= address < 0xC000:
            return self._memory[bank, address]
        if self._cgb and 0xC000 <= address < 0xE000:
            if address >= 0xD000 and bank == 0:
                bank = 1
            return self._memory[bank, address]
        return self._memory[address]

    def read_byte(self, label: str, offset: int = 0) -> int:
        bank, address, _ = self.symbol_info(label)
        return self._read(bank, address + offset)

    def read_bytes(self, label: str, length: Optional[int] = None, offset: int = 0) -> List[int]:
        bank, address, size = self.symbol_info(label)
        count = size if length is None else length
        return [self._read(bank, address + offset + index) for index in range(count)]

    def read_word(self, label: str, offset: int = 0) -> int:
        return big_endian(self.read_bytes(label, 2, offset))

    def read_flag(self, label: str, bit: int) -> bool:
        return bool(self.read_byte(label, bit // 8) & (1 << (bit % 8)))
