from gameboy_worlds.emulation.bomberman.base_metrics import (
    BombermanMaxCoreMetrics,
    BombermanMaxOCRMetric,
    BombermanPocketCoreMetrics,
    BombermanPocketOCRMetric,
    BombermanQuestCoreMetrics,
    BombermanQuestOCRMetric,
)
from gameboy_worlds.emulation.bomberman.test_metrics import (
    BattleActiveTerminateMetric,
    BombSelectOpenTerminateMetric,
    BombComponentSelectTerminateMetric,
    BookReadTerminateMetric,
    BombermanMaxGameOverTerminateMetric,
    BombermanPocketGameOverTerminateMetric,
    BombermanQuestGameOverTerminateMetric,
    BombermanQuestPauseMenuOpenTerminateMetric,
    CharabomSelectOpenTerminateMetric,
    DialogueActiveTerminateMetric,
    EnterCampTerminateMetric,
    ButtonRegionChangedTerminateMetric,
    EnterHouseTerminateMetric,
    AreaIntroTerminateMetric,
    HudBombCountChangedTerminateMetric,
    HudBottomRightChangedTerminateMetric,
    HudChangedTerminateMetric,
    HudPocketEnemyCountChangedTerminateMetric,
    HudEnemyCountChangedTerminateMetric,
    HudFireChangedTerminateMetric,
    HudHeartChangedTerminateMetric,
    JumpLevelSelectTerminateMetric,
    JumpRankingTerminateMetric,
    JumpResultsTerminateMetric,
    NpcDialogueTerminateMetric,
    PauseActiveTerminateMetric,
    PauseMenuOpenTerminateMetric,
    PitchAreaTerminateMetric,
    ShieldSelectTerminateMetric,
    SignDialogueTerminateMetric,
    StageBriefingTerminateMetric,
    StageSelectTerminateMetric,
    WorldClearTerminateMetric,
)
from gameboy_worlds.emulation.tracker import (
    DummySubGoalMetric,
    StateTracker,
    TestTrackerMixin,
)


class BombermanTracker(StateTracker):
    CORE_METRIC_CLASS = None

    def start(self):
        super().start()
        self.metric_classes.extend([self.CORE_METRIC_CLASS])


class BombermanBaseTestTracker(TestTrackerMixin, BombermanTracker):
    TERMINATION_TRUNCATION_METRIC = None
    SUBGOAL_METRIC = DummySubGoalMetric


class BombermanMaxTracker(BombermanTracker):
    CORE_METRIC_CLASS = BombermanMaxCoreMetrics


class BombermanMaxOCRTracker(BombermanMaxTracker):
    def start(self):
        super().start()
        self.metric_classes.extend([BombermanMaxOCRMetric])


class BombermanMaxBaseTestTracker(BombermanBaseTestTracker, BombermanMaxOCRTracker):
    pass


class BombermanMaxPauseMenuTestTracker(BombermanMaxBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = PauseMenuOpenTerminateMetric


class BombermanMaxStageSelectTestTracker(BombermanMaxBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = StageSelectTerminateMetric


class BombermanMaxGameOverTestTracker(BombermanMaxBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = BombermanMaxGameOverTerminateMetric


class BombermanMaxCharabomSelectTestTracker(BombermanMaxBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = CharabomSelectOpenTerminateMetric


class BombermanMaxStageBriefingTestTracker(BombermanMaxBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = StageBriefingTerminateMetric


class BombermanMaxPickupBombUpTestTracker(BombermanMaxBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = HudBombCountChangedTerminateMetric


class BombermanMaxDefeatEnemyTestTracker(BombermanMaxBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = HudEnemyCountChangedTerminateMetric


class BombermanMaxPickupFireUpTestTracker(BombermanMaxBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = HudFireChangedTerminateMetric


class BombermanMaxPitchAreaTestTracker(BombermanMaxBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = PitchAreaTerminateMetric


class BombermanPocketTracker(BombermanTracker):
    CORE_METRIC_CLASS = BombermanPocketCoreMetrics


class BombermanPocketOCRTracker(BombermanPocketTracker):
    def start(self):
        super().start()
        self.metric_classes.extend([BombermanPocketOCRMetric])


class BombermanPocketBaseTestTracker(BombermanBaseTestTracker, BombermanPocketOCRTracker):
    pass


class BombermanPocketPauseMenuTestTracker(BombermanPocketBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = PauseActiveTerminateMetric


class BombermanPocketForestAreaIntroTestTracker(BombermanPocketBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = AreaIntroTerminateMetric


class BombermanPocketOceanAreaIntroTestTracker(BombermanPocketBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = AreaIntroTerminateMetric


class BombermanPocketWorldClearTestTracker(BombermanPocketBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = WorldClearTerminateMetric


class BombermanPocketGameOverTestTracker(BombermanPocketBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = BombermanPocketGameOverTerminateMetric


class BombermanPocketJumpLevelSelectTestTracker(BombermanPocketBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = JumpLevelSelectTerminateMetric


class BombermanPocketJumpResultsTestTracker(BombermanPocketBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = JumpResultsTerminateMetric


class BombermanPocketJumpRankingTestTracker(BombermanPocketBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = JumpRankingTerminateMetric


class BombermanPocketHudChangedTestTracker(BombermanPocketBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = HudChangedTerminateMetric


class BombermanPocketHudEnemyCountChangedTestTracker(BombermanPocketBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = HudPocketEnemyCountChangedTerminateMetric


class BombermanPocketHudBottomRightChangedTestTracker(
    BombermanPocketBaseTestTracker
):
    TERMINATION_TRUNCATION_METRIC = HudBottomRightChangedTerminateMetric


class BombermanPocketHudHeartChangedTestTracker(BombermanPocketBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = HudHeartChangedTerminateMetric


class BombermanQuestTracker(BombermanTracker):
    CORE_METRIC_CLASS = BombermanQuestCoreMetrics


class BombermanQuestOCRTracker(BombermanQuestTracker):
    def start(self):
        super().start()
        self.metric_classes.extend([BombermanQuestOCRMetric])


class BombermanQuestBaseTestTracker(BombermanBaseTestTracker, BombermanQuestOCRTracker):
    pass


class BombermanQuestPauseMenuTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = BombermanQuestPauseMenuOpenTerminateMetric


class BombermanQuestGameOverTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = BombermanQuestGameOverTerminateMetric


class BombermanQuestBombSelectTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = BombSelectOpenTerminateMetric


class BombermanQuestDialogueTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = DialogueActiveTerminateMetric


class BombermanQuestNpcDialogueTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = NpcDialogueTerminateMetric


class BombermanQuestSignDialogueTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = SignDialogueTerminateMetric


class BombermanQuestBattleTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = BattleActiveTerminateMetric



class BombermanQuestShieldSelectTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = ShieldSelectTerminateMetric


class BombermanQuestBombComponentSelectTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = BombComponentSelectTerminateMetric


class BombermanQuestEnterCampTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterCampTerminateMetric


class BombermanQuestEnterHouseTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterHouseTerminateMetric


class BombermanQuestButtonRegionChangedTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = ButtonRegionChangedTerminateMetric


class BombermanQuestBookReadTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = BookReadTerminateMetric
