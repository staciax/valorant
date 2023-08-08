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
from ..asset import Asset
from ..enums import MELEE_WEAPON_ID, Locale
from ..localization import Localization
from .abc import BaseModel, ShopData

if TYPE_CHECKING:
    from typing_extensions import Self

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
        return f"<AltShotgunStats shotgun_pellet_count={self.shotgun_pellet_count} burst_rate={self.burst_rate}>"


class AirBurstStats:
    def __init__(self, data: AirBurstStatsPayload) -> None:
        self.shotgun_pellet_count: float = data['shotgunPelletCount']
        self.burst_distance: float = data['burstDistance']

    def __repr__(self) -> str:
        return f"<AirBurstStats shotgun_pellet_count={self.shotgun_pellet_count} burst_distance={self.burst_distance}>"


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
        self._wall_penetration: Optional[str] = data['wallPenetration']
        self._feature: Optional[str] = data['feature']
        self._fire_mode: Optional[str] = data['fireMode']
        self._alt_fire_type: Optional[str] = data['altFireType']
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

    @property
    def fire_mode(self) -> Optional[str]:
        if self._fire_mode is not None:
            return utils.removeprefix(self._fire_mode, 'EWeaponFireModeDisplayType::')
        return None

    @property
    def wall_penetration(self) -> Optional[str]:
        if self._wall_penetration is not None:
            return utils.removeprefix(self._wall_penetration, 'EWallPenetrationDisplayType::')
        return None

    @property
    def feature(self) -> Optional[str]:
        if self._feature is not None:
            return utils.removeprefix(self._feature, 'WeaponStatsFeature::')
        return None

    @property
    def alt_fire_type(self) -> Optional[str]:
        if self._alt_fire_type is not None:
            return utils.removeprefix(self._alt_fire_type, 'EWeaponAltFireDisplayType::')
        return None


class Weapon(BaseModel):
    def __init__(self, *, state: CacheState, data: WeaponPayload) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._data: WeaponPayload = data
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self._category: str = data['category']
        self._default_skin_uuid: str = data['defaultSkinUuid']
        self._display_icon: str = data['displayIcon']
        self._kill_stream_icon: str = data['killStreamIcon']
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
        self._is_random: bool = 'random' in self.asset_path.lower()

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        return f"<Weapon display_name={self.display_name!r}>"

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the weapon's name."""
        return self._display_name_localized

    @property
    def category(self) -> str:
        """:class: `str` Returns the weapon's category."""
        return utils.removeprefix(self._category, "EEquippableCategory::")

    @property
    def display_icon(self) -> Asset:
        """:class: `Asset` Returns the weapon's icon."""
        return Asset._from_url(self._state, self._display_icon)

    @property
    def kill_stream_icon(self) -> Asset:
        """:class: `Asset` Returns the weapon's kill stream icon."""
        return Asset._from_url(self._state, self._kill_stream_icon)

    def is_melee(self) -> bool:
        """:class: `bool` Returns whether the weapon is a melee weapon."""
        return self._is_melee

    @property
    def stats(self) -> Optional[WeaponStats]:
        """:class: `Optional[WeaponStats]` alias for :attr: `weapon_stats`"""
        return self.weapon_stats

    # helpers

    def is_random(self) -> bool:
        return self._is_random

    @classmethod
    def _copy(cls, weapon: Self) -> Self:
        self = cls.__new__(cls)  # bypass __init__
        self._uuid = weapon._uuid
        self._state = weapon._state
        self._data = weapon._data.copy()
        self._display_name = weapon._display_name
        self._category = weapon._category
        self._default_skin_uuid = weapon._default_skin_uuid
        self._display_icon = weapon._display_icon
        self._kill_stream_icon = weapon._kill_stream_icon
        self.asset_path = weapon.asset_path
        self.weapon_stats = weapon.weapon_stats
        self.shop_data = weapon.shop_data
        self.skins = weapon.skins
        self._is_melee = weapon._is_melee
        self._display_name_localized = weapon._display_name_localized
        self._is_random = weapon._is_random
        return self


class Skin(BaseModel):
    def __init__(self, *, state: CacheState, data: SkinPayload, parent: Weapon) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._data: SkinPayload = data
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self._theme_uuid: str = data['themeUuid']
        self._content_tier_uuid: Optional[str] = data['contentTierUuid']
        self._display_icon: str = data['displayIcon']
        self._wallpaper: Optional[str] = data['wallpaper']
        self.asset_path: str = data['assetPath']
        self.chromas: List[SkinChroma] = [
            SkinChroma(state=self._state, data=chroma, parent=self) for chroma in data['chromas']
        ]
        self.levels: List[SkinLevel] = [
            SkinLevel(state=self._state, data=level, parent=self, level_number=index)
            for index, level in enumerate(data['levels'])
        ]
        self.parent: Weapon = parent
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)
        self._is_random: bool = 'random' in self.asset_path.lower()

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        return f"<Skin display_name={self.display_name!r}>"

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the skin's name."""
        return self._display_name_localized

    @property
    def theme(self) -> Optional[Theme]:
        """:class: `Theme` Returns the skin's theme uuid."""
        return self._state.get_theme(self._theme_uuid)

    @property
    def content_tier(self) -> Optional[ContentTier]:
        """:class: `ContentTier` Returns the skin's rarity."""
        if self._content_tier_uuid is None:
            return None
        return self._state.get_content_tier(self._content_tier_uuid)

    @property
    def rarity(self) -> Optional[ContentTier]:
        """:class: `ContentTier` alias for :attr: `content_tier`"""
        return self.content_tier

    @property
    def display_icon(self) -> Optional[Asset]:
        """:class: `Asset` Returns the skin's icon."""
        if self._display_icon is None:
            return None
        return Asset._from_url(self._state, self._display_icon)

    @property
    def display_icon_fix(self) -> Optional[Asset]:
        """:class: `Asset` Returns the skin's icon."""
        display_icon = self._display_icon or (self.levels[0].display_icon if len(self.levels) > 0 else None)
        if display_icon is None:
            return None
        return Asset._from_url(self._state, str(display_icon))

    @property
    def wallpaper(self) -> Optional[Asset]:
        """:class: `Asset` Returns the skin's wallpaper."""
        if self._wallpaper is None:
            return None
        return Asset._from_url(self._state, url=self._wallpaper)

    def is_melee(self) -> bool:
        """:class: `bool` Returns whether the bundle is a melee."""
        return self.parent.is_melee()

    def is_random(self) -> bool:
        return self._is_random

    @classmethod
    def _copy(cls, skin: Self) -> Self:
        self = cls.__new__(cls)  # bypass __init__
        self._uuid = skin._uuid
        self._state = skin._state
        self._data = skin._data.copy()
        self._display_name = skin._display_name
        self._theme_uuid = skin._theme_uuid
        self._content_tier_uuid = skin._content_tier_uuid
        self._display_icon = skin._display_icon
        self._wallpaper = skin._wallpaper
        self.asset_path = skin.asset_path
        self.chromas = skin.chromas.copy()
        self.levels = skin.levels.copy()
        self.parent = skin.parent
        self._display_name_localized = skin._display_name_localized
        self._is_random = skin._is_random
        return self

    def get_skin_level(self, level: int) -> Optional[SkinLevel]:
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


class SkinChroma(BaseModel):
    def __init__(self, *, state: CacheState, data: SkinChromaPayload, parent: Skin) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._data: SkinChromaPayload = data
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self._display_icon: Optional[str] = data['displayIcon']
        self._full_render: str = data['fullRender']
        self._swatch: Optional[str] = data['swatch']
        self._streamed_video: Optional[str] = data['streamedVideo']
        self.asset_path: str = data['assetPath']
        self.parent: Skin = parent
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)
        self._is_random: bool = 'random' in self.asset_path.lower()

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        return f"<SkinChroma display_name={self.display_name!r}>"

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        """Returns the skin's display name localized to the given locale."""
        return self._display_name_localized.from_locale(locale=locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the skin's name."""
        return self._display_name_localized

    @property
    def display_icon(self) -> Optional[Asset]:
        """:class: `Asset` Returns the skin's icon."""
        if self._display_icon is None:
            return None
        return Asset._from_url(self._state, url=self._display_icon)

    @property
    def display_icon_fix(self) -> Optional[Asset]:
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

    @property
    def full_render(self) -> Optional[Asset]:
        """:class: `Asset` Returns the skin's icon full render."""
        if self._full_render is None:
            return None
        return Asset._from_url(self._state, url=self._full_render)

    @property
    def swatch(self) -> Optional[Asset]:
        """:class: `Asset` Returns the skin's swatch."""
        if self._swatch is None:
            return None
        return Asset._from_url(self._state, url=self._swatch)

    @property
    def streamed_video(self) -> Optional[Asset]:
        """:class: `Optional[Asset]` Returns the skin's video."""
        if self._streamed_video is None:
            return None
        return Asset._from_url(self._state, url=self._streamed_video)

    @property
    def video(self) -> Optional[Asset]:
        """:class: `Asset` alias for streamed_video."""
        return self.streamed_video

    # helper properties

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

    @classmethod
    def _copy(cls, skin_chroma: Self) -> Self:
        """Copies the given skin_chroma with the given parent."""
        self = cls.__new__(cls)  # bypass __init__
        self._uuid = skin_chroma._uuid
        self._state = skin_chroma._state
        self._data = skin_chroma._data.copy()
        self._display_name = skin_chroma._display_name
        self._display_icon = skin_chroma._display_icon
        self._full_render = skin_chroma._full_render
        self._swatch = skin_chroma._swatch
        self._streamed_video = skin_chroma._streamed_video
        self.asset_path = skin_chroma.asset_path
        self.parent = skin_chroma.parent
        self._display_name_localized = skin_chroma._display_name_localized
        self._is_random = skin_chroma._is_random
        return self


class SkinLevel(BaseModel):
    def __init__(self, *, state: CacheState, data: SkinLevelPayload, parent: Skin, level_number: int) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._data: SkinLevelPayload = data
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self._level: Optional[str] = data['levelItem']
        self._display_icon: Optional[str] = data['displayIcon']
        self._streamed_video: Optional[str] = data['streamedVideo']
        self.asset_path: str = data['assetPath']
        self._level_number: int = level_number
        self._is_level_one: bool = level_number == 0
        self.parent: Skin = parent
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)
        self._is_random: bool = 'random' in self.asset_path.lower()

    def __str__(self) -> str:
        return str(self.display_name)

    def __repr__(self) -> str:
        return f"<SkinLevel display_name={self.display_name!r} level={self.level!r}>"

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale=locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the skin's name."""
        return self._display_name_localized

    @property
    def level_item(self) -> str:
        """:class: `str` Returns the skin's level."""
        if self._level is None:
            return 'Normal'
        return utils.removeprefix(self._level, 'EEquippableSkinLevelItem::')

    @property
    def level(self) -> str:
        """:class: `str` alias for level_item."""
        return self.level_item

    @property
    def display_icon(self) -> Optional[Asset]:
        """:class: `Asset` Returns the skin's icon."""
        if self._display_icon is None:
            return None
        return Asset._from_url(self._state, url=self._display_icon)

    @property
    def display_icon_fix(self) -> Optional[Asset]:
        """:class: `Asset` Returns the skin's icon with fixed white background."""
        display_icon = self._display_icon or self.parent.display_icon or self.parent.parent.display_icon
        if display_icon is None:
            return None
        if isinstance(display_icon, Asset):
            return display_icon
        return Asset._from_url(self._state, url=display_icon)

    @property
    def streamed_video(self) -> Optional[Asset]:
        """:class: `Asset` Returns the skin's video."""
        if self._streamed_video is None:
            return None
        return Asset._from_url(self._state, url=self._streamed_video)

    @property
    def video(self) -> Optional[Asset]:
        """:class: `Asset` alias for streamed_video."""
        return self.streamed_video

    def is_level_one(self) -> bool:
        """:class: `bool` Returns whether the skin is level one."""
        return self._is_level_one

    # helper properties

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
        return self._is_random

    @classmethod
    def _copy(cls, skin_level: Self) -> Self:
        """Copies the given skin_level with the given parent."""
        self = cls.__new__(cls)  # bypass __init__
        self._uuid = skin_level._uuid
        self._state = skin_level._state
        self._data = skin_level._data.copy()
        self._display_name = skin_level._display_name
        self._level = skin_level._level
        self._display_icon = skin_level._display_icon
        self._streamed_video = skin_level._streamed_video
        self.asset_path = skin_level.asset_path
        self._level_number = skin_level._level_number
        self._is_level_one = skin_level._is_level_one
        self.parent = skin_level.parent._copy(skin_level.parent)
        self._display_name_localized = skin_level._display_name_localized
        self._is_random = skin_level._is_random
        return self
