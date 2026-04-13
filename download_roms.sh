#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------------------
# SETUP GUIDE
#
# This script downloads ROM files from your personal Google Drive and places
# them in the correct directory structure for GameBoyRL.
#
# Steps:
#   1. Legally obtain the .gb or .gbc ROM file for each game you want to use.
#      Only use ROMs for games you own.
#
#   2. Upload each ROM file to your own private Google Drive.
#      - Do NOT share the file or the link with anyone.
#      - Do NOT distribute the ROM or the link publicly.
#
#   3. For each game below, replace "PLACEHOLDER" with the Google Drive share
#      link for that ROM (right-click file in Drive -> "Get link").
#
#   4. Run this script from the GameBoyWorlds root:
#        bash download_roms.sh
#
# ---------------------------------------------------------------------------
# ROM data structure
#   rom_series[series]      = space-separated list of game names
#   rom_links[series:game]  = Google Drive link for that game
#
# Series/game names mirror GameBoyWorlds/configs/rom_data_path_vars.yaml
# ---------------------------------------------------------------------------

declare -A rom_series
declare -A rom_links

# -- pokemon -----------------------------------------------------------------
rom_series["pokemon"]="pokemon_red pokemon_crystal pokemon_fools_gold pokemon_prism pokemon_brown pokemon_starbeasts"
rom_links["pokemon:pokemon_red"]="PLACEHOLDER"
rom_links["pokemon:pokemon_crystal"]="PLACEHOLDER"
rom_links["pokemon:pokemon_fools_gold"]="PLACEHOLDER"
rom_links["pokemon:pokemon_prism"]="PLACEHOLDER"
rom_links["pokemon:pokemon_brown"]="PLACEHOLDER"
rom_links["pokemon:pokemon_starbeasts"]="PLACEHOLDER"

# -- hamtaro -----------------------------------------------------------------
rom_series["hamtaro"]="ham_hams_unite"
rom_links["hamtaro:ham_hams_unite"]="PLACEHOLDER"

# -- legend_of_zelda ---------------------------------------------------------
rom_series["legend_of_zelda"]="legend_of_zelda_links_awakening legend_of_zelda_the_oracle_of_seasons"
rom_links["legend_of_zelda:legend_of_zelda_links_awakening"]="PLACEHOLDER"
rom_links["legend_of_zelda:legend_of_zelda_the_oracle_of_seasons"]="PLACEHOLDER"

# -- sword_of_hope -----------------------------------------------------------
rom_series["sword_of_hope"]="sword_of_hope_1 sword_of_hope_2"
rom_links["sword_of_hope:sword_of_hope_1"]="PLACEHOLDER"
rom_links["sword_of_hope:sword_of_hope_2"]="PLACEHOLDER"

# -- deja_vu -----------------------------------------------------------------
rom_series["deja_vu"]="deja_vu_1 deja_vu_2"
rom_links["deja_vu:deja_vu_1"]="PLACEHOLDER"
rom_links["deja_vu:deja_vu_2"]="PLACEHOLDER"

# -- harrypotter -------------------------------------------------------------
rom_series["harrypotter"]="harrypotter_philosophersstone"
rom_links["harrypotter:harrypotter_philosophersstone"]="PLACEHOLDER"

# -- harvest_moon ------------------------------------------------------------
rom_series["harvest_moon"]="harvest_moon_1 harvest_moon_2 harvest_moon_3"
rom_links["harvest_moon:harvest_moon_1"]="PLACEHOLDER"
rom_links["harvest_moon:harvest_moon_2"]="PLACEHOLDER"
rom_links["harvest_moon:harvest_moon_3"]="PLACEHOLDER"

# ---------------------------------------------------------------------------
# 1. Install gdown
# ---------------------------------------------------------------------------
uv pip install gdown==6.0.0

# ---------------------------------------------------------------------------
# 2. Source config
# ---------------------------------------------------------------------------
CONFIG="configs/config.env"
if [[ ! -f "$CONFIG" ]]; then
    echo "ERROR: config file not found: $CONFIG" >&2
    exit 1
fi
# shellcheck source=/dev/null
source "$CONFIG"

if [[ -z "${storage_dir:-}" ]]; then
    echo "ERROR: storage_dir is not set in $CONFIG" >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# 3. Set ROM root path
# ---------------------------------------------------------------------------
rom_paths="$storage_dir/rom_data"

# ---------------------------------------------------------------------------
# 4. Download each ROM into $rom_paths/<series>/<game>/
# ---------------------------------------------------------------------------
for series in "${!rom_series[@]}"; do
    read -ra games <<< "${rom_series[$series]}"
    for game in "${games[@]}"; do
        link="${rom_links[$series:$game]}"
        dest="$rom_paths/$series/$game"
        mkdir -p "$dest"

        if [[ "$link" == "PLACEHOLDER" ]]; then
            echo "SKIPPING [$series / $game]: link not set"
            continue
        fi

        echo "Downloading [$series / $game] -> $dest"
        # gdown saves with the original Google Drive filename;
        # cd into dest so the file lands there directly.
        (cd "$dest" && gdown "$link")
    done
done

echo "All ROMs downloaded successfully."
