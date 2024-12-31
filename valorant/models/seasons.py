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

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import Field

from ..enums import SeasonType
from .base import BaseUUIDModel
from .localization import LocalizedField

__all__ = (
    'Border',
    'Competitive',
    'Season',
)

if TYPE_CHECKING:
    from ..client import Client


class Season(BaseUUIDModel):
    # uuid: str
    display_name: str | LocalizedField = Field(alias='displayName')
    title: str | LocalizedField | None
    type: SeasonType | None
    start_time: datetime = Field(alias='startTime')
    end_time: datetime = Field(alias='endTime')
    parent_uuid: UUID | None = Field(alias='parentUuid')
    asset_path: str = Field(alias='assetPath')

    # useful methods

    async def fetch_parent(self, *, client: Client) -> Season | None:
        if self.parent_uuid is None:
            return None
        return await client.fetch_season(str(self.parent_uuid))


class Border(BaseUUIDModel):
    # uuid: str
    level: int
    wins_required: int = Field(alias='winsRequired')
    display_icon: str = Field(alias='displayIcon')
    small_icon: str | None = Field(alias='smallIcon')
    asset_path: str = Field(alias='assetPath')


class Competitive(BaseUUIDModel):
    # uuid: str
    start_time: datetime = Field(alias='startTime')
    end_time: datetime = Field(alias='endTime')
    season_uuid: UUID = Field(alias='seasonUuid')
    competitive_tiers_uuid: UUID = Field(alias='competitiveTiersUuid')
    borders: list[Border] | None
    asset_path: str = Field(alias='assetPath')

    async def fetch_season(self, *, client: Client) -> Season | None:
        return await client.fetch_season(str(self.season_uuid))
