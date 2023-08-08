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

from typing import TYPE_CHECKING, Dict, Generic, List, Optional, TypeVar, Union

from ..asset import Asset
from ..enums import Locale
from ..localization import Localization
from .abc import BaseModel

if TYPE_CHECKING:
    from typing_extensions import Self

    from ..cache import CacheState
    from ..types.buddies import Buddy as BuddyPayload, BuddyLevel as BuddyLevelPayload
    from .themes import Theme

__all__ = (
    'Buddy',
    'BuddyLevel',
)

BuddyT = TypeVar('BuddyT', bound='Buddy')


class Buddy(BaseModel):
    def __init__(self, *, state: CacheState, data: BuddyPayload) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self._is_hidden_if_not_owned: bool = data['isHiddenIfNotOwned']
        self._theme_uuid: Optional[str] = data['themeUuid']
        self._display_icon: Optional[str] = data['displayIcon']
        self.asset_path: str = data['assetPath']
        self.levels: List[BuddyLevel] = [BuddyLevel(state=self._state, data=level, parent=self) for level in data['levels']]
        self._name_localized = Localization(self._display_name, locale=self._state.locale)

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        return f'<Buddy display_name={self.display_name!r}>'

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._name_localized.from_locale(locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the buddy's name."""
        return self._name_localized

    @property
    def theme(self) -> Optional[Theme]:
        """:class: `Theme` Returns the buddy's theme."""
        # Avoid circular import
        return self._state.get_theme(self._theme_uuid)

    @property
    def display_icon(self) -> Asset:
        """:class: `Asset` Returns the buddy's icon."""
        return Asset._from_url(state=self._state, url=self._display_icon)

    def is_hidden_if_not_owned(self) -> bool:
        """:class: `bool` Returns whether the buddy is hidden if not owned."""
        return self._is_hidden_if_not_owned

    # helper methods

    def get_buddy_level(self, level: int = 1) -> Optional[BuddyLevel]:
        """Returns the buddy level for the given level number."""
        return next((b for b in self.levels if b.charm_level == level), None)

    @classmethod
    def _copy(cls, buddy: Self) -> Self:
        """Creates a copy of the given buddy."""
        self = cls.__new__(cls)  # bypass __init__
        self._uuid = buddy._uuid
        self._state = buddy._state
        self._display_name = buddy._display_name
        self._is_hidden_if_not_owned = buddy._is_hidden_if_not_owned
        self._theme_uuid = buddy._theme_uuid
        self._display_icon = buddy._display_icon
        self.asset_path = buddy.asset_path
        self.levels = buddy.levels.copy()
        self._name_localized = buddy._name_localized
        return self


class BuddyLevel(BaseModel, Generic[BuddyT]):
    def __init__(self, *, state: CacheState, data: BuddyLevelPayload, parent: BuddyT) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._data: BuddyLevelPayload = data
        self.charm_level: int = data['charmLevel']
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self._display_icon: Optional[str] = data['displayIcon']
        self.asset_path: str = data['assetPath']
        self.parent: BuddyT = parent
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        return f'<BuddyLevel display_name={self.display_name!r}>'

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    @property
    def level(self) -> int:
        """:class: `int` alias for :attr: `BuddyLevel.charm_level`"""
        return self.charm_level

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the buddy's name."""
        return self._display_name_localized

    @property
    def display_icon(self) -> Asset:
        """:class: `str` Returns the buddy's display icon."""
        return Asset._from_url(state=self._state, url=self._display_icon)

    @classmethod
    def _copy(cls, buddy_level: Self) -> Self:
        """Creates a copy of the given buddy level."""
        self = cls.__new__(cls)  # bypass __init__
        self._uuid = buddy_level._uuid
        self._state = buddy_level._state
        self._data = buddy_level._data.copy()
        self.charm_level = buddy_level.charm_level
        self._display_name = buddy_level._display_name
        self._display_icon = buddy_level._display_icon
        self.asset_path = buddy_level.asset_path
        self.parent = buddy_level.parent._copy(buddy_level.parent)
        self._display_name_localized = buddy_level._display_name_localized
        return self
