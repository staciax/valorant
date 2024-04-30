

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

from typing import TYPE_CHECKING

from ..asset import Asset
from .base import BaseModel

# fmt: off
__all__ = (
    'LevelBorder',
)
# fmt: on

if TYPE_CHECKING:
    from ..cache import CacheState
    from ..types.level_borders import LevelBorder as LevelBorderPayload


class LevelBorder(BaseModel):
    def __init__(self, state: CacheState, data: LevelBorderPayload) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self.starting_level: int = data['startingLevel']
        self._level_number_appearance: str = data['levelNumberAppearance']
        self._small_player_card_appearance: str = data['smallPlayerCardAppearance']
        self.asset_path: str = data['assetPath']

    def __repr__(self) -> str:
        return f'<LevelBorder starting_level={self.starting_level!r}>'

    def __lt__(self, other: object) -> bool:
        return isinstance(other, LevelBorder) and self.starting_level < other.starting_level

    def __le__(self, other: object) -> bool:
        return isinstance(other, LevelBorder) and self.starting_level <= other.starting_level

    def __gt__(self, other: object) -> bool:
        return isinstance(other, LevelBorder) and self.starting_level > other.starting_level

    def __ge__(self, other: object) -> bool:
        return isinstance(other, LevelBorder) and self.starting_level >= other.starting_level

    @property
    def level_number_appearance(self) -> Asset:
        """:class: `Asset` Returns the level number appearance of the level border."""
        return Asset._from_url(state=self._state, url=self._level_number_appearance)

    @property
    def small_player_card_appearance(self) -> Asset:
        """:class: `Asset` Returns the small player card appearance of the level border."""
        return Asset._from_url(state=self._state, url=self._small_player_card_appearance)
