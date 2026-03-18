# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PokeWorlds is an AI research framework for training RL agents in GameBoy games. It bridges PyBoy emulation with the Gymnasium API, supporting Pokémon Red/Crystal/hacks, Zelda, and other titles.

## Setup & Installation

```bash
uv venv /path/to/env --python=3.12
source /path/to/env/bin/activate
uv pip install -e "."

# Headless environments:
uv pip uninstall opencv-python && uv pip install opencv-python-headless

# Download initial game data
python -m gameboy_worlds.setup_data pull --game all
```

`configs/private_vars.yaml` must exist with the `storage_dir` key pointing to where ROMs and save states live (this file is gitignored due to sensitive paths).

## Common Commands

```bash
# Run demos
python demos/emulator.py --play_mode random --save_video True
python demos/environment.py --play_mode random --render True

# Interactive dev mode
python dev/dev_play.py --game pokemon_red

# Save/manage game states
python dev/save_state.py --game <game> --state_name <name>
python dev/list_states.py
python dev/create_first_state.py --game <game>

# Test all game variants
bash quick_tests.sh

# Sync data with Hugging Face Hub
python -m gameboy_worlds.setup_data push --game pokemon_red
python -m gameboy_worlds.setup_data pull --game pokemon_red
```

## Architecture

The codebase has two main layers under `src/gameboy_worlds/`:

### Emulation Layer (`emulation/`)
- **`Emulator`** — wraps PyBoy, handles button presses (`LowLevelActions` enum), frame stepping, save states, video capture
- **`StateParser`** — extracts game state from screen captures (region matching) and WRAM memory reads
- **`StateTracker`** — tracks per-frame events and aggregates metrics over episodes; subclasses define termination/truncation conditions for benchmark tasks
- **`registry.py`** — maps game names → parser/tracker/emulator classes; each game subdirectory has its own registry

### Interface Layer (`interface/`)
- **`Environment`** — `gym.Env` subclass; implements `step()`, `reset()`, `render()`; reward computation lives here
- **`Controller`** — translates actions to button sequences; `LowLevelController` uses raw buttons, high-level controllers expose abstract actions (e.g., "open menu")
- **`registry.py`** — maps game names → environment/controller classes

### Registry Pattern
Both layers use a centralized registry for component discovery. New games are registered in `emulation/<game>/registry.py` and `interface/<game>/registry.py`, then imported into the top-level registries.

### Public API (`__init__.py`)
```python
from gameboy_worlds import get_environment, get_emulator, get_test_environment
from gameboy_worlds import get_benchmark_tasks, AVAILABLE_GAMES, clear_tmp_sessions
```

### Configuration
YAML configs in `configs/` are merged via `utils/parameter_handling.py`:
- `project_vars.yaml` — debug mode, seed, invalid action penalty
- `private_vars.yaml` — `storage_dir` (private, not committed)
- `gameboy_vars.yaml` — emulation speed, text speed, dev flags
- `rom_data_path_vars.yaml` — ROM file paths per game

## Adding a New Game

1. Create `emulation/<game>/` and `interface/<game>/` directories with `__init__.py` and `registry.py`
2. Subclass `StateParser`, `StateTracker`, `Emulator`, `Environment`, and optionally `Controller`
3. Register components in each `registry.py`
4. Add ROM path to `configs/rom_data_path_vars.yaml`
5. Create initial save state with `dev/create_first_state.py`

See `README_dev.md` for detailed walkthroughs on parsers, memory reading, reward functions, and benchmark tasks.
