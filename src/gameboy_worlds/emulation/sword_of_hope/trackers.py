from gameboy_worlds.emulation.tracker import (
    StateTracker,
    TestTrackerMixin,
    DummySubGoalMetric,
    make_subgoal_metric_class,
)
from gameboy_worlds.emulation.sword_of_hope.base_metrics import SwordOfHopeOCRMetric
from gameboy_worlds.emulation.sword_of_hope.test_metrics import (
    SoH2DialogueClearedTerminateMetric,
    SoH2DialogueActiveSubGoal,
    SoH2DialogueAdvancedTerminateMetric,
    SoH2DialogueInitiatedSubGoal,
    SoH2ExplorationMenuTerminateMetric,
    SoH2MenuOpenSubGoal,
    SoH2DialogueVisibleSubGoal,
    SoH2FirstAdjacentRoomTerminateMetric,
    SoH2StarterRoomSubGoal,
    MillRoomTerminateMetric,
    ShamanRoomTerminateMetric,
    DialogueClearedTerminateMetric,
    BattleWonTerminateMetric,
    ItemFoundTerminateMetric,
    PurchaseConfirmedTerminateMetric,
    ExplorationMenuTerminateMetric,
    DialogueAdvancedTerminateMetric,
    BattleMagicMenuTerminateMetric,
    TeleportResultTerminateMetric,
    MistressSecondDialogueTerminateMetric,
    SaveConfirmedTerminateMetric,
    HerbReceivedTerminateMetric,
    TrtFruitReceivedTerminateMetric,
    TreantDefeatedTerminateMetric,
    PassageRevealedTerminateMetric,
    GateOpenedTerminateMetric,
    ScrollReceivedTerminateMetric,
    CharmReceivedTerminateMetric,
    TeleportLandedTerminateMetric,
    EscapeConfirmedTerminateMetric,
    OldmanHouseSubGoal,
    InForestSubGoal,
    ShamanHouseSubGoal,
    DialogueActiveSubGoal,
    BattleActiveSubGoal,
    LookSelectedSubGoal,
    LookTargetOptionsSubGoal,
    ShopMenuOpenSubGoal,
    DialogueVisibleSubGoal,
    DialogueInitiatedSubGoal,
    MenuOpenSubGoal,
    MagicMenuOpenSubGoal,
    MistressFirstDialogueSubGoal,
    SavePromptVisibleSubGoal,
    LookPathTargetSubGoal,
    HitTargetShownSubGoal,
    HitWallTargetSubGoal,
    KeyMSelectedSubGoal,
    InBackroomSubGoal,
    GraceSelectedSubGoal,
    TeleportDestCursorSubGoal,
)


class SwordOfHopeOCRTracker(StateTracker):
    """
    Base StateTracker that always captures the full Game Boy screen as an OCR region.
    Used as the default tracker for both Sword of Hope 1 and Sword of Hope 2 so that
    OCR-eligible captures are always available for downstream agents.
    """

    def start(self):
        super().start()
        self.metric_classes.append(SwordOfHopeOCRMetric)


class SwordOfHope1TestTracker(TestTrackerMixin, SwordOfHopeOCRTracker):
    """
    Base TestTracker for Sword of Hope 1.
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create task-specific trackers.
    """

    TERMINATION_TRUNCATION_METRIC = MillRoomTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope2TestTracker(TestTrackerMixin, SwordOfHopeOCRTracker):
    """
    Base TestTracker for Sword of Hope 2.
    Inherit this class and set TERMINATION_TRUNCATION_METRIC to create task-specific trackers.
    """

    TERMINATION_TRUNCATION_METRIC = None
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope2DialogueClearTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the dialogue is cleared and control returns to the player.
    Subgoals: dialogue_active -> (termination) dialogue_cleared.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2DialogueClearedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2DialogueActiveSubGoal])


class SwordOfHope2TalkToNpcTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent talks to an NPC and advances one full dialogue page.
    Subgoals: dialogue_initiated -> (termination) dialogue_advanced.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2DialogueAdvancedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2DialogueInitiatedSubGoal])


class SwordOfHope2MenuOpenCloseTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent closes an open menu and returns to exploration.
    Subgoals: menu_open -> (termination) exploration_menu.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2ExplorationMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2MenuOpenSubGoal])


class SwordOfHope2FirstAdjacentRoomTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent reaches the first adjacent room from the start state
    (room_label/castle_corridor). Subgoal: castle_throne starting room visible.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2FirstAdjacentRoomTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2StarterRoomSubGoal])


class SwordOfHope2OverworldFromDefaultTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent reaches a stable overworld position with no open
    dialogue or menu (the Look/Open/Hit/Use/Magic/Power command grid is showing).
    Subgoals: dialogue_visible -> (termination) exploration_menu.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2ExplorationMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2DialogueVisibleSubGoal])


class SwordOfHope1MillRoomTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent reaches the Mill Room (first adjacent room from start).
    """

    TERMINATION_TRUNCATION_METRIC = MillRoomTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope1ShamanRoomTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent reaches the Shaman's Room.
    Subgoals: in_forest -> shaman_house -> (termination) shaman_room.
    """

    TERMINATION_TRUNCATION_METRIC = ShamanRoomTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([OldmanHouseSubGoal, InForestSubGoal, ShamanHouseSubGoal])


class SwordOfHope1DialogueClearTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the dialogue is cleared and control returns to the player.
    Subgoals: dialogue_active -> (termination) dialogue_cleared.
    """

    TERMINATION_TRUNCATION_METRIC = DialogueClearedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([DialogueActiveSubGoal])


class SwordOfHope1BattleWonTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the battle is won.
    Subgoals: battle_active -> (termination) battle_won.
    """

    TERMINATION_TRUNCATION_METRIC = BattleWonTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([BattleActiveSubGoal])


class SwordOfHope1LookItemTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when a hidden item is found by looking at an object.
    Subgoals: look_selected -> look_target_options -> (termination) item_found.
    """

    TERMINATION_TRUNCATION_METRIC = ItemFoundTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([LookSelectedSubGoal, LookTargetOptionsSubGoal])


class SwordOfHope1BuyItemTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when an item is purchased from a shop.
    Subgoals: shop_menu_open -> (termination) purchase_confirmed.
    """

    TERMINATION_TRUNCATION_METRIC = PurchaseConfirmedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([ShopMenuOpenSubGoal])


class SwordOfHope1OverworldFromDefaultTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent reaches a stable overworld position with no open
    dialogue or menu (the Look/Open/Hit/Use/Magic/Power command grid is showing).
    Subgoals: dialogue_visible -> (termination) exploration_menu.
    """

    TERMINATION_TRUNCATION_METRIC = ExplorationMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([DialogueVisibleSubGoal])


class SwordOfHope1TalkToNpcTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent talks to an NPC and advances one full dialogue page.
    Subgoals: dialogue_initiated -> (termination) dialogue_advanced.
    """

    TERMINATION_TRUNCATION_METRIC = DialogueAdvancedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([DialogueInitiatedSubGoal])


class SwordOfHope1MenuOpenCloseTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent closes an open menu and returns to exploration.
    Starts at menu_example.state (menu already open at t=0).
    Subgoals: menu_open -> (termination) exploration_menu.
    """

    TERMINATION_TRUNCATION_METRIC = ExplorationMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([MenuOpenSubGoal])


class SwordOfHope1BattleMagicCommandTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent selects a non-default battle command (Magic submenu open).
    Starts at battle_example.state (battle active at t=0, FIGHT menu default).
    Subgoals: battle_active -> (termination) battle_magic_menu.
    """

    TERMINATION_TRUNCATION_METRIC = BattleMagicMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([BattleActiveSubGoal])


class SwordOfHope1CastTeleportTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent opens Magic, selects Teleport and sees the result
    (destination list or 'cannot teleport' message).
    Starts at default.state (stable overworld, Lvl 1).
    Subgoals: magic_menu_open -> (termination) teleport_result.
    """

    TERMINATION_TRUNCATION_METRIC = TeleportResultTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([MagicMenuOpenSubGoal])


class SwordOfHope1TalkToNpcMultipleTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent talks to the same NPC twice and sees a distinct
    second-visit dialogue (progression event, e.g. Mistress giving Scroll of Grace).
    Starts at shop_forest.state (near the Mistress at the Forest Shop).
    Subgoals: mistress_first_dialogue -> (termination) mistress_second_dialogue.
    """

    TERMINATION_TRUNCATION_METRIC = MistressSecondDialogueTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([MistressFirstDialogueSubGoal])


class SwordOfHope1BinaryChoiceSaveTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent answers Yes to the Shaman's save prompt.
    Starts at at_shaman.state (player in front of Shaman, ready to talk).
    Subgoals: save_prompt_visible -> (termination) save_confirmed.
    """

    TERMINATION_TRUNCATION_METRIC = SaveConfirmedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SavePromptVisibleSubGoal])


class SwordOfHope1LookSurroundHerbTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent Looks at the Path target at Old Man's Forest [C5]
    and receives a Herb.
    Starts at forest_c5.state (player at [C5] in Old Man's Forest).
    Subgoals: look_path_target -> (termination) herb_received.
    """

    TERMINATION_TRUNCATION_METRIC = HerbReceivedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([LookPathTargetSubGoal])


class SwordOfHope1HitTreantItemTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent Hits the Treant area (post-kill) at Old Man's Forest
    [H2] and receives a TrtFruit (walkthrough event #19).
    Starts at near_treant_postkill.state (player at [H2] with Treant defeated).
    Subgoals: hit_target_shown -> (termination) trtfruit_received.
    """

    TERMINATION_TRUNCATION_METRIC = TrtFruitReceivedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([HitTargetShownSubGoal])


class SwordOfHope1DefeatTreantTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent defeats Treant in battle (walkthrough event #2),
    receiving Key M. Uses offensive magic (Firebal2 strategy, lvl 4+).
    Starts at treant_battle_start.state (Treant battle active, FIGHT menu default).
    Subgoals: battle_active -> (termination) treant_defeated.
    """

    TERMINATION_TRUNCATION_METRIC = TreantDefeatedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([BattleActiveSubGoal])


class SwordOfHope1HitWallPassageTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent Hits the wall at Martel's [B3] doll area and
    reveals an ivy vine passage (walkthrough: 'HIT the wall to reveal a vine').
    Starts at martel_b3.state (player in Martel's Domain at [B3]).
    Subgoals: hit_wall_target -> (termination) passage_revealed.
    """

    TERMINATION_TRUNCATION_METRIC = PassageRevealedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([HitWallTargetSubGoal])


class SwordOfHope1UseKeyUnlockTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent uses Key M at the Martel's Domain gate ([A4] in
    Old Man's Forest) and unlocks the passage to Martel's Domain.
    Starts at at_martel_gate.state (player at [A4] with Key M in inventory, gate still locked).
    Subgoals: key_m_selected -> (termination) gate_opened.
    """

    TERMINATION_TRUNCATION_METRIC = GateOpenedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([KeyMSelectedSubGoal])


class SwordOfHope1CollectScrollGraceTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent picks up the Scroll of Grace from the Forest Shop
    backroom (Old Man's Forest [E2]) after talking to the Mistress twice.
    Starts at mistress_backroom_access.state (player inside the backroom).
    Subgoals: in_backroom -> (termination) scroll_received.
    """

    TERMINATION_TRUNCATION_METRIC = ScrollReceivedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([InBackroomSubGoal])


class SwordOfHope1CastGraceAltarTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent casts the Grace spell at the Martel's Domain [F3]
    altar and receives the Charm (walkthrough event #4).
    Starts at at_martel_altar.state (player at [F3] with Scroll of Grace in inventory).
    Subgoals: grace_selected -> (termination) charm_received.
    """

    TERMINATION_TRUNCATION_METRIC = CharmReceivedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([GraceSelectedSubGoal])


class SwordOfHope1CompleteTeleportTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent completes a Teleport cast and lands at a destination.
    Starts from an overworld state (e.g. default).
    Subgoals: teleport_dest_cursor (destination list visible with cursor on a dest)
    -> (termination) teleport_landed (post-teleport command_area state).
    """

    TERMINATION_TRUNCATION_METRIC = TeleportLandedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([TeleportDestCursorSubGoal])


class SwordOfHope1EscapeBattleTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent successfully Escapes from a battle.
    Starts at battle_example.state (battle active at t=0).
    Subgoals: battle_active -> (termination) escape_confirmed
    (e.g. "You escaped!" or post-escape battle_command state).
    """

    TERMINATION_TRUNCATION_METRIC = EscapeConfirmedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([BattleActiveSubGoal])
