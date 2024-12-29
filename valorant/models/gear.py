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
    'Detail',
    'Gear',
    'ShopData',
)


class Detail(BaseModel):
    name: LocalizedField
    value: LocalizedField


class ShopData(BaseModel):
    cost: int
    category: str
    shop_order_priority: int = Field(alias='shopOrderPriority')
    category_text: LocalizedField = Field(alias='categoryText')
    grid_position: Any = Field(alias='gridPosition')
    can_be_trashed: bool = Field(alias='canBeTrashed')
    image: Any
    new_image: str = Field(alias='newImage')
    new_image2: Any = Field(alias='newImage2')
    asset_path: str = Field(alias='assetPath')


class Gear(BaseModel):
    uuid: str
    display_name: LocalizedField = Field(alias='displayName')
    description: LocalizedField
    descriptions: list[LocalizedField]
    details: list[Detail]
    display_icon: str = Field(alias='displayIcon')
    asset_path: str = Field(alias='assetPath')
    shop_data: ShopData = Field(alias='shopData')
