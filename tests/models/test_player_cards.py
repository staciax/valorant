from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from valorant import Client


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('player_card_uuid'),
    [
        ('cada2e3f-4b1d-8279-3e1a-49984a71d4d3'),  # "RGX 11z Pro Card" with theme uuid
        ('1711d20d-4b1c-c64a-14be-d4ae58a457c6'),  # "Dayglo Duo Card" without theme uuid
    ],
)
async def test_fetch_theme(client: Client, player_card_uuid: str) -> None:
    player_card = await client.fetch_player_card(player_card_uuid)
    theme = await player_card.fetch_theme(client=client)

    if player_card.theme_uuid:
        assert theme is not None
        assert theme.uuid == player_card.theme_uuid
