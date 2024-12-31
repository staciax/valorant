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
from uuid import UUID

from pydantic import Field

from ..enums import MissionTag, MissionType
from .base import BaseModel, BaseUUIDModel
from .localization import LocalizedField

__all__ = (
    'Mission',
    'Objective',
)


class Objective(BaseModel):
    objective_uuid: UUID = Field(alias='objectiveUuid')
    value: int


class Mission(BaseUUIDModel):
    # uuid: str
    display_name: str | LocalizedField | None = Field(alias='displayName')
    title: str | LocalizedField | None
    type: MissionType | None
    xp_grant: int = Field(alias='xpGrant')
    progress_to_complete: int = Field(alias='progressToComplete')
    activation_date: datetime = Field(alias='activationDate')
    expiration_date: datetime = Field(alias='expirationDate')
    tags: list[MissionTag] | None
    objectives: list[Objective] | None
    asset_path: str = Field(alias='assetPath')
