from gameboy_worlds.emulation.harvest_moon.base_metrics import (
    CoreHarvestMoonMetrics,
    HarvestMoonOCRMetric,
    HarvestMoonTestMetric,
)
from gameboy_worlds.emulation.harvest_moon.test_metrics import (
    CowBarnTerminateMetric,
    OutsideCowBarnSubgoal,
    ChickenCoopTerminateMetric,
    OutsideChickenCoopSubgoal,
)
from gameboy_worlds.utils import log_info
from gameboy_worlds.emulation.tracker import (
    StateTracker,
    TestTrackerMixin,
    DummySubGoalMetric,
    make_subgoal_metric_class,
)
from gameboy_worlds.emulation.harvest_moon.parsers import (
    AgentState,
)
from typing import Optional


class CoreHarvestMoonTracker(StateTracker):
    """
    StateTracker for core Harvest Moon metrics.
    """

    _REMOVE_GRID_OVERLAY = False
    """ Whether to remove the grid overlay drawn by the state parser when the agent is in FREE ROAM. This is useful for VLM based agents may need a coordinate grid overlayed onto the frame, but may cause issues for agents that do not understand that it is not a part of the game. """

    def start(self):
        super().start()
        self.metric_classes.extend([CoreHarvestMoonMetrics, HarvestMoonTestMetric])

    def step(self, *args, **kwargs):
        """
        Calls on super().step(), but then modifies the current frame to overlay the grid if the agent is in FREE ROAM.
        """
        super().step(*args, **kwargs)
        if self._REMOVE_GRID_OVERLAY:
            state = self.episode_metrics["harvest_moon_core"]["agent_state"]
            # if agent_state is in FREE ROAM, draw the grid, otherwise do not
            if state == AgentState.FREE_ROAM:
                screen = self.episode_metrics["core"]["current_frame"]
                screen = self.state_parser.draw_grid_overlay(current_frame=screen)
                self.episode_metrics["core"]["current_frame"] = screen
                previous_screens = self.episode_metrics["core"]["passed_frames"]
                if previous_screens is not None:
                    self.episode_metrics["core"]["passed_frames"][-1, :] = screen


class HarvestMoonOCRTracker(CoreHarvestMoonTracker):
    def start(self):
        super().start()
        self.metric_classes.extend([HarvestMoonOCRMetric])
        
class HarvestMoonTestTracker(TestTrackerMixin, HarvestMoonOCRTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = CowBarnTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric

class HarvestMoonCowBarnTracker(HarvestMoonTestTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = CowBarnTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideCowBarnSubgoal])
    
class HarvestMoonChickenCoopTracker(HarvestMoonTestTracker):
    """
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create a TestTracker for Harvest Moon games.
    """

    TERMINATION_TRUNCATION_METRIC = ChickenCoopTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OutsideChickenCoopSubgoal])
