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

import asyncio
import logging
from typing import TYPE_CHECKING, List, Optional, Type

from .cache import CacheState
from .enums import Locale
from .http import HTTPClient
from .models.agents import Agent
from .models.buddies import Buddy, BuddyLevel
from .models.bundles import Bundle
from .models.ceremonies import Ceremony
from .models.competitive_tiers import CompetitiveTier
from .models.content_tiers import ContentTier
from .models.contracts import Contract
from .models.currencies import Currency
from .models.events import Event
from .models.gamemodes import GameMode, GameModeEquippable
from .models.gear import Gear
from .models.level_borders import LevelBorder
from .models.maps import Map
from .models.missions import Mission
from .models.player_cards import PlayerCard
from .models.player_titles import PlayerTitle
from .models.seasons import CompetitiveSeason, Season
from .models.sprays import Spray, SprayLevel
from .models.themes import Theme
from .models.version import Version
from .models.weapons import Skin, SkinChroma, SkinLevel, Weapon
from .utils import MISSING

if TYPE_CHECKING:
    from types import TracebackType

    from typing_extensions import Self

_log = logging.getLogger(__name__)

# fmt: off
__all__ = (
    'Client',
)
# fmt: on


class Client:
    def __init__(self, locale: Locale = Locale.american_english) -> None:
        self.http: HTTPClient = HTTPClient()
        self.cache: CacheState = CacheState(locale=locale, http=self.http)
        self._ready: asyncio.Event = MISSING
        self._closed: bool = False

    async def __aenter__(self) -> Self:
        await self.init()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if not self.is_closed():
            await self.close()

    async def init(self) -> None:
        self._ready = asyncio.Event()
        await self.http.init()
        await self.cache.init()
        self._ready.set()
        _log.info('client initialized')

    async def reload(self) -> None:
        self.cache.clear()
        await self.cache.init()
        _log.info('client reloaded')

    def is_closed(self) -> bool:
        return self._closed

    def is_ready(self) -> bool:
        return self._ready is not MISSING and self._ready.is_set()

    async def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        if self._ready is not MISSING:
            self._ready.clear()

        self.cache.clear()
        await self.http.close()
        _log.info('client closed')

    def clear(self) -> None:
        self._closed = False
        self._ready.clear()
        self._ready = MISSING
        self.cache.clear()
        self.http.clear()

    async def wait_until_ready(self) -> None:
        if self._ready is not MISSING:
            await self._ready.wait()
        else:
            raise RuntimeError('Client not initialized yet.')

    # agents

    @property
    def agents(self) -> List[Agent]:
        return self.cache.agents

    def get_agent(self, uuid: str, /) -> Optional[Agent]:
        return self.cache.get_agent(uuid)

    async def fetch_agent(self, uuid: str, /) -> Optional[Agent]:
        await self.cache.fetch_agents()
        return self.get_agent(uuid)

    # buddies

    @property
    def buddies(self) -> List[Buddy]:
        return self.cache.buddies

    @property
    def buddy_levels(self) -> List[BuddyLevel]:
        return self.cache.buddy_levels

    def get_buddy(self, uuid: str, /) -> Optional[Buddy]:
        return self.cache.get_buddy(uuid)

    def get_buddy_level(self, uuid: str, /) -> Optional[BuddyLevel]:
        return self.cache.get_buddy_level(uuid)

    async def fetch_buddy(self, uuid: str, /) -> Optional[Buddy]:
        await self.cache.fetch_buddies()
        return self.get_buddy(uuid)

    async def fetch_buddy_level(self, uuid: str, /) -> Optional[BuddyLevel]:
        await self.cache.fetch_buddies()
        return self.get_buddy_level(uuid)

    # bundles

    @property
    def bundles(self) -> List[Bundle]:
        return self.cache.bundles

    def get_bundle(self, uuid: str, /) -> Optional[Bundle]:
        return self.cache.get_bundle(uuid)

    async def fetch_bundle(self, uuid: str, /) -> Optional[Bundle]:
        await self.cache.fetch_bundles()
        return self.get_bundle(uuid)

    # ceremonies

    @property
    def ceremonies(self) -> List[Ceremony]:
        return self.cache.ceremonies

    def get_ceremony(self, uuid: str, /) -> Optional[Ceremony]:
        return self.cache.get_ceremony(uuid)

    async def fetch_ceremony(self, uuid: str, /) -> Optional[Ceremony]:
        await self.cache.fetch_ceremonies()
        return self.get_ceremony(uuid)

    # competitive_tiers

    @property
    def competitive_tiers(self) -> List[CompetitiveTier]:
        return self.cache.competitive_tiers

    def get_competitive_tier(self, uuid: str, /) -> Optional[CompetitiveTier]:
        return self.cache.get_competitive_tier(uuid)

    async def fetch_competitive_tier(self, uuid: str, /) -> Optional[CompetitiveTier]:
        await self.cache.fetch_competitive_tiers()
        return self.get_competitive_tier(uuid)

    # content_tiers

    @property
    def content_tiers(self) -> List[ContentTier]:
        return self.cache.content_tiers

    def get_content_tier(self, uuid: str, /) -> Optional[ContentTier]:
        return self.cache.get_content_tier(uuid)

    async def fetch_content_tier(self, uuid: str, /) -> Optional[ContentTier]:
        await self.cache.fetch_content_tiers()
        return self.get_content_tier(uuid)

    # contracts

    @property
    def contracts(self) -> List[Contract]:
        return self.cache.contracts

    def get_contract(self, uuid: str, /) -> Optional[Contract]:
        return self.cache.get_contract(uuid)

    async def fetch_contract(self, uuid: str, /) -> Optional[Contract]:
        await self.cache.fetch_contracts()
        return self.get_contract(uuid)

    # currencies

    @property
    def currencies(self) -> List[Currency]:
        return self.cache.currencies

    def get_currency(self, uuid: str, /) -> Optional[Currency]:
        return self.cache.get_currency(uuid)

    async def fetch_currency(self, uuid: str, /) -> Optional[Currency]:
        await self.cache.fetch_currencies()
        return self.get_currency(uuid)

    # events

    @property
    def events(self) -> List[Event]:
        return self.cache.events

    def get_event(self, uuid: str, /) -> Optional[Event]:
        return self.cache.get_event(uuid)

    async def fetch_event(self, uuid: str, /) -> Optional[Event]:
        await self.cache.fetch_events()
        return self.get_event(uuid)

    # game_modes

    @property
    def game_modes(self) -> List[GameMode]:
        return self.cache.game_modes

    @property
    def game_mode_equippables(self) -> List[GameModeEquippable]:
        return self.cache.game_mode_equippables

    def get_game_mode(self, uuid: str, /) -> Optional[GameMode]:
        return self.cache.get_game_mode(uuid)

    def get_game_mode_equippable(self, uuid: str, /) -> Optional[GameModeEquippable]:
        return self.cache.get_game_mode_equippable(uuid)

    async def fetch_game_mode(self, uuid: str, /) -> Optional[GameMode]:
        await self.cache.fetch_game_modes()
        return self.get_game_mode(uuid)

    async def fetch_game_mode_equippable(self, uuid: str, /) -> Optional[GameModeEquippable]:
        await self.cache.fetch_game_modes()
        return self.get_game_mode_equippable(uuid)

    # gear

    @property
    def gear(self) -> List[Gear]:
        return self.cache.gear

    def get_gear(self, uuid: str, /) -> Optional[Gear]:
        return self.cache.get_gear(uuid)

    async def fetch_gear(self, uuid: str, /) -> Optional[Gear]:
        await self.cache.fetch_gear()
        return self.get_gear(uuid)

    # level_borders

    @property
    def level_borders(self) -> List[LevelBorder]:
        return self.cache.level_borders

    def get_level_border(self, uuid: str, /) -> Optional[LevelBorder]:
        return self.cache.get_level_border(uuid)

    async def fetch_level_border(self, uuid: str, /) -> Optional[LevelBorder]:
        await self.cache.fetch_level_borders()
        return self.get_level_border(uuid)

    # maps

    @property
    def maps(self) -> List[Map]:
        return self.cache.maps

    def get_map(self, uuid: str, /) -> Optional[Map]:
        return self.cache.get_map(uuid)

    async def fetch_map(self, uuid: str, /) -> Optional[Map]:
        await self.cache.fetch_maps()
        return self.get_map(uuid)

    # missions

    @property
    def missions(self) -> List[Mission]:
        return self.cache.missions

    def get_mission(self, uuid: str, /) -> Optional[Mission]:
        return self.cache.get_mission(uuid)

    async def fetch_mission(self, uuid: str, /) -> Optional[Mission]:
        await self.cache.fetch_missions()
        return self.get_mission(uuid)

    # player_cards

    @property
    def player_cards(self) -> List[PlayerCard]:
        return self.cache.player_cards

    def get_player_card(self, uuid: str) -> Optional[PlayerCard]:
        return self.cache.get_player_card(uuid)

    async def fetch_player_card(self, uuid: str) -> Optional[PlayerCard]:
        await self.cache.fetch_player_cards()
        return self.get_player_card(uuid)

    # player_titles

    @property
    def player_titles(self) -> List[PlayerTitle]:
        return self.cache.player_titles

    def get_player_title(self, uuid: str, /) -> Optional[PlayerTitle]:
        return self.cache.get_player_title(uuid)

    async def fetch_player_title(self, uuid: str, /) -> Optional[PlayerTitle]:
        await self.cache.fetch_player_titles()
        return self.get_player_title(uuid)

    # seasons

    @property
    def seasons(self) -> List[Season]:
        return self.cache.seasons

    def get_season(self, uuid: str, /) -> Optional[Season]:
        return self.cache.get_season(uuid)

    async def fetch_season(self, uuid: str, /) -> Optional[Season]:
        await self.cache.fetch_seasons()
        return self.get_season(uuid)

    @property
    def competitive_seasons(self) -> List[CompetitiveSeason]:
        return list(self.cache.competitive_seasons)

    def get_competitive_season(self, uuid: str, /) -> Optional[CompetitiveSeason]:
        return self.cache.get_competitive_season(uuid)

    def get_competitive_season_season_id(self, season_id: str, /) -> Optional[CompetitiveSeason]:
        for season in self.competitive_seasons:
            if season.season_uuid == season_id:
                return season
        return None

    async def fetch_competitive_season(self, uuid: str, /) -> Optional[CompetitiveSeason]:
        await self.cache.fetch_competitive_seasons()
        return self.get_competitive_season(uuid)

    # sprays

    @property
    def sprays(self) -> List[Spray]:
        return self.cache.sprays

    def get_spray(self, uuid: str, /) -> Optional[Spray]:
        return self.cache.get_spray(uuid)

    async def fetch_spray(self, uuid: str, /) -> Optional[Spray]:
        await self.cache.fetch_sprays()
        return self.get_spray(uuid)

    @property
    def spray_levels(self) -> List[SprayLevel]:
        return self.cache.spray_levels

    def get_spray_level(self, uuid: str, /) -> Optional[SprayLevel]:
        return self.cache.get_spray_level(uuid)

    async def fetch_spray_level(self, uuid: str, /) -> Optional[SprayLevel]:
        await self.cache.fetch_sprays()
        return self.get_spray_level(uuid)

    # themes

    @property
    def themes(self) -> List[Theme]:
        return self.cache.themes

    def get_theme(self, uuid: str) -> Optional[Theme]:
        return self.cache.get_theme(uuid)

    async def fetch_theme(self, uuid: str) -> Optional[Theme]:
        await self.cache.fetch_themes()
        return self.get_theme(uuid)

    # version

    @property
    def version(self) -> Version:
        return self.cache.version

    async def fetch_version(self) -> Version:
        await self.cache.fetch_version()
        return self.version

    # weapons

    @property
    def weapons(self) -> List[Weapon]:
        return self.cache.weapons

    def get_weapon(self, uuid: str, /) -> Optional[Weapon]:
        return self.cache.get_weapon(uuid)

    async def fetch_weapon(self, uuid: str, /) -> Optional[Weapon]:
        await self.cache.fetch_weapons()
        return self.get_weapon(uuid)

    async def _fetch_weapon(self) -> None:
        data = await self.http.get_weapons()
        self.cache._add_weapons(data)

    @property
    def skins(self) -> List[Skin]:
        return self.cache.skins

    def get_skin(self, uuid: str, /) -> Optional[Skin]:
        return self.cache.get_skin(uuid)

    async def fetch_skin(self, uuid: str, /) -> Optional[Skin[Weapon]]:
        await self.cache.fetch_weapons()
        a = await self.fetch_skin(uuid)
        return self.get_skin(uuid)

    @property
    def skin_chromas(self) -> List[SkinChroma]:
        return self.cache.skin_chromas

    def get_skin_chroma(self, uuid: str, /) -> Optional[SkinChroma[Skin]]:
        return self.cache.get_skin_chroma(uuid)

    async def fetch_skin_chroma(self, uuid: str, /) -> Optional[SkinChroma[Skin]]:
        await self.cache.fetch_weapons()
        return self.get_skin_chroma(uuid)

    @property
    def skin_levels(self) -> List[SkinLevel[Skin]]:
        return self.cache.skin_levels

    def get_skin_level(self, uuid: str, /) -> Optional[SkinLevel[Skin]]:
        return self.cache.get_skin_level(uuid)

    async def fetch_skin_level(self, uuid: str, /) -> Optional[SkinLevel[Skin]]:
        await self.cache.fetch_weapons()
        return self.get_skin_level(uuid)
