from __future__ import annotations

from datetime import datetime

import pytest

from valorant.models.version import Version, VersionInfo


@pytest.mark.parametrize(
    ('version_str', 'expected'),
    [
        ('1.0.0.1', VersionInfo(1, 0, 0, 1)),
        ('10.09.00.3470802', VersionInfo(10, 9, 0, 3470802)),
    ],
)
def test_different_versions(version_str: str, expected: VersionInfo) -> None:
    version = Version(
        manifestId='',
        branch='',
        version=version_str,
        buildVersion='',
        engineVersion='',
        riotClientVersion='',
        riotClientBuild='',
        buildDate=datetime(2025, 5, 1, 0, 0, 0),
    )

    assert version.version_info == expected
