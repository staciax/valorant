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

from typing import Any

from pydantic import Field

from .base import BaseModel, BaseUUIDModel
from .localization import LocalizedField

__all__ = (
    'Callout',
    'Location',
    'Map',
)


class Location(BaseModel):
    x: float
    y: float


class Callout(BaseModel):
    region_name: str | LocalizedField = Field(alias='regionName')
    super_region_name: str | LocalizedField = Field(alias='superRegionName')
    location: Location


class Map(BaseUUIDModel):
    # uuid: str
    display_name: str | LocalizedField = Field(alias='displayName')
    narrative_description: Any = Field(alias='narrativeDescription')
    tactical_description: str | LocalizedField | None = Field(alias='tacticalDescription')
    coordinates: str | LocalizedField | None
    display_icon: str | None = Field(alias='displayIcon')
    list_view_icon: str = Field(alias='listViewIcon')
    list_view_icon_tall: str | None = Field(alias='listViewIconTall')
    splash: str
    stylized_background_image: str | None = Field(alias='stylizedBackgroundImage')
    premier_background_image: str | None = Field(alias='premierBackgroundImage')
    asset_path: str = Field(alias='assetPath')
    map_url: str = Field(alias='mapUrl')
    x_multiplier: float = Field(alias='xMultiplier')
    y_multiplier: float = Field(alias='yMultiplier')
    x_scalar_to_add: float = Field(alias='xScalarToAdd')
    y_scalar_to_add: float = Field(alias='yScalarToAdd')
    callouts: list[Callout] | None
