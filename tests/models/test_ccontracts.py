from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from valorant import Client


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('contract_uuid'),
    [
        ('bf278489-4e68-1daf-2461-e6b822d8ad22'),  # "Season 25 // Act III"
    ],
)
async def test_reward_fetch_item(client: Client, contract_uuid: str) -> None:
    contract = await client.fetch_contract(contract_uuid)
    content = contract.content

    reward_types = []

    for chapter in content.chapters:
        for level in chapter.levels:
            if level.reward.type in reward_types:
                continue

            item = await level.reward.fetch_item(client=client)
            assert item.uuid == level.reward.uuid

            reward_types.append(level.reward.type)

        if chapter.free_rewards:
            for free_reward in chapter.free_rewards:
                if free_reward.type in reward_types:
                    continue

                item = await free_reward.fetch_item(client=client)
                assert item.uuid == free_reward.uuid

                reward_types.append(free_reward.type)


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('contract_uuid'),
    [
        ('bf278489-4e68-1daf-2461-e6b822d8ad22'),  # "Season 25 // Act III" realtion type is "Season"
        ('cae6ab4a-4b4a-69a0-3c7a-48b17e313f52'),  # "Gekko Gear" realtion type is "Agent"
        ('7391acae-47d2-809c-0148-14a10c56df50'),  # "Champions Pass" realtion type is "Event"
        ('a3dd5293-4b3d-46de-a6d7-4493f0530d9b'),  # "PLAY TO UNLOCK AGENTS" realtion type is null
    ],
)
async def test_content_fetch_relationship(client: Client, contract_uuid: str) -> None:
    contract = await client.fetch_contract(contract_uuid)
    content = contract.content

    relationship = await content.fetch_relationship(client=client)

    if content.relation_type and content.relation_uuid:
        assert relationship is not None
        assert relationship.uuid == content.relation_uuid
