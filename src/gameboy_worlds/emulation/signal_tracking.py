from abc import abstractmethod
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from gameboy_worlds.emulation.parser import StateParser
from gameboy_worlds.emulation.tracker import MetricGroup
from gameboy_worlds.utils import log_error

STUCK_AFTER_STEPS = 200


class SignalSeries:
    __slots__ = (
        "current", "previous", "first", "minimum", "maximum", "total", "count",
        "total_increase", "total_decrease", "n_changes", "last_change_step", "changes",
    )

    def __init__(self):
        self.current = None
        self.previous = None
        self.first = None
        self.minimum = None
        self.maximum = None
        self.total = 0.0
        self.count = 0
        self.total_increase = 0.0
        self.total_decrease = 0.0
        self.n_changes = 0
        self.last_change_step = 0
        self.changes: List[Tuple[int, float]] = []

    def update(self, value: float, step: int) -> None:
        if self.current is None:
            self.first = value
            self.minimum = value
            self.maximum = value
            self.changes.append((step, value))
            self.last_change_step = step
        elif value != self.current:
            difference = value - self.current
            if difference > 0:
                self.total_increase += difference
            else:
                self.total_decrease -= difference
            self.n_changes += 1
            self.last_change_step = step
            self.changes.append((step, value))
            self.minimum = min(self.minimum, value)
            self.maximum = max(self.maximum, value)
        self.previous = self.current
        self.current = value
        self.total += value
        self.count += 1

    def summary(self, step: int) -> Dict[str, Any]:
        return {
            "current": self.current,
            "delta": 0 if self.previous is None else self.current - self.previous,
            "change_from_first": self.current - self.first,
            "min": self.minimum,
            "max": self.maximum,
            "mean": self.total / self.count,
            "total_increase": self.total_increase,
            "total_decrease": self.total_decrease,
            "n_changes": self.n_changes,
            "steps_since_change": step - self.last_change_step,
        }


class MemorySignalsMetric(MetricGroup):
    """
    Reports (compact, safe to keep once per step):
    - steps, ready, clock_seconds
    - situational: per-signal summary from SignalSeries.summary
    - progress: per-signal current, peak and the step the peak was first reached
    - exploration, combat, efficiency: UNTESTED, see the comments on each update method

    Full series live on the metric, not in the report, because reports are retained per step:
    tracker.metrics["memory_signals"].history("money") returns (step, value) change points, and
    tracker.metrics["memory_signals"].as_array("money") expands them to one value per step.

    Final Reports:
    - episodes: one report per finished episode.
    """

    NAME = "memory_signals"
    REQUIRED_PARSER = StateParser

    def start(self):
        if not hasattr(self.state_parser, "memory"):
            log_error(
                f"{type(self.state_parser).__name__} has no memory map, so MemorySignalsMetric cannot run.",
                self._parameters,
            )
        self.episodes: List[Dict[str, Any]] = []
        super().start()

    def reset(self, first: bool = False):
        if not first:
            self._record_episode()
        self._episode_recorded = False
        self.steps = 0
        self.ready = False
        self.clock_first: Optional[float] = None
        self.clock_current: Optional[float] = None
        self.situational_series: Dict[str, SignalSeries] = {}
        self.progress_series: Dict[str, SignalSeries] = {}
        self.peak_reached_step: Dict[str, int] = {}
        self.unique_maps = set()
        self.unique_tiles = set()
        self.previous_map = None
        self.previous_tile = None
        self.tile_visits = 0
        self.map_changes = 0
        self.last_new_tile_step = 0
        self.reset_combat()

    def close(self):
        self._record_episode()

    def _record_episode(self) -> None:
        if self.steps > 1 and not self._episode_recorded:
            self.episodes.append(self.report())
            self._episode_recorded = True

    @abstractmethod
    def is_ready(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def read_situational(self) -> Dict[str, Optional[float]]:
        raise NotImplementedError

    @abstractmethod
    def read_progress(self) -> Dict[str, Optional[float]]:
        raise NotImplementedError

    @abstractmethod
    def read_position(self) -> Optional[Tuple[Any, Tuple[int, int], Optional[bool]]]:
        raise NotImplementedError

    def read_clock_seconds(self) -> Optional[float]:
        return None

    def experience_signal(self) -> Optional[str]:
        return None

    def reset_combat(self) -> None:
        self.combat: Dict[str, Any] = {}

    def update_combat(self) -> None:
        return

    def step(self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]):
        self.ready = self.is_ready()
        if not self.ready:
            return
        self.steps += 1
        clock = self.read_clock_seconds()
        if clock is not None:
            if self.clock_first is None:
                self.clock_first = clock
            self.clock_current = clock
        for name, value in self.read_situational().items():
            if value is not None:
                self.situational_series.setdefault(name, SignalSeries()).update(value, self.steps)
        for name, value in self.read_progress().items():
            if value is None:
                continue
            series = self.progress_series.setdefault(name, SignalSeries())
            if series.maximum is None or value > series.maximum:
                self.peak_reached_step[name] = self.steps
            series.update(value, self.steps)
        self.update_exploration()
        self.update_combat()

    # UNTESTED: exploration counters have not been validated against real play.
    # Location is skipped while map_settled is False. Games without that flag (Brown, Prism, Zelda)
    # instead wait until a new map has been seen on two consecutive steps, which has not been shown
    # to remove every stale coordinate read during a warp.
    def update_exploration(self) -> None:
        position = self.read_position()
        if position is None:
            return
        map_key, tile, settled = position
        if settled is False:
            return
        if settled is None and map_key != self.previous_map:
            self.previous_map = map_key
            self.previous_tile = None
            return
        if map_key != self.previous_map:
            self.previous_map = map_key
            self.previous_tile = None
        if map_key not in self.unique_maps:
            if self.unique_maps:
                self.map_changes += 1
            self.unique_maps.add(map_key)
        elif self.previous_tile is None:
            self.map_changes += 1
        location = (map_key, tile)
        if location != self.previous_tile:
            self.tile_visits += 1
            self.previous_tile = location
        if location not in self.unique_tiles:
            self.unique_tiles.add(location)
            self.last_new_tile_step = self.steps

    def exploration_report(self) -> Dict[str, Any]:
        steps_since_new = self.steps - self.last_new_tile_step
        return {
            "unique_maps": len(self.unique_maps),
            "unique_tiles": len(self.unique_tiles),
            "tile_visits": self.tile_visits,
            "revisit_ratio": 1 - len(self.unique_tiles) / self.tile_visits if self.tile_visits else 0.0,
            "map_changes": self.map_changes,
            "steps_since_new_tile": steps_since_new,
            "stuck": steps_since_new >= STUCK_AFTER_STEPS,
        }

    # UNTESTED: efficiency rates depend on the exploration counters and the game clock, and have not
    # been validated against real play. Rates per minute are None for games with no readable clock.
    def efficiency_report(self) -> Dict[str, Any]:
        elapsed = None
        if self.clock_first is not None:
            elapsed = self.clock_current - self.clock_first
        result: Dict[str, Any] = {
            "game_minutes": None if elapsed is None else elapsed / 60,
            "new_tiles_per_100_steps": 100 * len(self.unique_tiles) / self.steps if self.steps else 0.0,
            "milestone_steps": dict(self.peak_reached_step),
        }
        name = self.experience_signal()
        if name in self.progress_series:
            series = self.progress_series[name]
            gained = series.maximum - series.first
            result["experience_per_100_steps"] = 100 * gained / self.steps
            if elapsed:
                result["experience_per_game_minute"] = gained / (elapsed / 60)
        return result

    def report(self) -> Dict[str, Any]:
        return {
            "steps": self.steps,
            "ready": self.ready,
            "clock_seconds": self.clock_current,
            "situational": {
                name: series.summary(self.steps)
                for name, series in self.situational_series.items()
            },
            "progress": {
                name: {
                    "current": series.current,
                    "peak": series.maximum,
                    "peak_reached_step": self.peak_reached_step.get(name),
                }
                for name, series in self.progress_series.items()
            },
            "exploration": self.exploration_report(),
            "combat": dict(self.combat),
            "efficiency": self.efficiency_report(),
        }

    def report_final(self) -> Dict[str, Any]:
        return {"episodes": list(self.episodes)}

    def signal_names(self) -> List[str]:
        return sorted(self.situational_series) + sorted(self.progress_series)

    def _series(self, name: str) -> SignalSeries:
        if name in self.situational_series:
            return self.situational_series[name]
        if name in self.progress_series:
            return self.progress_series[name]
        log_error(
            f"Unknown memory signal '{name}'. Available signals: {self.signal_names()}",
            self._parameters,
        )

    def history(self, name: str) -> List[Tuple[int, float]]:
        return list(self._series(name).changes)

    def as_array(self, name: str) -> np.ndarray:
        changes = self._series(name).changes
        values = np.full(self.steps, np.nan)
        for index, (step, value) in enumerate(changes):
            end = changes[index + 1][0] - 1 if index + 1 < len(changes) else self.steps
            values[step - 1 : end] = value
        return values
