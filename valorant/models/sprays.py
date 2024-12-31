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
from uuid import UUID

from pydantic import Field

from .base import BaseUUIDModel
from .localization import LocalizedField

__all__ = (
    'Level',
    'Spray',
)

if TYPE_CHECKING:
    from ..client import Client
    from .themes import Theme


class Level(BaseUUIDModel):
    # uuid: str
    spray_level: int = Field(alias='sprayLevel')
    display_name: str | LocalizedField = Field(alias='displayName')
    display_icon: str | None = Field(alias='displayIcon')
    asset_path: str = Field(alias='assetPath')


class Spray(BaseUUIDModel):
    # uuid: str
    display_name: str | LocalizedField = Field(alias='displayName')
    category: str | None
    theme_uuid: UUID | None = Field(alias='themeUuid')
    is_null_spray: bool = Field(alias='isNullSpray')
    hide_if_not_owned: bool = Field(alias='hideIfNotOwned')
    display_icon: str | None = Field(alias='displayIcon')
    full_icon: str | None = Field(alias='fullIcon')
    full_transparent_icon: str | None = Field(alias='fullTransparentIcon')
    animation_png: str | None = Field(alias='animationPng')
    animation_gif: str | None = Field(alias='animationGif')
    asset_path: str = Field(alias='assetPath')
    levels: list[Level]

    # useful methods

    async def fetch_theme(self, *, client: Client) -> Theme | None:
        if self.theme_uuid is None:
            return None
        return await client.fetch_theme(str(self.theme_uuid))
