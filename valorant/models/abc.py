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

import abc
from typing import TYPE_CHECKING, Dict, Optional, Union

from ..asset import Asset
from ..enums import Locale
from ..localization import Localization

if TYPE_CHECKING:
    from ..cache import CacheState
    from ..types.object import GridPosition as GridPositionPayload, ShopData as ShopDataPayload
    from .gear import Gear
    from .weapons import Weapon


__all__ = (
    'BaseModel',
    'GridPosition',
    'ShopData',
)


class BaseModel(abc.ABC):
    __slots__ = ('_uuid',)

    def __init__(self, uuid: str) -> None:
        self._uuid = uuid

    @property
    def uuid(self) -> str:
        # TODO: str to UUID
        return self._uuid

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} uuid={self.uuid!r}>'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.uuid == other.uuid

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.uuid)


class GridPosition:
    def __init__(self, data: GridPositionPayload) -> None:
        self.row: float = data['row']
        self.column: float = data['column']

    def __repr__(self) -> str:
        return f'<GridPosition row={self.row} column={self.column}>'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, GridPosition) and self.row == other.row and self.column == other.column

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)


class ShopData:
    def __init__(self, *, state: CacheState, item: Union[Weapon, Gear], data: ShopDataPayload) -> None:
        self._item: Union[Weapon, Gear] = item
        self._state: CacheState = state
        self.cost: int = data['cost']
        self.category: Optional[str] = data['category']
        self._category_text: Union[str, Dict[str, str]] = data['categoryText']
        self.grid_position: Optional[GridPosition] = None
        if data['gridPosition'] is not None:
            self.grid_position = GridPosition(data['gridPosition'])
        self.can_be_trashed: bool = data['canBeTrashed']
        self._image: Optional[str] = data['image']
        self._new_image: Optional[str] = data['newImage']
        self._new_image_2: Optional[str] = data['newImage2']
        self.asset_path: str = data['assetPath']
        self._category_text_localized: Localization = Localization(self._category_text, locale=self._state.locale)

    def __repr__(self) -> str:
        return f'<ShopData category_text={self.category_text} cost={self.cost}>'

    def __int__(self) -> int:
        return self.cost

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ShopData) and self.item == other.item and self.cost == other.cost

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def category_text_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._category_text_localized.from_locale(locale)

    @property
    def item(self) -> Union[Weapon, Gear]:
        """:class: `Weapon` or :class: `Gear` Returns the item."""
        return self._item

    @property
    def category_text(self) -> Localization:
        """:class: `str` Returns the weapon's shop category text."""
        return self._category_text_localized

    @property
    def image(self) -> Optional[Asset]:
        """:class: `Asset` Returns the weapon's image."""
        return Asset._from_url(self._state, url=self._image) if self._image else None

    @property
    def new_image(self) -> Optional[Asset]:
        """:class: `Asset` Returns the weapon's new image."""
        return Asset._from_url(self._state, url=self._new_image) if self._new_image else None

    @property
    def new_image_2(self) -> Optional[Asset]:
        """:class: `Asset` Returns the weapon's new image 2."""
        return Asset._from_url(self._state, url=self._new_image_2) if self._new_image_2 else None
