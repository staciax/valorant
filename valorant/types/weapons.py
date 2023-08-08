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

from typing import Dict, List, Optional, TypedDict, Union

from .object import Object, ShopData
from .response import Response


class AdsStats(TypedDict):
    zoomMultiplier: float
    fireRate: float
    runSpeedMultiplier: float
    burstCount: int
    firstBulletAccuracy: float


class AltShotgunStats(TypedDict):
    shotgunPelletCount: int
    burstRate: float


class AirBurstStats(TypedDict):
    shotgunPelletCount: int
    burstDistance: float


class DamageRange(TypedDict):
    rangeStartMeters: float
    rangeEndMeters: float
    headDamage: float
    bodyDamage: float
    legDamage: float


class WeaponStats(TypedDict):
    fireRate: float
    magazineSize: int
    runSpeedMultiplier: float
    equipTimeSeconds: float
    reloadTimeSeconds: float
    firstBulletAccuracy: float
    shotgunPelletCount: int
    wallPenetration: str
    feature: Optional[str]
    fireMode: Optional[str]
    altFireType: Optional[str]
    adsStats: Optional[AdsStats]
    altShotgunStats: Optional[AltShotgunStats]
    airBurstStats: Optional[AirBurstStats]
    damageRanges: List[DamageRange]


class Chroma(Object):
    displayName: Union[str, Dict[str, str]]
    displayIcon: Optional[str]
    fullRender: str
    swatch: Optional[str]
    streamedVideo: Optional[str]
    assetPath: str


class Level(Object):
    displayName: Union[str, Dict[str, str]]
    levelItem: str
    displayIcon: Optional[str]
    streamedVideo: Optional[str]
    assetPath: str


class Skin(Object):
    displayName: Union[str, Dict[str, str]]
    themeUuid: str
    contentTierUuid: str
    displayIcon: str
    wallpaper: str
    assetPath: str
    chromas: List[Chroma]
    levels: List[Level]


class Weapon(Object):
    displayName: Union[str, Dict[str, str]]
    category: str
    defaultSkinUuid: str
    displayIcon: str
    killStreamIcon: str
    assetPath: str
    weaponStats: Optional[WeaponStats]
    shopData: Optional[ShopData]
    skins: List[Skin]


Weapons = Response[List[Weapon]]
WeaponUUID = Response[Weapon]

Skins = Response[List[Skin]]
SkinUUID = Response[Skin]

SkinLevels = Response[List[Level]]
SkinLevel = Level
SkinLevelUUID = Response[Level]

SkinChromas = Response[List[Chroma]]
SkinChroma = Chroma
SkinChromaUUID = Response[Chroma]
