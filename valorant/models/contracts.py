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

import logging
from typing import TYPE_CHECKING, TypeAlias
from uuid import UUID

from pydantic import Field

from ..enums import RelationType, RewardType
from .base import BaseModel, BaseUUIDModel
from .localization import LocalizedField

__all__ = (
    'Chapter',
    'Content',
    'Contract',
    'Level',
    'Reward',
)

if TYPE_CHECKING:
    from ..client import Client
    from .agents import Agent
    from .buddies import Level as BuddyLevel
    from .currencies import Currency
    from .events import Event
    from .player_cards import PlayerCard
    from .player_titles import PlayerTitle
    from .seasons import Season
    from .sprays import Spray
    from .weapons import Level as SkinLevel

    RewardItemType: TypeAlias = SkinLevel | BuddyLevel | Currency | PlayerCard | PlayerTitle | Spray

log = logging.getLogger(__name__)


class Reward(BaseUUIDModel):
    # uuid: str
    type: RewardType
    amount: int
    is_highlighted: bool = Field(alias='isHighlighted')

    # useful methods

    async def fetch_item(self, *, client: Client) -> RewardItemType | None:  # noqa: PLR0911
        if self.type is RewardType.skin_level:
            return await client.fetch_skin_level(str(self.uuid))
        if self.type is RewardType.buddy_level:
            return await client.fetch_buddy_level(str(self.uuid))
        if self.type is RewardType.player_card:
            return await client.fetch_player_card(str(self.uuid))
        if self.type is RewardType.player_title:
            return await client.fetch_player_title(str(self.uuid))
        if self.type is RewardType.spray:
            return await client.fetch_spray(str(self.uuid))
        if self.type is RewardType.currency:
            return await client.fetch_currency(str(self.uuid))
        log.warning('Unknown reward type: %s', self.type)
        return None


class Level(BaseModel):
    reward: Reward
    xp: int
    vp_cost: int = Field(alias='vpCost')
    is_purchasable_with_vp: bool = Field(alias='isPurchasableWithVP')
    dough_cost: int = Field(alias='doughCost')
    is_purchasable_with_dough: bool = Field(alias='isPurchasableWithDough')


# TODO: add index chapter
class Chapter(BaseModel):
    is_epilogue: bool = Field(alias='isEpilogue')
    levels: list[Level]
    free_rewards: list[Reward] | None = Field(alias='freeRewards')


class Content(BaseModel):
    relation_type: RelationType | None = Field(alias='relationType')
    relation_uuid: UUID | None = Field(alias='relationUuid')
    chapters: list[Chapter]
    premium_reward_schedule_uuid: str | None = Field(alias='premiumRewardScheduleUuid')
    premium_vp_cost: int = Field(alias='premiumVPCost')

    # useful methods

    async def fetch_relationship(self, *, client: Client) -> Agent | Event | Season | None:
        if self.relation_type is None or self.relation_uuid is None:
            return None
        if self.relation_type is RelationType.agent:
            return await client.fetch_agent(str(self.relation_uuid))
        if self.relation_type is RelationType.event:
            return await client.fetch_event(str(self.relation_uuid))
        if self.relation_type is RelationType.season:
            return await client.fetch_season(str(self.relation_uuid))
        log.warning('Unknown relation type: %s, uuid: %s', self.relation_type, self.relation_uuid)
        return None


class Contract(BaseUUIDModel):
    # uuid: str
    display_name: str | LocalizedField = Field(alias='displayName')
    display_icon: str | None = Field(alias='displayIcon')
    ship_it: bool = Field(alias='shipIt')
    use_level_vp_cost_override: bool = Field(alias='useLevelVPCostOverride')
    level_vp_cost_override: int = Field(alias='levelVPCostOverride')
    free_reward_schedule_uuid: str = Field(alias='freeRewardScheduleUuid')
    content: Content
    asset_path: str = Field(alias='assetPath')
