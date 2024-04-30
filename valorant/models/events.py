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

from .. import utils
from ..localization import Localization
from .base import BaseModel

if TYPE_CHECKING:
    import datetime

    from ..cache import CacheState
    from ..enums import Locale
    from ..types.events import Event as EventPayload

# fmt: off
__all__ = (
    'Event',
)
# fmt: on


class Event(BaseModel):
    def __init__(self, state: CacheState, data: EventPayload) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self._short_display_name: Union[str, Dict[str, str]] = data['shortDisplayName']
        self._start_time_iso: str = data['startTime']
        self._end_time_iso: str = data['endTime']
        self.asset_path: str = data['assetPath']
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)
        self._short_display_name_localized: Localization = Localization(
            self._short_display_name, locale=self._state.locale
        )

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        return f'<Event display_name={self.display_name!r}>'

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    def short_display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._short_display_name_localized.from_locale(locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the agent's name."""
        return self._display_name_localized

    @property
    def short_display_name(self) -> Localization:
        """:class: `str` Returns the agent's short name."""
        return self._short_display_name_localized

    @property
    def start_time(self) -> datetime.datetime:
        """:class: `datetime.datetime` Returns the event's start time."""
        return utils.parse_iso_datetime(self._start_time_iso)

    @property
    def end_time(self) -> datetime.datetime:
        """:class: `datetime.datetime` Returns the event's end time."""
        return utils.parse_iso_datetime(self._end_time_iso)
