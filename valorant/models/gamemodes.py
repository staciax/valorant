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
    from ..cache import CacheState
    from ..types.gamemodes import (
        GameFeatureOverride as GameFeatureOverridePayload,
        GameMode as GameModePayload,
        GameModeEquippable as GameModeEquippablePayload,
        GameRuleBoolOverride as GameRuleBoolOverridePayload,
    )
    from .weapons import Weapon

# fmt: off
__all__ = (
    'GameFeatureOverride',
    'GameMode',
    'GameModeEquippable',
    'GameRuleBoolOverride',
)
# fmt: on


class GameFeatureOverride:
    def __init__(self, data: GameFeatureOverridePayload) -> None:
        self.feature_name: str = data['featureName']
        self.state: bool = data['state']

    def __repr__(self) -> str:
        return f'<GameFeatureOverride feature_name={self.feature_name!r} state={self.state!r}>'

    def __bool__(self) -> bool:
        return self.state


class GameRuleBoolOverride:
    def __init__(self, data: GameRuleBoolOverridePayload) -> None:
        self.rule_name: str = data['ruleName']
        self.state: bool = data['state']

    def __bool__(self) -> bool:
        return self.state

    def __repr__(self) -> str:
        return f'<GameRuleBoolOverride rule_name={self.rule_name!r} state={self.state!r}>'


class GameMode(BaseModel):
    def __init__(self, state: CacheState, data: GameModePayload) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self._duration: Union[str, Dict[str, str]] = data['duration']
        self.allows_match_timeouts: bool = data['allowsMatchTimeouts']
        self._is_team_voice_allowed: bool = data['isTeamVoiceAllowed']
        self._is_minimap_hidden: bool = data['isMinimapHidden']
        self.orb_count: int = data['orbCount']
        self.rounds_per_half: int = data['roundsPerHalf']
        self.team_roles: Optional[List[str]] = data['teamRoles']
        self.game_feature_overrides: Optional[List[GameFeatureOverride]] = None
        if data['gameFeatureOverrides'] is not None:
            self.game_feature_overrides = [GameFeatureOverride(feature) for feature in data['gameFeatureOverrides']]
        self.game_rule_bool_overrides: Optional[List[GameRuleBoolOverride]] = None
        if data['gameRuleBoolOverrides'] is not None:
            self.game_rule_bool_overrides = [GameRuleBoolOverride(rule) for rule in data['gameRuleBoolOverrides']]
        self._display_icon: Optional[str] = data['displayIcon']
        self.asset_path: str = data['assetPath']
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)
        self._duration_localized: Localization = Localization(self._duration, locale=self._state.locale)

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        return f'<GameMode display_name={self.display_name!r}>'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, GameMode) and self.uuid == other.uuid

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    # def __contains__(self, item: Union[GameMode, GameModeType]) -> bool:
    #     ...

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    def duration_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._duration_localized.from_locale(locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the game mode's name."""
        return self._display_name_localized

    @property
    def duration(self) -> Localization:
        """:class: `str` Returns the game mode's duration."""
        return self._duration_localized

    @property
    def display_icon(self) -> Optional[Asset]:
        """:class: `Asset` Returns the game mode's display icon."""
        if self._display_icon is None:
            return None
        return Asset(self._state, self._display_icon)

    def is_team_voice_allowed(self) -> bool:
        """:class: `bool` Returns whether the game mode allows team voice."""
        return self._is_team_voice_allowed

    def is_minimap_hidden(self) -> bool:
        """:class: `bool` Returns whether the game mode hides the minimap."""
        return self._is_minimap_hidden


class GameModeEquippable(BaseModel):
    def __init__(self, state: CacheState, data: GameModeEquippablePayload) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self._category: Optional[str] = data['category']
        self._display_icon: str = data['displayIcon']
        self._kill_stream_icon: str = data['killStreamIcon']
        self.asset_path: str = data['assetPath']
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        return f'<GameModeEquippable display_name={self.display_name!r}>'

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the game mode's name."""
        return self._display_name_localized

    @property
    def category(self) -> Optional[str]:
        """:class: `str` Returns the game mode's category."""
        return utils.removeprefix(self._category, 'EEquippableCategory::') if self._category else None

    @property
    def display_icon(self) -> Asset:
        """:class: `Asset` Returns the game mode's display icon."""
        return Asset._from_url(self._state, url=self._display_icon)

    @property
    def kill_stream_icon(self) -> Asset:
        """:class: `Asset` Returns the game mode's kill stream icon."""
        return Asset._from_url(self._state, url=self._kill_stream_icon)

    def weapon(self) -> Optional[Weapon]:
        """:class: `Weapon` Returns the game mode's weapon."""
        # special weapon for game mode
        return self._state.get_weapon(self._uuid)
