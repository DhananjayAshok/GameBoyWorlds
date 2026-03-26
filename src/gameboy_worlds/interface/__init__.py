"""
This submodule handles the interface between the emulator and external agents. The core classes here are:

1. `HighLevelAction`: The base class for all high level actions that can be executed on the emulator. Handles the logic of mapping high level actions to a sequence of low level actions on the emulator and can be seamlessly converted to and from Gym action spaces.
2. `Controller`: Organizes and manages multiple `HighLevelAction` instances, providing a unified Gym action space and methods to execute a variety of high level actions on the emulator. Especially relevant when the action inputs will come from language based agents (e.g. humans or VLMs), this class maps input strings to specific high level actions.
3. `Environment`: The class that implements the Gym API, combining an `Emulator` and a `Controller` to provide observations, rewards, and episode termination logic.

You can skim the abstract base class documentation to understand the structure they follow, but where you focus will depend on your goals:
* If you want to implement new high level actions, focus on the `HighLevelAction` class and its methods.
* If you want to implement new environments or test scenarios, focus on the `Environment` class and its methods.
"""

from gameboy_worlds.interface.action import HighLevelAction
from gameboy_worlds.interface.controller import Controller
from gameboy_worlds.interface.environment import Environment
