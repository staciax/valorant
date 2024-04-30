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
from ..enums import Locale, MissionType, try_enum
from ..localization import Localization
from .base import BaseModel

if TYPE_CHECKING:
    import datetime

    from ..cache import CacheState
    from ..types.missions import Mission as MissionPayload, Objective as ObjectivePayload

# fmt: off
__all__ = (
    'Mission',
)
# fmt: on


class Objective(BaseModel):
    def __init__(self, data: ObjectivePayload) -> None:
        super().__init__(data['objectiveUuid'])
        self.value: int = data['value']

    def __repr__(self) -> str:
        return f'<Objective value={self.value!r}>'

    def __str__(self) -> str:
        return str(self.value)

    def __int__(self) -> int:
        return self.value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Objective) and self.value == other.value

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: object) -> bool:
        return isinstance(other, Objective) and self.value < other.value

    def __le__(self, other: object) -> bool:
        return isinstance(other, Objective) and self.value <= other.value

    def __gt__(self, other: object) -> bool:
        return isinstance(other, Objective) and self.value > other.value

    def __ge__(self, other: object) -> bool:
        return isinstance(other, Objective) and self.value >= other.value


class Mission(BaseModel):
    def __init__(self, state: CacheState, data: MissionPayload) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._display_name: Optional[Union[str, Dict[str, str]]] = data['displayName']
        self._title: Optional[Union[str, Dict[str, str]]] = data['title']
        self.type: MissionType = MissionType.none
        if data['type'] is not None:
            self.type = try_enum(MissionType, data['type'])
        self.xp_grant: int = data['xpGrant']
        self.progress_to_complete: int = data['progressToComplete']
        self._activation_date_iso: str = data['activationDate']
        self._expiration_date_iso: str = data['expirationDate']
        self.tags: Optional[List[str]] = data['tags']
        self.objectives: Optional[List[Objective]] = None
        if data['objectives'] is not None:
            self.objectives = [Objective(obj) for obj in data['objectives']]
        self.asset_path: str = data['assetPath']
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)
        self._title_localized: Localization = Localization(self._title, locale=self._state.locale)

    def __str__(self) -> str:
        return self.title.locale

    def __repr__(self) -> str:
        return f'<Mission title={self.title!r}>'

    def __int__(self) -> int:
        return self.xp_grant

    @property
    def xp(self) -> int:
        """:class: `int` alias for :attr: `Mission.xp_grant`"""
        return self.xp_grant

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    def title_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._title_localized.from_locale(locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the mission's name."""
        return self._display_name_localized

    @property
    def title(self) -> Localization:
        """:class: `str` Returns the mission's title."""
        return self._title_localized

    @property
    def activation_date(self) -> Optional[datetime.datetime]:
        """:class: `datetime.datetime` Returns the mission's activation date."""
        return utils.parse_iso_datetime(self._activation_date_iso) if self._activation_date_iso else None

    @property
    def expiration_date(self) -> Optional[datetime.datetime]:
        """:class: `datetime.datetime` Returns the mission's expiration date."""
        return utils.parse_iso_datetime(self._expiration_date_iso) if self._expiration_date_iso else None
