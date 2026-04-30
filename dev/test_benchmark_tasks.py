from gameboy_worlds import get_test_environment, AVAILABLE_BENCHMARKS
from gameboy_worlds.utils import load_parameters
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import click
import numpy as np
import os

# python dev/test_benchmark_tasks.py --benchmark pokemon


@click.command()
@click.option(
    "--benchmark",
    type=click.Choice(AVAILABLE_BENCHMARKS),
    default="pokemon",
    help="Benchmark task to run.",
)
@click.option(
    "--max_steps",
    type=int,
    default=50,
    help="Maximum number of steps to run in the environment.",
)
@click.option(
    "--n_sample",
    type=int,
    default=100,
    help="Number of samples to run.",
)
def main(
    benchmark,
    max_steps,
    n_sample,
):
    parameters = load_parameters()
    np.random.seed(parameters["seed"])
    os.makedirs("results", exist_ok=True)
    df = pd.read_csv(f"benchmark/tests/{benchmark}.csv")
    per_episode = []
    for idx, row in tqdm(
        df.iterrows(), total=len(df), desc=f"Running {benchmark} tasks"
    ):
        environment = get_test_environment(
            row,
            max_steps=max_steps,
            save_video=n_sample <= 5,
            session_name=f"{benchmark}",
        )

        # play for random actions:
        def play_agent(environment):
            subgoals_all = None
            subgoals_reached = []
            success = False
            environment.reset()
            done = False
            while not done:
                action = environment.action_space.sample()
                obs, reward, terminated, truncated, info = environment.step(action)
                done = terminated or truncated
                if subgoals_all is None:
                    subgoals_all = info["subgoals"]["all"]
                subgoals_completed = info["subgoals"]["completed"]
                for subgoal in subgoals_completed:
                    if subgoal not in subgoals_reached:
                        subgoals_reached.append(subgoal)
                step_count = info["core"]["steps"]
                if terminated:
                    success = True
                    return success, subgoals_all, subgoals_reached, step_count
            return success, subgoals_all, subgoals_reached, None

        n_subgoals = None
        successes = []
        perc_subgoals_reached = []
        step_counts_if_success = []
        for idx in tqdm(
            range(n_sample), desc=f"Running samples for task {idx}", leave=False
        ):
            success, subgoals_all, subgoals_reached, step_count = play_agent(
                environment
            )
            successes.append(success)
            if n_subgoals is None:
                n_subgoals = len(subgoals_all)
            perc_subgoals_reached.append(
                len(subgoals_reached) / n_subgoals if n_subgoals > 0 else 0
            )
            if success:
                step_counts_if_success.append(step_count)
        per_episode.append(
            {
                "idx": idx,
                "task": row["task"],
                "success_rate": np.mean(successes),
                "perc_subgoals_mean": np.mean(perc_subgoals_reached),
                "perc_subgoals_std": np.std(perc_subgoals_reached),
                "steps_on_completion": (
                    np.mean(step_counts_if_success) if step_counts_if_success else None
                ),
            }
        )
    df_episode = pd.DataFrame(per_episode)
    df_episode.to_csv(f"results/{benchmark}.csv", index=False)
    print(f"Results for benchmark: {benchmark}")
    print(
        f"Average Success Rate: {df_episode['success_rate'].mean()} +- {df_episode['success_rate'].std()}"
    )
    print(
        f"Average % Subgoals Completed: {df_episode['perc_subgoals_mean'].mean()} +- {df_episode['perc_subgoals_mean'].std()}"
    )
    print(
        f"Subgoal completion standard deviation: {df_episode['perc_subgoals_std'].mean()} +- {df_episode['perc_subgoals_std'].std()}"
    )
    for idx, row in df_episode.iterrows():
        print(
            f"Task: {row['task']}, Success Rate: {row['success_rate']}, Perc Subgoals: {row['perc_subgoals_mean']}, Subgoal Std: {row['perc_subgoals_std']}, Steps on Completion: {row['steps_on_completion']}"
        )


if __name__ == "__main__":
    main()
