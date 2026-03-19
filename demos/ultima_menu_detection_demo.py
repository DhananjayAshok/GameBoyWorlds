"""
Demo: Ultima Runes of Virtue - Menu Detection

This script demonstrates the menu detection feature by:
1. Playing the game in free_roam mode (walking around)
2. Opening the menu (START) to show in_menu detection
3. Closing the menu and walking more
4. Repeating to show the state transitions

Outputs a video with the game screen and annotated agent_state.
"""

from gameboy_worlds import get_emulator
from gameboy_worlds.emulation.emulator import LowLevelActions
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def main():
    emu = get_emulator(
        game="ultima_runes_of_virtue", headless=True, init_state="gameplay"
    )
    emu.reset()

    # Define a sequence of actions to demonstrate menu detection
    # Use None as action to indicate "tick only" (stay in current state)
    action_sequence = []

    # Walk around (free_roam)
    for _ in range(4):
        action_sequence.append(("RIGHT", LowLevelActions.PRESS_ARROW_RIGHT))
    for _ in range(3):
        action_sequence.append(("UP", LowLevelActions.PRESS_ARROW_UP))

    # Open menu
    action_sequence.append(("START (open menu)", LowLevelActions.PRESS_BUTTON_START))

    # Stay in menu for a few frames (tick without pressing anything)
    for _ in range(3):
        action_sequence.append(("(in menu - idle)", None))

    # Close menu
    action_sequence.append(("START (close menu)", LowLevelActions.PRESS_BUTTON_START))

    # Walk more
    for _ in range(4):
        action_sequence.append(("LEFT", LowLevelActions.PRESS_ARROW_LEFT))
    for _ in range(3):
        action_sequence.append(("DOWN", LowLevelActions.PRESS_ARROW_DOWN))

    # Open menu again
    action_sequence.append(("START (open menu)", LowLevelActions.PRESS_BUTTON_START))
    for _ in range(3):
        action_sequence.append(("(in menu - idle)", None))

    # Close menu
    action_sequence.append(("START (close menu)", LowLevelActions.PRESS_BUTTON_START))

    # Final walk
    for _ in range(3):
        action_sequence.append(("UP", LowLevelActions.PRESS_ARROW_UP))

    # Collect frames and states
    frames_data = []
    for action_name, action in action_sequence:
        if action is not None:
            emu.step(action)
        else:
            # Tick without any input to keep the current state
            emu._pyboy.tick(8, True)
            emu.state_tracker.step()
        frame = emu.get_current_frame().copy()
        report = emu.state_tracker.report()
        agent_state = report.get("ultima_core", {}).get("agent_state", "unknown")
        frames_data.append((frame, agent_state, action_name))

    emu.close()

    # Create video with matplotlib
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))

    def update(idx):
        ax.clear()
        frame, state, action = frames_data[idx]
        ax.imshow(frame[:, :, 0], cmap="gray")

        color = "red" if state == "in_menu" else "green"
        ax.set_title(
            f"Agent State: {state}",
            fontsize=18,
            fontweight="bold",
            color=color,
            pad=10,
        )
        ax.set_xlabel(f"Action: {action}  |  Step: {idx + 1}/{len(frames_data)}", fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])
        return []

    ani = animation.FuncAnimation(
        fig, update, frames=len(frames_data), interval=800, blit=False
    )

    output_path = "storage/ultima_menu_detection_demo.mp4"
    ani.save(output_path, writer="ffmpeg", fps=2, dpi=100)
    plt.close()
    print(f"Video saved to: {output_path}")

    # Also print a text summary
    print("\n=== State Transition Log ===")
    for i, (_, state, action) in enumerate(frames_data):
        marker = ">>>" if "menu" in action.lower() or "START" in action else "   "
        print(f"{marker} Step {i+1:2d} | Action: {action:25s} | agent_state: {state}")


if __name__ == "__main__":
    main()
