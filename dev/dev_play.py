from gameboy_worlds import get_emulator, AVAILABLE_GAMES
import click


@click.command()
@click.option(
    "--game",
    type=click.Choice(AVAILABLE_GAMES),
    default="pokemon_red",
    help="Variant of the Pokemon game to emulate.",
)
@click.option(
    "--state_tracker_class",
    type=str,
    default="default",
    help="Variant of the state tracker to use.",
)
@click.option(
    "--init_state", type=str, default=None, help="Name of the initial state file"
)
@click.option(
    "--save_video",
    type=bool,
    default=False,
    help="Whether to save a video of the gameplay.",
)
@click.option(
    "--gameshark",
    type=str,
    default=None,
    multiple=True,
    help="GameShark code(s) to apply on startup (e.g. 0101C7C9). Can be repeated for multiple codes.",
)
def main(game, state_tracker_class, init_state, save_video, gameshark):
    env = get_emulator(
        game=game,
        init_state=init_state,
        headless=False,
        state_tracker_class=state_tracker_class,
        save_video=save_video,
    )
    for code in gameshark:
        env._pyboy.gameshark.add(code)
        print(f"GameShark code applied: {code}")
    env._dev_play()


if __name__ == "__main__":
    main()
