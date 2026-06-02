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
    SoH2PowerStatsFirstPageTerminateMetric,
    SoH2MagicMenuOpenTerminateMetric,
    SoH2ItemMenuOpenTerminateMetric,
    SoH2LookShopkeeperTerminateMetric,
    SoH2WeaponsShopMenuOpenTerminateMetric,
    SoH2CursorOnCprSwordTerminateMetric,
    SoH2ShopBuySellMenuTerminateMetric,
    SoH2CursorOnWheatTerminateMetric,
    SoH2CursorOnClashTerminateMetric,
    SoH2Temple1fTerminateMetric,
    SoH2OutsideTempleSubGoal,
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
    TreantDefeatedTerminateMetric,
    GateOpenedTerminateMetric,
    ScrollReceivedTerminateMetric,
    CharmReceivedTerminateMetric,
    TeleportLandedTerminateMetric,
    EscapeConfirmedTerminateMetric,
    CursorOnLookTerminateMetric,
    CursorOnOpenTerminateMetric,
    CursorOnUseTerminateMetric,
    CursorOnMagicTerminateMetric,
    CursorOnHitTerminateMetric,
    CursorOnPowerTerminateMetric,
    PowerStatsFirstPageTerminateMetric,
    CursorOnAutoTerminateMetric,
    ShopMenuOpenTerminateMetric,
    LookSelectedTerminateMetric,
    MenuOpenTerminateMetric,
    MagicMenuOpenTerminateMetric,
    DialogueInitiatedTerminateMetric,
    BattleActiveTerminateMetric,
    TeleportDestCursorTerminateMetric,
    LookTargetOptionsTerminateMetric,
    CursorOnFirebalTerminateMetric,
    CursorOnFirebal2TerminateMetric,
    CursorOnStripallTerminateMetric,
    CursorOnFirebalSubGoal,
    CursorOnFirebal2SubGoal,
    CursorOnStripallSubGoal,
    CursorOnTeleportOldmanTerminateMetric,
    CursorOnHerbUseTerminateMetric,
    CursorOnKeymUseTerminateMetric,
    OldmanHouseTerminateMetric,
    PowerStatsLastPageSubGoal,
    CursorOnTeleportOldmanSubGoal,
    PowerStatsFirstPageSubGoal,
    BattleMagicMenuSubGoal,
    SoH2BattleActiveTerminateMetric,
    SoH2CursorOnMotionTerminateMetric,
    SoH2CursorOnTheoSubGoal,
    SoH2PowerStatsExpPageSubGoal,
    SoH2CursorOnShopFirstItemTerminateMetric,
    SoH2CursorOnShopFirstItemSubGoal,
    SoH2CursorOnShopThirdItemTerminateMetric,
    SoH2CursorOnFirstWeaponTerminateMetric,
    SoH2CursorOnFirstWeaponSubGoal,
    SoH2CursorOnSecondWeaponTerminateMetric,
    SoH2CursorOnSecondWeaponSubGoal,
    SoH2CursorOnThirdWeaponTerminateMetric,
    SoH2LookTreeTargetTerminateMetric,
    SoH2BattleMagicMenuSubGoal,
    SoH2CursorOnAutoSubGoal,
    SoH2CursorOnClashSubGoal,
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
    CursorOnLookSubGoal,
    CursorOnOpenSubGoal,
    CursorOnUseSubGoal,
    CursorOnMagicSubGoal,
    CursorOnHitSubGoal,
    CursorOnPowerSubGoal,
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


class SwordOfHope2CursorOnPowerTestTracker(SwordOfHope2TestTracker):
    """Cursor at POWER in the exploration command grid. Region: status_command."""
    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnPowerTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope2PowerFirstPageTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent reaches the Power stats first page.
    Shorter scope than view_exp_needed_test (which cycles past the first page).
    Starts at default.state.
    Subgoals: cursor_on_power -> (termination) power_stats_first_page.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2PowerStatsFirstPageTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2CursorOnPowerSubGoal])


class SwordOfHope2OpenMagicMenuTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent opens the Magic submenu from exploration.
    Starts at default.state.
    Subgoals: cursor_on_magic -> (termination) magic_menu_open.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2MagicMenuOpenTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2CursorOnMagicSubGoal])


class SwordOfHope2OpenItemViewTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent opens the Item (inventory) submenu.
    Shorter scope than open_item_menu_test (which proceeds to the Use submenu).
    Starts at default.state.
    Subgoals: cursor_on_item -> (termination) item_menu_open.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2ItemMenuOpenTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2CursorOnItemSubGoal])


class SwordOfHope2LookShopkeeperTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent looks at the weapons-shop shopkeeper (Look menu
    with cursor on shopkeeper visible).
    Starts at weapons_shop_example.state (player adjacent to the shopkeeper).
    Subgoals: cursor_on_look -> (termination) look_shopkeeper.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2LookShopkeeperTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2CursorOnLookSubGoal])


class SwordOfHope2OpenWeaponsShopBuyTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent reaches the weapons shop's BUY item list.
    Shorter scope than buy_cpr_sword_test.
    Starts at weapons_shop_example.state.
    Subgoals: shop_buy_sell_menu -> (termination) weapons_shop_menu_open.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2WeaponsShopMenuOpenTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2ShopBuySellMenuSubGoal])


class SwordOfHope2CursorOnCprSwordTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the cursor is on CPR Sword (3rd entry) in the weapons shop
    item list. Shorter scope than buy_cpr_sword_test (no purchase confirmation).
    Starts at weapons_shop_example.state.
    Subgoals: weapons_shop_menu_open -> (termination) cursor_on_cpr_sword.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnCprSwordTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2WeaponsShopMenuOpenSubGoal])


class SwordOfHope2OpenUseMenuTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the Use submenu opens after selecting a usable item.
    Shorter scope than use_wheat_test (which proceeds to wheat consumption).
    Starts at hit_tree_example.state (Wheat in inventory).
    Subgoals: item_menu_open -> cursor_on_wheat -> (termination) use_menu_open.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2UseMenuOpenTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class(
        [SoH2ItemMenuOpenSubGoal, SoH2CursorOnWheatSubGoal]
    )


class SwordOfHope2OpenShopBuySellTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the BUY/SELL choice menu opens after engaging the
    shopkeeper. Shorter scope than open_weapons_shop_buy_test (which proceeds
    to the BUY item list).
    Starts at weapons_shop_example.state.
    Subgoals: look_shopkeeper -> (termination) shop_buy_sell_menu.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2ShopBuySellMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2LookShopkeeperSubGoal])


class SwordOfHope2CursorOnWheatTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the cursor lands on Wheat in the Item submenu.
    Shorter scope than use_wheat_test (which proceeds to consumption).
    Starts at hit_tree_example.state.
    Subgoals: item_menu_open -> (termination) cursor_on_wheat.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnWheatTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2ItemMenuOpenSubGoal])


class SwordOfHope2BattleClashTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the cursor lands on CLASH in the battle command row.
    Mirror of cursor_on_auto_test but for the default attack command.
    Starts at battle_example.state.
    Subgoals: battle_active -> (termination) cursor_on_clash.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnClashTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2BattleActiveSubGoal])


class SwordOfHope2EnterTempleFirstFloorTestTracker(SwordOfHope2TestTracker):
    """
    Terminates when the agent reaches the Ancient Temple's 1st floor from
    outside the temple entrance. Story event #1 in SoH2 — leave Castle,
    find Ancient Temple. Starts at outside_temple.state.
    Subgoals: outside_temple -> (termination) temple_1f.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2Temple1fTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2OutsideTempleSubGoal])


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


class SwordOfHope1DefeatTreantTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent defeats Treant in battle (walkthrough event #2),
    receiving Key M. Uses offensive magic (Firebal2 strategy, lvl 4+).
    Starts at treant_battle_start.state (Treant battle active, FIGHT menu default).
    Subgoals: battle_active -> (termination) treant_defeated.
    """

    TERMINATION_TRUNCATION_METRIC = TreantDefeatedTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([BattleActiveSubGoal])


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


class SwordOfHope1CursorOnLookTestTracker(SwordOfHope1TestTracker):
    """Cursor at LOOK in the exploration command grid. Region: status_command."""
    TERMINATION_TRUNCATION_METRIC = CursorOnLookTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope1CursorOnOpenTestTracker(SwordOfHope1TestTracker):
    """Cursor at OPEN in the exploration command grid."""
    TERMINATION_TRUNCATION_METRIC = CursorOnOpenTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope1CursorOnUseTestTracker(SwordOfHope1TestTracker):
    """Cursor at USE in the exploration command grid."""
    TERMINATION_TRUNCATION_METRIC = CursorOnUseTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope1CursorOnMagicTestTracker(SwordOfHope1TestTracker):
    """Cursor at MAGIC in the exploration command grid."""
    TERMINATION_TRUNCATION_METRIC = CursorOnMagicTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope1CursorOnHitTestTracker(SwordOfHope1TestTracker):
    """Cursor at HIT in the exploration command grid."""
    TERMINATION_TRUNCATION_METRIC = CursorOnHitTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope1CursorOnPowerTestTracker(SwordOfHope1TestTracker):
    """Cursor at POWER in the exploration command grid."""
    TERMINATION_TRUNCATION_METRIC = CursorOnPowerTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope1CycleThroughCommandsTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent has cycled the cursor through all 6 commands
    in order (LOOK -> OPEN -> USE -> MAGIC -> HIT -> POWER) without pressing
    A on any of them.
    Starts at default.state.
    Subgoals: cursor_on_look -> cursor_on_open -> cursor_on_use
              -> cursor_on_magic -> cursor_on_hit
              -> (termination) cursor_on_power.
    """

    TERMINATION_TRUNCATION_METRIC = CursorOnPowerTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class(
        [
            CursorOnLookSubGoal,
            CursorOnOpenSubGoal,
            CursorOnUseSubGoal,
            CursorOnMagicSubGoal,
            CursorOnHitSubGoal,
        ]
    )


class SwordOfHope1OpenStatusViewTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent reaches the Power menu's first stats page.
    Full chain: navigate cursor to Power in command grid -> press A to open
    Power -> first stats page visible.
    Starts at default.state.
    Subgoals: cursor_on_power -> (termination) power_stats_first_page.
    """

    TERMINATION_TRUNCATION_METRIC = PowerStatsFirstPageTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([CursorOnPowerSubGoal])


class SwordOfHope1AutoBattleTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the agent navigates the cursor onto the AUTO command in
    the battle command row. Tests command-row navigation in battle.
    Starts at battle_example.state.
    Subgoals: battle_active -> (termination) cursor_on_auto.
    """

    TERMINATION_TRUNCATION_METRIC = CursorOnAutoTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([BattleActiveSubGoal])


class SwordOfHope1ShopMenuOpenTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the shop's buy menu first opens. Shorter scope than
    buy_item_test (which proceeds to purchase confirmation).
    Starts at shop_forest.state.
    Subgoals: dummy (single-step interaction).
    """

    TERMINATION_TRUNCATION_METRIC = ShopMenuOpenTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope1LookCommandSelectTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the LOOK command is selected in the command grid.
    Shorter scope than look_item_test (which proceeds to item discovery).
    Starts at default.state.
    Subgoals: dummy (single-step cursor + A).
    """

    TERMINATION_TRUNCATION_METRIC = LookSelectedTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope1MenuOpenTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the command menu first opens. Shorter scope than
    menu_open_close_test (which proceeds to closing back to exploration).
    Starts at default.state.
    Subgoals: dummy (single-step menu trigger).
    """

    TERMINATION_TRUNCATION_METRIC = MenuOpenTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope1MagicMenuOpenTestTracker(SwordOfHope1TestTracker):
    """
    Terminates when the Magic spell list opens from the overworld. Shorter
    scope than cast_teleport_test (which proceeds to casting Teleport).
    Starts at default.state.
    Subgoals: dummy (single navigation chain to open Magic submenu).
    """

    TERMINATION_TRUNCATION_METRIC = MagicMenuOpenTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


class SwordOfHope1DialogueInitiatedTestTracker(SwordOfHope1TestTracker):
    """
    Terminates the moment an NPC dialogue page first appears. Shorter scope
    than talk_to_npc_test (which proceeds through one full dialogue advance).
    Starts at default.state.
    Subgoals: dummy (single talk action).
    """

    TERMINATION_TRUNCATION_METRIC = DialogueInitiatedTerminateMetric
    SUBGOAL_METRIC = DummySubGoalMetric


# ---------------------------------------------------------------------------
# SoH1 — 50-task push: reasoning-hard trackers
# Zero-capture set: each task reuses existing termination .npy but enforces a
# non-trivial subgoal sequence the agent must satisfy (open-then-cancel,
# constrained cycle paths, in-battle menu-cancel reasoning).
# Capture-pending set: each task terminates on a "cursor on a specific list
# entry" target the user will capture in dev_play.
# ---------------------------------------------------------------------------


class SwordOfHope1CancelMagicMenuTestTracker(SwordOfHope1TestTracker):
    """
    Open the Magic submenu from exploration, then back out without casting.
    Tests menu-cancel reasoning: agent must understand the B-button semantics
    and recognize the difference between "open menu" and "commit to action".
    Init: default.state. Subgoal: magic_menu_open -> (term) exploration_menu.
    """

    TERMINATION_TRUNCATION_METRIC = ExplorationMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([MagicMenuOpenSubGoal])


class SwordOfHope1CancelPowerMenuTestTracker(SwordOfHope1TestTracker):
    """
    Open the Power stats menu, view first stats page, then close back to
    exploration. Multi-step menu navigation with a deliberate exit.
    Init: default.state. Subgoal: power_stats_first_page -> (term) exploration_menu.
    """

    TERMINATION_TRUNCATION_METRIC = ExplorationMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([PowerStatsFirstPageSubGoal])


class SwordOfHope1CancelTeleportMenuTestTracker(SwordOfHope1TestTracker):
    """
    Open Magic -> Teleport -> destination list, then cancel back to
    exploration without teleporting. Tests cancellation of nested menus.
    Init: default.state. Subgoal: teleport_dest_cursor -> (term) exploration_menu.
    """

    TERMINATION_TRUNCATION_METRIC = ExplorationMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([TeleportDestCursorSubGoal])


class SwordOfHope1CancelShopMenuTestTracker(SwordOfHope1TestTracker):
    """
    Open the shop's buy menu, then exit without purchasing. Distinguishes
    "browse the inventory" from "commit to a purchase".
    Init: shop_forest.state. Subgoal: shop_menu_open -> (term) exploration_menu.
    """

    TERMINATION_TRUNCATION_METRIC = ExplorationMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([ShopMenuOpenSubGoal])


class SwordOfHope1CancelLookOptionsTestTracker(SwordOfHope1TestTracker):
    """
    Select LOOK and view the target options, then back out without choosing.
    Pure inspection task: information-gather without committing.
    Init: default.state. Subgoal: look_target_options -> (term) exploration_menu.
    """

    TERMINATION_TRUNCATION_METRIC = ExplorationMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([LookTargetOptionsSubGoal])


class SwordOfHope1BattleMagicCancelTestTracker(SwordOfHope1TestTracker):
    """
    In battle, open the Magic submenu, then back out without casting. Battle
    contexts have a different default cursor; agent must learn the in-battle
    cancel pattern is symmetric to the overworld one.
    Init: battle_example.state. Subgoal: battle_magic_menu -> (term) battle_active.
    """

    TERMINATION_TRUNCATION_METRIC = BattleActiveTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([BattleMagicMenuSubGoal])


class SwordOfHope1CycleBackToLookTestTracker(SwordOfHope1TestTracker):
    """
    Starting from cursor on LOOK, the agent must cycle the cursor through the
    command grid all the way around (LOOK -> ... -> POWER -> wrap -> LOOK).
    Termination matches the original LOOK position but the SUBGOAL forces the
    agent to have actually visited POWER en route - otherwise it would just
    stay in place. Tests cyclic navigation understanding.
    Init: default.state. Subgoal: cursor_on_power -> (term) cursor_on_look.
    """

    TERMINATION_TRUNCATION_METRIC = CursorOnLookTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([CursorOnPowerSubGoal])


class SwordOfHope1CycleToPowerViaMagicTestTracker(SwordOfHope1TestTracker):
    """
    Navigate cursor to POWER, but only via MAGIC (constrained path). Forces the
    agent to take the lower-row route rather than the shortest L->R top-row
    route. Tests constrained-path reasoning.
    Init: default.state. Subgoal: cursor_on_magic -> (term) cursor_on_power.
    """

    TERMINATION_TRUNCATION_METRIC = CursorOnPowerTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([CursorOnMagicSubGoal])


class SwordOfHope1CursorOnFirebalTestTracker(SwordOfHope1TestTracker):
    """
    In battle, open the Magic submenu and navigate the cursor to the FIREBAL
    spell specifically (not Firebal2, not other spells). Firebal is a
    battle-only spell in SoH1. Tests spell selection under list ambiguity.
    Init: pre_treant_engage.state (lvl 4 Theo with Firebal learned, in battle).
    Subgoal: battle_magic_menu -> (term) cursor_on_firebal.
    """

    TERMINATION_TRUNCATION_METRIC = CursorOnFirebalTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([BattleMagicMenuSubGoal])


class SwordOfHope1CursorOnFirebal2TestTracker(SwordOfHope1TestTracker):
    """
    In battle, open the Magic submenu and cursor on FIREBAL2 specifically
    (the upgraded variant). Battle-only spell. Tests fine-grained spell
    distinction in the battle Magic list.
    Init: pre_treant_engage.state (verify Firebal2 is in spell list at lvl 4).
    Subgoal: battle_magic_menu -> (term) cursor_on_firebal2.
    """

    TERMINATION_TRUNCATION_METRIC = CursorOnFirebal2TerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([BattleMagicMenuSubGoal])


class SwordOfHope1CursorOnStripallTestTracker(SwordOfHope1TestTracker):
    """
    In battle, open the Magic submenu and cursor on STRIPALL specifically.
    Stripall is a battle-only debuff spell that strips enemy buffs/defense.
    Tests spell-purpose disambiguation: agent must distinguish damage spells
    (Firebal/Firebal2) from utility spells (Stripall) in the same list.
    Init: pre_treant_engage.state.
    Subgoal: battle_magic_menu -> (term) cursor_on_stripall.
    """

    TERMINATION_TRUNCATION_METRIC = CursorOnStripallTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([BattleMagicMenuSubGoal])


class SwordOfHope1CursorOnTeleportOldmanTestTracker(SwordOfHope1TestTracker):
    """
    Cast Teleport and navigate the destination cursor onto OLD MAN'S HOUSE
    specifically (not Shaman's, not Forest). Tests destination disambiguation.
    Init: near_treant_postkill.state (multiple teleport destinations available).
    Subgoal: teleport_dest_cursor -> (term) cursor_on_teleport_oldman.
    """

    TERMINATION_TRUNCATION_METRIC = CursorOnTeleportOldmanTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([TeleportDestCursorSubGoal])


class SwordOfHope1CursorOnHerbUseTestTracker(SwordOfHope1TestTracker):
    """
    Open the Use submenu and navigate cursor to HERB specifically (not Key M,
    not Scroll, not other items). Tests inventory item disambiguation.
    Init: mistress_backroom_access_collected.state (has Scroll + Herb).
    Subgoal: cursor_on_use -> (term) cursor_on_herb_use.
    """

    TERMINATION_TRUNCATION_METRIC = CursorOnHerbUseTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([CursorOnUseSubGoal])


class SwordOfHope1CursorOnKeymUseTestTracker(SwordOfHope1TestTracker):
    """
    Open the Use submenu and navigate cursor to KEY M specifically. Tests
    inventory disambiguation in the at_martel_gate context where Key M is
    the correct (quest-required) item among other inventory entries.
    Init: at_martel_gate.state. Subgoal: cursor_on_use -> (term) cursor_on_keym_use.
    """

    TERMINATION_TRUNCATION_METRIC = CursorOnKeymUseTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([CursorOnUseSubGoal])


class SwordOfHope1BattleStripallCancelTestTracker(SwordOfHope1TestTracker):
    """
    In battle, navigate to STRIPALL in the Magic submenu (cursor on Stripall),
    then back out without casting it. Tests inspect-without-commit reasoning
    in a battle context with a non-default spell choice.
    Init: pre_treant_engage.state (battle active, Theo at lvl 4+).
    Subgoals (2):
        battle_magic_menu -> cursor_on_stripall -> (term) battle_active.
    """

    TERMINATION_TRUNCATION_METRIC = BattleActiveTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class(
        [BattleMagicMenuSubGoal, CursorOnStripallSubGoal]
    )


class SwordOfHope1ViewPowerThenTeleportOldmanTestTracker(SwordOfHope1TestTracker):
    """
    Long-horizon composite reasoning task: agent must inspect player stats
    THEN travel via Teleport. Full chain:
      1. Navigate command cursor to POWER, press A to open Power stats
      2. Scroll through the Power stat slides to the LAST page
      3. Press B to close back to exploration
      4. Open Magic submenu -> select TELEPORT
      5. In destination list, navigate cursor to OLD MAN'S HOUSE
      6. Press A to confirm; agent lands at Old Man's House
    Termination: room_label shows oldman_house.
    Init: lvl5_overworld.state (player at lvl 5+, Teleport unlocked, Old Man's
    House available as a teleport destination).
    Subgoals (3, in order):
        cursor_on_power -> power_stats_last_page -> cursor_on_teleport_oldman
        -> (term) oldman_house.
    Tests: long-horizon planning with menu-inspect-then-act reasoning across
    three distinct UI contexts (command grid, Power stats menu, Teleport
    destination list) before the agent commits to the travel action.
    """

    TERMINATION_TRUNCATION_METRIC = OldmanHouseTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class(
        [
            CursorOnPowerSubGoal,
            PowerStatsLastPageSubGoal,
            CursorOnTeleportOldmanSubGoal,
        ]
    )


# ---------------------------------------------------------------------------
# SoH2 — 50-task push: reasoning-hard trackers
# ---------------------------------------------------------------------------


class SwordOfHope2CancelMagicMenuTestTracker(SwordOfHope2TestTracker):
    """
    Open the Magic submenu from exploration, then back out without casting.
    Mirror of SoH1 variant. Tests menu-cancel reasoning.
    Init: lvl2_overworld.state (Theo has Motion spell available).
    Subgoal: magic_menu_open -> (term) exploration_menu.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2ExplorationMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2MagicMenuOpenSubGoal])


class SwordOfHope2CancelItemMenuTestTracker(SwordOfHope2TestTracker):
    """
    Open the Item submenu (inventory list), then back out without using
    anything. Tests inventory-browse vs commit-to-use distinction.
    Init: hit_tree_example.state (Wheat in inventory).
    Subgoal: item_menu_open -> (term) exploration_menu.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2ExplorationMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2ItemMenuOpenSubGoal])


class SwordOfHope2CancelShopMenuTestTracker(SwordOfHope2TestTracker):
    """
    Open a shop's buy menu, then exit without purchasing.
    Init: shop_example.state. Subgoal: shop_menu_open -> (term) exploration_menu.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2ExplorationMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2ShopMenuOpenSubGoal])


class SwordOfHope2CancelWeaponsShopBuyTestTracker(SwordOfHope2TestTracker):
    """
    Navigate into the weapons shop BUY item list, then exit without buying.
    Init: weapons_shop_example.state.
    Subgoal: weapons_shop_menu_open -> (term) exploration_menu.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2ExplorationMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2WeaponsShopMenuOpenSubGoal])


class SwordOfHope2CancelLookShopkeeperTestTracker(SwordOfHope2TestTracker):
    """
    Look at the weapons-shop shopkeeper, then back out without engaging.
    Tests Look-without-interact distinction.
    Init: weapons_shop_example.state.
    Subgoal: look_shopkeeper -> (term) exploration_menu.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2ExplorationMenuTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2LookShopkeeperSubGoal])


class SwordOfHope2AutoToClashBattleTestTracker(SwordOfHope2TestTracker):
    """
    Starting in battle, navigate cursor to AUTO first, then move it back to
    CLASH (reverse selection). Tests reversible cursor reasoning in battle.
    Init: battle_example.state.
    Subgoal: cursor_on_auto -> (term) cursor_on_clash.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnClashTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2CursorOnAutoSubGoal])


class SwordOfHope2ClashToAutoBattleTestTracker(SwordOfHope2TestTracker):
    """
    Starting in battle, cursor on CLASH (default), navigate to AUTO.
    Mirror of the AUTO->CLASH variant. Tests reverse-direction cursor.
    Init: battle_example.state.
    Subgoal: cursor_on_clash -> (term) cursor_on_auto.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnAutoTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2CursorOnClashSubGoal])


class SwordOfHope2CursorOnMotionTestTracker(SwordOfHope2TestTracker):
    """
    Open the Magic submenu and navigate the cursor to MOTION (the lvl-2
    overworld spell). SoH2's party system requires an extra step compared to
    SoH1: agent must first pick the party member (Theo) before their spell
    list is shown.
    Init: lvl2_overworld.state.
    Subgoals (2, in order):
        magic_menu_open (party member list visible)
        -> cursor_on_theo (cursor on Theo in party list, about to confirm)
        -> (term) cursor_on_motion (cursor on Motion in Theo's spell list).
    """

    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnMotionTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class(
        [SoH2MagicMenuOpenSubGoal, SoH2CursorOnTheoSubGoal]
    )


class SwordOfHope2CursorOnShopFirstItemTestTracker(SwordOfHope2TestTracker):
    """
    In a generic shop's buy list, cursor on the FIRST item entry. Tests "go
    to top of list" reasoning - distinguished from "cursor on Wheat" which is
    a different shop layout.
    Init: shop_example.state.
    Subgoal: shop_menu_open -> (term) cursor_on_shop_first_item.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnShopFirstItemTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2ShopMenuOpenSubGoal])


class SwordOfHope2CursorOnShopThirdItemTestTracker(SwordOfHope2TestTracker):
    """
    Same shop as cursor_on_shop_first_item_test, but cursor on the THIRD item
    entry. Tests bounded list navigation — agent must traverse from the
    default cursor position (first item) down to the third.
    Init: shop_example.state.
    Subgoals (2): shop_menu_open -> cursor_on_shop_first_item ->
        (term) cursor_on_shop_third_item.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnShopThirdItemTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class(
        [SoH2ShopMenuOpenSubGoal, SoH2CursorOnShopFirstItemSubGoal]
    )


class SwordOfHope2CursorOnFirstWeaponTestTracker(SwordOfHope2TestTracker):
    """
    In the weapons shop, cursor on the FIRST weapon entry. Distinguished from
    cursor_on_cpr_sword_test (3rd entry) - tests "top of list" navigation.
    Init: weapons_shop_example.state.
    Subgoal: weapons_shop_menu_open -> (term) cursor_on_first_weapon.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnFirstWeaponTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2WeaponsShopMenuOpenSubGoal])


class SwordOfHope2CursorOnSecondWeaponTestTracker(SwordOfHope2TestTracker):
    """
    Weapons shop, cursor on the SECOND weapon entry. Tests single-step
    navigation from the first item position.
    Init: weapons_shop_example.state.
    Subgoals (2): weapons_shop_menu_open -> cursor_on_first_weapon ->
        (term) cursor_on_second_weapon.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnSecondWeaponTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class(
        [SoH2WeaponsShopMenuOpenSubGoal, SoH2CursorOnFirstWeaponSubGoal]
    )


class SwordOfHope2CursorOnThirdWeaponTestTracker(SwordOfHope2TestTracker):
    """
    Weapons shop, cursor on the THIRD weapon entry (CPR Sword in current
    shop layout). Distinguished from cursor_on_cpr_sword_test by framing:
    this tests bounded-list navigation by position, not by name.
    Init: weapons_shop_example.state.
    Subgoals (3): weapons_shop_menu_open -> cursor_on_first_weapon ->
        cursor_on_second_weapon -> (term) cursor_on_third_weapon.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2CursorOnThirdWeaponTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class(
        [
            SoH2WeaponsShopMenuOpenSubGoal,
            SoH2CursorOnFirstWeaponSubGoal,
            SoH2CursorOnSecondWeaponSubGoal,
        ]
    )


class SwordOfHope2LookTreeTargetTestTracker(SwordOfHope2TestTracker):
    """
    Use LOOK on a grass tile (not the shopkeeper, not the tree). Tests
    target disambiguation in the Look menu where multiple visible targets
    are available.
    Init: hit_tree_example.state (grass tiles nearby).
    Subgoal: cursor_on_look -> (term) look_tree_target.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2LookTreeTargetTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class([SoH2CursorOnLookSubGoal])


class SwordOfHope2ViewPowerThenCastMotionTestTracker(SwordOfHope2TestTracker):
    """
    Long-horizon composite reasoning task (SoH2 mirror of SoH1's
    view_power_then_teleport_oldman_test):
      1. Navigate command cursor to POWER, press A
      2. Scroll through Power stats first page to the exp/level page
      3. Press B to close Power back to exploration
      4. Open Magic submenu, choose Theo, choose Motion, confirm cast
    Termination: motion_result (Motion cast confirmation dialogue).
    Init: lvl2_overworld.state.
    Subgoals (3, in order):
        cursor_on_power -> power_stats_first_page -> power_stats_exp_page
        -> (term) motion_result.
    Tests: inspect-then-act long-horizon planning across Power menu and
    party-magic chain.
    """

    TERMINATION_TRUNCATION_METRIC = SoH2MotionResultTerminateMetric
    SUBGOAL_METRIC = make_subgoal_metric_class(
        [
            SoH2CursorOnPowerSubGoal,
            SoH2PowerStatsFirstPageSubGoal,
            SoH2PowerStatsExpPageSubGoal,
        ]
    )


