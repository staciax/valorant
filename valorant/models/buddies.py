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

from .base import BaseModel, LocalizedField

__all__ = (
    'Buddy',
    'Level',
)


class Level(BaseModel):
    uuid: str
    charm_level: int = Field(alias='charmLevel')
    hide_if_not_owned: bool = Field(alias='hideIfNotOwned')
    display_name: LocalizedField = Field(alias='displayName')
    display_icon: str = Field(alias='displayIcon')
    asset_path: str = Field(alias='assetPath')

    def __repr__(self) -> str:
        return f'<Level display_name={self.display_name!r}>'


class Buddy(BaseModel):
    uuid: str
    display_name: LocalizedField = Field(alias='displayName')
    is_hidden_if_not_owned: bool = Field(alias='isHiddenIfNotOwned')
    theme_uuid: Any = Field(alias='themeUuid')
    display_icon: str = Field(alias='displayIcon')
    asset_path: str = Field(alias='assetPath')
    levels: list[Level]

    def __repr__(self) -> str:
        return f'<Buddy display_name={self.display_name!r}>'
