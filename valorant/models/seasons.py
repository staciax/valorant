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
from ..enums import Locale
from ..localization import Localization
from .abc import BaseModel

if TYPE_CHECKING:
    import datetime
    from uuid import UUID

    from ..cache import CacheState
    from ..types.seasons import (
        Border as BorderPayload,
        CompetitiveSeason as CompetitiveSeasonPayload,
        Season as SeasonPayload,
    )
    from .competitive_tiers import CompetitiveTier


__all__ = (
    'Border',
    'CompetitiveSeason',
    'Season',
)


class Season(BaseModel):
    def __init__(self, state: CacheState, data: SeasonPayload) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self.type: Optional[str] = data['type']
        self._start_time_iso: Union[str, datetime.datetime] = data['startTime']
        self._end_time_iso: Union[str, datetime.datetime] = data['endTime']
        self._parent_uuid: Optional[str] = data['parentUuid']
        self.asset_path: str = data['assetPath']
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        attrs = [('display_name', self.display_name), ('type', self.type)]
        joined = ' '.join('%s=%r' % t for t in attrs)
        return f'<{self.__class__.__name__} {joined}>'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Season) and other.id == self.id

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @property
    def id(self) -> UUID:
        return self.uuid

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the season's name."""
        return self._display_name_localized

    @property
    def start_time(self) -> datetime.datetime:
        """:class: `datetime.datetime` Returns the season's start time."""
        return utils.parse_iso_datetime(str(self._start_time_iso))

    @property
    def end_time(self) -> datetime.datetime:
        """:class: `datetime.datetime` Returns the season's end time."""
        return utils.parse_iso_datetime(str(self._end_time_iso))

    @property
    def parent(self) -> Optional[Season]:
        """:class: `Season` Returns the season's parent."""
        return self._state.get_season(self._parent_uuid)


class Border(BaseModel):
    def __init__(self, *, state: CacheState, data: BorderPayload) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self.level: int = data['level']
        self.wins_required: int = data['winsRequired']
        self._display_icon: Optional[str] = data['displayIcon']
        self._small_icon: Optional[str] = data['smallIcon']
        self.asset_path: str = data['assetPath']

    def __repr__(self) -> str:
        attrs = [('level', self.level), ('wins_required', self.wins_required)]
        joined = ' '.join('%s=%r' % t for t in attrs)
        return f'<{self.__class__.__name__} {joined}>'

    @property
    def display_icon(self) -> Optional[Asset]:
        """:class: `Asset` Returns the border's display icon."""
        if self._display_icon is None:
            return None
        return Asset._from_url(self._state, url=self._display_icon)

    @property
    def small_icon(self) -> Optional[Asset]:
        """:class: `Asset` Returns the border's small icon."""
        if self._small_icon is None:
            return None
        return Asset._from_url(self._state, url=self._small_icon)


class CompetitiveSeason(BaseModel):
    def __init__(self, state: CacheState, data: CompetitiveSeasonPayload) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._start_time_iso: Union[str, datetime.datetime] = data['startTime']
        self._end_time_iso: Union[str, datetime.datetime] = data['endTime']
        self.season_uuid: str = data['seasonUuid']
        self.competitive_tiers_uuid: str = data['competitiveTiersUuid']
        self.borders: Optional[List[Border]] = None
        if data['borders'] is not None:
            self.borders = [Border(state=self._state, data=border) for border in data['borders']]
        self.asset_path: str = data['assetPath']

    def __repr__(self) -> str:
        attrs = [
            ('start_time', self.start_time),
            ('end_time', self.end_time),
        ]
        joined = ' '.join('%s=%r' % t for t in attrs)
        return f'<{self.__class__.__name__} {joined}>'

    @property
    def start_time(self) -> datetime.datetime:
        """:class: `datetime.datetime` Returns the season's start time."""
        return utils.parse_iso_datetime(str(self._start_time_iso))

    @property
    def end_time(self) -> datetime.datetime:
        """:class: `datetime.datetime` Returns the season's end time."""
        return utils.parse_iso_datetime(str(self._end_time_iso))

    @property
    def season(self) -> Optional[Season]:
        """:class: `Season` Returns the season."""
        return self._state.get_season(self.season_uuid)

    @property
    def competitive_tiers(self) -> Optional[CompetitiveTier]:
        """:class: `CompetitiveTier` Returns the competitive tiers."""
        return self._state.get_competitive_tier(self.competitive_tiers_uuid)
