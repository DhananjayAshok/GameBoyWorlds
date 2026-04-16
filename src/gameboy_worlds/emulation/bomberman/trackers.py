from gameboy_worlds.emulation.bomberman.base_metrics import (
    BombermanMaxCoreMetrics,
    BombermanPocketCoreMetrics,
    BombermanQuestCoreMetrics,
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
    CloudAreaIntroTerminateMetric,
    CloudZoneTerminateMetric,
    DesertZoneTerminateMetric,
    DialogueActiveTerminateMetric,
    EnterCampTerminateMetric,
    EvilAreaIntroTerminateMetric,
    FieldZoneTerminateMetric,
    ForestAreaIntroTerminateMetric,
    ForestZoneTerminateMetric,
    HudBombCountChangedTerminateMetric,
    HudBottomRightChangedTerminateMetric,
    HudChangedTerminateMetric,
    HudEnemyCountChangedTerminateMetric,
    HudFireChangedTerminateMetric,
    HudHeartChangedTerminateMetric,
    JumpLevelSelectTerminateMetric,
    JumpRankingTerminateMetric,
    JumpResultsTerminateMetric,
    NpcDialogueTerminateMetric,
    OceanAreaIntroTerminateMetric,
    PauseActiveTerminateMetric,
    PauseMenuOpenTerminateMetric,
    PitchAreaTerminateMetric,
    ShieldSelectTerminateMetric,
    SignDialogueTerminateMetric,
    StageBriefingTerminateMetric,
    StageSelectTerminateMetric,
    WindAreaIntroTerminateMetric,
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


class BombermanMaxBaseTestTracker(BombermanBaseTestTracker, BombermanMaxTracker):
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


class BombermanPocketBaseTestTracker(BombermanBaseTestTracker, BombermanPocketTracker):
    pass


class BombermanPocketPauseMenuTestTracker(BombermanPocketBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = PauseActiveTerminateMetric


class BombermanPocketForestAreaIntroTestTracker(BombermanPocketBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = ForestAreaIntroTerminateMetric


class BombermanPocketOceanAreaIntroTestTracker(BombermanPocketBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = OceanAreaIntroTerminateMetric


class BombermanPocketWindAreaIntroTestTracker(BombermanPocketBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = WindAreaIntroTerminateMetric


class BombermanPocketCloudAreaIntroTestTracker(BombermanPocketBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = CloudAreaIntroTerminateMetric


class BombermanPocketEvilAreaIntroTestTracker(BombermanPocketBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = EvilAreaIntroTerminateMetric


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


class BombermanPocketHudBottomRightChangedTestTracker(
    BombermanPocketBaseTestTracker
):
    TERMINATION_TRUNCATION_METRIC = HudBottomRightChangedTerminateMetric


class BombermanPocketHudHeartChangedTestTracker(BombermanPocketBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = HudHeartChangedTerminateMetric


class BombermanQuestTracker(BombermanTracker):
    CORE_METRIC_CLASS = BombermanQuestCoreMetrics


class BombermanQuestBaseTestTracker(BombermanBaseTestTracker, BombermanQuestTracker):
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


class BombermanQuestFieldZoneTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = FieldZoneTerminateMetric


class BombermanQuestForestZoneTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = ForestZoneTerminateMetric


class BombermanQuestDesertZoneTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = DesertZoneTerminateMetric


class BombermanQuestCloudZoneTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = CloudZoneTerminateMetric


class BombermanQuestShieldSelectTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = ShieldSelectTerminateMetric


class BombermanQuestBombComponentSelectTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = BombComponentSelectTerminateMetric


class BombermanQuestEnterCampTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = EnterCampTerminateMetric


class BombermanQuestBookReadTestTracker(BombermanQuestBaseTestTracker):
    TERMINATION_TRUNCATION_METRIC = BookReadTerminateMetric
