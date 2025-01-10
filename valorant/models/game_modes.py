"""
The MIT License (MIT).

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

from pydantic import Field

from ..enums import GameFeature, GameRule
from .base import BaseModel, BaseUUIDModel
from .localization import LocalizedField

__all__ = (
    'Equippable',
    'GameFeatureOverride',
    'GameMode',
    'GameRuleBoolOverride',
)

if TYPE_CHECKING:
    from ..client import Client
    from .weapons import Weapon


class GameFeatureOverride(BaseModel):
    feature_name: GameFeature = Field(alias='featureName')
    state: bool


class GameRuleBoolOverride(BaseModel):
    rule_name: GameRule = Field(alias='ruleName')
    state: bool


class GameMode(BaseUUIDModel):
    # uuid: str
    display_name: str | LocalizedField = Field(alias='displayName')
    description: str | LocalizedField | None
    duration: str | LocalizedField | None
    economy_type: str | None = Field(alias='economyType')
    allows_match_timeouts: bool = Field(alias='allowsMatchTimeouts')
    is_team_voice_allowed: bool = Field(alias='isTeamVoiceAllowed')
    is_minimap_hidden: bool = Field(alias='isMinimapHidden')
    orb_count: int = Field(alias='orbCount')
    rounds_per_half: int = Field(alias='roundsPerHalf')
    team_roles: list[str] | None = Field(alias='teamRoles')
    game_feature_overrides: list[GameFeatureOverride] | None = Field(alias='gameFeatureOverrides')
    game_rule_bool_overrides: list[GameRuleBoolOverride] | None = Field(alias='gameRuleBoolOverrides')
    display_icon: str | None = Field(alias='displayIcon')
    list_view_icon_tall: str | None = Field(alias='listViewIconTall')
    asset_path: str = Field(alias='assetPath')


class Equippable(BaseUUIDModel):
    # uuid: str
    display_name: str | LocalizedField = Field(alias='displayName')
    category: str
    display_icon: str = Field(alias='displayIcon')
    kill_stream_icon: str = Field(alias='killStreamIcon')
    asset_path: str = Field(alias='assetPath')

    # useful methods

    async def fetch_weapon(self, *, client: Client) -> Weapon | None:
        return await client.fetch_weapon(str(self.uuid))
