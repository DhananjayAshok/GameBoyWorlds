from poke_worlds import get_environment, AVAILABLE_GAMES
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
    "--play_mode",
    type=click.Choice(["human", "random", "random_play"]),
    default="random",
    help="Play mode: 'random' for random actions.",
)
@click.option(
    "--environment_variant",
    type=str,
    default="default",
    help="The environment variant to use.",
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
@click.option(
    "--render",
    type=bool,
    default=False,
    help="Whether to render the environment with PyGame.",
)
@click.option(
    "--save_video",
    type=bool,
    default=None,
    help="Whether to save a video of the gameplay. If not specified, uses default from config.",
)
@click.option(
    "--show_mode",
    type=click.Choice(["state", "obs"]),
    default="state",
    help="Whether to show the state metrics or raw observations during human play.",
)
def main(
    game,
    play_mode,
    environment_variant,
    max_steps,
    init_state,
    state_tracker_class,
    render,
    save_video,
    show_mode,
):
    if play_mode == "human":
        controller_variant = "state_wise"
    else:
        controller_variant = play_mode.replace("random", "low_level")
    environment = get_environment(
        game=game,
        environment_variant=environment_variant,
        controller_variant=controller_variant,
        save_video=save_video,
        max_steps=max_steps,
        headless=True,
        init_state=init_state,
        state_tracker_class=state_tracker_class,
    )
    if play_mode != "human":
        steps = 0
        pbar = tqdm(total=max_steps)
        rewards = []
        while steps < max_steps:
            action = environment.action_space.sample()
            observation, reward, terminated, truncated, info = environment.step(action)
            rewards.append(reward)
            if render:
                environment.render()
            if terminated or truncated:
                break
            steps += 1
            pbar.update(1)
        pbar.close()
        environment.close()
        if render:
            # Plot rewards over time
            plt.plot(rewards)
            plt.xlabel("Step")
            plt.ylabel("Reward")
            plt.title("Rewards over Time")
            plt.show()
        else:
            print(f"Episode finished after {steps} steps with total reward {sum(rewards)}")
    else:
        show_obs = show_mode == "obs"
        show_info = not show_obs
        environment.human_step_play(show_obs=show_obs, show_info=show_info)


if __name__ == "__main__":
    main()
