from typing import Optional

from gameboy_worlds.emulation.pokemon.parsers import (
    MemoryBasedPokemonCrystalStateParser,
    MemoryBasedPokemonRedStateParser,
    PokemonBrownStateParser,
    PokemonCrystalStateParser,
    PokemonPrismStateParser,
    PokemonRedStateParser,
)
from gameboy_worlds.emulation.tracker import (
    RegionMatchTerminationOnlyMetric,
    TerminationMetric,
    RegionMatchTerminationMetric,
    RegionMatchSubGoal,
    SubGoal,
    AnyRegionMatchSubGoal,
)
from gameboy_worlds.emulation.pokemon.base_metrics import (
    PokemonExitBattleTruncationMetric,
)
import numpy as np


class PokemonCenterTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom_half"
    _TERMINATION_TARGET_NAME = "viridian_pokemon_center_entrance"


class OutsideViridianCenterSubgoal(AnyRegionMatchSubGoal):
    NAME = "outside_viridian_center"
    _NAMED_REGIONS = [
        "screen_middle",
        "screen_middle",
    ]
    _TARGET_NAMES = [
        "outside_viridian_center_from_left",
        "outside_viridian_center_from_right",
    ]


class MtMoonTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom_half"
    _TERMINATION_TARGET_NAME = "mt_moon_entrance"


class SpeakToBillCompleteTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "talk_bill_complete"


class PickupPokeballTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "pick_up_pokeball_starting"


class ReadTrainersTipsSignTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "trainers_tips_sign"


class SpeakToCinnabarGymAideCompleteTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "cinnabar_gym_aid_complete"


class SpeakToCinnabarMonkTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "talk_cinnabar_monk"


class UsedNotVeryEffectiveAttackOnSeakingTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "used_not_very_effective_attack"


class DefeatedBrockTerminateMetric(
    RegionMatchTerminationMetric, PokemonExitBattleTruncationMetric
):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "defeated_brock"


class DefeatedLassTerminateMetric(
    RegionMatchTerminationMetric, PokemonExitBattleTruncationMetric
):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "defeated_lass"


class CaughtPidgeyTerminateMetric(
    RegionMatchTerminationMetric, PokemonExitBattleTruncationMetric
):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "caught_pidgey"


class CaughtPikachuTerminateMetric(
    RegionMatchTerminationMetric, PokemonExitBattleTruncationMetric
):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "caught_pikachu"


class BoughtPotionAtPewterPokemartTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom_half"
    _TERMINATION_TARGET_NAME = "bought_potion_at_pewter_pokemart"


class UsedPotionOnCharmanderTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "used_potion_on_charmander"


class OpenMapTerminateMetric(TerminationMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    def determine_terminated(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ) -> bool:
        all_frames = [current_frame]
        if recent_frames is not None:
            all_frames = recent_frames
        for frame in all_frames:
            self.state_parser: PokemonRedStateParser
            in_map = self.state_parser.named_region_matches_target(
                frame, "map_bottom_right"
            )
            if in_map:
                return True
        return False


class TriedBuyBikeTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "cant_afford"


class ClickVolcanobadgeTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "volcanobadge_info"


class OpenedCeruleanHouseMapTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "opened_cerulean_house_map"


class SquirtleFaintedTerminateMetric(
    RegionMatchTerminationMetric, PokemonExitBattleTruncationMetric
):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "defeated_blue_cerulean_bridge"


class ClickedSwitchTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "clicked_switch"


class UsedSurfAshTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "used_blastoise_surf_ash"


class Sold1PsychicTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "sold_1_psychich_at_cinnabar"


class EncounteredGhostTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "encountered_ghost"


class RateMewNameTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "rate_mew_name"


class ReadLetterTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "read_letter"


class SpokeToEliteFourTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "spoke_to_elite_four"


class UsedSuperRodTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "used_super_rod"


class LookedIntoBinocularsTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "looked_into_binoculars"


class SpokeToPikachuTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "spoke_to_pikachu"


class OutsideSilfCoTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "screen_middle"
    _TERMINATION_TARGET_NAME = "outside_silf_co"


class OutsideRobbedHouseBackTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "screen_middle"
    _TERMINATION_TARGET_NAME = "outside_robbed_house_back"


class GaveMewtwoToDaycareTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "gave_mewtwo_to_daycare"


class ReadSaffronSignTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "read_saffron_sign"


class MarioGamePlayedTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "mario_game_played"


class TossedUltraballTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "tossed_ultraball"


class OutsideSeafoamIslandsTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "screen_middle"
    _TERMINATION_TARGET_NAME = "outside_seafoam_islands"


class FlyToPalletTownFromCinnabarTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "fly_to_pallet_town_from_cinnabar"


class WithdrewStaryuTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "withdrew_staryu"


class UsedToxicOnPidgeottoTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "used_toxic_on_pidgeotto"


class SwitchedToStaryuTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "screen_bottom_half"
    _TERMINATION_TARGET_NAME = "switched_to_staryu"


class CaughtGoldeenTerminateMetric(
    RegionMatchTerminationMetric, PokemonExitBattleTruncationMetric
):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "caught_goldeen"


class TriedToTeachStaryuToxicTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "tried_to_teach_staryu_toxic"


class PlayFluteTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "play_flute"


class OpenedSquirtlePokedexTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "screen_quadrant_2"
    _TERMINATION_TARGET_NAME = "opened_squirtle_pokedex"


class OpenedBlastoiseStatusTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "screen_quadrant_2"
    _TERMINATION_TARGET_NAME = "opened_blastoise_status"


class CharizardMovesTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "charizard_moves"


class SpokeToLeaderTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "spoke_to_leader"


class ReachGiovanniAreaTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonRedStateParser

    _TERMINATION_NAMED_REGION = "screen_middle"
    _TERMINATION_TARGET_NAME = "reach_giovanni_area"


# ---------------------------------------------------------------------------
# Pokemon Crystal metrics
# ---------------------------------------------------------------------------


class EnteredCherrygroveCentreTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "screen_middle"
    _TERMINATION_TARGET_NAME = "entered_cherrygrove_centre"


class WatchedTvTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "watched_tv"


class SawMirrorTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "saw_mirror"


class SpokeToChildTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "spoke_to_child"


class GotBerryTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "got_berry"


class TookDragonairItemTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "took_dragonair_item"


class GavePidgeotCleanseTagTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "gave_pidgeot_cleanse_tag"


class OpenedTyphlosionEntryTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "screen_quadrant_2"
    _TERMINATION_TARGET_NAME = "opened_typhlosion_entry"


class ExitedMtMortarTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "exited_mt_mortar"


class GotBiteTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "got_bite"


class ReadElmComputerTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "read_elm_computer"


class SpokeToAideTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "spoke_to_aide"


class UsedEscapeRopeTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "used_escape_rope"


class SpokeToVioletGymLeaderTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "spoke_to_violet_gym_leader"


class BoughtAntidoteTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "bought_antidote"


class SoldReviveTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "sold_revive"


class PidgeotLearnedToxicTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "pidgeot_learned_toxic"


class GotAlanNumberTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "got_alan_number"


class InteractedCutTreeTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "interacted_cut_tree"


class PickedUpParlzHealTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "picked_up_parlz_heal"


class ReadBookTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "read_book"


class SpokeToMortyTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "spoke_to_morty"


class EnteredBurnedTowerTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "screen_middle"
    _TERMINATION_TARGET_NAME = "entered_burned_tower"


class MiltankSadTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "miltank_sad"


class GotGoodRodTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "got_good_rod"


class EnteredLighthouseTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "screen_middle"
    _TERMINATION_TARGET_NAME = "entered_lighthouse"


class SpokeToRedHairGirlTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "spoke_to_red_hair_girl"


class ForgotGustTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "forgot_gust"


class LeftIcePathTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "left_ice_path"


class IceMazeOtherSideTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "ice_maze_other_side"


class UsedSuperEffectiveAttackTerminateMetric(
    RegionMatchTerminationMetric, PokemonExitBattleTruncationMetric
):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "used_super_effective_attack"


class CaughtDelibirdTerminateMetric(
    RegionMatchTerminationMetric, PokemonExitBattleTruncationMetric
):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "caught_delibird"


class EncounteredTangelaTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "encountered_tangela"


class SpokeToSlowpokeTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "spoke_to_slowpoke"


class GotCharcoalTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "got_charcoal"


class SpokeToAzaleaGymTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "spoke_to_azalea_gym"


class GotFastballTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "got_fastball"


class GaveKurtApricotTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "gave_kurt_apricot"


class CantDoThatTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "cant_do_that"


class UsedHeadbuttTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "used_headbutt"


class TookSuicunePicTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "screen"
    _TERMINATION_TARGET_NAME = "suicune_pic"


class UsedSurfCrystalTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "used_surf"


class SeerSawAlakazamTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "seer_saw_alakazam"


class OpenedMailboxTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "opened_mailbox"


class CalledMomTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "called_mom"


class CaughtPonytaTerminateMetric(
    RegionMatchTerminationMetric, PokemonExitBattleTruncationMetric
):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "caught_ponyta"


class UsedFlashTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "used_flash"


class BattleTowerExplanationTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "battle_tower_explanation"


class DefeatedWillTerminateMetric(
    RegionMatchTerminationMetric, PokemonExitBattleTruncationMetric
):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "defeated_will"


class DefeatedKogaTerminateMetric(
    RegionMatchTerminationMetric, PokemonExitBattleTruncationMetric
):
    REQUIRED_PARSER = PokemonCrystalStateParser

    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "defeated_koga"


# ---------------------------------------------------------------------------
# Pokemon Red full-game metrics
# ---------------------------------------------------------------------------


class _MemoryBadgeSubGoal(SubGoal):
    BADGE_NAME = None

    def _check_completed(self, frame: np.ndarray, parser) -> bool:
        return parser.has_badge(self.BADGE_NAME)


class PokemonRedBoulderBadgeSubGoal(_MemoryBadgeSubGoal):
    NAME = "collect_boulder_badge"
    BADGE_NAME = "boulder"


class PokemonRedCascadeBadgeSubGoal(_MemoryBadgeSubGoal):
    NAME = "collect_cascade_badge"
    BADGE_NAME = "cascade"


class PokemonRedThunderBadgeSubGoal(_MemoryBadgeSubGoal):
    NAME = "collect_thunder_badge"
    BADGE_NAME = "thunder"


class PokemonRedRainbowBadgeSubGoal(_MemoryBadgeSubGoal):
    NAME = "collect_rainbow_badge"
    BADGE_NAME = "rainbow"


class PokemonRedSoulBadgeSubGoal(_MemoryBadgeSubGoal):
    NAME = "collect_soul_badge"
    BADGE_NAME = "soul"


class PokemonRedMarshBadgeSubGoal(_MemoryBadgeSubGoal):
    NAME = "collect_marsh_badge"
    BADGE_NAME = "marsh"


class PokemonRedVolcanoBadgeSubGoal(_MemoryBadgeSubGoal):
    NAME = "collect_volcano_badge"
    BADGE_NAME = "volcano"


class PokemonRedEarthBadgeSubGoal(_MemoryBadgeSubGoal):
    NAME = "collect_earth_badge"
    BADGE_NAME = "earth"


class PokemonRedChampionshipTerminateMetric(TerminationMetric):
    REQUIRED_PARSER = MemoryBasedPokemonRedStateParser

    def determine_terminated(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ) -> bool:
        return self.state_parser.has_completed_championship()


# ---------------------------------------------------------------------------
# Pokemon Brown metrics
# ---------------------------------------------------------------------------


class PokemonBrownMarineBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_marine_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_marine_badge"


class PokemonBrownHailBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_hail_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_hail_badge"


class PokemonBrownSproutBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_sprout_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_sprout_badge"


class PokemonBrownSparkyBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_sparky_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_sparky_badge"


class PokemonBrownFistBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_fist_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_fist_badge"


class PokemonBrownEquityBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_equity_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_equity_badge"


class PokemonBrownStarBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_star_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_star_badge"


class PokemonBrownPsiBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_psi_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_psi_badge"


class PokemonBrownChampionshipTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonBrownStateParser
    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "collect_championship"


# ---------------------------------------------------------------------------
# Pokemon Crystal full-game metrics
# ---------------------------------------------------------------------------


class PokemonCrystalZephyrBadgeSubGoal(_MemoryBadgeSubGoal):
    NAME = "collect_zephyr_badge"
    BADGE_NAME = "zephyr"


class PokemonCrystalHiveBadgeSubGoal(_MemoryBadgeSubGoal):
    NAME = "collect_hive_badge"
    BADGE_NAME = "hive"


class PokemonCrystalPlainBadgeSubGoal(_MemoryBadgeSubGoal):
    NAME = "collect_plain_badge"
    BADGE_NAME = "plain"


class PokemonCrystalFogBadgeSubGoal(_MemoryBadgeSubGoal):
    NAME = "collect_fog_badge"
    BADGE_NAME = "fog"


class PokemonCrystalMineralBadgeSubGoal(_MemoryBadgeSubGoal):
    NAME = "collect_mineral_badge"
    BADGE_NAME = "mineral"


class PokemonCrystalStormBadgeSubGoal(_MemoryBadgeSubGoal):
    NAME = "collect_storm_badge"
    BADGE_NAME = "storm"


class PokemonCrystalGlacierBadgeSubGoal(_MemoryBadgeSubGoal):
    NAME = "collect_glacier_badge"
    BADGE_NAME = "glacier"


class PokemonCrystalRisingBadgeSubGoal(_MemoryBadgeSubGoal):
    NAME = "collect_rising_badge"
    BADGE_NAME = "rising"


class PokemonCrystalChampionshipTerminateMetric(TerminationMetric):
    REQUIRED_PARSER = MemoryBasedPokemonCrystalStateParser

    def determine_terminated(
        self, current_frame: np.ndarray, recent_frames: Optional[np.ndarray]
    ) -> bool:
        return self.state_parser.has_completed_championship()


# ---------------------------------------------------------------------------
# Pokemon Prism metrics
# ---------------------------------------------------------------------------


class PokemonPrismPyreBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_pyre_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_pyre_badge"


class PokemonPrismNatureBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_nature_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_nature_badge"


class PokemonPrismCharmBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_charm_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_charm_badge"


class PokemonPrismMidnightBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_midnight_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_midnight_badge"


class PokemonPrismMuscleBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_muscle_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_muscle_badge"


class PokemonPrismHazeBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_haze_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_haze_badge"


class PokemonPrismRaucousBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_raucous_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_raucous_badge"


class PokemonPrismNaljoBadgeSubGoal(RegionMatchSubGoal):
    NAME = "collect_naljo_badge"
    _NAMED_REGION = "dialogue_box_middle"
    _TARGET_NAME = "collect_naljo_badge"


class PokemonPrismChampionshipTerminateMetric(RegionMatchTerminationOnlyMetric):
    REQUIRED_PARSER = PokemonPrismStateParser
    _TERMINATION_NAMED_REGION = "dialogue_box_middle"
    _TERMINATION_TARGET_NAME = "collect_championship"
