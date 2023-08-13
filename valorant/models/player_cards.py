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

from typing import TYPE_CHECKING, Dict, Optional, Union

from ..asset import Asset
from ..enums import Locale
from ..localization import Localization
from .abc import BaseModel

if TYPE_CHECKING:
    from ..cache import CacheState
    from ..types.player_cards import PlayerCard as PlayerCardPayload
    from .themes import Theme

# fmt: off
__all__ = (
    'PlayerCard',
)
# fmt: on


class PlayerCard(BaseModel):
    def __init__(self, *, state: CacheState, data: PlayerCardPayload) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self._is_hidden_if_not_owned: bool = data.get('isHiddenIfNotOwned', False)
        self._theme_uuid: Optional[str] = data['themeUuid']
        self._display_icon: Optional[str] = data['displayIcon']
        self._small_art: Optional[str] = data['smallArt']
        self._wide_art: Optional[str] = data['wideArt']
        self._large_art: Optional[str] = data['largeArt']
        self.asset_path: str = data['assetPath']

        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        return f'<PlayerCard display_name={self.display_name!r}>'

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the player card's name."""
        return self._display_name_localized

    @property
    def display_icon(self) -> Optional[Asset]:
        """:class: `Asset` Returns the player card's icon."""
        if self._display_icon is None:
            return None
        return Asset._from_url(state=self._state, url=self._display_icon)

    @property
    def small_art(self) -> Optional[Asset]:
        """:class: `Asset` Returns the player card's small art."""
        if self._small_art is None:
            return None
        return Asset._from_url(state=self._state, url=self._small_art)

    @property
    def wide_art(self) -> Optional[Asset]:
        """:class: `Asset` Returns the player card's wide art."""
        if self._wide_art is None:
            return None
        return Asset._from_url(state=self._state, url=self._wide_art)

    @property
    def large_art(self) -> Optional[Asset]:
        """:class: `Asset` Returns the player card's large art."""
        if self._large_art is None:
            return None
        return Asset._from_url(state=self._state, url=self._large_art)

    @property
    def theme(self) -> Optional[Theme]:
        """:class: `Theme` Returns the player card's theme."""
        return self._state.get_theme(self._theme_uuid)

    def is_hidden_if_not_owned(self) -> bool:
        """:class: `bool` Returns whether the player card is hidden if not owned."""
        return self._is_hidden_if_not_owned
