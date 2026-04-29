from typing import Optional

import numpy as np

from gameboy_worlds.emulation.sword_of_hope.parsers import _BaseSwordOfHopeParser
from gameboy_worlds.emulation.tracker import OCRegionMetric


class SwordOfHopeOCRMetric(OCRegionMetric):
    REQUIRED_PARSER = _BaseSwordOfHopeParser

    def reset(self, first=False):
        super().reset(first)

    def start(self):
        self.kinds = {"full_screen": "full_screen"}
        super().start()

    def can_read_kind(self, current_frame: np.ndarray, kind: str) -> bool:
        return True
