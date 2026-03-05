<div align="center">
  <picture>
    <img alt="Gameboy Environments" src="assets/logo_tilt.png" width="350px" style="max-width: 100%;">
  </picture>
  <br>
  
  **Building Intelligent and General Pokémon Agents**
  
  <br>
    <a href="https://github.com/DhananjayAshok/PokeWorlds/blob/main/LICENSE" target="_blank" rel="noopener noreferrer"><img alt="GitHub" src="https://img.shields.io/badge/license-MIT-blue"></a>
    <a href="https://dhananjayashok.github.io/" target="_blank" rel="noopener noreferrer"><img alt="Documentation" src="https://img.shields.io/website/http/huggingface.co/docs/transformers/index.svg?down_color=red&down_message=offline&up_message=online"></a>
    <a href="https://dhananjayashok.github.io/PokeWorlds/" target="_blank" rel="noopener noreferrer"><img alt="GitHub" src="https://img.shields.io/badge/documentation-pdoc-red"></a>
</div>


<img src="assets/logo.png" width="70px"> is an AI research framework for training and evaluating generally capable agents in the world of Pokémon, complete with flexible Python simulators and unified environment wrappers around Gen I and Gen II Pokémon games. 

![](assets/worlds_random.gif)


Challenge your agents to explore, build general skills and master one of the most iconic game universes ever created.

# Core Features

**Gym Interface For GameBoy Games:**
<img src="assets/logo.png" width="70px"> bridges the gap between the GameBoy / GameBoyColour [emulators](https://docs.pyboy.dk/) and the standard Reinforcement Learning [Gym](https://gymnasium.farama.org/) API. Users can quickly develop agents to play through the game, and test them in a variety of scenarios across multiple game versions. 

**Lightweight Environment Parsing:**
<img src="assets/logo.png" width="70px"> provides simple mechanisms to determine the basic state of the agent and identify specific event triggers that occur in the game, allowing one to form descriptive state spaces and track a broad range of metrics over playthroughs. 

**Abstracted Action Space and Low Level Controllers:**
While all games can be played with joystick inputs and a few buttons, not all inputs are meaningful at all times (e.g. when in dialogue, the agent cannot perform any action until the conversation is complete, temporarily reducing the meaningful action space to a single button.) Another major hurdle to progress is the difficulty of learning how abstract actions (e.g. "Open the player menu") correspond to low level game console inputs (e.g. Click 'Start' and then move in the menu until you are on the 'Player' option, then click 'A').

<img src="assets/logo.png" width="70"> allows language-capable agents to play the game without any awareness of the buttons, and perform actions purely by verbalising its intent (e.g. "openmenu(player)"). Our low-level controllers then process the request and convert it into the required sequence of button inputs, providing a layer of abstraction. 


**General and "Unleaked" Test Environments:**
<img src="assets/logo.png" width="70"> not only supports classic titles like PokémonRed and PokémonCrystal, but also includes multiple fan-made variants such as [PokémonPrism](https://rainbowdevs.com/title/prism/), that place the agent in completely new regions, sometimes with  fan-made Pokémon ([Fakémon](https://en.wikipedia.org/wiki/Fakemon)). The research value of these fan-made games is considerable:

* Fan-made games are an ideal environment to test the *generalization* capabilities of an agent trained in the original games. To perform well in these unseen environments, agents must learn transferrable skills like battle competence and maze navigation, as opposed to memorizing the solutions to the original games.
* Unlike the original games, fan-made games are scarcely documented and so models trained on internet-scale corpora (e.g. Large Language Models) are unlikely to have already acquired a rich base of knowledge regarding the game areas or particular Fakémon. While good performance in PokémonRed may be a result of the backbone model's data being contaminated with walkthroughs and internet guides, the same concern is far less valid for more obscure fan-made games.

# Table of Contents

- [Installation](#Installation)
- [Quickstart](#Quickstart)
- [Developer Tools](#Development)

# Installation

The installation consists of four steps:
1. Environment Setup
2. Storage Directory Configuration
3. ROM Setup
4. Final test

## Environment Setup
Create and activate a virtual environment with [uv](https://docs.astral.sh/uv/), a fast Rust-based Python package and project manager.

```bash
uv venv /path/to/env --python=3.12
```

This may be a pre-existing environment for another project. Then, source the environment
* On Windows:
```powershell
/path/to/env/Scripts/Activate
```
* On Linux:
```bash
source /path/to/env/bin/activate
```

Then, clone the <img src="assets/logo.png" width="70"> repo and install it as a `pip` package:
```
git clone https://github.com/DhananjayAshok/PokeWorlds
cd PokeWorlds
uv pip install -e "."
```

If you are in a headless environment, running with this configuration may fail. In that case try:
```
uv pip uninstall opencv-python
uv pip install opencv-python-headless
```

You can now `import gameboy_worlds` from anywhere. But you can't really run anything just yet. 

## Storage Directory Configuration

By default, this project assumes that you can store files and emulator outputs (logs, screenshots, video captures etc.) in the `storage` folder under the root directory of the project. Some people may want to store this in a different location (e.g. if your storage on the root system is limited). If you wish to set a different location for storage, edit the appropriate configuration setting in the [config file](configs/private_vars.yaml).

When you are happy with the `storage` destination, run the following command:
```python
bash sync_all.sh
```
If you do not have `bash` (e.g. on Windows), run:
```python
python -m gameboy_worlds.setup_data pull --game all
```


## ROM Setup

Next, you must legally acquire ROMs for Pokémon from Nintendo (perhaps by dumping the ROM file from your own catridge). Despite how easy they are to obtain, we discourage any attempts to use <img src="assets/logo.png" width="70"> with unofficialy downloaded ROMs. The following base game ROMs are supported:
* Pokémon Red (save as `PokemonRed.gb`)
* Pokémon Crystal (save as `PokemonCrystal.gbc`)

Additionally, our testing environment uses several Pokémon ROM patches / hacks that alter the game in some way. The official way to acquire these can be obtained is by applying a "patch" to the original ROM. After patching the original ROM, you will be left with a `.gb` or `.gbc` file. Once again, despite their widespread availability, we do not advise you to download the pre-patched ROMs. We support:
* [Pokémon Brown](https://rainbowdevs.com/title/brown/) (save as `PokemonBrown.gbc`)
* [Pokémon Prism](https://rainbowdevs.com/title/prism/) (save as `PokemonPrism.gbc`)
* [Pokémon Fool's Gold](https://www.pokecommunity.com/threads/pok%C3%A9mon-fools-gold-a-hack-of-crystal-where-everything-is-familiar-yet-different.433723/) (save as `PokemonFoolsGold.gbc`)
* [Pokémon Star Beasts](https://www.pokecommunity.com/threads/star-beasts-asteroid-version.530552/) (save as `PokemonStarBeasts.gb`)

Once you have a ROM (`.gb` or `.gbc` file), place it in the appropriate path. For example, the ROM for Pokémon Red should be placed in `<path_to_storage_directory_from_config>/rom_data/pokemon_red/PokemonRed.gb`. See the [config folder](configs/) for the expected path to each supported game. 

## Test

Check that setup is fine by running (requires a screen to render):
```bash
python demos/emulator.py
```
This should open up a GameBoy window where you can play the Pokémon Red game. 

To try a headless test / see how a random agent does, try:
```bash
python demos/emulator.py --play_mode random --save_video True # You can see this in headed mode with --headless False
```
The video gets saved to the `sessions` folder of your `storage_dir` directory.

You can also test the Gym compatible environment version of this with:
```bash
python demos/environment.py --play_mode random # run with --render True to see the screen
```

To test all the supported variants, run:
```bash
bash quick_tests.sh
```


# Quickstart

It doesn't take much to get started in <img src="assets/logo.png" width="70">. Below is a simple [example](demos/environment.py) of an agent that takes random actions in Pokémon Red:
```python
from gameboy_worlds import get_environment

# Get the Pokémon Red environment
environment = get_environment(game="pokemon_red", environment_variant="dummy", controller_variant="low_level", headless=True) 
# set headless=False to see the screen

# Run an episode in the environment
done = False
while not done:
  # Pick a random action from the available options
  action = environment.action_space.sample()
  # Make a step with the action
  observation, reward, terminated, truncated, info = environment.step(action)
  done = terminated or truncated
environment.close()
print(f"Done with episode:")
print(environment.get_final_info())
```

This agent seems to open the menus a lot. We can avoid this by abstracting away the action space to a higher level. To do this, simply switch the `controller_variant` to `low_level_play`.


# Development
For a detailed guide on implementing new features and development with <img src="assets/logo.png" width="70">, see the [developer guide](README_dev.md).




```bibtex
```
