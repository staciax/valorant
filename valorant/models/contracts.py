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

import logging
from typing import TYPE_CHECKING, Dict, List, Optional, Union

from ..asset import Asset
from ..enums import Locale, RelationType, RewardType, try_enum
from ..localization import Localization
from .abc import BaseModel

if TYPE_CHECKING:
    from uuid import UUID

    from ..cache import CacheState
    from ..types.contracts import (
        Chapter as ChapterPayload,
        Content as ContentPayload,
        Contract as ContractPayload,
        Level as LevelPayload,
        Reward as RewardPayload,
    )
    from .agents import Agent
    from .buddies import BuddyLevel
    from .currencies import Currency
    from .events import Event
    from .player_cards import PlayerCard
    from .player_titles import PlayerTitle
    from .seasons import Season
    from .sprays import Spray
    from .weapons import SkinLevel

# fmt: off
__all__ = (
    'Contract',
)
# fmt: on

_log = logging.getLogger(__name__)


class Reward(BaseModel):
    def __init__(self, state: CacheState, data: RewardPayload, chapter: Chapter, free_reward: bool = False) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self.type: RewardType = try_enum(RewardType, data['type'])
        self.amount: int = data['amount']
        self._is_highlighted: bool = data['isHighlighted']
        self._is_free: bool = free_reward
        self.chapter: Chapter = chapter

    def get_item(self) -> Optional[Union[Agent, SkinLevel, BuddyLevel, Currency, PlayerCard, PlayerTitle, Spray]]:
        if self.type is RewardType.skin_level:
            return self._state.get_skin_level(str(self.uuid))
        elif self.type is RewardType.buddy_level:
            return self._state.get_buddy_level(str(self.uuid))
        elif self.type is RewardType.player_card:
            return self._state.get_player_card(str(self.uuid))
        elif self.type is RewardType.player_title:
            return self._state.get_player_title(str(self.uuid))
        elif self.type is RewardType.spray:
            return self._state.get_spray(str(self.uuid))
        elif self.type is RewardType.agent:
            return self._state.get_agent(str(self.uuid))
        elif self.type is RewardType.currency:
            return self._state.get_currency(str(self.uuid))
        _log.warning(f'Unknown reward type: {self.type}')
        return None

    def is_highlighted(self) -> bool:
        return self._is_highlighted

    def is_free(self) -> bool:
        return self._is_free


class Level:
    def __init__(self, state: CacheState, data: LevelPayload, chapter: Chapter) -> None:
        self._state: CacheState = state
        self.reward: Reward = Reward(self._state, data['reward'], chapter)
        self.xp: int = data['xp']
        self.vp_cost: int = data['vpCost']
        self._is_purchasable_with_vp: bool = data['isPurchasableWithVP']
        self.dough_cost: int = data['doughCost']
        self._is_purchasable_with_dough: bool = data['isPurchasableWithDough']
        self.chapter: Chapter = chapter

    def is_purchasable_with_vp(self) -> bool:
        return self._is_purchasable_with_vp

    def is_purchasable_with_dough(self) -> bool:
        return self._is_purchasable_with_dough


class Chapter:
    def __init__(self, state: CacheState, data: ChapterPayload, index: int) -> None:
        self._state: CacheState = state
        self._is_epilogue: bool = data['isEpilogue']
        self.levels: List[Level] = [Level(self._state, level, self) for level in data['levels']]
        self.free_rewards: Optional[List[Reward]] = None
        if data['freeRewards'] is not None:
            self.free_rewards = [Reward(self._state, reward, self, free_reward=True) for reward in data['freeRewards']]
        self.index: int = index

    def is_epilogue(self) -> bool:
        return self._is_epilogue

    # helper methods

    def get_all_rewards(self) -> List[Reward]:
        """:class: `List[Reward]` Returns all rewards."""
        return [level.reward for level in self.levels]


class Content:
    def __init__(self, state: CacheState, data: ContentPayload) -> None:
        self._state: CacheState = state
        if data['relationType'] is None:
            self.relation_type: RelationType = RelationType.none
        else:
            self.relation_type = try_enum(RelationType, data['relationType'])
        self._relation_uuid: Optional[str] = data['relationUuid']
        self._chapters: List[Chapter] = [
            Chapter(self._state, chapter, index) for index, chapter in enumerate(data['chapters'])
        ]
        self.premium_reward_schedule_uuid: Optional[str] = data['premiumRewardScheduleUuid']
        self.premium_vp_cost: int = data['premiumVPCost']

    @property
    def chapters(self) -> List[Chapter]:
        return self._chapters

    @property
    def relationship(self) -> Optional[Union[Agent, Event, Season]]:
        if self.relation_type is RelationType.agent:
            return self._state.get_agent(self._relation_uuid)
        elif self.relation_type is RelationType.event:
            return self._state.get_event(self._relation_uuid)
        elif self.relation_type is RelationType.season:
            return self._state.get_season(self._relation_uuid)
        if self.relation_type and self._relation_uuid:
            _log.warning(f'Unknown relationship type={self.relation_type!r} uuid={self._relation_uuid!r}')
        return None

    # helper methods

    def get_all_rewards(self) -> List[Reward]:
        """:class: `List[Reward]` Returns all rewards."""
        return [level.reward for chapter in self.chapters for level in chapter.levels]


class Contract(BaseModel):
    def __init__(self, state: CacheState, data: ContractPayload) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._data: ContractPayload = data
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self._display_icon: Optional[str] = data['displayIcon']
        self.ship_it: bool = data['shipIt']
        self.free_reward_schedule_uuid: str = data['freeRewardScheduleUuid']
        self._content: Content = Content(self._state, data['content'])
        self.asset_path: str = data['assetPath']
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        return f'<Contract display_name={self.display_name!r}>'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Contract) and self.uuid == other.uuid

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    @property
    def id(self) -> UUID:
        """:class: `UUID` Returns the contract id."""
        return self.uuid

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the contract's name."""
        return self._display_name_localized

    @property
    def display_icon(self) -> Optional[Asset]:
        """:class: `Asset` Returns the contract's icon."""
        if self._display_icon is None:
            return None
        return Asset._from_url(self._state, self._display_icon)

    @property
    def content(self) -> Content:
        """:class: `Content` Returns the contract's content."""
        return self._content
