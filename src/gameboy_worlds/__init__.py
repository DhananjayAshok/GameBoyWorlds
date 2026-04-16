"""
Documentation for the <img src="https://dhananjayashok.github.io/GameBoyWorlds/assets/logo_tilt.png" width="70px"> package.

### Navigating the Documentation
This page and some of the nested links will look a bit empty, but rest assured, the documentation is there. You just need to look for it a little.
There are two ways to navigate the documentation:
1. **Sidebar Navigation**: Use the sidebar on the left to explore different modules. Expand the sections to find detailed documentation.
2. **Search Functionality**: Use the search bar at the top of the sidebar to quickly find specific classes, methods, or keywords within the documentation.

### Package Structure
* `emulation` is the "root" of this project. It handles GameBoy emulation, allows users to parse the game state, and tracks relevant game state information at every step of gameplay. Look here if you want to:
    - Parse the game state to extract relevant information (e.g. Player location, current party, inventory items).
    - Check for specific triggers or events in the game (e.g. Did the player open the menu? Did the player enter a battle?).
    - Track specific metrics or information over multiple steps of gameplay (e.g. Number of regions visited, number of battles won, etc).
    - Change how the game is run (e.g. automatically skip dialogues and cutscenes, etc).
* `interface` is where we create the actions that agents can take in the game (e.g. `Seek(looking for prof oak, npc)` that tries to locate an NPC on the screen, determine which one is prof oak, move towards him and then interact with him, all in one command). The submodule also has the Gym API integration which allows us to train RL agents on top of the game. Look here if you want to:
    - Create new high level actions, which compose multiple button presses into a single action. These actions can use VLMs to help guide their behavior (e.g. using VLMs to determine which grid cell of the screen contains the target object to interact with).
    - Create new environments or test scenarios, with different observation spaces, reward functions, and termination conditions for the game.


### Notable API Imports
**Utils Submodule:**
* `get_benchmark_tasks_dfs`: Function to get benchmark tasks for evaluating agents in different game variants.

**Emulation Submodule:**
* `AVAILABLE_GAMES`: List of available game variants supported by the package.
* `get_emulator`: Factory function to get an emulator instance for a specified game variant.
* `get_available_init_states`: Function to get a list of available initial states for a specified game variant.
* `clear_tmp_sessions`: Function to clear temporary emulator sessions.

**Interface Submodule:**
* `AVAILABLE_BENCHMARKS`: List of available benchmark modules for evaluating agents.
* `get_environment`: Factory function to get an environment instance for a specified game variant and environment variant.
* `get_test_environment`: Function to create a test environment based on a benchmark task.
* `get_training_environments_kwargs`: Function to get keyword arguments for creating training environments for a specified game variant.
* `get_shifted_environments_kwargs`: Function to get keyword arguments for creating shifted environments for domain adaptation experiments.

"""

from gameboy_worlds.utils import get_benchmark_tasks_dfs

from gameboy_worlds.emulation.registry import (
    AVAILABLE_GAMES,
    get_emulator,
    get_available_init_states,
)
from gameboy_worlds.interface.registry import (
    AVAILABLE_BENCHMARKS,
    get_environment,
    get_test_environment,
    get_training_environments_kwargs,
    get_shifted_environments_kwargs,
)
from gameboy_worlds.emulation import clear_tmp_sessions
