"""
Screen-only checks for fades and blank transition screens.

A fade changes the palette, not the picture: every shade moves together towards one colour (black in Pokemon Red,
white in Pokemon Crystal) until the screen is a single colour, and then the next screen fades in. These checks only
look at pixel values. The thresholds are tuned on Pokemon Red, Crystal, Brown and Prism.
"""

from typing import Optional

import numpy as np

BLANK_FRACTION = 0.9
""" A blank frame has at least this fraction of its pixels in one shade... """

BLANK_MAX_RANGE = 100
""" ...and its darkest and lightest shades at most this far apart. Menus and battle screens are mostly white too, but their text is black. """

MIN_CHANGED_FRACTION = 0.05
""" A recolouring changes at least this fraction of the pixels. """

MIN_TONE_CONSISTENCY = 0.9
""" In a recolouring, at least this fraction of the pixels follow one old-shade to new-shade mapping. """

MIN_CONTRAST_CHANGE = 0.25
""" In a recolouring, the contrast changes by at least this fraction of the larger of the two contrasts. """


def _gray(frame: np.ndarray) -> np.ndarray:
    frame = np.asarray(frame)
    return frame[..., 0] if frame.ndim == 3 else frame


def _contrast(frame: np.ndarray) -> float:
    low, high = np.percentile(frame, [5, 95])
    return float(high - low)


def _tone_consistency(previous: np.ndarray, current: np.ndarray) -> float:
    pairs = np.bincount(
        previous.ravel().astype(np.int64) * 256 + current.ravel(), minlength=256 * 256
    )
    return pairs.reshape(256, 256).max(axis=1).sum() / previous.size


def is_blank(frame: np.ndarray) -> bool:
    """
    Checks whether the screen is (nearly) a single shade, as in the middle of a fade or on a transition screen.

    Args:
        frame (np.ndarray): The screen frame.
    Returns:
        bool: True if the frame is blank.
    """
    frame = _gray(frame)
    dominant = np.bincount(frame.ravel()).max() / frame.size
    return (
        dominant >= BLANK_FRACTION
        and int(frame.max()) - int(frame.min()) <= BLANK_MAX_RANGE
    )


def is_recoloured(previous: np.ndarray, current: np.ndarray) -> bool:
    """
    Checks whether ``current`` is ``previous`` with its shades remapped and its contrast clearly changed, as in one step of a fade.

    Args:
        previous (np.ndarray): The earlier screen frame.
        current (np.ndarray): The later screen frame.
    Returns:
        bool: True if ``current`` is a recolouring of ``previous``.
    """
    previous, current = _gray(previous), _gray(current)
    if (previous != current).mean() < MIN_CHANGED_FRACTION:
        return False
    before, after = _contrast(previous), _contrast(current)
    if abs(before - after) < MIN_CONTRAST_CHANGE * max(before, after, 1.0):
        return False
    return _tone_consistency(previous, current) >= MIN_TONE_CONSISTENCY


def is_fading(current: np.ndarray, previous: Optional[np.ndarray] = None) -> bool:
    """
    Checks whether the screen is in a fade: blank, or one fade step away from the frame before it.

    Args:
        current (np.ndarray): The current screen frame.
        previous (Optional[np.ndarray]): The frame before it, if known.
    Returns:
        bool: True if the screen is fading.
    """
    if is_blank(current):
        return True
    return previous is not None and is_recoloured(previous, current)
