from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from valorant import Client


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('skin_uuid'),
    [
        ('89be9866-4807-6235-2a95-499cd23828df'),  # "Altitude Odin" with theme uuid
    ],
)
async def test_skin_fetch_theme(client: Client, skin_uuid: str) -> None:
    skin = await client.fetch_skin(skin_uuid)
    theme = await skin.fetch_theme(client=client)

    assert theme.uuid == skin.theme_uuid


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('skin_uuid'),
    [
        ('89be9866-4807-6235-2a95-499cd23828df'),  # "Altitude Odin" with content tier uuid
        ('f454efd1-49cb-372f-7096-d394df615308'),  # "Standard Odin" without content tier uuid
    ],
)
async def test_skin_fetch_content_tier(client: Client, skin_uuid: str) -> None:
    skin = await client.fetch_skin(skin_uuid)
    content_tier = await skin.fetch_content_tier(client=client)

    if skin.content_tier_uuid:
        assert content_tier is not None
        assert content_tier.uuid == skin.content_tier_uuid
