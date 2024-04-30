"""
The MIT License (MIT)

Copyright (c) 2023-present STACiA

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional, Union

from .. import utils
from ..enums import MELEE_WEAPON_ID, Locale
from ..localization import Localization
from .base import BaseModel, ShopData

if TYPE_CHECKING:
    from ..cache import CacheState
    from ..types.weapons import (
        AdsStats as AdsStatsPayload,
        AirBurstStats as AirBurstStatsPayload,
        AltShotgunStats as AltShotgunStatsPayload,
        DamageRange as DamageRangePayload,
        Skin as SkinPayload,
        SkinChroma as SkinChromaPayload,
        SkinLevel as SkinLevelPayload,
        Weapon as WeaponPayload,
        WeaponStats as WeaponStatsPayload,
    )
    from .content_tiers import ContentTier
    from .themes import Theme

__all__ = (
    'AdsStats',
    'AirBurstStats',
    'AltShotgunStats',
    'DamageRange',
    'Skin',
    'SkinChroma',
    'SkinLevel',
    'Weapon',
    'WeaponStats',
)


class AdsStats:
    def __init__(self, data: AdsStatsPayload) -> None:
        self.zoom_multiplier: float = data['zoomMultiplier']
        self.fire_rate: float = data['fireRate']
        self.run_speed_multiplier: float = data['runSpeedMultiplier']
        self.burst_count: float = data['burstCount']
        self.first_bullet_accuracy: float = data['firstBulletAccuracy']

    def __repr__(self) -> str:
        attrs = [
            ('zoom_multiplier', self.zoom_multiplier),
            ('fire_rate', self.fire_rate),
            ('run_speed_multiplier', self.run_speed_multiplier),
            ('burst_count', self.burst_count),
            ('first_bullet_accuracy', self.first_bullet_accuracy),
        ]
        joined = ' '.join('%s=%r' % t for t in attrs)
        return f'<{self.__class__.__name__} {joined}>'


class AltShotgunStats:
    def __init__(self, data: AltShotgunStatsPayload) -> None:
        self.shotgun_pellet_count: float = data['shotgunPelletCount']
        self.burst_rate: float = data['burstRate']

    def __repr__(self) -> str:
        return f'<AltShotgunStats shotgun_pellet_count={self.shotgun_pellet_count} burst_rate={self.burst_rate}>'


class AirBurstStats:
    def __init__(self, data: AirBurstStatsPayload) -> None:
        self.shotgun_pellet_count: float = data['shotgunPelletCount']
        self.burst_distance: float = data['burstDistance']

    def __repr__(self) -> str:
        return f'<AirBurstStats shotgun_pellet_count={self.shotgun_pellet_count} burst_distance={self.burst_distance}>'


class DamageRange:
    def __init__(self, data: DamageRangePayload) -> None:
        self.range_start_meters: float = data['rangeStartMeters']
        self.range_end_meters: float = data['rangeEndMeters']
        self.head_damage: float = data['headDamage']
        self.body_damage: float = data['bodyDamage']
        self.leg_damage: float = data['legDamage']

    def __repr__(self) -> str:
        attrs = [
            ('range_start_meters', self.range_start_meters),
            ('range_end_meters', self.range_end_meters),
            ('head_damage', self.head_damage),
            ('body_damage', self.body_damage),
            ('leg_damage', self.leg_damage),
        ]
        joined = ' '.join('%s=%r' % t for t in attrs)
        return f'<{self.__class__.__name__} {joined}>'


class WeaponStats:
    def __init__(self, data: WeaponStatsPayload) -> None:
        self.fire_rate: float = data['fireRate']
        self.magazine_size: int = data['magazineSize']
        self.run_speed_multiplier: float = data['runSpeedMultiplier']
        self.equip_time_seconds: float = data['equipTimeSeconds']
        self.reload_time_seconds: float = data['reloadTimeSeconds']
        self.first_bullet_accuracy: float = data['firstBulletAccuracy']
        self.shotgun_pellet_count: int = data['shotgunPelletCount']
        self.wall_penetration: Optional[str] = data['wallPenetration']
        self.feature: Optional[str] = data['feature']
        self.fire_mode: Optional[str] = data['fireMode']
        self.alt_fire_type: Optional[str] = data['altFireType']
        self.ads_stats: Optional[AdsStats] = None
        if data['adsStats'] is not None:
            self.ads_stats = AdsStats(data['adsStats'])
        self.alt_shotgun_stats: Optional[AltShotgunStats] = None
        if data['altShotgunStats'] is not None:
            self.alt_shotgun_stats = AltShotgunStats(data['altShotgunStats'])
        self.air_burst_stats: Optional[AirBurstStats] = None
        if data['airBurstStats'] is not None:
            self.air_burst_stats = AirBurstStats(data['airBurstStats'])
        self.damage_ranges: List[DamageRange] = [DamageRange(x) for x in data['damageRanges']]

    def __repr__(self) -> str:
        attrs = [
            ('fire_rate', self.fire_rate),
            ('magazine_size', self.magazine_size),
            ('run_speed_multiplier', self.run_speed_multiplier),
            ('equip_time_seconds', self.equip_time_seconds),
            ('reload_time_seconds', self.reload_time_seconds),
            ('first_bullet_accuracy', self.first_bullet_accuracy),
            ('shotgun_pellet_count', self.shotgun_pellet_count),
            ('wall_penetration', self.wall_penetration),
            ('feature', self.feature),
            ('fire_mode', self.fire_mode),
            ('alt_fire_type', self.alt_fire_type),
            ('ads_stats', self.ads_stats),
            ('alt_shotgun_stats', self.alt_shotgun_stats),
            ('air_burst_stats', self.air_burst_stats),
            ('damage_ranges', self.damage_ranges),
        ]
        joined = ' '.join('%s=%r' % t for t in attrs)
        return f'<{self.__class__.__name__} {joined}>'


class Weapon(BaseModel):
    def __init__(self, *, state: CacheState, data: WeaponPayload) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self.category: str = data['category']
        self._default_skin_uuid: str = data['defaultSkinUuid']
        self.display_icon: str = data['displayIcon']
        self.kill_stream_icon: str = data['killStreamIcon']
        self.asset_path: str = data['assetPath']
        self.weapon_stats: Optional[WeaponStats] = None
        if data['weaponStats'] is not None:
            self.weapon_stats = WeaponStats(data['weaponStats'])
        self.shop_data: Optional[ShopData] = None
        if data['shopData'] is not None:
            self.shop_data = ShopData(state=self._state, item=self, data=data['shopData'])
        self.skins: List[Skin] = [Skin(state=self._state, data=skin, parent=self) for skin in data['skins']]
        self._is_melee: bool = True if self.uuid == MELEE_WEAPON_ID else False
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        return f'<Weapon display_name={self.display_name!r}>'

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the weapon's name."""
        return self._display_name_localized

    def is_melee(self) -> bool:
        """:class: `bool` Returns whether the weapon is a melee weapon."""
        return self._is_melee

    @property
    def stats(self) -> Optional[WeaponStats]:
        """:class: `Optional[WeaponStats]` alias for :attr: `weapon_stats`"""
        return self.weapon_stats

    # helpers

    def is_random(self) -> bool:
        return 'random' in self.asset_path.lower()


class Skin(BaseModel):
    def __init__(self, *, state: CacheState, data: SkinPayload, parent: Weapon) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self.theme_uuid: str = data['themeUuid']
        self.content_tier_uuid: Optional[str] = data['contentTierUuid']
        self.display_icon: str = data['displayIcon']
        self.wallpaper: Optional[str] = data['wallpaper']
        self.asset_path: str = data['assetPath']
        self.chromas: List[Chroma] = [Chroma(state=self._state, data=chroma, parent=self) for chroma in data['chromas']]
        self.levels: List[Level] = [
            Level(state=self._state, data=level, parent=self, level_number=index)
            for index, level in enumerate(data['levels'])
        ]
        self.parent: Weapon = parent
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        return f'<Skin display_name={self.display_name!r}>'

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the skin's name."""
        return self._display_name_localized

    @property
    def theme(self) -> Optional[Theme]:
        """:class: `Theme` Returns the skin's theme uuid."""
        return self._state.get_theme(self.theme_uuid)

    @property
    def content_tier(self) -> Optional[ContentTier]:
        """:class: `ContentTier` Returns the skin's rarity."""
        if self.content_tier_uuid is None:
            return None
        return self._state.get_content_tier(self.content_tier_uuid)

    @property
    def rarity(self) -> Optional[ContentTier]:
        """:class: `ContentTier` alias for :attr: `content_tier`"""
        return self.content_tier

    @property
    def display_icon_fix(self) -> Optional[str]:
        """:class: `Asset` Returns the skin's icon."""
        display_icon = self.display_icon or (self.levels[0].display_icon if len(self.levels) > 0 else None)
        if display_icon is None:
            return None
        return display_icon

    def is_melee(self) -> bool:
        """:class: `bool` Returns whether the bundle is a melee."""
        return self.parent.is_melee()

    def is_random(self) -> bool:
        return 'random' in self.asset_path.lower()

    # helpers

    def get_skin_level(self, level: int) -> Optional[Level]:
        """get the skin's level with the given level.

        Parameters
        ----------
        level: :class: `int`
            The level of the skin level to get.

        Returns
        -------
        Optional[:class: `SkinLevel`]
            The skin level with the given level.
        """
        return next((skin_level for skin_level in self.levels if skin_level.level_number == level), None)


class Chroma(BaseModel):
    def __init__(self, *, state: CacheState, data: SkinChromaPayload, parent: Skin) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self.display_icon: Optional[str] = data['displayIcon']
        self.full_render: str = data['fullRender']
        self.swatch: Optional[str] = data['swatch']
        self.streamed_video: Optional[str] = data['streamedVideo']
        self.asset_path: str = data['assetPath']
        self.parent: Skin = parent
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        return f'<SkinChroma display_name={self.display_name!r}>'

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        """Returns the skin's display name localized to the given locale."""
        return self._display_name_localized.from_locale(locale=locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the skin's name."""
        return self._display_name_localized

    @property
    def display_icon_fix(self) -> Optional[str]:
        """:class: `Asset` Returns the skin's icon with fixed white background."""

        skin = self.parent

        if skin is None:
            return self.display_icon

        display_icon = skin.display_icon
        if len(skin.levels) > 0:
            display_icon = skin.levels[0].display_icon

        weapon = skin.parent
        if weapon is None:
            return display_icon

        self_name = utils.removeprefix(self.display_name.default, 'Standard ')
        if self_name.lower() == weapon.display_name.default.lower():  # check if skin name is same as weapon name
            display_icon = weapon.display_icon or display_icon

        return display_icon

    # helpers

    @property
    def theme(self) -> Optional[Theme]:
        """:class: `Theme` Returns the skin's theme uuid."""
        return self.parent.theme

    @property
    def content_tier(self) -> Optional[ContentTier]:
        """:class: `ContentTier` Returns the skin's rarity."""
        return self.parent.content_tier

    @property
    def rarity(self) -> Optional[ContentTier]:
        """:class: `ContentTier` alias for content_tier."""
        return self.content_tier

    def is_melee(self) -> bool:
        """:class: `bool` Returns whether the bundle is a melee."""
        return self.parent.is_melee()

    def is_random(self) -> bool:
        return 'random' in self.asset_path.lower()


class Level(BaseModel):
    def __init__(self, *, state: CacheState, data: SkinLevelPayload, parent: Skin, level_number: int) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self.level_item: Optional[str] = data['levelItem']
        self.display_icon: Optional[str] = data['displayIcon']
        self.streamed_video: Optional[str] = data['streamedVideo']
        self.asset_path: str = data['assetPath']
        self._level_number: int = level_number
        self._is_level_one: bool = level_number == 0
        self.parent: Skin = parent
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)

    def __str__(self) -> str:
        return str(self.display_name)

    def __repr__(self) -> str:
        return f'<SkinLevel display_name={self.display_name!r} level={self.level!r}>'

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale=locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the skin's name."""
        return self._display_name_localized

    @property
    def level(self) -> Optional[str]:
        """:class: `str` alias for level_item."""
        return self.level_item

    @property
    def display_icon_fix(self) -> Optional[str]:
        """:class: `Asset` Returns the skin's icon with fixed white background."""
        display_icon = self.display_icon or self.parent.display_icon or self.parent.parent.display_icon
        if display_icon is None:
            return None
        return display_icon

    def is_level_one(self) -> bool:
        """:class: `bool` Returns whether the skin is level one."""
        return self._is_level_one

    # helpers

    @property
    def level_number(self) -> int:
        """:class: `int` Returns the skin's level number."""
        return self._level_number

    @property
    def theme(self) -> Optional[Theme]:
        """:class: `Theme` Returns the skin's theme uuid."""
        return self.parent.theme

    @property
    def content_tier(self) -> Optional[ContentTier]:
        """:class: `ContentTier` Returns the skin's rarity."""
        return self.parent.content_tier

    @property
    def rarity(self) -> Optional[ContentTier]:
        """:class: `ContentTier` alias for content_tier."""
        return self.content_tier

    def is_melee(self) -> bool:
        """:class: `bool` Returns whether the bundle is a melee."""
        return self.parent.is_melee()

    def is_random(self) -> bool:
        """:class: `bool` Returns whether the skin is random."""
        return 'random' in self.asset_path.lower()


SkinChroma = Chroma
SkinLevel = Level
