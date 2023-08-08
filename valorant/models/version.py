"""
The MIT License (MIT)

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

from typing import TYPE_CHECKING, Optional

from .. import utils

if TYPE_CHECKING:
    import datetime

    from ..cache import CacheState
    from ..types.version import Version_ as VersionPayload

# fmt: off
__all__ = (
    'Version',
)
# fmt: on


class Version:
    def __init__(self, state: Optional[CacheState], data: VersionPayload) -> None:
        self._state: Optional[CacheState] = state
        self.manifest_id: str = data['manifestId']
        self.branch: str = data['branch']
        self.version: str = data['version']
        self.build_version: str = data['buildVersion']
        self.engine_version: str = data['engineVersion']
        self.riot_client_version: str = data['riotClientVersion']
        self.riot_client_build: str = data['riotClientBuild']
        self._build_date_iso: str = data['buildDate']

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Version) and other.manifest_id == self.manifest_id

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.version)

    def __str__(self) -> str:
        return self.version

    def __repr__(self) -> str:
        attrs = [
            ('manifest_id', self.manifest_id),
            ('branch', self.branch),
            ('version', self.version),
            ('build_version', self.build_version),
            ('engine_version', self.engine_version),
            ('riot_client_version', self.riot_client_version),
            ('build_date_iso', self.build_date),
        ]
        joined = ' '.join('%s=%r' % t for t in attrs)
        return f'<{self.__class__.__name__} {joined}>'

    @property
    def build_date(self) -> datetime.datetime:
        """:class:`datetime.datetime`: The build date of the version."""
        return utils.parse_iso_datetime(self._build_date_iso)
