from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from valorant import Client


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('season_uuid'),
    [
        ('0df5adb9-4dcb-6899-1306-3e9860661dd3'),  # "Closed Beta" with parent uuid
        ('3f61c772-4560-cd3f-5d3f-a7ab5abda6b3'),  # "ACT I" without parent uuid (EPISODE 1)
    ],
)
async def test_fetch_parent_season(client: Client, season_uuid: str) -> None:
    season = await client.fetch_season(season_uuid)
    parent_season = await season.fetch_parent(client=client)

    if season.parent_uuid:
        assert parent_season is not None
        assert parent_season.uuid == season.parent_uuid


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('season_competitive_uuid'),
    [
        ('8d9e3688-470b-c0e0-5b20-ca964d907adb'),  # some competitive season
        ('6b0f1bc6-4555-2405-9034-c9af64cf1cb1'),  # some competitive season
    ],
)
async def test_fetch_season_competitive(client: Client, season_competitive_uuid: str) -> None:
    season_competitive = await client.fetch_competitive_season(season_competitive_uuid)

    season = await season_competitive.fetch_season(client=client)
    assert season_competitive.season_uuid == season.uuid
