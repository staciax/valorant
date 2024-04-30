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

from ..localization import Localization
from .base import BaseModel

if TYPE_CHECKING:
    from ..cache import CacheState
    from ..enums import Locale
    from ..types.sprays import Spray as SprayPayload, SprayLevel as SprayLevelPayload
    from .themes import Theme

__all__ = (
    'Spray',
    'SprayLevel',
)


class Spray(BaseModel):
    def __init__(self, *, state: CacheState, data: SprayPayload) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self.category: Optional[str] = data['category']
        self.theme_uuid: Optional[str] = data['themeUuid']
        self._is_null_spray: bool = data['isNullSpray']
        self.display_icon: str = data['displayIcon']
        self.full_icon: Optional[str] = data['fullIcon']
        self.full_transparent_icon: Optional[str] = data['fullTransparentIcon']
        self.animation_png: Optional[str] = data['animationPng']
        self.animation_gif: Optional[str] = data['animationGif']
        self.asset_path: str = data['assetPath']
        self.levels: List[Level] = [Level(state=self._state, data=level, parent=self) for level in data['levels']]
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        return f'<Spray display_name={self.display_name!r}>'

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the skin's name."""
        return self._display_name_localized

    @property
    def theme(self) -> Optional[Theme]:
        if self.theme_uuid is None:
            return None
        return self._state.get_theme(self.theme_uuid)

    def is_null_spray(self) -> bool:
        """:class: `bool` Returns a boolean representing whether the skin is a null spray."""
        return self._is_null_spray


class Level(BaseModel):
    def __init__(self, state: CacheState, data: SprayLevelPayload, parent: Spray) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self.spray_level: int = data['sprayLevel']
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self.display_icon: Optional[str] = data['displayIcon']
        self.asset_path: str = data['assetPath']
        self.parent: Spray = parent
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        return f'<SprayLevel display_name={self.display_name!r}>'

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the spray's name."""
        return self._display_name_localized

    @property
    def level(self) -> int:
        """:class: `int` alias for :attr: `SprayLevel.spray_level`"""
        return self.spray_level


SprayLevel = Level
