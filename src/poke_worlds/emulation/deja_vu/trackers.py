from poke_worlds.utils import log_info
from poke_worlds.emulation.tracker import MetricGroup, StateTracker, OCRegionMetric, TestTrackerMixin
from poke_worlds.emulation.deja_vu.parsers import (
    DejaVuStateParser,
    AgentState,
    # BaseDejaVu1StateParser,
    # MemoryBasedDejaVuStateParser,
)
from poke_worlds.emulation.deja_vu.base_metrics import (
    DejaVuTestMetric,
    CoreDejaVuMetrics,
    DejaVuOCRMetric,
)
from typing import Optional, Type
import numpy as np

class CoreDejaVuTracker(StateTracker):
    """
    StateTracker for core Deja Vu metrics.
    """

    _REMOVE_GRID_OVERLAY = False
    """ Whether to remove the grid overlay drawn by the state parser when the agent is in FREE ROAM. This is useful for VLM based agents may need a coordinate grid overlayed onto the frame, but may cause issues for agents that do not understand that it is not a part of the game. """


    def start(self):
        super().start()
        self.metric_classes.extend([CoreDejaVuMetrics, DejaVuTestMetric])

    def step(self, *args, **kwargs):
        """
        Calls on super().step(), but then modifies the current frame to overlay the grid if the agent is in FREE ROAM.
        """
        super().step(*args, **kwargs)
        
        if self._REMOVE_GRID_OVERLAY:
            state = self.episode_metrics["dejavu_core"]["agent_state"]
            # if agent_state is in FREE ROAM, draw the grid, otherwise do not
            if state == AgentState.FREE_ROAM:
                screen = self.episode_metrics["core"]["current_frame"]
                screen = self.state_parser.draw_grid_overlay(current_frame=screen)
                self.episode_metrics["core"]["current_frame"] = screen
                previous_screens = self.episode_metrics["core"]["passed_frames"]
                if previous_screens is not None:
                    self.episode_metrics["core"]["passed_frames"][-1, :] = screen


class DejaVuOCRTracker(CoreDejaVuTracker):
    def start(self):
        super().start()
        self.metric_classes.extend([DejaVuOCRMetric])


class DejaVuTestTracker(TestTrackerMixin, DejaVuOCRTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Deja Vu games.
    """

    TERMINATION_TRUNCATION_METRIC = None  # Must be set by subclass
