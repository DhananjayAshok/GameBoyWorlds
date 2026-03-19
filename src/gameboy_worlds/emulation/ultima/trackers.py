from gameboy_worlds.emulation.ultima.base_metrics import CoreUltimaMetrics
from gameboy_worlds.emulation.tracker import StateTracker


class CoreUltimaTracker(StateTracker):
    """
    StateTracker for Ultima: Runes of Virtue.

    Tracks agent_state (in_menu vs free_roam) via CoreUltimaMetrics.
    """

    def start(self):
        super().start()
        self.metric_classes.extend([CoreUltimaMetrics])
