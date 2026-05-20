from typing import Optional

import numpy as np

from gameboy_worlds.emulation.runes_of_virtue.parsers import (
    RunesOfVirtueStateParser,
)
from gameboy_worlds.emulation.tracker import (
    RegionMatchTerminationOnlyMetric,
    TerminationMetric,
)


class RunesOfVirtue1OpenMenuTerminateMetric(TerminationMetric):
    """Terminates the episode when the player opens the inventory menu in Runes of Virtue 1."""

    REQUIRED_PARSER = RunesOfVirtueStateParser

    def determine_terminated(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ) -> bool:
        all_frames = [current_frame]
        if recent_frames is not None:
            all_frames = recent_frames
        for frame in all_frames:
            self.state_parser: RunesOfVirtueStateParser
            if self.state_parser.is_in_menu(frame):
                return True
        return False


class RunesOfVirtue2OpenMenuTerminateMetric(TerminationMetric):
    """Terminates the episode when the player opens the inventory menu in Runes of Virtue 2."""

    REQUIRED_PARSER = RunesOfVirtueStateParser

    def determine_terminated(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ) -> bool:
        all_frames = [current_frame]
        if recent_frames is not None:
            all_frames = recent_frames
        for frame in all_frames:
            self.state_parser: RunesOfVirtueStateParser
            if self.state_parser.is_in_menu(frame):
                return True
        return False


class RunesOfVirtue1KingDialogTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when the king's dialog is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "king_dialog_indicator"
    _TERMINATION_TARGET_NAME = "king_dialog"


class RunesOfVirtue2ReadBookTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when an opened book is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "book_open"


class RunesOfVirtue2NystulDialogTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when Nystul's dialog is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "dialog_indicator"
    _TERMINATION_TARGET_NAME = "nystul_dialog"


class RunesOfVirtue2BlacksmithFailBuyShieldTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the blacksmith's failed shield purchase dialog is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "dialog_indicator"
    _TERMINATION_TARGET_NAME = "blacksmith_fail_buy_shield"


class RunesOfVirtue2SherryMouseDialogTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when Sherry the mouse's dialog is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "dialog_indicator"
    _TERMINATION_TARGET_NAME = "sherry_mouse_dialog"


class RunesOfVirtue2SandyCookDialogTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when Sandy the cook's dialog is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "dialog_indicator"
    _TERMINATION_TARGET_NAME = "sandy_cook_dialog"


class RunesOfVirtue2LordWhitsaberDialogTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when Lord Whitsaber's dialog is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "dialog_indicator"
    _TERMINATION_TARGET_NAME = "lord_whitsaber_dialog"


class RunesOfVirtue2CaveOfDishonourTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when the player has entered the Cave of Dishonour."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cave_of_dishonour"


class RunesOfVirtue2CavernOfHatredTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when the player has entered the Cavern of Hatred."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_hatred"


class RunesOfVirtue2CaveOfDishonourLadder1TerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player reaches the first ladder in the Cave of Dishonour."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cave_of_dishonour_ladder_1"


class RunesOfVirtue2DeathScreenTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when the death / game over screen is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "death_screen_indicator"
    _TERMINATION_TARGET_NAME = "death_screen"


class RunesOfVirtue1ChucklesDialogTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when Chuckles's dialog is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "dialog_indicator"
    _TERMINATION_TARGET_NAME = "chuckles_dialog"


class RunesOfVirtue1GnuGnu1DialogTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when Gnu Gnu's 1st store dialog is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "dialog_indicator"
    _TERMINATION_TARGET_NAME = "gnu_gnu_1_dialog"


class RunesOfVirtue1GnuGnu2DialogTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when Gnu Gnu's 2nd store dialog is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "dialog_indicator"
    _TERMINATION_TARGET_NAME = "gnu_gnu_2_dialog"


class RunesOfVirtue1SherryDialogTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when Sherry's dialog is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "dialog_indicator"
    _TERMINATION_TARGET_NAME = "sherry_dialog"


class RunesOfVirtue1CaveOfDeceitTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when the player is inside the Cave of Deceit."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "cave_of_deceit_indicator"
    _TERMINATION_TARGET_NAME = "cave_of_deceit"


class RunesOfVirtue1TelescopeViewTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when the telescope view is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "telescope_view_indicator"
    _TERMINATION_TARGET_NAME = "telescope_view"


class RunesOfVirtue1DeathScreenTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when the death / game over screen is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "death_screen_indicator"
    _TERMINATION_TARGET_NAME = "death_screen"
