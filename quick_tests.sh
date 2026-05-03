#!/bin/bash

variants=("pokemon_red" "pokemon_crystal" "pokemon_brown" "pokemon_prism" "pokemon_fools_gold" "pokemon_starbeasts" "sword_of_hope_1" "sword_of_hope_2" "deja_vu_1" "deja_vu_2" "harvest_moon_1" "harvest_moon_2" "harvest_moon_3" "harry_potter_philosophers_stone" "legend_of_zelda_links_awakening" "legend_of_zelda_the_oracle_of_seasons")


echo "Testing emulator..."
for variant in "${variants[@]}"; do
    echo "  Variant: $variant"
    python demos/emulator.py --play_mode random --game $variant
done

echo "Testing environment..."
for variant in "${variants[@]}"; do
    echo "  Variant: $variant"
    python demos/environment.py --play_mode random --game $variant
done
