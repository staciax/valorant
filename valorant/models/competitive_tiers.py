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

from ..asset import Asset
from ..enums import Locale
from ..localization import Localization
from .abc import BaseModel

if TYPE_CHECKING:
    from ..cache import CacheState
    from ..types.competitive_tiers import CompetitiveTier as CompetitiveTierPayload, Tier as TierPayload


__all__ = (
    'CompetitiveTier',
    'Tier',
)


class Tier:
    def __init__(self, state: CacheState, data: TierPayload) -> None:
        self._state: CacheState = state
        self.tier: int = data['tier']
        self._name: Union[str, Dict[str, str]] = data['tierName']
        self.division: Optional[str] = data['division']
        self._division_name: Union[str, Dict[str, str]] = data['divisionName']
        self.color: str = data['color']
        self.background_color: str = data['backgroundColor']
        self._small_icon: Optional[str] = data['smallIcon']
        self._large_icon: Optional[str] = data['largeIcon']
        self._rank_triangle_down_icon: Optional[str] = data['rankTriangleDownIcon']
        self._rank_triangle_up_icon: Optional[str] = data['rankTriangleUpIcon']
        self._name_locale: Localization = Localization(self._name, locale=self._state.locale)
        self._division_name_localized: Localization = Localization(self._division_name, locale=self._state.locale)

    def __str__(self) -> str:
        return self.name.locale

    def __repr__(self) -> str:
        return f'<Tier tier={self.tier!r} name={self.name!r} division={self.division!r}>'

    def __hash__(self) -> int:
        return hash(self.tier)

    def __eq__(self, other) -> bool:
        return isinstance(other, Tier) and self.tier == other.tier

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: object) -> bool:
        return isinstance(other, Tier) and self.tier < other.tier

    def __le__(self, other: object) -> bool:
        return isinstance(other, Tier) and self.tier <= other.tier

    def __gt__(self, other: object) -> bool:
        return isinstance(other, Tier) and self.tier > other.tier

    def __ge__(self, other: object) -> bool:
        return isinstance(other, Tier) and self.tier >= other.tier

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._name_locale.from_locale(locale)

    def division_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._division_name_localized.from_locale(locale)

    @property
    def name(self) -> Localization:
        """:class: `str` Returns the tier's name."""
        return self._name_locale

    @property
    def display_name(self) -> Localization:
        """:class: `Localization` alias for :attr:`name`"""
        return self.name

    @property
    def division_name(self) -> Localization:
        """:class: `str` Returns the tier's division."""
        return self._division_name_localized

    @property
    def small_icon(self) -> Optional[Asset]:
        """:class: `Asset` Returns the tier's small icon."""
        if self._small_icon is None:
            return None
        return Asset(self._state, self._small_icon)

    @property
    def large_icon(self) -> Optional[Asset]:
        """:class: `Asset` Returns the tier's large icon."""
        if self._large_icon is None:
            return None
        return Asset(self._state, self._large_icon)

    @property
    def rank_triangle_down_icon(self) -> Optional[Asset]:
        """:class: `Asset` Returns the tier's rank triangle down icon."""
        if self._rank_triangle_down_icon is None:
            return None
        return Asset(self._state, self._rank_triangle_down_icon)

    @property
    def rank_triangle_up_icon(self) -> Optional[Asset]:
        """:class: `Asset` Returns the tier's rank triangle up icon."""
        if self._rank_triangle_up_icon is None:
            return None
        return Asset(self._state, self._rank_triangle_up_icon)


class CompetitiveTier(BaseModel):
    def __init__(self, state: CacheState, data: CompetitiveTierPayload) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self.asset_object_name: str = data['assetObjectName']
        self._tiers: Dict[int, Tier] = {tier['tier']: Tier(state=self._state, data=tier) for tier in data['tiers']}
        self.asset_path: str = data['assetPath']

    def __str__(self) -> str:
        return self.asset_object_name

    def __repr__(self) -> str:
        return f'<CompetitiveTier asset_object_name={self.asset_object_name!r}>'

    @property
    def tiers(self) -> List[Tier]:
        """:class: `list` Returns the competitive tier's tiers."""
        return list(self._tiers.values())

    def get_tier(self, tier: int) -> Optional[Tier]:
        """Returns the tier with the given tier number."""
        return self._tiers.get(tier)
