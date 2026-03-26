from gameboy_worlds.emulation.hamtaro.base_metrics import HamtaroCoreMetrics
from gameboy_worlds.emulation.tracker import StateTracker


class HamtaroTracker(StateTracker):
    """Minimal tracker scaffold for Hamtaro variants."""

    def start(self):
        super().start()
        self.metric_classes.extend([HamtaroCoreMetrics])
