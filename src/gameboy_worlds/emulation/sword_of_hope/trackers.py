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
    SoH2PowerMenuLastSlideSubGoal,
    SoH2BattleWonTerminateMetric,
    SoH2BattleActiveSubGoal,
    SoH2EscapeConfirmedTerminateMetric,
    SoH2WheatPurchasedTerminateMetric,
    SoH2ShopMenuOpenTerminateMetric,
    SoH2ShopMenuOpenSubGoal,
    SoH2BattleMagicMenuTerminateMetric,
    SoH2MotionResultTerminateMetric,
    SoH2MagicMenuOpenSubGoal,
    SoH2ItemFoundTerminateMetric,
    SoH2LookTargetSubGoal,
    SoH2CprSwordPurchasedTerminateMetric,
    SoH2WeaponsShopMenuOpenSubGoal,
    SoH2LookShopkeeperSubGoal,
    SoH2ShopBuySellMenuSubGoal,
    SoH2CursorOnCprSwordSubGoal,
    SoH2CursorOnAutoTerminateMetric,
    SoH2WheatFromTreeTerminateMetric,
    SoH2HitTreeTargetSubGoal,
    SoH2UseMenuOpenTerminateMetric,
    SoH2ItemMenuOpenSubGoal,
    SoH2UseMenuOpenSubGoal,
    SoH2WheatConsumedTerminateMetric,
    SoH2CursorOnWheatSubGoal,
    SoH2PowerStatsExpPageTerminateMetric,
    SoH2CursorOnPowerSubGoal,
    SoH2PowerStatsFirstPageSubGoal,
    SoH2CursorOnLookTerminateMetric,
    SoH2CursorOnItemTerminateMetric,
    SoH2CursorOnOpenTerminateMetric,
    SoH2CursorOnMagicTerminateMetric,
    SoH2CursorOnHitTerminateMetric,
    SoH2CursorOnPowerTerminateMetric,
    SoH2CursorOnLookSubGoal,
    SoH2CursorOnItemSubGoal,
    SoH2CursorOnOpenSubGoal,
    SoH2CursorOnMagicSubGoal,
    SoH2CursorOnHitSubGoal,
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
    Terminates when the agent closes the Power menu and returns to exploration.
    Starts at default.state (exploration menu showing). The agent must navigate
    cursor onto Power, open Power, cycle through stat slides, then press B to
    close back to exploration.
    Subgoals: power_menu_last_slide -> (termination) exploration_menu.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2ExplorationMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2PowerMenuLastSlideSubGoal])


class SwordOfHope2FirstAdjacentRoomTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent reaches Riccar Castle (first adjacent room from
    the King's Room). Subgoal: kings_room starting room visible.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2FirstAdjacentRoomTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2StarterRoomSubGoal])


class SwordOfHope2BattleWonTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent wins a battle in SoH2.
    Starts at battle_example.state (battle active at t=0).
    Subgoals: battle_active -> (termination) battle_won.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2BattleWonTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2BattleActiveSubGoal])


class SwordOfHope2EscapeBattleTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent successfully escapes from a battle in SoH2.
    Starts at battle_example.state (battle active at t=0).
    Subgoals: battle_active -> (termination) escape_confirmed.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2EscapeConfirmedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2BattleActiveSubGoal])


class SwordOfHope2OpenShopMenuTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent opens a shop's buy menu.
    Starts at shop_example.state (player in front of a shop).
    No subgoals (single-step interaction).
    """

    TERMINATION_TRUNCATION_METRIC = SoH2ShopMenuOpenTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope2BattleMagicCommandTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent selects MAGIC in battle and the magic submenu shows.
    Starts at battle_example.state.
    Subgoals: battle_active -> (termination) battle_magic_menu.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2BattleMagicMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2BattleActiveSubGoal])


class SwordOfHope2AutoBattleTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent navigates the cursor onto the AUTO command in
    the battle command row. Tests command-row navigation.
    Starts at battle_example.state.
    Subgoals: battle_active -> (termination) cursor_on_auto.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnAutoTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2BattleActiveSubGoal])


class SwordOfHope2OpenItemMenuTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent reaches the Use submenu via Item -> Use chain.
    SoH2 inventory flow: press ITEM (inventory list) -> press A on an item to
    bring up the Use submenu.
    Starts at default.state.
    Subgoals: item_menu_open -> (termination) use_menu_open.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2UseMenuOpenTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2ItemMenuOpenSubGoal])


class SwordOfHope2CursorOnLookTestTracker(SwordOfHope2TestTracker):
    """Cursor at LOOK in the exploration command grid. Region: status_command."""
    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnLookTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope2CursorOnItemTestTracker(SwordOfHope2TestTracker):
    """Cursor at ITEM in the exploration command grid."""
    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnItemTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope2CursorOnOpenTestTracker(SwordOfHope2TestTracker):
    """Cursor at OPEN in the exploration command grid."""
    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnOpenTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope2CursorOnMagicTestTracker(SwordOfHope2TestTracker):
    """Cursor at MAGIC in the exploration command grid."""
    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnMagicTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope2CursorOnHitTestTracker(SwordOfHope2TestTracker):
    """Cursor at HIT in the exploration command grid."""
    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnHitTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope2CycleThroughCommandsTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent has cycled the cursor through all 6 commands
    in order (LOOK -> ITEM -> OPEN -> MAGIC -> HIT -> POWER) without pressing
    A on any of them.
    Starts at default.state.
    Subgoals: cursor_on_look -> cursor_on_item -> cursor_on_open
              -> cursor_on_magic -> cursor_on_hit
              -> (termination) cursor_on_power.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnPowerTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class(
        [
            SoH2CursorOnLookSubGoal,
            SoH2CursorOnItemSubGoal,
            SoH2CursorOnOpenSubGoal,
            SoH2CursorOnMagicSubGoal,
            SoH2CursorOnHitSubGoal,
        ]
    )


class SwordOfHope2ViewExpNeededTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent reaches the Power stats page that shows
    "X more EXP needed for level up". Full chain: navigate to Power in
    command grid -> open Power menu (first stats page) -> cycle to last
    EXP page.
    Starts at lvl3_overworld.state (Theo at lvl 3, stable overworld).
    Subgoals: cursor_on_power -> power_stats_first_page
              -> (termination) power_stats_exp_page.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2PowerStatsExpPageTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class(
        [SoH2CursorOnPowerSubGoal, SoH2PowerStatsFirstPageSubGoal]
    )


class SwordOfHope2UseWheatTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent uses Wheat from inventory and consumes it.
    Full chain: ITEM submenu -> cursor on Wheat -> press A (Use submenu) ->
    confirm USE -> wheat consumption dialogue.
    Starts at wheat_in_inventory.state (player has Wheat in inventory at a
    stable overworld position).
    Subgoals: item_menu_open -> cursor_on_wheat -> use_menu_open
              -> (termination) wheat_consumed.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2WheatConsumedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class(
        [SoH2ItemMenuOpenSubGoal, SoH2CursorOnWheatSubGoal, SoH2UseMenuOpenSubGoal]
    )


class SwordOfHope2HitTreeWheatTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent uses Hit on a tree at Riccar Woods [A4] and
    receives Wheat. Wheat drops are randomized — may take 1, 2, or more
    hits — so the agent must keep Hitting until the wheat dialogue appears.
    Starts at hit_tree_example.state (player adjacent to the [A4] tree).
    Subgoals: hit_tree_target -> (termination) wheat_from_tree.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2WheatFromTreeTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2HitTreeTargetSubGoal])


class SwordOfHope2CastMotionTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent casts Motion magic from the overworld.
    Starts at lvl2_overworld.state (Theo at level 2 with Motion spell available).
    Subgoals: magic_menu_open -> (termination) motion_result.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2MotionResultTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2MagicMenuOpenSubGoal])


class SwordOfHope2LookItemTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent uses Look on an object and discovers an item.
    Starts at look_example.state (player adjacent to a Lookable object).
    Subgoals: look_target -> (termination) item_found.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2ItemFoundTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2LookTargetSubGoal])


class SwordOfHope2BuyWheatTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent buys Wheat from a shop in SoH2.
    Starts at shop_example.state (player in front of a shop, ready to interact).
    Wheat is item-specific because the post-buy dialogue contains the item name
    ("WHEAT? Thank you"), so the capture is keyed to wheat.
    Subgoals: shop_menu_open -> (termination) wheat_purchased.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2WheatPurchasedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2ShopMenuOpenSubGoal])


class SwordOfHope2BuyCprSwordTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent buys the CPR Sword (3rd item) from the Weapons Shop.
    Starts at weapons_shop_example.state (player adjacent to the shopkeeper, ready to Look).
    Multi-step interaction:
      1. Look menu with cursor on shopkeeper
      2. After A on shopkeeper, BUY/SELL choice menu
      3. After picking BUY, item list visible (cursor on first item)
      4. Cursor navigated down to CPR Sword (3rd entry)
      5. After confirming, "CPR SWORD? Thank you"
    Subgoals: look_shopkeeper -> shop_buy_sell_menu -> weapons_shop_menu_open
              -> cursor_on_cpr_sword -> (termination) cpr_sword_purchased.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2CprSwordPurchasedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class(
        [
            SoH2LookShopkeeperSubGoal,
            SoH2ShopBuySellMenuSubGoal,
            SoH2WeaponsShopMenuOpenSubGoal,
            SoH2CursorOnCprSwordSubGoal,
        ]
    )


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
