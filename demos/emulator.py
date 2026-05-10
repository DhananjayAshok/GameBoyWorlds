"""
Usage:
python demos/emulator.py --game pokemon_red --play_mode human
"""

from gameboy_worlds import get_emulator, AVAILABLE_GAMES
import click


@click.command()
@click.option(
    "--game",
    type=click.Choice(AVAILABLE_GAMES),
    default="pokemon_red",
    help="Variant of the game to emulate.",
)
@click.option(
    "--init_state", type=str, default=None, help="Name of the initial state file"
)
@click.option(
    "--play_mode",
    type=click.Choice(["human", "random"]),
    default="human",
    help="Play mode: 'human' for manual play, 'random' for random actions.",
)
@click.option(
    "--headless",
    type=bool,
    default=None,
    help="Whether to run the emulator in headless mode (no GUI).",
)
@click.option(
    "--save_video",
    type=bool,
    default=None,
    help="Whether to save a video of the gameplay. If not specified, uses default from config.",
)
def main(game, init_state, play_mode, headless, save_video):
    if play_mode == "human":
        emulator = get_emulator(
            game=game, init_state=init_state, headless=False, save_video=save_video
        )
        emulator.human_play()
    else:
        if headless != False:
            headless = True
        emulator = get_emulator(
            game=game, init_state=init_state, headless=headless, save_video=save_video
        )
        emulator.random_play()


if __name__ == "__main__":
    main()
