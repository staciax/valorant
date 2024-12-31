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

from .base import BaseUUIDModel
from .localization import LocalizedField

__all__ = ('Bundle',)


class Bundle(BaseUUIDModel):
    # uuid: str
    display_name: str | LocalizedField = Field(alias='displayName')
    display_name_sub_text: str | LocalizedField | None = Field(alias='displayNameSubText')
    description: str | LocalizedField
    extra_description: str | LocalizedField | None = Field(alias='extraDescription')
    promo_description: str | LocalizedField | None = Field(alias='promoDescription')
    use_additional_context: bool = Field(alias='useAdditionalContext')
    display_icon: str = Field(alias='displayIcon')
    display_icon2: str = Field(alias='displayIcon2')
    logo_icon: str | None = Field(alias='logoIcon')
    vertical_promo_image: str | None = Field(alias='verticalPromoImage')
    asset_path: str = Field(alias='assetPath')
