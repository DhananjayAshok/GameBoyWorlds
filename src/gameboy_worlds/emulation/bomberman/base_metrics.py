from typing import Optional

import numpy as np

from gameboy_worlds.emulation.tracker import MetricGroup, OCRegionMetric
from gameboy_worlds.emulation.bomberman.parsers import (
    BombermanMaxParser,
    BombermanPocketParser,
    BombermanQuestParser,
)


class BombermanCoreMetrics(MetricGroup):
    METRIC_METHODS = {}

    def reset(self, first=False):
        for metric_name in self.METRIC_METHODS:
            setattr(self, metric_name, False)

    def close(self):
        self.reset()

    def step(self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]):
        for metric_name, parser_method in self.METRIC_METHODS.items():
            if callable(parser_method):
                value = parser_method(self.state_parser, current_frame)
            else:
                value = getattr(self.state_parser, parser_method)(current_frame)
            setattr(self, metric_name, value)

    def report(self) -> dict:
        return {metric_name: getattr(self, metric_name) for metric_name in self.METRIC_METHODS}

    def report_final(self) -> dict:
        return {}


class BombermanMaxCoreMetrics(BombermanCoreMetrics):
    NAME = "bomberman_max_core"
    REQUIRED_PARSER = BombermanMaxParser
    METRIC_METHODS = {
        "is_in_menu": "is_in_menu",
        "is_in_battle": "is_in_battle",
        "is_in_charabom_select": "is_in_charabom_select",
        "is_stage_briefing": "is_stage_briefing_active",
    }


class BombermanPocketCoreMetrics(BombermanCoreMetrics):
    NAME = "bomberman_pocket_core"
    REQUIRED_PARSER = BombermanPocketParser
    METRIC_METHODS = {
        "is_in_menu": "is_in_menu",
        "is_paused": "is_paused",
    }


class BombermanQuestCoreMetrics(BombermanCoreMetrics):
    NAME = "bomberman_quest_core"
    REQUIRED_PARSER = BombermanQuestParser
    METRIC_METHODS = {
        "is_in_menu": "is_in_menu",
        "is_in_dialogue": "is_in_dialogue",
        "is_in_npc_dialogue": "is_in_npc_dialogue",
        "is_reading_sign": "is_reading_sign",
        "is_in_battle": "is_in_battle",
    }


class BombermanQuestOCRMetric(OCRegionMetric):
    REQUIRED_PARSER = BombermanQuestParser

    @property
    def parser(self) -> BombermanQuestParser:
        return self.state_parser  # type: ignore

    def start(self):
        self.kinds = {"dialogue": "dialogue_box"}
        super().start()

    def can_read_kind(self, current_frame: np.ndarray, kind: str) -> bool:
        if kind == "dialogue":
            return self.parser.is_in_dialogue(current_frame)
        return False


class BombermanPocketOCRMetric(OCRegionMetric):
    REQUIRED_PARSER = BombermanPocketParser

    @property
    def parser(self) -> BombermanPocketParser:
        return self.state_parser  # type: ignore

    def start(self):
        self.kinds = {"area_intro": "area_intro_block"}
        super().start()

    def can_read_kind(self, current_frame: np.ndarray, kind: str) -> bool:
        if kind == "area_intro":
            return self.parser.is_in_any_area_intro(current_frame)
        return False


class BombermanMaxOCRMetric(OCRegionMetric):
    REQUIRED_PARSER = BombermanMaxParser

    @property
    def parser(self) -> BombermanMaxParser:
        return self.state_parser  # type: ignore

    def start(self):
        self.kinds = {"stage_briefing": "stage_briefing_box"}
        super().start()

    def can_read_kind(self, current_frame: np.ndarray, kind: str) -> bool:
        if kind == "stage_briefing":
            return self.parser.is_stage_briefing_active(current_frame)
        return False
