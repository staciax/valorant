"""
The MIT License (MIT).

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

from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import Field

from ..enums import ShopCategory, WeaponCategory
from .base import BaseModel, BaseUUIDModel
from .localization import LocalizedField  # Changed from language to localization

__all__ = (
    'AdsStats',
    'AirBurstStats',
    'AltShotgunStat',
    'DamageRange',
    'GridPosition',
    'ShopData',
    'WeaponStats',
)


if TYPE_CHECKING:
    from ..client import Client
    from .content_tiers import ContentTier
    from .themes import Theme


class AdsStats(BaseModel):
    zoom_multiplier: float = Field(alias='zoomMultiplier')
    fire_rate: float = Field(alias='fireRate')
    run_speed_multiplier: float = Field(alias='runSpeedMultiplier')
    burst_count: int = Field(alias='burstCount')
    first_bullet_accuracy: float = Field(alias='firstBulletAccuracy')


class DamageRange(BaseModel):
    range_start_meters: int = Field(alias='rangeStartMeters')
    range_end_meters: int = Field(alias='rangeEndMeters')
    head_damage: float = Field(alias='headDamage')
    body_damage: int = Field(alias='bodyDamage')
    leg_damage: float = Field(alias='legDamage')


class AltShotgunStat(BaseModel):
    shotgun_pellet_count: int = Field(alias='shotgunPelletCount')
    burst_rate: float = Field(alias='burstRate')


class AirBurstStats(BaseModel):
    shotgun_pellet_count: int = Field(alias='shotgunPelletCount')
    burst_distance: float = Field(alias='burstDistance')


class WeaponStats(BaseModel):
    fire_rate: float = Field(alias='fireRate')
    magazine_size: int = Field(alias='magazineSize')
    run_speed_multiplier: float = Field(alias='runSpeedMultiplier')
    equip_time_seconds: float = Field(alias='equipTimeSeconds')
    reload_time_seconds: float = Field(alias='reloadTimeSeconds')
    first_bullet_accuracy: float = Field(alias='firstBulletAccuracy')
    shotgun_pellet_count: int = Field(alias='shotgunPelletCount')
    wall_penetration: str = Field(alias='wallPenetration')
    feature: str | None
    fire_mode: str | None = Field(alias='fireMode')
    alt_fire_type: str | None = Field(alias='altFireType')
    ads_stats: AdsStats | None = Field(alias='adsStats')
    alt_shotgun_stats: AltShotgunStat | None = Field(alias='altShotgunStats')
    air_burst_stats: AirBurstStats | None = Field(alias='airBurstStats')
    damage_ranges: list[DamageRange] = Field(alias='damageRanges')


class GridPosition(BaseModel):
    row: int
    column: int


class ShopData(BaseModel):
    cost: int
    category: ShopCategory
    shop_order_priority: int = Field(alias='shopOrderPriority')
    category_text: str | LocalizedField = Field(alias='categoryText')
    grid_position: GridPosition | None = Field(alias='gridPosition')
    can_be_trashed: bool = Field(alias='canBeTrashed')
    image: str | None
    new_image: str = Field(alias='newImage')
    new_image2: str | None = Field(alias='newImage2')
    asset_path: str = Field(alias='assetPath')


class Chroma(BaseUUIDModel):
    # uuid: str
    display_name: str | LocalizedField = Field(alias='displayName')
    display_icon: str | None = Field(alias='displayIcon')
    full_render: str = Field(alias='fullRender')
    swatch: str | None
    streamed_video: str | None = Field(alias='streamedVideo')
    asset_path: str = Field(alias='assetPath')


class Level(BaseUUIDModel):
    # uuid: str
    display_name: str | LocalizedField = Field(alias='displayName')
    level_item: str | None = Field(alias='levelItem')
    display_icon: str | None = Field(alias='displayIcon')
    streamed_video: str | None = Field(alias='streamedVideo')
    asset_path: str = Field(alias='assetPath')


class Skin(BaseUUIDModel):
    # uuid: str
    display_name: str | LocalizedField = Field(alias='displayName')
    theme_uuid: UUID = Field(alias='themeUuid')
    content_tier_uuid: UUID | None = Field(alias='contentTierUuid')
    display_icon: str | None = Field(alias='displayIcon')
    wallpaper: str | None
    asset_path: str = Field(alias='assetPath')
    chromas: list[Chroma]
    levels: list[Level]

    # useful methods

    async def fetch_theme(self, *, client: Client) -> Theme | None:
        if self.theme_uuid is None:
            return None
        return await client.fetch_theme(str(self.theme_uuid))

    async def fetch_content_tier(self, *, client: Client) -> ContentTier | None:
        if self.content_tier_uuid is None:
            return None
        return await client.fetch_content_tier(str(self.content_tier_uuid))


class Weapon(BaseUUIDModel):
    # uuid: str
    display_name: str | LocalizedField = Field(alias='displayName')
    category: WeaponCategory
    default_skin_uuid: str = Field(alias='defaultSkinUuid')
    display_icon: str = Field(alias='displayIcon')
    kill_stream_icon: str = Field(alias='killStreamIcon')
    asset_path: str = Field(alias='assetPath')
    weapon_stats: WeaponStats | None = Field(alias='weaponStats')
    shop_data: ShopData | None = Field(alias='shopData')
    skins: list[Skin]
