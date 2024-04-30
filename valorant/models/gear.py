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
from ..localization import Localization
from .base import BaseModel, ShopData

if TYPE_CHECKING:
    from ..cache import CacheState
    from ..enums import Locale
    from ..types.gear import Gear_ as GearPayload

# fmt: off
__all__ = (
    'Gear',
)
# fmt: on


class Gear(BaseModel):
    def __init__(self, state: CacheState, data: GearPayload) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self._description: Union[str, Dict[str, str]] = data['description']
        self._display_icon: str = data['displayIcon']
        self.asset_path: str = data['assetPath']
        self.shop_data: ShopData = ShopData(state=self._state, item=self, data=data['shopData'])
        self._display_name_localized = Localization(self._display_name, locale=self._state.locale)
        self._description_localized = Localization(self._description, locale=self._state.locale)

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        return f'<Gear display_name={self.display_name!r}>'

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    def description_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._description_localized.from_locale(locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the gear's name."""
        return self._display_name_localized

    @property
    def description(self) -> Localization:
        """:class: `str` Returns the gear's description."""
        return self._description_localized

    @property
    def display_icon(self) -> Asset:
        """:class: `Asset` Returns the gear's display icon."""
        return Asset._from_url(state=self._state, url=self._display_icon)
