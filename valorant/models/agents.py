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

from datetime import datetime
from typing import Any

from pydantic import Field
from pydantic_extra_types.color import Color

from ..enums import AbilitySlot
from .base import BaseModel, BaseUUIDModel
from .localization import LocalizedField  # Changed from language to localization

__all__ = (
    'Ability',
    'Agent',
    'Recruitment',
    'Role',
)


class Role(BaseUUIDModel):
    # uuid: str
    display_name: str | LocalizedField = Field(alias='displayName')
    description: str | LocalizedField
    display_icon: str = Field(alias='displayIcon')
    asset_path: str = Field(alias='assetPath')

    def __repr__(self) -> str:
        return f'<Role display_name={self.display_name!r}>'


class Recruitment(BaseModel):
    counter_id: str = Field(alias='counterId')
    milestone_id: str = Field(alias='milestoneId')
    milestone_threshold: int = Field(alias='milestoneThreshold')
    use_level_vp_cost_override: bool = Field(alias='useLevelVpCostOverride')
    level_vp_cost_override: int = Field(alias='levelVpCostOverride')
    start_date: datetime = Field(alias='startDate')
    end_date: datetime = Field(alias='endDate')


class Ability(BaseModel):
    slot: AbilitySlot
    display_name: str | LocalizedField = Field(alias='displayName')
    description: str | LocalizedField
    display_icon: str | None = Field(alias='displayIcon')

    def __repr__(self) -> str:
        return f'<Ability display_name={self.display_name!r}>'


class Agent(BaseUUIDModel):
    # uuid: str
    display_name: str | LocalizedField = Field(alias='displayName')
    description: str | LocalizedField
    developer_name: str = Field(alias='developerName')
    release_date: datetime = Field(alias='releaseDate')
    character_tags: list[str | LocalizedField] | None = Field(alias='characterTags')
    display_icon: str = Field(alias='displayIcon')
    display_icon_small: str = Field(alias='displayIconSmall')
    bust_portrait: str | None = Field(alias='bustPortrait')
    full_portrait: str | None = Field(alias='fullPortrait')
    full_portrait_v2: str | None = Field(alias='fullPortraitV2')
    killfeed_portrait: str = Field(alias='killfeedPortrait')
    background: str | None
    background_gradient_colors: list[Color] = Field(alias='backgroundGradientColors')
    asset_path: str = Field(alias='assetPath')
    is_full_portrait_right_facing: bool = Field(alias='isFullPortraitRightFacing')
    is_playable_character: bool = Field(alias='isPlayableCharacter')
    is_available_for_test: bool = Field(alias='isAvailableForTest')
    is_base_content: bool = Field(alias='isBaseContent')
    role: Role | None
    recruitment_data: Recruitment | None = Field(alias='recruitmentData')
    abilities: list[Ability]
    voice_line: Any = Field(alias='voiceLine')

    def __repr__(self) -> str:
        return f'<Agent display_name={self.display_name!r}>'
