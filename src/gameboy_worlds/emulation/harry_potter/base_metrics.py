from typing import Optional
from gameboy_worlds.emulation.harry_potter.parsers import _BaseHarryPotterParser
from gameboy_worlds.emulation.tracker import OCRegionMetric
import numpy as np


class HarryPotterOCRMetric(OCRegionMetric):
    """
    Captures dialogue screen regions for OCR when dialogue is active in Harry Potter games.
    Does not perform OCR itself — exposes captured regions as numpy arrays
    in the info dict for downstream agents/tools to process.

    Requires the parser to have:
    - A "dialogue_box_full" named screen region (the full dialogue area to capture)
    - dialogue_box_open() and dialogue_box_empty() methods

    Reports (via OCRegionMetric):
    - ocr_regions: Dict mapping "dialogue" -> np.ndarray of shape (n, h, w, c)
    - step: The step number when OCR text was detected
    """

    REQUIRED_PARSER = _BaseHarryPotterParser

    def start(self):
        self.kinds = {
            "dialogue": "dialogue_box_full",
        }
        super().start()

    def can_read_kind(self, current_frame: np.ndarray, kind: str) -> bool:
        self.state_parser: _BaseHarryPotterParser
        if kind == "dialogue":
            in_dialogue = self.state_parser.dialogue_box_open(current_frame)
            dialogue_empty = self.state_parser.dialogue_box_empty(current_frame)
            return in_dialogue and not dialogue_empty
        return False
