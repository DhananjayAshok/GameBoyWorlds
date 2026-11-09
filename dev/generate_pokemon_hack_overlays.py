import collections
import hashlib
import json
import os

import click

MIN_CONSERVED_SITES = 5
MIN_CONSERVED_FRACTION = 0.25
LOAD_OPCODES = (0xFA, 0xEA, 0x21, 0x11, 0x01)
TWO_BYTE = {0x06, 0x0E, 0x16, 0x18, 0x1E, 0x20, 0x26, 0x28, 0x2E, 0x30, 0x36, 0x38, 0x3E, 0xC6, 0xCB, 0xCE, 0xD6, 0xDE, 0xE0, 0xE6, 0xEE, 0xF0, 0xF6, 0xF8, 0xFE, 0xE8}
THREE_BYTE = {0x01, 0x08, 0x11, 0x21, 0x31, 0xC2, 0xC3, 0xC4, 0xCA, 0xCC, 0xCD, 0xD2, 0xD4, 0xDA, 0xDC, 0xEA, 0xFA}
RELATIVE_JUMPS = {0x18, 0x20, 0x28, 0x30, 0x38}
ABSOLUTE_JUMPS = {0xC2, 0xC3, 0xC4, 0xCA, 0xCC, 0xCD, 0xD2, 0xD4, 0xDA, 0xDC}
SEQUENCE_LENGTH = 5

HACKS = {
    "pokemon_brown": {
        "base_rom": "pokemon_red/PokemonRed.gb",
        "hack_rom": "pokemon_brown/PokemonBrown.gb",
        "base_data": "pokered.json",
        "names": {
            "species": {"bank": 0x3F, "addr": 0x7000, "layout": "fixed", "stride": 10, "first_id": 1, "count": 254},
            "moves": {"bank": 0x2C, "addr": 0x4000, "layout": "terminated", "stride": None, "first_id": 1, "count": 254},
            "items": {"bank": 0x40, "addr": 0x4000, "layout": "terminated", "stride": None, "first_id": 1, "count": 101},
        },
        "verified_in_game": {
            "wBagItems": "decoded list matches the Item screen",
            "wBoxItems": "terminated list decodes to named items in every state",
            "wCurMapHeight": "player stays inside the decoded bounds across every state",
            "wPlayTimeHours": "poked value appears on the trainer card",
            "wPlayTimeSeconds": "advances with emulated time",
            "wPlayTimeFrames": "advances with emulated time",
            "hJoyHeld": "reflects a held button",
            "hJoyPressed": "reflects a new button press",
        },
        "relocated": {},
        "struct_prefixes": {
            "wPartyMons": ["wPartyMon1", "wPartyMon2", "wPartyMon3", "wPartyMon4", "wPartyMon5", "wPartyMon6"],
        },
        "battle_struct_fields": ["Species", "HP", "Status", "Type", "Type1", "Type2", "Moves", "Level", "Stats", "MaxHP", "Attack", "Defense", "Speed", "Special", "PP"],
        "unverified_suffixes": ["DVs", "HPExp", "AttackExp", "DefenseExp", "SpeedExp", "SpecialExp", "CatchRate", "BoxLevel"],
    },
    "pokemon_prism": {
        "base_rom": "pokemon_crystal/PokemonCrystal.gbc",
        "hack_rom": "pokemon_prism/PokemonPrism.gbc",
        "base_data": "pokecrystal.json",
        "names": {
            "species": {"bank": 0x05, "addr": 0x55E5, "layout": "fixed", "stride": 10, "first_id": 1, "count": 254},
            "moves": {"bank": 0x11, "addr": 0x61BC, "layout": "length_prefixed", "stride": None, "first_id": 1, "count": 254},
            "items": {"bank": 0x11, "addr": 0x4000, "layout": "length_prefixed", "stride": None, "first_id": 1, "count": 180},
        },
        "verified_in_game": {
            "wPlayerName": "poked name appears in the start menu and trainer card",
            "wRivalName": "decodes to player-entered names across states",
            "wMoney": "poked value appears on the trainer card",
            "wGameTimeHours": "poked value appears on the trainer card",
            "wGameTimeMinutes": "poked value appears on the trainer card",
            "wGameTimeSeconds": "advances with emulated time",
            "wGameTimeFrames": "advances with emulated time",
            "wTilemap": "text drawn by the game decodes from it on every checked screen",
            "wMapHeight": "player stays inside the decoded bounds across every state",
            "wBattleMon": "decoded species, level, HP and moves match the battle screen",
            "wBattleMonNickname": "decoded name matches the battle screen",
            "wEnemyMon": "decoded species and level match the battle screen",
            "wEnemyMonNickname": "decoded name matches the battle screen",
            "wPokedexCaught": "only set bit is the party species, zeroing it blanks the Pokedex list",
            "wPokedexSeen": "zeroing it blanks the Pokedex list",
            "wPartyMonNicknames": "decoded names match the battle and party screens",
            "hJoyDown": "reflects a held button",
        },
        "relocated": {
            "wNumItems": [1, 0xD866, 1, "poked list appears in the Pack items pocket"],
            "wItems": [1, 0xD867, 81, "poked list appears in the Pack items pocket"],
            "wNumKeyItems": [1, 0xD8B8, 1, "poked list appears in the Pack key items pocket"],
            "wKeyItems": [1, 0xD8B9, 51, "poked list appears in the Pack key items pocket"],
            "wNumBalls": [1, 0xD8EC, 1, "poked list appears in the Pack balls pocket"],
            "wBalls": [1, 0xD8ED, 49, "poked list appears in the Pack balls pocket"],
        },
        "struct_prefixes": {
            "wPartyMons": ["wPartyMon1", "wPartyMon2", "wPartyMon3", "wPartyMon4", "wPartyMon5", "wPartyMon6"],
        },
        "battle_struct_fields": ["Species", "Item", "Moves", "PP", "Level", "Status", "HP", "MaxHP", "Stats", "Attack", "Defense", "Speed", "SpclAtk", "SpclDef", "Type", "Type1", "Type2"],
        "unverified_suffixes": ["DVs", "HPExp", "AtkExp", "DefExp", "SpdExp", "SpcExp", "StatExp", "Happiness", "PokerusStatus", "CaughtData", "CaughtTime", "CaughtGender", "CaughtLevel", "CaughtLocation"],
    },
}


def normalized_sequence(rom, position):
    tokens = []
    for _ in range(SEQUENCE_LENGTH):
        if position >= len(rom) - 3:
            return None
        opcode = rom[position]
        if opcode in THREE_BYTE:
            operand = rom[position + 1] | rom[position + 2] << 8
            if opcode in ABSOLUTE_JUMPS or operand < 0x8000:
                tokens.append((opcode,))
            else:
                tokens.append((opcode, operand))
            position += 3
        elif opcode in TWO_BYTE:
            tokens.append((opcode,) if opcode in RELATIVE_JUMPS else (opcode, rom[position + 1]))
            position += 2
        else:
            tokens.append((opcode,))
            position += 1
        if opcode in (0xC9, 0xD9, 0xC3, 0xE9):
            break
    return tuple(tokens)


def access_sites(rom, addresses):
    sites = collections.defaultdict(list)
    for position in range(len(rom) - 3):
        if rom[position] in LOAD_OPCODES:
            address = rom[position + 1] | rom[position + 2] << 8
            if address in addresses:
                sites[address].append(position)
    return sites


def conservation(base, hack, addresses):
    base_sites = access_sites(base, addresses)
    hack_sites = access_sites(hack, addresses)
    scores = {}
    for address, sites in base_sites.items():
        hack_sequences = {normalized_sequence(hack, position) for position in hack_sites.get(address, [])}
        conserved = sum(
            1
            for position in sites
            if normalized_sequence(base, position) is not None
            and normalized_sequence(base, position) in hack_sequences
        )
        scores[address] = (len(sites), len(hack_sites.get(address, [])), conserved)
    return scores


@click.command()
@click.option("--rom_dir", required=True, help="The rom_data/pokemon directory.")
@click.option("--out_dir", default="src/gameboy_worlds/emulation/pokemon/memory_data")
def main(rom_dir, out_dir):
    for hack_name, spec in HACKS.items():
        with open(os.path.join(rom_dir, spec["base_rom"]), "rb") as handle:
            base = handle.read()
        with open(os.path.join(rom_dir, spec["hack_rom"]), "rb") as handle:
            hack = handle.read()
        with open(os.path.join(out_dir, spec["base_data"])) as handle:
            base_data = json.load(handle)
        by_address = collections.defaultdict(list)
        for label, (bank, address, _) in base_data["symbols"].items():
            if address >= 0xC000:
                by_address[address].append(label)
        scores = conservation(base, hack, set(by_address))
        evidence = {}
        labels = set()
        for address, (base_sites, hack_sites, conserved) in scores.items():
            passes = conserved >= MIN_CONSERVED_SITES and conserved >= MIN_CONSERVED_FRACTION * base_sites
            for label in by_address[address]:
                evidence[label] = [base_sites, hack_sites, conserved]
                if passes:
                    labels.add(label)
        code_verified = len(labels)
        for label in spec["verified_in_game"]:
            labels.add(label)
        relocated = {}
        for label, (bank, address, size, reason) in spec["relocated"].items():
            labels.add(label)
            relocated[label] = {"symbol": [bank, address, size], "reason": reason}
        for parent, prefixes in spec["struct_prefixes"].items():
            if parent in labels:
                for label in base_data["symbols"]:
                    if label.startswith(tuple(prefixes)):
                        labels.add(label)
        for parent in ("wBattleMon", "wEnemyMon"):
            for field in spec["battle_struct_fields"]:
                if parent + field in base_data["symbols"]:
                    labels.add(parent + field)
        labels = {
            label
            for label in labels
            if not (
                label.startswith(("wPartyMon", "wBattleMon", "wEnemyMon"))
                and label.endswith(tuple(spec["unverified_suffixes"]))
            )
        }
        overlay = {
            "rom_sha1": hashlib.sha1(hack).hexdigest(),
            "criteria": {"min_conserved_sites": MIN_CONSERVED_SITES, "min_conserved_fraction": MIN_CONSERVED_FRACTION},
            "names": spec["names"],
            "labels": sorted(labels),
            "verified_in_game": spec["verified_in_game"],
            "relocated": relocated,
            "code_evidence": {label: evidence[label] for label in sorted(labels) if label in evidence},
        }
        with open(os.path.join(out_dir, f"{hack_name}.json"), "w") as handle:
            json.dump(overlay, handle, separators=(",", ":"), sort_keys=True)
        print(hack_name, "sha1", overlay["rom_sha1"], "code_verified", code_verified, "total", len(labels))


if __name__ == "__main__":
    main()
