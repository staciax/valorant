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
    from ..types.bundles import Bundle as BundlePayload
    from .buddies import Buddy
    from .player_cards import PlayerCard
    from .player_titles import PlayerTitle
    from .sprays import Spray
    from .weapons import Skin

    BundleItem = Union[Skin, Buddy, Spray, PlayerCard, PlayerTitle]

# fmt: off
__all__ = (
    'Bundle',
)
# fmt: on


class Bundle(BaseModel):
    def __init__(self, *, state: CacheState, data: BundlePayload) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self._display_name_sub_text: Optional[Union[str, Dict[str, str]]] = data['displayNameSubText']
        self._description: Union[str, Dict[str, str]] = data['description']
        self._extra_description: Optional[Union[str, Dict[str, str]]] = data['extraDescription']
        self._promo_description: Optional[Union[str, Dict[str, str]]] = data['promoDescription']
        self.use_additional_context: bool = data['useAdditionalContext']
        self.display_icon: str = data['displayIcon']
        self.display_icon_2: str = data['displayIcon2']
        self.vertical_promo_image: str = data['verticalPromoImage']
        self.asset_path: str = data['assetPath']
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)
        self._display_name_sub_text_localized: Localization = Localization(
            self._display_name_sub_text, locale=self._state.locale
        )
        self._description_localized: Localization = Localization(self._description, locale=self._state.locale)
        self._extra_description_localized: Localization = Localization(
            self._extra_description, locale=self._state.locale
        )
        self._promo_description_localized: Localization = Localization(
            self._promo_description, locale=self._state.locale
        )
        self._items: List[BundleItem] = []

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        return f'<Bundle display_name={self.display_name!r}>'

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    def display_name_sub_text_localized(self, locale: Optional[Union[Locale, str]] = None) -> Optional[str]:
        if self._description is None:
            return None
        return self._display_name_sub_text_localized.from_locale(locale)

    def description_localized(self, locale: Optional[Union[Locale, str]] = None) -> Optional[str]:
        if self._description is None:
            return None
        return self._description_localized.from_locale(locale)

    def extra_description_localized(self, locale: Optional[Union[Locale, str]] = None) -> Optional[str]:
        if self._extra_description is None:
            return None
        return self._extra_description_localized.from_locale(locale)

    def promo_description_localized(self, locale: Optional[Union[Locale, str]] = None) -> Optional[str]:
        if self._promo_description is None:
            return None
        return self._promo_description_localized.from_locale(locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the bundle's name."""
        return self._display_name_localized

    @property
    def display_name_sub_text(self) -> Optional[Localization]:
        """:class: `str` Returns the bundle's sub name."""
        if self._display_name_sub_text is None:
            return None
        return self._display_name_sub_text_localized

    @property
    def description(self) -> Optional[Localization]:
        """:class: `str` Returns the bundle's description."""
        if self._description is None:
            return None
        return self._description_localized

    @property
    def extra_description(self) -> Optional[Localization]:
        """:class: `str` Returns the bundle's description extra localizations."""
        if self._extra_description is None:
            return None
        return self._extra_description_localized

    @property
    def promo_description(self) -> Optional[Localization]:
        """:class: `str` Returns the bundle's description promo."""
        if self._promo_description is None:
            return None
        return self._promo_description_localized

    def _add_item(self, item: Union[Skin, Buddy, Spray, PlayerCard]) -> None:
        self._items.append(item)

    @property
    def items(self) -> List[BundleItem]:
        """:class: `List[Union[Buddy, Spray, PlayerCard]]` Returns the bundle's items."""
        return self._items

    @property
    def buddies(self) -> List[Buddy]:
        """:class: `List[Buddy]` Returns the bundle's buddies."""
        # avoid circular imports
        from .buddies import Buddy

        return [item for item in self._items if isinstance(item, Buddy)]

    @property
    def sprays(self) -> List[Spray]:
        """:class: `List[Spray]` Returns the bundle's sprays."""
        # avoid circular imports
        from .sprays import Spray

        return [item for item in self._items if isinstance(item, Spray)]

    @property
    def player_cards(self) -> List[PlayerCard]:
        """:class: `List[PlayerCard]` Returns the bundle's player cards."""
        # avoid circular imports
        from .player_cards import PlayerCard

        return [item for item in self._items if isinstance(item, PlayerCard)]

    @property
    def skins(self) -> List[Skin]:
        """:class: `List[Skin]` Returns the bundle's skins."""
        # avoid circular imports
        from .weapons import Skin

        return [item for item in self._items if isinstance(item, Skin)]
