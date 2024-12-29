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

from pydantic import Field

from .base import BaseModel, LocalizedField

__all__ = (
    'Border',
    'Competitive',
    'Season',
)


class Season(BaseModel):
    uuid: str
    display_name: LocalizedField = Field(alias='displayName')
    title: LocalizedField | None
    type: str | None
    start_time: datetime = Field(alias='startTime')
    end_time: datetime = Field(alias='endTime')
    parent_uuid: str | None = Field(alias='parentUuid')
    asset_path: str = Field(alias='assetPath')


class Border(BaseModel):
    uuid: str
    level: int
    wins_required: int = Field(alias='winsRequired')
    display_icon: str = Field(alias='displayIcon')
    small_icon: str | None = Field(alias='smallIcon')
    asset_path: str = Field(alias='assetPath')


class Competitive(BaseModel):
    uuid: str
    start_time: datetime = Field(alias='startTime')
    end_time: datetime = Field(alias='endTime')
    season_uuid: str = Field(alias='seasonUuid')
    competitive_tiers_uuid: str = Field(alias='competitiveTiersUuid')
    borders: list[Border] | None
    asset_path: str = Field(alias='assetPath')
