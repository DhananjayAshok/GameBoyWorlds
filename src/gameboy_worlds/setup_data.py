"""
Syncs data with Hugging Face Hub repositories for easy sharing of files.
Run with:
```bash
python -m gameboy_worlds.setup_data --help
```

or
```bash
python -m gameboy_worlds.setup_data push --game pokemon_red
```

or perhaps:
```bash
python -m gameboy_worlds.setup_data pull --game pokemon_red
```
"""

from gameboy_worlds.utils import log_error, log_info, log_warn, load_parameters
from gameboy_worlds import AVAILABLE_GAMES
import click
from huggingface_hub import HfApi
import os

loaded_parameters = load_parameters()
repo_namespace = "DJ-Research"


def check_variant(game, parameters):
    if game.lower() not in AVAILABLE_GAMES + ["all"]:
        log_error(
            f"Game {game} is not in the list of available variants: {AVAILABLE_GAMES}. Add it to the emulation registry before you proceed.",
            parameters,
        )
    games = [game] if game != "all" else AVAILABLE_GAMES
    for game in games:
        if f"{game}_rom_data_path" not in parameters:
            log_error(
                f"{game}_rom_data not found in parameters. You must add it to a config file.",
                parameters,
            )


@click.command()
@click.option(
    "--game",
    type=str,
    required=True,
    help="The game or game variant to create the repo for.",
)
@click.pass_obj
def create_hub_repo(parameters, game):
    """
    Create a new repo on the Hugging Face Hub. This should only be called once for each game_variant.
    Once set up, the repo will contain a mirror of what we expect (not including the ROM file itself) in the rom_data directory of that variant.
    """
    check_variant(game, parameters)
    games = [game] if game != "all" else AVAILABLE_GAMES
    for game in games:
        repo_name = f"GameBoy-{game}"
        repo_id = f"{repo_namespace}/{repo_name}"
        api = parameters["api"]
        api.create_repo(
            repo_id=repo_id, repo_type="dataset", exist_ok=False, private=False
        )
        log_info(
            f"Successfully created repo {repo_id} on the Hugging Face Hub.", parameters
        )


@click.command()
@click.option(
    "--game",
    type=str,
    required=True,
    help="The game or game variant to sync the repo for.",
)
@click.pass_obj
def sync(parameters, game):
    """
    Update the local repo with data from the HuggingFace Hub.
    """
    check_variant(game, parameters)
    games = [game] if game != "all" else AVAILABLE_GAMES
    for game in games:
        repo_name = f"GameBoy-{game}"
        repo_id = f"{repo_namespace}/{repo_name}"

        rom_data_path = parameters[f"{game}_rom_data_path"] + "/"
        if not os.path.exists(rom_data_path):
            os.makedirs(rom_data_path)
        api = parameters["api"]
        api.snapshot_download(
            repo_id=repo_id, repo_type="dataset", local_dir=rom_data_path
        )
        log_info(
            f"Tried to sync repo at {repo_namespace}/{repo_name} with directory {rom_data_path}. Check output above for success",
            parameters,
        )


@click.command()
@click.option(
    "--game",
    type=str,
    required=True,
    help="The game or game variant to push the repo for.",
)
@click.pass_obj
def push_data_to_hub(parameters, game):
    """
    Upload local data to the Hugging Face Hub.
    """
    check_variant(game, parameters)
    if game == "all":
        raise ValueError(
            f"Pushing to all is unsafe. Please specify a game variant to push."
        )
    games = [game] if game != "all" else AVAILABLE_GAMES
    for game in games:
        repo_name = f"GameBoy-{game}"
        api = parameters["api"]
        repo_id = f"{repo_namespace}/{repo_name}"
        rom_data_path = parameters[f"{game}_rom_data_path"] + "/"
        if not os.path.exists(rom_data_path):
            log_error(
                f"Rom data path {rom_data_path} does not exist. Cannot push to hub.",
                parameters,
            )
        api.upload_large_folder(
            repo_id=repo_id,
            repo_type="dataset",
            folder_path=rom_data_path,
            ignore_patterns=["*.gb", "*.gbc"],
        )
        log_info(
            f"Tried to push data from {rom_data_path} to repo {repo_namespace}/{repo_name} on the Hugging Face Hub.",
            parameters,
        )


@click.group()
@click.pass_context
def main(ctx, **input_parameters):
    api = HfApi()
    loaded_parameters["api"] = api
    ctx.obj = loaded_parameters


main.add_command(create_hub_repo, name="init")
main.add_command(sync, name="pull")
main.add_command(push_data_to_hub, name="push")

if __name__ == "__main__":
    main()
