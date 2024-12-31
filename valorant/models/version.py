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
from functools import cached_property
from typing import NamedTuple

from pydantic import BaseModel, Field, computed_field

__all__ = ('Version',)


class VersionInfo(NamedTuple):
    major: int
    minor: int
    patch: int
    build: int


class Version(BaseModel):
    manifest_id: str = Field(alias='manifestId')
    branch: str
    version: str
    build_version: str = Field(alias='buildVersion')
    engine_version: str = Field(alias='engineVersion')
    riot_client_version: str = Field(alias='riotClientVersion')
    riot_client_build: str = Field(alias='riotClientBuild')
    build_date: datetime = Field(alias='buildDate')

    @computed_field  # type: ignore[prop-decorator]
    @cached_property
    def version_info(self) -> VersionInfo:
        major, minor, patch, build = map(int, self.version.split('.'))
        return VersionInfo(major=major, minor=minor, patch=patch, build=build)
