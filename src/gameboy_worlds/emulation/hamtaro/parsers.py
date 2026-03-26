import os
from enum import Enum

import numpy as np

from gameboy_worlds.utils import verify_parameters, log_error, log_warn
from gameboy_worlds.emulation.parser import NamedScreenRegion, StateParser


class _BaseHamtaroParser(StateParser):
    """
    Minimal parser scaffold for Hamtaro variants.

    This only configures rom_data_path so the base StateParser can run.
    """

    VARIANT = ""

    def __init__(self, pyboy, parameters):
        verify_parameters(parameters)
        variant = self.VARIANT
        if f"{variant}_rom_data_path" not in parameters:
            log_error(
                f"ROM data path not found for variant: {variant}. Add {variant}_rom_data_path to config files.",
                parameters,
            )
        self.rom_data_path = parameters[f"{variant}_rom_data_path"]
        super().__init__(pyboy, parameters)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(variant={self.VARIANT})"


class AgentState(Enum):
    FREE_ROAM = 0
    IN_DIALOGUE = 1
    IN_MENU = 2


class HamtaroStateParser(_BaseHamtaroParser):
    """
    Hamtaro parser with optional reference-region matching.

    If captured reference regions are available under rom_data/captures, they are
    used for menu and dialogue detection. Otherwise the parser falls back to
    broad visual heuristics so dev_play remains usable before bootstrapping.
    """

    REGIONS = [
        ("dialogue_top_border", 8, 96, 144, 4),
        ("dialogue_bottom_border", 8, 140, 144, 4),
        ("menu_top_band", 45, 6, 25, 94),
        ("menu_bottom_band", 10, 100, 135, 10),
    ]

    DIALOGUE_TOP_Y = 96
    DIALOGUE_BOTTOM_Y = 140

    def __init__(self, pyboy, parameters):
        named_regions = []
        super().__init__(pyboy, parameters)
        captures_dir = os.path.join(self.rom_data_path, "captures")
        for region_name, start_x, start_y, width, height in self.REGIONS:
            target_path = os.path.join(captures_dir, region_name)
            if not os.path.exists(f"{target_path}.npy"):
                target_path = None
            region = NamedScreenRegion(
                region_name,
                start_x,
                start_y,
                width,
                height,
                parameters=parameters,
                target_path=target_path,
            )
            expected_shape = (height, width, 1)
            if region.target is not None and region.target.shape != expected_shape:
                log_warn(
                    f"Ignoring stale capture for {region_name}: expected shape {expected_shape}, found {region.target.shape}. Re-capture this region in dev_play.",
                    parameters,
                )
                region.target = None
                region.target_path = None
            named_regions.append(region)
        self.named_screen_regions.update(
            {region.name: region for region in named_regions}
        )

    def _has_target(self, region_name: str) -> bool:
        region = self.named_screen_regions.get(region_name)
        return region is not None and region.target is not None

    def _matches_all_available(self, current_screen: np.ndarray, region_names) -> bool:
        available_regions = [name for name in region_names if self._has_target(name)]
        if len(available_regions) == 0:
            return False
        try:
            return all(
                self.named_region_matches_target(current_screen, region_name)
                for region_name in available_regions
            )
        except (RuntimeError, ValueError):
            return False

    def _row_dark_fraction(self, frame: np.ndarray, row_idx: int) -> float:
        row = frame[row_idx, :, 0]
        return float(np.mean(row < 40))

    def _region_dark_fraction(
        self, frame: np.ndarray, x0: int, y0: int, x1: int, y1: int
    ) -> float:
        region = frame[y0:y1, x0:x1, 0]
        return float(np.mean(region < 90))

    def _region_bright_fraction(
        self, frame: np.ndarray, x0: int, y0: int, x1: int, y1: int
    ) -> float:
        region = frame[y0:y1, x0:x1, 0]
        return float(np.mean(region > 180))

    def is_in_dialogue(self, current_screen: np.ndarray) -> bool:
        if self._matches_all_available(
            current_screen, ["dialogue_top_border", "dialogue_bottom_border"]
        ):
            return True
        top_border = self._row_dark_fraction(current_screen, self.DIALOGUE_TOP_Y)
        bottom_border = self._row_dark_fraction(
            current_screen, self.DIALOGUE_BOTTOM_Y
        )
        text_density = self._region_dark_fraction(current_screen, 12, 108, 148, 132)
        background_brightness = self._region_bright_fraction(
            current_screen, 12, 108, 148, 132
        )
        return (
            top_border > 0.45
            and bottom_border > 0.45
            and text_density > 0.06
            and background_brightness > 0.30
        )

    def is_in_menu(self, current_screen: np.ndarray) -> bool:
        if self._matches_all_available(
            current_screen, ["menu_top_band", "menu_bottom_band"]
        ):
            return True
        if self.is_in_dialogue(current_screen):
            return False
        top_band_dark = self._region_dark_fraction(current_screen, 0, 0, 160, 14)
        bottom_band_dark = self._region_dark_fraction(current_screen, 0, 104, 160, 144)
        center_bright = self._region_bright_fraction(current_screen, 20, 20, 140, 124)
        return top_band_dark > 0.35 and bottom_band_dark > 0.35 and center_bright > 0.2

    def get_agent_state(self, current_screen: np.ndarray) -> AgentState:
        if self.is_in_menu(current_screen):
            return AgentState.IN_MENU
        if self.is_in_dialogue(current_screen):
            return AgentState.IN_DIALOGUE
        return AgentState.FREE_ROAM


class HamtaroHamHamHeartbreakParser(HamtaroStateParser):
    VARIANT = "hamtaro_ham_ham_heartbreak"


class HamtaroHamHamsUniteParser(HamtaroStateParser):
    VARIANT = "hamtaro_ham_hams_unite"
