from typing import Optional, Dict, Any, List, Tuple

from gymnasium import spaces

from poke_worlds.emulation.deja_vu.base_metrics import CoreDejaVuMetrics
from poke_worlds.utils import load_parameters, log_dict, log_info
from poke_worlds.emulation.deja_vu.emulators import DejaVuEmulator
from poke_worlds.emulation.deja_vu.trackers import (
    DejaVuOCRTracker,
    CoreDejaVuTracker,
    # DejaVuEnterCastleTestTracker,
)
from poke_worlds.emulation.deja_vu.parsers import AgentState
from poke_worlds.interface.environment import (
    DummyEnvironment,
    Environment,
    TestEnvironmentMixin,
)
from poke_worlds.interface.controller import Controller

import gymnasium as gym
import numpy as np


class DejaVuEnvironment(DummyEnvironment):
    """
    A basic Deja Vu Environment.
    
    Deja Vu is a detective mystery game focused on investigation and puzzle-solving.
    The game mechanics include exploration, dialogue interactions, and deduction puzzles.
    """

    REQUIRED_EMULATOR = DejaVuEmulator
    REQUIRED_STATE_TRACKER = CoreDejaVuMetrics


class DejaVuOCREnvironment(DejaVuEnvironment):
    """
    A Deja Vu Environment that includes OCR region captures and agent state.
    
    Provides screen pixels and agent state information for vision-based agents.
    Agent state includes: Free Roam, In Dialogue, In Menu, In Puzzle.
    """

    REQUIRED_STATE_TRACKER = DejaVuOCRTracker
    REQUIRED_EMULATOR = DejaVuEmulator

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def override_emulator_kwargs(emulator_kwargs: dict) -> dict:
        required_tracker = DejaVuOCRTracker
        Environment.override_state_tracker_class(emulator_kwargs, required_tracker)
        return emulator_kwargs


class DejaVuTestEnvironment(TestEnvironmentMixin, DejaVuOCREnvironment):
    """
    A test environment for Deja Vu that integrates testing utilities with OCR capabilities.
    """
    pass


# class DejaVuEnterCastleEnv(Environment):
#     """
#     A Deja Vu environment where the agent must enter the castle as quickly as possible.
    
#     This is a simplified investigation task that measures the agent's ability to navigate
#     the game world and complete a basic objective. The agent is rewarded for reaching
#     the castle location and completing the entry sequence.
#     """

#     REQUIRED_TRACKER = DejaVuEnterCastleTestTracker

#     def __init__(
#         self,
#         emulator: DejaVuEmulator,
#         controller: Controller,
#         parameters: Optional[dict] = None,
#     ):
#         """
#         Initializes the Environment with the given emulator and controller.
#         """
#         self._parameters = load_parameters(parameters)
#         self._emulator = emulator
#         self._controller = controller
#         # observation space is a dictionary with "location" key containing the (x, y) coordinates of the player
#         # and "facing" key containing the direction the player is facing
#         coord_space = gym.spaces.Box(low=0, high=255, shape=(2,), dtype=np.uint16)
#         direction_space = gym.spaces.Discrete(4)  # Up, Down, Left, Right
#         state_space = gym.spaces.Discrete(4)  # Free Roam, In Dialogue, In Menu, In Puzzle
        
#         self.observation_space = gym.spaces.Dict(
#             {
#                 "location": coord_space,
#                 "facing": direction_space,
#                 "state": state_space,
#             }
#         )
#         """ The observation space includes the player location, facing direction, and current agent state. """
#         super().__init__()

#     @staticmethod
#     def override_emulator_kwargs(emulator_kwargs: dict) -> dict:
#         """
#         Override default emulator keyword arguments for this environment.
#         """
#         Environment.override_state_tracker_class(
#             emulator_kwargs, DejaVuEnterCastleTestTracker
#         )
#         return emulator_kwargs

#     def get_observation(self, **kwargs):
#         info = self.get_info()
        
#         # Get player location from the game state
#         location_data = info.get("deja_vu_location", {})
#         location = location_data.get("current_location", [0, 0])
#         coords = np.array(location[:2], dtype=np.uint16)
        
#         # Get player facing direction (if available in state tracking)
#         direction = location_data.get("direction", (1, 0))
#         facing = None
#         if direction == (1, 0):
#             facing = 0  # Right
#         elif direction == (-1, 0):
#             facing = 1  # Left
#         elif direction == (0, -1):
#             facing = 2  # Up
#         elif direction == (0, 1):
#             facing = 3  # Down
#         else:
#             facing = 0  # Default to right
        
#         # Get current agent state
#         agent_state = info.get("dejavu_core", {}).get("agent_state", AgentState.FREE_ROAM)
#         state_value = agent_state.value if isinstance(agent_state, AgentState) else int(agent_state)
        
#         observation = {
#             "location": coords,
#             "facing": facing,
#             "state": state_value,
#         }
#         return observation

#     def determine_terminated(
#         self, start_state, action, action_kwargs, transition_states, action_success
#     ):
#         """
#         Episode terminates when the agent enters the castle.
#         """
#         states = transition_states
#         for state in states:
#             # Check if the castle entry termination metric was triggered
#             if state.get("dejavu_core", {}).get("entered_castle", False):
#                 return True
#         return super().determine_terminated(
#             start_state,
#             action,
#             action_kwargs,
#             transition_states,
#             action_success,
#         )

#     def determine_reward(
#         self, start_state, action, action_kwargs, transition_states, action_success
#     ) -> float:
#         """
#         Reward the agent for entering the castle as quickly as possible.
        
#         Provides guidance through:
#         - Negative reward for excessive exploration time
#         - Small reward for proximity to castle location
#         - Large reward for successfully entering the castle
#         """
#         current_state = transition_states[-1]
        
#         # Check if castle has been entered
#         entered_castle = current_state.get("dejavu_core", {}).get("entered_castle", False)
#         n_steps = current_state["core"]["steps"]
        
#         if entered_castle:
#             # Large reward for entering the castle, with a bonus for speed
#             step_bonus = 200 / (n_steps + 1)
#             return 500.0 + step_bonus
        
#         # Penalty for taking too long without entering the castle
#         if n_steps >= self._emulator.max_steps - 2:
#             return -10.0
        
#         # Get current location for distance-based rewards
#         location_data = current_state.get("deja_vu_location", {})
#         current_location = location_data.get("current_location", [0, 0])
        
#         # Castle location (approximate, can be adjusted based on actual game layout)
#         castle_location = np.array([120, 80], dtype=np.float32)
#         player_pos = np.array(current_location[:2], dtype=np.float32)
        
#         # Calculate euclidean distance to castle
#         distance = np.linalg.norm(player_pos - castle_location)
        
#         # Provide graduated rewards based on distance
#         if distance < 10:
#             return 2.0  # Very close to castle
#         elif distance < 30:
#             return 0.5  # Closer to castle
#         elif distance < 60:
#             return -0.5  # Moving towards castle area
#         else:
#             return -2.0  # Far from castle
