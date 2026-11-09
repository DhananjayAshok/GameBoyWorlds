import hashlib
import json
import os
import re
import subprocess

import click

GEN1 = "pokered"
GEN2 = "pokecrystal"
ROM_SHA1 = {
    GEN1: "ea9bcae617fdf159b045185467ae58b2e4a48b9a",
    GEN2: "f2f52230b536214ef7c9924f483392993e226cfb",
}
SYM_FILE = {GEN1: "pokered.sym", GEN2: "pokecrystal11.sym"}
ROM_PATH = {
    GEN1: "pokemon_red/PokemonRed.gb",
    GEN2: "pokemon_crystal/PokemonCrystal.gbc",
}
NAME_TABLES = {
    GEN1: {
        "species": ("MonsterNames", "fixed", 10, 190),
        "moves": ("MoveNames", "terminated", None, 165),
        "items": ("ItemNames", "terminated", None, 97),
    },
    GEN2: {
        "species": ("PokemonNames", "fixed", 10, 251),
        "moves": ("MoveNames", "terminated", None, 251),
        "items": ("ItemNames", "terminated", None, 255),
    },
}
SYM_LINE = re.compile(r"^([0-9a-fA-F]{2}):([0-9a-fA-F]{4}) (\S+)")


def region_of(addr):
    if 0xA000 <= addr < 0xC000:
        return "sram", 0xC000
    if 0xC000 <= addr < 0xD000:
        return "wram0", 0xD000
    if 0xD000 <= addr < 0xE000:
        return "wramx", 0xE000
    if 0xFF80 <= addr < 0xFFFF:
        return "hram", 0xFFFF
    return None, None


def parse_symbols(path):
    rom_labels = {}
    labels = {}
    for line in open(path):
        match = SYM_LINE.match(line)
        if not match:
            continue
        bank, addr, label = int(match[1], 16), int(match[2], 16), match[3]
        if "." in label:
            continue
        if addr < 0x8000:
            rom_labels.setdefault(label, (bank, addr))
            continue
        region, _ = region_of(addr)
        if region is not None:
            labels.setdefault(label, (bank, addr))
    starts = {}
    for bank, addr in labels.values():
        region, _ = region_of(addr)
        starts.setdefault((region, bank), set()).add(addr)
    ordered = {key: sorted(value) for key, value in starts.items()}
    symbols = {}
    for label, (bank, addr) in labels.items():
        region, end = region_of(addr)
        addresses = ordered[(region, bank)]
        position = addresses.index(addr)
        following = addresses[position + 1] if position + 1 < len(addresses) else end
        symbols[label] = [bank, addr, following - addr]
    return symbols, rom_labels


class ConstParser:
    def __init__(self):
        self.values = {}
        self.const_value = 0
        self.const_inc = 1
        self.rs = 0
        self.maps = {}
        self.map_group = 0
        self.map_number = 1
        self.trainer_classes = {}
        self.next_trainer_class = 0

    def evaluate(self, expression):
        text = expression.strip()
        text = re.sub(r"\$([0-9a-fA-F]+)", lambda m: str(int(m[1], 16)), text)
        text = re.sub(r"%([01]+)", lambda m: str(int(m[1], 2)), text)
        names = dict(self.values)
        names["const_value"] = self.const_value
        names["_RS"] = self.rs
        try:
            return int(eval(text, {"__builtins__": {}}, names))
        except Exception:
            return None

    def define(self, name):
        self.values[name] = self.const_value
        self.const_value += self.const_inc

    def feed(self, path):
        for raw in open(path):
            line = raw.split(";")[0].strip()
            if not line:
                continue
            parts = line.split(None, 1)
            command, rest = parts[0], parts[1] if len(parts) > 1 else ""
            arguments = [item.strip() for item in rest.split(",")] if rest else []
            if command == "const_def":
                start = self.evaluate(arguments[0]) if arguments else 0
                self.const_value = start if start is not None else 0
                increment = self.evaluate(arguments[1]) if len(arguments) > 1 else 1
                self.const_inc = increment if increment is not None else 1
            elif command == "const":
                self.define(arguments[0])
            elif command == "shift_const":
                self.values[arguments[0]] = 1 << self.const_value
                self.const_value += 1
            elif command == "const_skip":
                amount = self.evaluate(arguments[0]) if arguments else 1
                self.const_value += self.const_inc * (amount or 0)
            elif command == "const_next":
                target = self.evaluate(arguments[0])
                if target is not None:
                    self.const_value = target
            elif command == "rsreset":
                self.rs = 0
            elif command == "add_hm":
                self.define(f"HM_{arguments[0]}")
            elif command == "add_tm":
                self.define(f"TM_{arguments[0]}")
            elif command == "newgroup":
                self.const_value += self.const_inc
                self.map_group = self.const_value
                self.map_number = 1
            elif command == "map_const":
                width = self.evaluate(arguments[1])
                height = self.evaluate(arguments[2])
                if self.map_group:
                    key = f"{self.map_group}:{self.map_number}"
                    self.map_number += 1
                else:
                    key = str(self.const_value)
                    self.const_value += self.const_inc
                self.maps[key] = {"name": arguments[0], "width": width, "height": height}
            elif command == "trainer_const":
                self.trainer_classes[self.const_value] = arguments[0]
                self.define(arguments[0])
            elif command == "trainerclass":
                self.trainer_classes[self.next_trainer_class] = arguments[0]
                self.values[arguments[0]] = self.next_trainer_class
                self.next_trainer_class += 1
                self.const_value = 1
                self.const_inc = 1
            elif command == "DEF":
                match = re.match(r"(\w+)\s+(EQU|=|rb|rw)\s*(.*)$", rest)
                if not match:
                    continue
                name, kind, expression = match[1], match[2], match[3]
                if kind in ("rb", "rw"):
                    self.values[name] = self.rs
                    self.rs += 2 if kind == "rw" else (self.evaluate(expression) or 1)
                else:
                    value = self.evaluate(expression)
                    if value is not None:
                        self.values[name] = value


def parse_charmap(path):
    charmap = {}
    for line in open(path, encoding="utf-8"):
        match = re.match(r'\s*charmap\s+"([^"]+)",\s*\$([0-9a-fA-F]+)', line)
        if match:
            charmap.setdefault(int(match[2], 16), match[1])
    return charmap


def const_listing(path):
    value = 0
    increment = 1
    names = {}
    prefixes = {"const": "", "add_hm": "HM_", "add_tm": "TM_"}
    evaluator = ConstParser()
    for raw in open(path):
        parts = raw.split(";")[0].strip().split(None, 1)
        if not parts:
            continue
        command, rest = parts[0], parts[1].strip() if len(parts) > 1 else ""
        arguments = [item.strip() for item in rest.split(",")] if rest else []
        evaluator.const_value = value
        if command in prefixes and arguments:
            names[value] = prefixes[command] + arguments[0]
            value += increment
        elif command == "const_def":
            value = evaluator.evaluate(arguments[0]) if arguments else 0
            increment = evaluator.evaluate(arguments[1]) if len(arguments) > 1 else 1
        elif command == "const_skip":
            value += increment * (evaluator.evaluate(arguments[0]) if arguments else 1)
        elif command == "const_next":
            value = evaluator.evaluate(arguments[0])
    return names


def parse_engine_flags(source, symbols):
    parser = ConstParser()
    constants_dir = os.path.join(source, "constants")
    for file in sorted(os.listdir(constants_dir)):
        if file.endswith(".asm"):
            parser.feed(os.path.join(constants_dir, file))
    names = const_listing(os.path.join(constants_dir, "engine_flags.asm"))
    ordered = [names[index] for index in sorted(names)]
    flags = {}
    unresolved = []
    entries = []
    for raw in open(os.path.join(source, "data/events/engine_flags.asm")):
        line = raw.split(";")[0].strip()
        if line.startswith("engine_flag "):
            location, bit = [item.strip() for item in line[len("engine_flag "):].split(",")]
            entries.append((location, bit))
    if len(entries) != len(ordered):
        raise ValueError(
            f"engine flag count mismatch: {len(entries)} entries vs {len(ordered)} constants"
        )
    for name, (location, bit) in zip(ordered, entries):
        offset = 0
        match = re.match(r"(\w+)\s*\+\s*(.+)$", location)
        if match:
            location = match[1]
            offset = parser.evaluate(match[2])
        bit_value = parser.evaluate(bit)
        if location not in symbols or bit_value is None or offset is None:
            unresolved.append(name)
            continue
        flags[name] = [
            symbols[location][0],
            symbols[location][1] + offset + bit_value // 8,
            bit_value % 8,
        ]
    return flags, unresolved


def git_head(path):
    return subprocess.check_output(["git", "-C", path, "rev-parse", "HEAD"], text=True).strip()


def build(game, source, symbols_dir, rom_dir):
    with open(os.path.join(rom_dir, ROM_PATH[game]), "rb") as handle:
        digest = hashlib.sha1(handle.read()).hexdigest()
    if digest != ROM_SHA1[game]:
        raise ValueError(f"{game} ROM sha1 {digest} is not the build the symbols describe")
    symbols, rom_labels = parse_symbols(os.path.join(symbols_dir, SYM_FILE[game]))
    constants = os.path.join(source, "constants")
    names = {}
    for key, (label, layout, stride, count) in NAME_TABLES[game].items():
        bank, addr = rom_labels[label]
        names[key] = {"bank": bank, "addr": addr, "layout": layout, "stride": stride, "first_id": 1, "count": count}
    maps = ConstParser()
    maps.feed(os.path.join(constants, "map_constants.asm"))
    trainers = ConstParser()
    trainers.feed(os.path.join(constants, "trainer_constants.asm"))
    data = {
        "source": {
            "repo": f"https://github.com/pret/{game}",
            "commit": git_head(source),
            "symbols_commit": git_head(symbols_dir),
            "symbols_file": SYM_FILE[game],
            "rom_sha1": digest,
        },
        "symbols": symbols,
        "names": names,
        "maps": maps.maps,
        "trainer_classes": {str(k): v for k, v in trainers.trainer_classes.items()},
        "charmap": {str(k): v for k, v in parse_charmap(os.path.join(constants, "charmap.asm")).items()},
        "types": {str(k): v for k, v in const_listing(os.path.join(constants, "type_constants.asm")).items()},
        "items": {str(k): v for k, v in const_listing(os.path.join(constants, "item_constants.asm")).items()},
        "species": {str(k): v for k, v in const_listing(os.path.join(constants, "pokemon_constants.asm")).items()},
        "moves": {str(k): v for k, v in const_listing(os.path.join(constants, "move_constants.asm")).items()},
    }
    if game == GEN1:
        data["pokedex_order"] = list(rom_labels["PokedexOrder"])
        data["events"] = {v: k for k, v in const_listing(os.path.join(constants, "event_constants.asm")).items()}
        data["toggles"] = {v: k for k, v in const_listing(os.path.join(constants, "toggle_constants.asm")).items()}
        data["unresolved"] = []
    else:
        data["events"] = {v: k for k, v in const_listing(os.path.join(constants, "event_flags.asm")).items()}
        data["landmarks"] = {str(k): v for k, v in const_listing(os.path.join(constants, "landmark_constants.asm")).items()}
        engine_flags, unresolved = parse_engine_flags(source, symbols)
        data["engine_flags"] = engine_flags
        data["unresolved"] = unresolved
    return data


@click.command()
@click.option("--pret_dir", required=True, help="Directory holding pokered, pokered_sym, pokecrystal, pokecrystal_sym.")
@click.option("--rom_dir", required=True, help="The rom_data/pokemon directory.")
@click.option("--out_dir", default="src/gameboy_worlds/emulation/pokemon/memory_data")
def main(pret_dir, rom_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for game in (GEN1, GEN2):
        data = build(game, os.path.join(pret_dir, game), os.path.join(pret_dir, f"{game}_sym"), rom_dir)
        with open(os.path.join(out_dir, f"{game}.json"), "w") as handle:
            json.dump(data, handle, separators=(",", ":"), sort_keys=True)
        print(
            game,
            "symbols", len(data["symbols"]),
            "events", len(data["events"]),
            "maps", len(data["maps"]),
            "trainer_classes", len(data["trainer_classes"]),
            "engine_flags", len(data.get("engine_flags", {})),
            "toggles", len(data.get("toggles", {})),
            "unresolved", data["unresolved"],
        )


if __name__ == "__main__":
    main()
