#!/bin/bash

variants=("pokemon_red" "pokemon_crystal" "pokemon_brown" "pokemon_prism" "pokemon_fools_gold" "pokemon_starbeasts" "sword_of_hope_1" "sword_of_hope_2")


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
#python demos/environment.py --play_mode random