<div align="center">
  <picture>
    <img alt="Pokémon Environments" src="assets/logo_tilt.png" width="350px" style="max-width: 100%;">
  </picture>
  <br>
  
  **Actually Building Intelligent and General Pokémon Agents**
  
  <br>
    <a href="https://github.com/DhananjayAshok/GameBoyWorlds/blob/main/LICENSE" target="_blank" rel="noopener noreferrer"><img alt="GitHub" src="https://img.shields.io/badge/license-MIT-blue"></a>
    <a href="https://dhananjayashok.github.io/" target="_blank" rel="noopener noreferrer"><img alt="Documentation" src="https://img.shields.io/website/http/huggingface.co/docs/transformers/index.svg?down_color=red&down_message=offline&up_message=online"></a>
    <a href="https://dhananjayashok.github.io/GameBoyWorlds/" target="_blank" rel="noopener noreferrer"><img alt="GitHub" src="https://img.shields.io/badge/documentation-pdoc-red"></a>
</div>

<img src="assets/logo.png" width="70px"> is organized into 2 primary modules:
* `emulation`: Handles GameBoy emulation, parsing and state tracking
* `interface`: Implements high level actions, and Gym-compliant environments

See the [API documentation](https://dhananjayashok.github.io/GameBoyWorlds/) to understand the code base, the rest of this document goes into details on how you would implement new features or test tasks in <img src="assets/logo.png" width="70">. 

  - [Custom Starting States](#I-want-to-create-my-own-starting-states)
  - [Descriptive State and Event Tracking](#I-want-to-track-fine-grained-details)
  - [Reward Engineering](#I-want-to-engineer-my-own-reward-functions)
  - [Adding New ROMs](#I-want-to-add-a-new-ROM-Hack)
  - [Adding New Test Tasks] # TODO
  - [Useful things](#useful-things)

### I want to create my own starting states
Easy. The only question is whether you want to save an mGBA state (perhaps you use cheats to lazily put the agent in a very specific state) or save a PyBoy state directly (i.e. you start from an existing state and play to the new state).

**From mGBA state:**

First, start with mGBA and **make sure** to match the text box frame options from the existing default states. This is vital to ensure the state parsing system works. Play till the point you want to replicate with a state and save the game (go to the start menu and save) in the state you want to restore from. This will make a `game_ROMNAME.sav` file in the same directory as the rom file. Then run:

```bash
python dev/save_state.py --game <game> --state_name <name>
```

This will save the state and allows you to load it by specifying it as a state name. 


To get to the state from PyBoy, first make sure the `gameboy_dev_play_stop` parameter is [configured](configs/gameboy_vars.yaml) to `false`. Then, run:
```bash 
python dev/dev_play.py --game <game> --init_state <optional_starting_state>
```

This will run the game with the option to enter dev mode. Play the game like you usually would, until you reach the state you want to save. Then, go to [the gameboy configs](configs/gameboy_vars.yaml) *while* playing the game (at the state you want to save), change the `gameboy_dev_play_stop` parameter to `true` (save the configs file) and then check the terminal. You will get a message with the possible dev actions. The one you're looking for is `s <name>`, which saves the state.

Regardless of how you did it, you can test that your state save worked with:
```bash
python demos/emulator --game <game> --init_state <name>
```

### I want to track fine-grained details
Maybe you want to enhance the observation space of the agent with information about the current playthrough (e.g. current map ID, enemy team level). Perhaps you want to train text-only / weak visual agents, and parse as much of the screen image as possible into numerical signals / text (e.g. your team stats, bag contents). Some might not even care about their agents, but want to have a sophisticated set of metrics that they can look at to assess goal conditions, judge the quality of a playthrough, or [craft a good reward function](#i-want-to-engineer-my-own-reward-functions). 

Whatever your motivation, <img src="assets/logo.png" width="70"> provides a powerful set of approaches for reading game states, and then allows you to aggregate over these values over time to compute useful metrics for reward assignment and evaluation. 

The first thing to do is detect an event at a moment in time. This is done in subclasses of the `StateParser` [object](src/gameboy_worlds//emulation/emulator.py) in one of two ways: 

1. **Emulator Screen Captures:** Often particular game states can be cleanly identified by a unique text popup, or some other characteristic marker on the screen. Any of these can be easily captured and checked with the existing parsing system. For example, the current implementation for Pokémon Red has screen captures set up to identify which starter the player chooses. See the [section below](#state-parser-set-up) for examples of this being done. See the [`StateParser` API documentation](https://dhananjayashok.github.io/GameBoyWorlds/gameboy_worlds/emulation/parser.html) for a quick overview on how this works.  
2. **Memory Slot Hooks:** A strong alternative is to just directly read statistics from the game's WRAM. Visually inaccessible information (e.g. the attack stats of all Pokémon on the opponents team) are often easy to obtain this way. The only catch is, this method relies on knowing which memory slots to look for. That's easy enough for games which have excellent [decompilation guides](https://github.com/pret/pokered/blob/symbols/pokered.sym), but is much harder to do for ROM hacks which may mess around with the slots arbitrarily or less popular games. See the [memory reader](src/gameboy_worlds/emulation/pokemon/parsers.py) state parser to get a sense of how you should go about this. 

These approaches allow your state parsers to give instant-wise decisions or indications when an event has occured. You can then configure your `StateTracker` to use the parser to check for this flag / read this information, and store appropriate metrics. See the existing [parsers](src/gameboy_worlds/emulation/pokemon/parsers.py) and [trackers](src/gameboy_worlds/emulation/pokemon/trackers.py) for examples. 

### I want to add a new ROM Hack or GameBoy Game
Setting up a new game is an easy process at a basic level, but can be an involved endeavour if you want to make the new environment a strong one. Please do reach out to me if you have any questions, and we can work to merge the new ROM into <img src="assets/logo.png" width="70"> together. 

#### Initial Steps:

0. Set the repo to `debug` mode by editing the [config file](configs/project_vars.yaml)
1. Create a `<game>_rom_data_path` parameter in the [configs](configs) (either as a new file or in an existing one)
2. Obtain the ROM and place it in the desired path under the ROM data folder. Remember, the `<game>_rom_data_path` folder is rooted at the `storage_dir` from the [configs](configs/private_vars.yaml). 
4. Go to the [registry](src/gameboy_worlds/emulation/registry.py) and add the ROM name to :
    - `GAME_TO_GB_NAME`: This will be the name the system expects to find in `<storage>/<game>_rom_data_path/` 
    - `_STRONGEST_PARSERS`: with `DummyParser` as the value. 
    - `AVAILABLE_STATE_TRACKERS`: give it a `default` value of `StateTracker`. 
    - `AVAILABLE_EMULATORS`: give it a `default` value of `Emulator`.
5. Run `python dev/create_first_state.py --game <game>`. This will create a default state. You will not be able to run the `Emulator` on this ROM before doing this. 
6. Run `python dev/dev_play.py --game <game>` (with the [`gameboy_dev_play_stop` parameter](configs/gameboy_vars.yaml) set to `false`) and proceed through the game until you reach a satisfactory default starting state. Then, open the [config file](configs/gameboy_vars.yaml) and set `gameboy_dev_play_stop` to `true` and save the config file. This will trigger a dev mode and ask you for a terminal input. Enter `s default` and you will set that as the new default state. Enter `s initial` as well to save it properly. 

I have provided an [example](https://drive.google.com/file/d/1fsMjkOjpbyeLLNxP3JVaj6uVXycwSAVC/view?usp=sharing) video for this process. *Note*: In the video, I set the text speed to fast. This was the wrong choice, and so I have set it to slow in all states. 

#### State Parser Set Up:
The above steps will let you play the game on the emulator, but the real power of this framework is only realized when you get involved and create a proper `StateParser`. As mentioned in the [section above](#i-want-to-track-fine-grained-details), this is done either by reading from gameboy memory states or by setting up screen captures to track events. Here, I detail the screen capture method. 

Simply put, this approach aims to capture a given region of the games frame at the right moment, hence saving what the screen "looks like" when a particular event occurs. For example, in Pokémon, the top right of the screen always has the edge of the player menu, and is hence a reliable signal as to whether or not the player is in the menu. The exact regions and events to capture will depend on the game, but the most important components are:
- `NamedScreenRegion`: Every `StateParser` can define certain boxes within the game screen (e.g. the top right portion where the player menu identifier will pop up). These can linked to one or more reference targets, that you need to manually capture once and save. After you save the target, the `StateParser` allows you to take any game frame, select the region in question, and compare it to the reference image. Once you've designated the named regions in the state parser, run the game in dev play mode, stop the game at the moment you want to capture. Then, run `c <region_name>` to save the screen region at that point. The [Pokémon parsers](src/gameboy_worlds/emulation/pokemon/parsers.py) show a clear example of this, and I have provided an [example](https://drive.google.com/file/d/1EEpoxHAnNwdSMSYcc93xrQCcLzbtVCyX/view?usp=sharing) video of the frames being captured. 

You will know that you have filled out all required regions when you can run `python demos/emulator.py --game <game>` without debug mode. 

To use the `StateParser` you created, make sure to:
- Add the parser to the registry
- Create a `MetricGroup` objects that calls on the parsers methods and capabilities in its `step` method
- Add these `MetricGroup` objects to a `StateParser` and then add that to the registry

#### Enabling Environment
To enable an agent to play the game in a gym-style environment loop, you must create a simple `Environment` subclass with implementations for the abstract methods, and add this to the interface registry. That is now a gym-compliant game environment. 

#### Creating HighLevelActions
The above set up gives you more descriptive state information, but still forces the agents use simple button presses to play the game. You must think of decent actions you can implement, and create `HighLevelAction` subclasses to execute them. 

#### 


### I want to engineer my own reward functions

<img src="assets/logo.png" width="70"> avoids most domain-knowledge specific reward design, with a motivation of having the agent discover the best policy with minimal guidance. But it's absolutely possible to use your knowledge of the game to create sophisticated reward systems, like [other people](https://www.youtube.com/watch?v=DcYLT37ImBY&feature=youtu.be) have. 

You'll likely want to gather as much state and trajectory information as possible, for which you should see the [section above](#I-want-to-create-my-own-starting-states).

Then, you'll want to create your own `Environment` subclass, and configure the reward return. See [`PokemonRedChooseCharmanderFastEnv`](src/gameboy_worlds/interface/pokemon/environments.py#90) for more


### Extras:

**Setup Speedrun Guide:**
I've documented the fastest workflow I have found to capturing all the screens for a Pokémon ROM hack properly. This may come in handy for someone. 

Start by just playing through the game (super high `gameboy_headed_emulation_speed`) and establishing save states for the following:
1. `initial`: Right out of the intro screen with options set to fastest / least animation
2. `starter`: Right before the player needs to make a choice of starter
3. `pokedex`: Not too long after the player obtains the Pokedex, but anywhere you like. 

Then, start with:
```
python dev/dev_play.py --game <game> --init_state initial
```
You can tick off the following captures:
* `dialogue_bottom_right`: usually theres something you can interact with in your starting room
* `menu_top_right`: open the start menu
* `pc_top_left`: there is often a PC in your room
* `player_card_middle`: open your player card
* `map_bottom_right`: usually there's a map around you

Then, switch out to the start choice state with `l starter`. Use this state to capture:
* `dialogue_choice_bottom_right`: confirmation message for starter
* `name_entity_top_left`: give the starter a nickname
* `battle_enemy_hp_text`: either a rival battle or just your first Pokémon battle
* `battle_player_hp_text`: same
* `pokemon_list_hp_text`: can do once you've got the starter

Then honestly you probably want to exit with `e` and start again at the `pokedex` state with:
```bash
python dev/dev_play.py --game <game> --init_state pokedex
```
You'll get a message letting you know what's left. You can finish them all off now. If any of the captures weren't clean and good, you should leave them for the end and override their named screen regions. 

Using this process I'm able to set up all but one capture in [under 10 minutes](https://drive.google.com/file/d/1KkZZe3ON-0EWiBs_EhrAHc9D7lsQmCxW/view?usp=sharing) (the video cuts off with only `pokedex_info_height_text` unassigned because it needs to be manually repositioned as an override region). 

### I want to add a new test task

To create a new test task that automatically detects when an agent succeeds (or fails) at a specific goal, follow these steps:

**1. Create an initial state**
First, create a starting state from which your task is achievable. See the [section above](#i-want-to-create-my-own-starting-states) for detailed instructions on creating states.

**2. Define termination and truncation conditions**
- **Termination**: The goal has been achieved. This should be a reliably reproducible screen element that always appears when the goal is reached (e.g., unique dialogue when defeating a specific trainer). In this framework, termination always equals task success - we avoid failure termination signals to prevent agents from using them as learning feedback.
- **Truncation**: Optional. Cut the episode short when the player can no longer achieve the task (e.g., walked too far away). Maximum environment / emulator steps are handled automatically, so don't bother implementing that. 

**3. Set up parser for screen capture (if needed)**
If your termination condition relies on a specific screen capture not already available in the parser, you'll need to add it. See the [screen capture method](#state-parser-set-up) in the [section above](#i-want-to-track-fine-grained-details) for guidance on capturing named screen regions.

Make sure to use `python -m gameboy_worlds.setup_data push --game <game>` to update the cloud database. 

**4. Create the termination/truncation metric**
Make a child or descendant of the [TerminationTruncationTracker](src/gameboy_worlds/emulation/tracker.py) :
- For termination only: `TerminationMetric` ([line 466](src/gameboy_worlds/emulation/tracker.py:466))
- For both termination and truncation: `TerminationTruncationMetric` ([line 368](src/gameboy_worlds/emulation/tracker.py:368))

If using screen region comparisons (most common), inherit from:
- `RegionMatchTerminationMetric` ([line 717](src/gameboy_worlds/emulation/tracker.py:717))
- `RegionMatchTruncationMetric` ([line 693](src/gameboy_worlds/emulation/tracker.py:693))

Example: [`PokemonCenterTerminateMetric`](src/gameboy_worlds/emulation/pokemon/test_metrics.py:15) inherits from both `RegionMatchTerminationMetric` and `TerminationMetric`.

**5. Create the test tracker**
Most trackers can be created by simply setting the `TERMINATION_TRUNCATION_METRIC` class parameter. See [`PokemonRedCenterTestTracker`](src/gameboy_worlds/emulation/pokemon/trackers.py:72) for an example.

```python
class MyTestTracker(PokemonTestTracker):
    TERMINATION_TRUNCATION_METRIC = MyCustomTerminateMetric
```

**6. Register the tracker**
Add your new tracker to the [`AVAILABLE_STATE_TRACKERS`](src/gameboy_worlds/emulation/registry.py:58) dictionary in the registry with a descriptive name.

**7. Test your implementation**
Verify it works with the test play script:

```bash
python dev/dev_play.py --game <game> --state_tracker_class <your_tracker_name> --init_state <your_start_state>
```

The game should automatically stop when you reach the termination/truncation condition.

*Example video: [here](https://drive.google.com/file/d/1j5u8N1OFm45pa6sf3aGnXxfFyYaDt8Ei/view?usp=sharing)*


### Useful Things

* `demos/environment.py`: You can specify a game, environment_variant or controller_variant to test parsing, HighLevelActions etc.

Everything in `dev`:
* `dev_play.py`: vital for being able to play the game, pause the game and capture the screen or enter a breakpoint. 
* `list_states.py`: prints out all of the states you've saved so far and writes them to `tmp_state_list.csv`

