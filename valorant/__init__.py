"""
Valorant API Wrapper
~~~~~~~~~~~~~~~~~~~
A basic wrapper for the Valorant API.
:copyright: (c) 2023-present STACiA
:license: MIT, see LICENSE for more details.
"""

__title__ = 'valorant'
__author__ = 'STACiA'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023-present STACiA'
__version__ = '1.0.9a'

from typing import Literal, NamedTuple

from . import models as models, utils as utils
from .client import Client as Client
from .enums import (
    MELEE_WEAPON_ID as MELEE_WEAPON_ID,
    AbilitySlot as AbilitySlot,
    Locale as Locale,
    MissionType as MissionType,
    RelationType as RelationType,
    RewardType as RewardType,
    try_enum as try_enum,
)
from .localization import Localization as Localization
from .models import (
    Ability as Ability,
    AdsStats as AdsStats,
    Agent as Agent,
    AirBurstStats as AirBurstStats,
    AltShotgunStats as AltShotgunStats,
    BaseModel as BaseModel,
    Border as Border,
    Buddy as Buddy,
    BuddyLevel as BuddyLevel,
    Bundle as Bundle,
    Callout as Callout,
    Ceremony as Ceremony,
    Chapter as Chapter,
    ChapterLevel as ChapterLevel,
    CompetitiveSeason as CompetitiveSeason,
    CompetitiveTier as CompetitiveTier,
    Content as Content,
    ContentTier as ContentTier,
    Contract as Contract,
    Currency as Currency,
    DamageRange as DamageRange,
    Event as Event,
    GameFeatureOverride as GameFeatureOverride,
    GameMode as GameMode,
    GameModeEquippable as GameModeEquippable,
    GameRuleBoolOverride as GameRuleBoolOverride,
    Gear as Gear,
    GridPosition as GridPosition,
    Level as Level,
    LevelBorder as LevelBorder,
    Location as Location,
    Map as Map,
    Media as Media,
    Mission as Mission,
    PlayerCard as PlayerCard,
    PlayerTitle as PlayerTitle,
    Reward as Reward,
    Role as Role,
    Season as Season,
    ShopData as ShopData,
    Skin as Skin,
    SkinChroma as SkinChroma,
    SkinLevel as SkinLevel,
    Spray as Spray,
    SprayLevel as SprayLevel,
    Theme as Theme,
    Tier as Tier,
    Version as Version,
    VoiceLine as VoiceLine,
    VoiceLineLocalization as VoiceLineLocalization,
    Weapon as Weapon,
    WeaponStats as WeaponStats,
)


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    release: Literal['alpha', 'beta', 'final']


version_info: VersionInfo = VersionInfo(major=1, minor=0, micro=9, release='alpha')

del NamedTuple, Literal, VersionInfo
