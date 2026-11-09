import hashlib
import json
import os
import re
import subprocess

import click

LADX_MD5 = "7351daa3c0a91d8f6fe2fbcca6182478"
SEASONS_MD5 = "f2dc6c4e093e4f8c6cbea80e8dbd62cb"
LADX_ROM = "legend_of_zelda_links_awakening/LegendOfZeldaLinksAwakening.gbc"
SEASONS_ROM = "legend_of_zelda_the_oracle_of_seasons/LegendOfZeldaTheOracleOfSeasons.gbc"


LADX_ANNOTATION_TYPOS = {"wDB6D": 0xDB6D}
SEASONS_INSTANCES = {"w1Link": (1, 0xD000)}


def rom_digest(path):
    with open(path, "rb") as handle:
        return hashlib.md5(handle.read()).hexdigest()


def git_head(path):
    return subprocess.check_output(["git", "-C", path, "rev-parse", "HEAD"], text=True).strip()


def with_sizes(labels):
    starts = {}
    for bank, address in labels.values():
        starts.setdefault((bank, address >= 0xFF80), set()).add(address)
    ordered = {key: sorted(values) for key, values in starts.items()}
    symbols = {}
    for label, (bank, address) in labels.items():
        addresses = ordered[(bank, address >= 0xFF80)]
        position = addresses.index(address)
        following = addresses[position + 1] if position + 1 < len(addresses) else address + 1
        symbols[label] = [bank, address, following - address]
    return symbols


def parse_ladx_file(path):
    labels = {}
    mismatches = []
    bank = 0
    counter = None
    pending = []
    for raw in open(path):
        code, _, comment = raw.partition(";")
        code = code.strip()
        comment = comment.strip()
        match = re.match(r'section\s+"[^"]*",\s*\w+\[\$([0-9a-fA-F]+)\](?:,\s*bank\[(\d+)\])?', code, re.IGNORECASE)
        if match:
            counter = int(match[1], 16)
            bank = int(match[2]) if match[2] else 0
            pending = []
            continue
        match = re.match(r"^(\w+)::?$", code)
        if match:
            pending.append(match[1])
            hex_comment = re.match(r"^([0-9a-fA-F]{4})\b", comment)
            if hex_comment and counter is None:
                counter = int(hex_comment[1], 16)
            continue
        match = re.match(r"^ds\s+(.+)$", code)
        if match:
            hex_comment = re.match(r"^([0-9a-fA-F]{4})\b", comment)
            annotated = int(hex_comment[1], 16) if hex_comment else None
            if pending and pending[0] in LADX_ANNOTATION_TYPOS:
                annotated = LADX_ANNOTATION_TYPOS[pending[0]]
            if annotated is not None:
                if counter is not None and annotated != counter:
                    mismatches.append((pending[:1], hex(counter), hex(annotated)))
                counter = annotated
            if counter is not None:
                for label in pending:
                    labels[label] = (bank, counter)
            pending = []
            expression = match[1].strip()
            if re.fullmatch(r"\$[0-9a-fA-F]+", expression):
                size = int(expression[1:], 16)
            elif re.fullmatch(r"\d+", expression):
                size = int(expression)
            else:
                size = None
            counter = counter + size if (counter is not None and size is not None) else None
    return labels, mismatches


def parse_seasons(path):
    labels = {}
    active = [True]
    counter = None
    pending = None
    stack = []
    dropped = []
    diverged = False
    for raw in open(path):
        code, _, comment = raw.partition(";")
        code = code.strip()
        comment = comment.strip()
        lowered = code.lower()
        if lowered.startswith(".ramsection"):
            counter = None
            diverged = False
            continue
        if lowered.startswith(".ifdef"):
            stack.append(code.split()[1])
            active.append(active[-1] and code.split()[1] != "ROM_AGES")
            continue
        if lowered.startswith(".ifndef"):
            stack.append("not")
            active.append(active[-1])
            continue
        if lowered.startswith(".if "):
            stack.append("other")
            active.append(active[-1])
            continue
        if lowered.startswith(".else"):
            name = stack[-1] if stack else ""
            parent = active[-2]
            active[-1] = parent and name == "ROM_AGES"
            continue
        if lowered.startswith(".endif"):
            stack.pop()
            active.pop()
            continue
        if not active[-1]:
            continue
        match = re.match(r"^(\w+):$", code)
        if match:
            name = match[1]
            two = re.match(r"^\$([0-9a-fA-F]{4})/\$([0-9a-fA-F]{4})", comment)
            seasons_only = re.match(r"^-/\$([0-9a-fA-F]{4})", comment)
            single = re.match(r"^\$([0-9a-fA-F]{4})\b", comment)
            address = None
            if two:
                address = int(two[2], 16)
                diverged = diverged or two[1] != two[2]
            elif seasons_only:
                address = int(seasons_only[1], 16)
            elif single and not diverged:
                address = int(single[1], 16)
            elif counter is not None:
                address = counter
                if single and int(single[1], 16) != counter and "ROM_SEASONS" in stack:
                    dropped.append((name, hex(counter), single[0]))
            elif single and "ROM_SEASONS" in stack:
                address = int(single[1], 16)
            else:
                dropped.append((name, None, single[0] if single else None))
            if address is not None:
                labels[name] = (1 if 0xD000 <= address < 0xE000 else 0, address)
                counter = address
            pending = name
            continue
        if counter is None:
            continue
        if re.match(r"^db\b", lowered):
            counter += 1
        elif re.match(r"^dw\b", lowered):
            counter += 2
        elif lowered.startswith("dsb") or lowered.startswith("dsw"):
            argument = code.split(None, 1)[1].strip() if len(code.split(None, 1)) > 1 else ""
            value = None
            if re.fullmatch(r"\$[0-9a-fA-F]+", argument):
                value = int(argument[1:], 16)
            elif re.fullmatch(r"\d+", argument):
                value = int(argument)
            if value is None:
                counter = None
            else:
                counter += value * (2 if lowered.startswith("dsw") else 1)
        elif lowered.startswith(".ends") or "instanceof" in lowered:
            counter = None
    return labels, dropped


def parse_ladx_hram(path):
    labels, mismatches = parse_ladx_file(path)
    return labels, mismatches


def parse_inventory_names(path):
    names = {}
    for line in open(path):
        match = re.match(r"\s*(?:DEF\s+)?(INVENTORY_\w+)\s+(?:equ|EQU)\s+\$([0-9a-fA-F]+)", line)
        if match:
            names.setdefault(int(match[2], 16), match[1])
    return {str(key): value for key, value in names.items()}


@click.command()
@click.option("--ladx_dir", required=True, help="Checkout of zladx/LADX-Disassembly with src/constants.")
@click.option("--oracles_dir", required=True, help="Checkout of Stewmath/oracles-disasm with include/.")
@click.option("--rom_dir", required=True, help="The rom_data/legend_of_zelda directory.")
@click.option("--out_dir", default="src/gameboy_worlds/emulation/legend_of_zelda/memory_data")
def main(ladx_dir, oracles_dir, rom_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    digest = rom_digest(os.path.join(rom_dir, LADX_ROM))
    if digest != LADX_MD5:
        raise ValueError(f"Link's Awakening ROM md5 {digest} is not azle-r2")
    wram, wram_mismatches = parse_ladx_file(os.path.join(ladx_dir, "src/constants/memory/wram.asm"))
    hram, hram_mismatches = parse_ladx_hram(os.path.join(ladx_dir, "src/constants/memory/hram.asm"))
    ladx = {
        "source": {"repo": "https://github.com/zladx/LADX-Disassembly", "commit": git_head(ladx_dir), "rom_md5": digest},
        "symbols": with_sizes({**wram, **hram}),
        "inventory_items": parse_inventory_names(os.path.join(ladx_dir, "src/constants/inventory.asm")),
        "annotation_mismatches": [[str(a), b, c] for a, b, c in wram_mismatches + hram_mismatches],
    }
    with open(os.path.join(out_dir, "links_awakening.json"), "w") as handle:
        json.dump(ladx, handle, separators=(",", ":"), sort_keys=True)
    digest = rom_digest(os.path.join(rom_dir, SEASONS_ROM))
    if digest != SEASONS_MD5:
        raise ValueError(f"Oracle of Seasons ROM md5 {digest} is not the disassembly's seasons build")
    labels, dropped = parse_seasons(os.path.join(oracles_dir, "include/wram.s"))
    labels.update(SEASONS_INSTANCES)
    seasons = {
        "source": {"repo": "https://github.com/Stewmath/oracles-disasm", "commit": git_head(oracles_dir), "rom_md5": digest},
        "symbols": with_sizes(labels),
        "dropped": [list(map(str, item)) for item in dropped],
    }
    with open(os.path.join(out_dir, "oracle_of_seasons.json"), "w") as handle:
        json.dump(seasons, handle, separators=(",", ":"), sort_keys=True)
    print("links_awakening", len(ladx["symbols"]), "inventory", len(ladx["inventory_items"]), "mismatches", ladx["annotation_mismatches"][:12])
    print("oracle_of_seasons", len(seasons["symbols"]), "dropped", len(dropped), seasons["dropped"][:10])


if __name__ == "__main__":
    main()
