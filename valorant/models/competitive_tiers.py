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

from pydantic import Field
from pydantic_extra_types.color import Color

from ..enums import DivisionTier
from .base import BaseModel, BaseUUIDModel
from .localization import LocalizedField

__all__ = (
    'CompetitiveTier',
    'Tier',
)


class Tier(BaseModel):
    tier: int
    tier_name: str | LocalizedField = Field(alias='tierName')
    division: DivisionTier
    division_name: str | LocalizedField = Field(alias='divisionName')
    color: Color
    background_color: Color = Field(alias='backgroundColor')
    small_icon: str | None = Field(alias='smallIcon')
    large_icon: str | None = Field(alias='largeIcon')
    rank_triangle_down_icon: str | None = Field(alias='rankTriangleDownIcon')
    rank_triangle_up_icon: str | None = Field(alias='rankTriangleUpIcon')


class CompetitiveTier(BaseUUIDModel):
    # uuid: str
    asset_object_name: str = Field(alias='assetObjectName')
    tiers: list[Tier]
    asset_path: str = Field(alias='assetPath')
