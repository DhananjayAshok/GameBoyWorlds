variants=("pokemon_red" "pokemon_crystal" "pokemon_brown" "pokemon_prism" "pokemon_fools_gold" "pokemon_starbeasts")

for variant in "${variants[@]}"; do
    python -m poke_worlds.setup_data pull --game $variant
done