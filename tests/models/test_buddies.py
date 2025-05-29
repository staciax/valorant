from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from valorant import Client


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('buddy_uuid'),
    [
        ('0eab96da-ed34-4bdb-978f-b02b2fb4ebcc'),  # "Reaver" Buddy" with theme uuid
        ('72a48d20-40b8-8a99-1c96-c7a549af4640'),  # "Sentinels of Light Buddy" without theme uuid
    ],
)
async def test_fetch_theme(client: Client, buddy_uuid: str) -> None:
    buddy = await client.fetch_buddy(buddy_uuid)
    theme = await buddy.fetch_theme(client=client)

    if buddy.theme_uuid:
        assert theme is not None
        assert theme.uuid == buddy.theme_uuid
