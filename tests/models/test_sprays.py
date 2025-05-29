from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from valorant import Client


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('spray_uuid'),
    [
        ('8035dd5d-4ddd-5dbd-165c-9886574fdff5'),  # "RGX 11z Pro Spray" with theme uuid
        ('3d2bcfc5-442b-812e-3c08-9180d6b36077'),  # "Caught on Camera Spray" without theme uuid
    ],
)
async def test_fetch_theme(client: Client, spray_uuid: str) -> None:
    spray = await client.fetch_spray(spray_uuid)
    theme = await spray.fetch_theme(client=client)

    if spray.theme_uuid:
        assert theme is not None
        assert theme.uuid == spray.theme_uuid
