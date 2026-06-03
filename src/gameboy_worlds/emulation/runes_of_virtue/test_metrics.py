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
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "king_dialog"


class RunesOfVirtue2ReadBookTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when an opened book is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "book_open"


class RunesOfVirtue2BlockedRoomEnteredTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player has entered the blocked room."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "blocked_room_entered"


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


class RunesOfVirtue2CaveOfDishonourEnterFloor2TerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player enters floor 2 in the Cave of Dishonour."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cave_of_dishonour_enter_floor_2"


class RunesOfVirtue2CaveOfDishonourEnterFloor3TerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player enters floor 3 in the Cave of Dishonour."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cave_of_dishonour_enter_floor_3"


class RunesOfVirtue2GrabCheeseFromKitchenTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player grabs the cheese from the kitchen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "kitchen_cheese_grabbed"


class RunesOfVirtue2GiveCheeseToSherryTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player gives the cheese to Sherry."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cheese_given_to_sherry"


class RunesOfVirtue2ClimbLadderBehindLockedDoorTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player climbs the ladder behind the locked door."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "ladder_behind_locked_door_climbed"


class RunesOfVirtue2InteractWithMapOnTableTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player interacts with the map on the table."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "table_map_interacted"


class RunesOfVirtue2FindLadderBackFromCastleTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player finds a ladder back from the castle."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "castle_ladder_back_found"


class RunesOfVirtue2UnlockDoorAndSaveTholdenTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player unlocks the door and saves Tholden."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "dialog_indicator"
    _TERMINATION_TARGET_NAME = "tholden_saved"


class RunesOfVirtue2FindLadderOutOfCavernOfHatredTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player finds a ladder out of the Cavern of Hatred."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "left_playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_hatred_ladder_out_found"


class RunesOfVirtue2BringTholdenBackToKingTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player brings Tholden back to the king."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "dialog_indicator"
    _TERMINATION_TARGET_NAME = "tholden_brought_back_to_king"


class RunesOfVirtue2AttendCastleCeremonyTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player attends the ceremony in the castle."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "dialog_indicator"
    _TERMINATION_TARGET_NAME = "castle_ceremony_attended"


class RunesOfVirtue2CavernOfHatredGate1UnlockedTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the first Cavern of Hatred gate is unlocked."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_hatred_gate_1_unlocked"


class RunesOfVirtue2CavernOfHatredLadderRoom2TerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player enters the second ladder room in the Cavern of Hatred."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_hatred_ladder_room_2"


class RunesOfVirtue2CavernOfHatredLadder2TerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player reaches the second ladder in the Cavern of Hatred."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_hatred_ladder_2"


class RunesOfVirtue2CavernOfHatredGrabKeyTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player grabs the key in the Cavern of Hatred."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_hatred_grab_key"


class RunesOfVirtue2CavernOfHatredEnterFloor4TerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player enters floor 4 in the Cavern of Hatred."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_hatred_enter_floor_4"


class RunesOfVirtue2CavernOfHatredEnterFloor5TerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player enters floor 5 in the Cavern of Hatred."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_hatred_enter_floor_5"


class RunesOfVirtue2CavernOfHatredEnterFloor6TerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player enters floor 6 in the Cavern of Hatred."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_hatred_enter_floor_6"


class RunesOfVirtue2CavernOfHatredEnterFloor7TerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player enters floor 7 in the Cavern of Hatred."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_hatred_enter_floor_7"


class RunesOfVirtue2DeathScreenTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when the death / game over screen is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "death_screen_indicator"
    _TERMINATION_TARGET_NAME = "death_screen"


class RunesOfVirtue1ChucklesDialogTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when Chuckles's dialog is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "chuckles_dialog"


class RunesOfVirtue1GnuGnu1DialogTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when Gnu Gnu's 1st store dialog is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "gnu_gnu_1_dialog"


class RunesOfVirtue1GnuGnu2DialogTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when Gnu Gnu's 2nd store dialog is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "gnu_gnu_2_dialog"


class RunesOfVirtue1SherryDialogTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when Sherry's dialog is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "sherry_dialog"


class RunesOfVirtue1CavernOfHatredTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when the player is inside the Cavern of Hatred."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "cave_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_hatred"


class RunesOfVirtue1CavernOfDeceitTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when the player is inside the Cavern of Deceit."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "cave_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_deceit"


class RunesOfVirtue1CavernOfCowardiceTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player is inside the Cavern of Cowardice."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "cave_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_cowardice"


class RunesOfVirtue1CavernOfCowardiceEnterFloor2TerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player enters floor 2 of the Cavern of Cowardice."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_cowardice_enter_floor_2"


class RunesOfVirtue1CavernOfCowardiceEnterFloor3TerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player enters floor 3 of the Cavern of Cowardice."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_cowardice_enter_floor_3"


class RunesOfVirtue1CavernOfCowardiceFloor3ChestOpenedTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player opens the floor 3 chest in the Cavern of Cowardice."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_cowardice_floor_3_chest_opened"


class RunesOfVirtue1CavernOfCowardiceEnterFloor4TerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player enters floor 4 of the Cavern of Cowardice."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "top_playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_cowardice_enter_floor_4"


class RunesOfVirtue1CavernOfCowardiceSherryFloor4DialogTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when Sherry's floor 4 dialog is on screen in the Cavern of Cowardice."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_cowardice_sherry_floor_4_dialog"


class RunesOfVirtue1CavernOfCowardiceTakeStewFloor4TerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player takes stew on floor 4 of the Cavern of Cowardice."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_cowardice_take_stew_floor_4"


class RunesOfVirtue1CavernOfCowardiceObtainCoinFloor4TerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player obtains the coin on floor 4 of the Cavern of Cowardice."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_cowardice_obtain_coin_floor_4"


class RunesOfVirtue1DrCatDialogTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when Dr. Cat's dialog is on screen."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "dr_cat_dialog"


class RunesOfVirtue1DrCatCatsLairDialogTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when Dr. Cat's dialog is on screen in the Cat's Lair."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "dr_cat_cats_lair_dialog"


class RunesOfVirtue1ShipRiddenTerminateMetric(RegionMatchTerminationOnlyMetric):
    """Terminates when the player is riding the ship."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "ship_ridden"


class RunesOfVirtue1BasementLadderUnlockedTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player unlocks the basement ladder."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "basement_ladder_unlocked"


class RunesOfVirtue1BasementChestOpenedTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player opens the basement chest."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "basement_chest_opened"


class RunesOfVirtue1CavernOfHatredEnterFloor2TerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player enters floor 2 of the Cavern of Hatred."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_hatred_enter_floor_2"


class RunesOfVirtue1CavernOfHatredSherryFloor2DialogTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when Sherry's floor 2 dialog is on screen in the Cavern of Hatred."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_hatred_sherry_floor_2_dialog"


class RunesOfVirtue1CavernOfHatredChooseDoorWithSherryTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when Sherry asks the player to choose a door in the Cavern of Hatred."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_hatred_choose_door_with_sherry"


class RunesOfVirtue1CavernOfHatredChooseRightDoorMelissaDialogTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when Melissa's dialog is on screen after choosing the right door."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_hatred_choose_right_door_melissa_dialog"


class RunesOfVirtue1CavernOfHatredEnterFloor3TerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player enters floor 3 of the Cavern of Hatred."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_hatred_enter_floor_3"


class RunesOfVirtue1CavernOfHatredEnterFloor4TerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player enters floor 4 of the Cavern of Hatred."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "top_playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_hatred_enter_floor_4"


class RunesOfVirtue1CavernOfHatredChestFloor1OpenedTerminateMetric(
    RegionMatchTerminationOnlyMetric
):
    """Terminates when the player opens the floor 1 chest in the Cavern of Hatred."""

    REQUIRED_PARSER = RunesOfVirtueStateParser
    _TERMINATION_NAMED_REGION = "playfield_indicator"
    _TERMINATION_TARGET_NAME = "cavern_of_hatred_chest_floor_1_opened"


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
