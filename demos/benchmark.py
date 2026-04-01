from gameboy_worlds import get_environment, AVAILABLE_GAMES
from tqdm import tqdm
import matplotlib.pyplot as plt
import click

# python demos/environment.py --play_mode human


@click.command()
@click.option(
    "--game",
    type=click.Choice(AVAILABLE_GAMES),
    default="pokemon_red",
    help="Variant of the game to emulate.",
)
@click.option(
    "--max_steps",
    type=int,
    default=500,
    help="Maximum number of steps to run in the environment.",
)
@click.option(
    "--init_state",
    type=str,
    default="default",
    help="Initial state to start the environment in (if supported).",
)
@click.option(
    "--state_tracker_class",
    type=str,
    default="default",
    help="State tracker class to use.",
)
def main(
    game,
    max_steps,
    init_state,
    state_tracker_class,
):
    environment = get_environment(
        game=game,
        environment_variant="test",
        controller_variant="low_level_play",
        save_video=True,
        max_steps=max_steps,
        headless=True,
        init_state=init_state,
        state_tracker_class=state_tracker_class,
    )
    environment.human_step_play(show_obs=False, show_info=True)


if __name__ == "__main__":
    main()
