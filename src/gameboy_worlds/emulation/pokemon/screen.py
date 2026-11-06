"""
Screen-only checks for fades, blank transition screens, and whether the map scrolled.

A fade changes the palette, not the picture: every shade moves together towards one colour (black in Pokemon Red,
white in Pokemon Crystal) until the screen is a single colour, and then the next screen fades in. These checks only
look at pixel values. The thresholds are tuned on Pokemon Red, Crystal, Brown and Prism.
"""

from typing import Optional, Tuple

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


SCROLL_MAX_SHIFT = 32
""" The farthest a scroll is searched, in pixels: a ledge hop moves two cells (32 px) on one press. """

SCROLL_MIN_SHIFT = 2
""" Shifts below this many pixels are not counted as a scroll. """

SCROLL_MARGIN = 0.02
""" A scroll (or its absence) is only called when the best fit beats the other by this fraction of the compared pixels... """

SCROLL_RATIO = 0.6
""" ...and, for a scroll, mismatches at most this fraction of what no shift at all mismatches. """

PLAYER_BOX = (52, 88, 56, 88)
""" Screen rows and columns (y0, y1, x0, x1) left out of the comparison: the player sprite, which turns and animates in place. Generous upward for the Gen 1 sprite offset. """

SCROLL_UNIT = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
""" (dy, dx) of the player's move on screen. The map content moves the other way. """


def _shifted_mismatch(previous: np.ndarray, current: np.ndarray, direction: str, shift: int) -> float:
    dy, dx = SCROLL_UNIT[direction]
    h, w = current.shape
    # the player moved by (dy, dx) * shift, so current[y, x] shows what previous showed at (y + dy*shift, x + dx*shift)
    oy, ox = dy * shift, dx * shift
    ys, xs = slice(max(0, -oy), min(h, h - oy)), slice(max(0, -ox), min(w, w - ox))
    cur = current[ys, xs]
    prev = previous[max(0, oy):max(0, oy) + cur.shape[0], max(0, ox):max(0, ox) + cur.shape[1]]
    keep = np.ones(cur.shape, dtype=bool)
    y0, y1, x0, x1 = PLAYER_BOX
    keep[max(0, y0 - ys.start):max(0, y1 - ys.start), max(0, x0 - xs.start):max(0, x1 - xs.start)] = False
    return float((cur != prev)[keep].mean())


def scroll_shift(previous: np.ndarray, current: np.ndarray, direction: str) -> Tuple[int, float, float]:
    """
    How far, in pixels, the map scrolled under the player between two frames, searched along ``direction``.

    Args:
        previous (np.ndarray): The earlier screen frame.
        current (np.ndarray): The later screen frame.
        direction (str): The direction the player was moving in: up, down, left or right.
    Returns:
        Tuple[int, float, float]: The best-fitting shift of at least SCROLL_MIN_SHIFT pixels, the fraction of pixels it mismatches, and the fraction that no shift at all mismatches.
    """
    previous, current = _gray(previous).astype(np.int16), _gray(current).astype(np.int16)
    still = _shifted_mismatch(previous, current, direction, 0)
    best, best_mismatch = 0, 1.0
    for shift in range(SCROLL_MIN_SHIFT, SCROLL_MAX_SHIFT + 1):
        mismatch = _shifted_mismatch(previous, current, direction, shift)
        if mismatch < best_mismatch:
            best, best_mismatch = shift, mismatch
    return best, best_mismatch, still


def judge_scroll(previous: np.ndarray, current: np.ndarray, direction: str) -> Optional[bool]:
    """
    Whether the map scrolled under the player along ``direction`` between two frames. Tile animations, a turning player and wandering NPCs change pixels without shifting the picture, so they are not mistaken for a step.

    Args:
        previous (np.ndarray): The earlier screen frame.
        current (np.ndarray): The later screen frame.
        direction (str): The direction the player was moving in.
    Returns:
        Optional[bool]: True if the map scrolled, False if it clearly did not, None if the screen cannot tell (a blank screen, or one texture repeating everywhere).
    """
    if direction not in SCROLL_UNIT:
        return None
    _, moved, still = scroll_shift(previous, current, direction)
    if moved < still - SCROLL_MARGIN and moved <= SCROLL_RATIO * still:
        return True
    if still < moved - SCROLL_MARGIN:
        return False
    return None
