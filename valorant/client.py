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
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import TracebackType

    from aiohttp import ClientSession
    from typing_extensions import Self


from .http import HTTPClient
from .models.agents import Agent
from .models.base import Response
from .models.buddies import Buddy, Level as BuddyLevel
from .models.bundles import Bundle
from .models.ceremonies import Ceremony
from .models.competitive_tiers import CompetitiveTier
from .models.content_tiers import ContentTier
from .models.contracts import Contract
from .models.currencies import Currency
from .models.events import Event
from .models.gamemodes import Equippable as GameModeEquippable, GameMode
from .models.gear import Gear
from .models.level_borders import LevelBorder
from .models.maps import Map
from .models.missions import Mission
from .models.player_cards import PlayerCard
from .models.player_titles import PlayerTitle
from .models.seasons import Competitive as CompetitiveSeason, Season
from .models.sprays import Level as SprayLevel, Spray
from .models.themes import Theme
from .models.version import Version
from .models.weapons import Chroma as SkinChroma, Level as SkinLevel, Skin, Weapon

_log = logging.getLogger(__name__)

# fmt: off
__all__ = (
    'Client',
)
# fmt: on

# TODO: support default locale


class Client:
    def __init__(
        self,
        *,
        session: ClientSession | None = None,
    ) -> None:
        self.http: HTTPClient = HTTPClient(session)
        self._closed: bool = False

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if not self.is_closed():
            await self.close()

    async def start(self) -> None:
        await self.http.start()
        _log.info('client started')

    def is_closed(self) -> bool:
        return self._closed

    async def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        await self.http.close()
        _log.info('client closed')

    def clear(self) -> None:
        self._closed = False
        self.http.clear()

    # agents

    async def fetch_agent(self, uuid: str, /) -> Agent | None:
        data = await self.http.get_agent(uuid)
        agent = Response[Agent].model_validate(data)
        return agent.data

    async def fetch_agents(self) -> list[Agent]:
        data = await self.http.get_agents()
        agents = Response[list[Agent]].model_validate(data)
        return agents.data

    # buddies

    async def fetch_buddy(self, uuid: str, /) -> Buddy | None:
        data = await self.http.get_buddy(uuid)
        buddy = Response[Buddy].model_validate(data)
        return buddy.data

    async def fetch_buddies(self) -> list[Buddy]:
        data = await self.http.get_buddies()
        buddies = Response[list[Buddy]].model_validate(data)
        return buddies.data

    async def fetch_buddy_level(self, uuid: str, /) -> BuddyLevel | None:
        data = await self.http.get_buddy_level(uuid)
        buddy_level = Response[BuddyLevel].model_validate(data)
        return buddy_level.data

    async def fetch_buddy_levels(self) -> list[BuddyLevel]:
        data = await self.http.get_buddy_levels()
        buddy_levels = Response[list[BuddyLevel]].model_validate(data)
        return buddy_levels.data

    # bundles

    async def fetch_bundle(self, uuid: str, /) -> Bundle | None:
        data = await self.http.get_bundle(uuid)
        bundle = Response[Bundle].model_validate(data)
        return bundle.data

    async def fetch_bundles(self) -> list[Bundle]:
        data = await self.http.get_bundles()
        bundles = Response[list[Bundle]].model_validate(data)
        return bundles.data

    # ceremonies

    async def fetch_ceremony(self, uuid: str, /) -> Ceremony | None:
        data = await self.http.get_ceremony(uuid)
        ceremony = Response[Ceremony].model_validate(data)
        return ceremony.data

    async def fetch_ceremonies(self) -> list[Ceremony]:
        data = await self.http.get_ceremonies()
        ceremonies = Response[list[Ceremony]].model_validate(data)
        return ceremonies.data

    # competitive_tiers

    async def fetch_competitive_tier(self, uuid: str, /) -> CompetitiveTier | None:
        data = await self.http.get_competitive_tier(uuid)
        competitive_tier = Response[CompetitiveTier].model_validate(data)
        return competitive_tier.data

    async def fetch_competitive_tiers(self) -> list[CompetitiveTier]:
        data = await self.http.get_competitive_tiers()
        competitive_tiers = Response[list[CompetitiveTier]].model_validate(data)
        return competitive_tiers.data

    # content_tiers

    async def fetch_content_tier(self, uuid: str, /) -> ContentTier | None:
        data = await self.http.get_content_tier(uuid)
        content_tier = Response[ContentTier].model_validate(data)
        return content_tier.data

    async def fetch_content_tiers(self) -> list[ContentTier]:
        data = await self.http.get_content_tiers()
        content_tiers = Response[list[ContentTier]].model_validate(data)
        return content_tiers.data

    # contracts

    async def fetch_contract(self, uuid: str, /) -> Contract | None:
        data = await self.http.get_contract(uuid)
        contract = Response[Contract].model_validate(data)
        return contract.data

    async def fetch_contracts(self) -> list[Contract]:
        data = await self.http.get_contracts()
        contracts = Response[list[Contract]].model_validate(data)
        return contracts.data

    # currencies

    async def fetch_currency(self, uuid: str, /) -> Currency | None:
        data = await self.http.get_currency(uuid)
        currency = Response[Currency].model_validate(data)
        return currency.data

    async def fetch_currencies(self) -> list[Currency]:
        data = await self.http.get_currencies()
        currencies = Response[list[Currency]].model_validate(data)
        return currencies.data

    # events

    async def fetch_event(self, uuid: str, /) -> Event | None:
        data = await self.http.get_event(uuid)
        event = Response[Event].model_validate(data)
        return event.data

    async def fetch_events(self) -> list[Event]:
        data = await self.http.get_events()
        events = Response[list[Event]].model_validate(data)
        return events.data

    # game_modes

    async def fetch_game_mode(self, uuid: str, /) -> GameMode | None:
        data = await self.http.get_game_mode(uuid)
        game_mode = Response[GameMode].model_validate(data)
        return game_mode.data

    async def fetch_game_modes(self) -> list[GameMode]:
        data = await self.http.get_game_modes()
        game_modes = Response[list[GameMode]].model_validate(data)
        return game_modes.data

    async def fetch_game_mode_equippable(self, uuid: str, /) -> GameModeEquippable | None:
        data = await self.http.get_game_mode_equippable(uuid)
        game_mode_equippable = Response[GameModeEquippable].model_validate(data)
        return game_mode_equippable.data

    async def fetch_game_mode_equippables(self) -> list[GameModeEquippable]:
        data = await self.http.get_game_mode_equippables()
        game_mode_equippables = Response[list[GameModeEquippable]].model_validate(data)
        return game_mode_equippables.data

    # gear

    async def fetch_gear(self, uuid: str, /) -> Gear | None:
        data = await self.http.get_gear(uuid)
        gear = Response[Gear].model_validate(data)
        return gear.data

    async def fetch_gears(self) -> list[Gear]:
        data = await self.http.get_all_gear()
        gears = Response[list[Gear]].model_validate(data)
        return gears.data

    # level_borders

    async def fetch_level_border(self, uuid: str, /) -> LevelBorder | None:
        data = await self.http.get_level_border(uuid)
        level_border = Response[LevelBorder].model_validate(data)
        return level_border.data

    async def fetch_level_borders(self) -> list[LevelBorder]:
        data = await self.http.get_level_borders()
        level_borders = Response[list[LevelBorder]].model_validate(data)
        return level_borders.data

    # maps

    async def fetch_map(self, uuid: str, /) -> Map | None:
        data = await self.http.get_map(uuid)
        map_ = Response[Map].model_validate(data)
        return map_.data

    async def fetch_maps(self) -> list[Map]:
        data = await self.http.get_maps()
        maps = Response[list[Map]].model_validate(data)
        return maps.data

    # missions

    async def fetch_mission(self, uuid: str, /) -> Mission | None:
        data = await self.http.get_mission(uuid)
        mission = Response[Mission].model_validate(data)
        return mission.data

    async def fetch_missions(self) -> list[Mission]:
        data = await self.http.get_missions()
        missions = Response[list[Mission]].model_validate(data)
        return missions.data

    # player cards

    async def fetch_player_card(self, uuid: str, /) -> PlayerCard | None:
        data = await self.http.get_player_card(uuid)
        player_card = Response[PlayerCard].model_validate(data)
        return player_card.data

    async def fetch_player_cards(self) -> list[PlayerCard]:
        data = await self.http.get_player_cards()
        player_cards = Response[list[PlayerCard]].model_validate(data)
        return player_cards.data

    # player titles

    async def fetch_player_title(self, uuid: str, /) -> PlayerTitle | None:
        data = await self.http.get_player_title(uuid)
        player_title = Response[PlayerTitle].model_validate(data)
        return player_title.data

    async def fetch_player_titles(self) -> list[PlayerTitle]:
        data = await self.http.get_player_titles()
        player_titles = Response[list[PlayerTitle]].model_validate(data)
        return player_titles.data

    # seasons

    async def fetch_season(self, uuid: str, /) -> Season | None:
        data = await self.http.get_season(uuid)
        season = Response[Season].model_validate(data)
        return season.data

    async def fetch_seasons(self) -> list[Season]:
        data = await self.http.get_seasons()
        seasons = Response[list[Season]].model_validate(data)
        return seasons.data

    async def competitive_season(self, uuid: str, /) -> CompetitiveSeason | None:
        data = await self.http.get_competitive_season(uuid)
        competitive_season = Response[CompetitiveSeason].model_validate(data)
        return competitive_season.data

    async def competitive_seasons(self) -> list[CompetitiveSeason]:
        data = await self.http.get_competitive_seasons()
        competitive_seasons = Response[list[CompetitiveSeason]].model_validate(data)
        return competitive_seasons.data

    # sprays

    async def fetch_spray(self, uuid: str, /) -> Spray | None:
        data = await self.http.get_spray(uuid)
        spray = Response[Spray].model_validate(data)
        return spray.data

    async def fetch_sprays(self) -> list[Spray]:
        data = await self.http.get_sprays()
        sprays = Response[list[Spray]].model_validate(data)
        return sprays.data

    async def fetch_spray_level(self, uuid: str, /) -> SprayLevel | None:
        data = await self.http.get_spray_level(uuid)
        spray_level = Response[SprayLevel].model_validate(data)
        return spray_level.data

    async def fetch_spray_levels(self) -> list[SprayLevel]:
        data = await self.http.get_spray_levels()
        spray_levels = Response[list[SprayLevel]].model_validate(data)
        return spray_levels.data

    # themes

    async def fetch_theme(self, uuid: str, /) -> Theme | None:
        data = await self.http.get_theme(uuid)
        theme = Response[Theme].model_validate(data)
        return theme.data

    async def fetch_themes(self) -> list[Theme]:
        data = await self.http.get_themes()
        themes = Response[list[Theme]].model_validate(data)
        return themes.data

    # weapons

    async def fetch_weapon(self, uuid: str, /) -> Weapon | None:
        data = await self.http.get_weapon(uuid)
        weapon = Response[Weapon].model_validate(data)
        return weapon.data

    async def fetch_weapons(self) -> list[Weapon]:
        data = await self.http.get_weapons()
        weapons = Response[list[Weapon]].model_validate(data)
        return weapons.data

    async def fetch_weapon_skin(self, uuid: str, /) -> Skin | None:
        data = await self.http.get_weapon_skin(uuid)
        skin = Response[Skin].model_validate(data)
        return skin.data

    async def fetch_weapon_skins(self) -> list[Skin]:
        data = await self.http.get_weapon_skins()
        skins = Response[list[Skin]].model_validate(data)
        return skins.data

    async def fetch_weapon_skin_chroma(self, uuid: str, /) -> SkinChroma | None:
        data = await self.http.get_weapon_skin_chroma(uuid)
        skin_chroma = Response[SkinChroma].model_validate(data)
        return skin_chroma.data

    async def fetch_weapon_skin_chromas(self) -> list[SkinChroma]:
        data = await self.http.get_weapon_skin_chromas()
        skin_chromas = Response[list[SkinChroma]].model_validate(data)
        return skin_chromas.data

    async def fetch_weapon_skin_level(self, uuid: str, /) -> SkinLevel | None:
        data = await self.http.get_weapon_skin_level(uuid)
        skin_level = Response[SkinLevel].model_validate(data)
        return skin_level.data

    async def fetch_weapon_skin_levels(self) -> list[SkinLevel]:
        data = await self.http.get_weapon_skin_levels()
        skin_levels = Response[list[SkinLevel]].model_validate(data)
        return skin_levels.data

    # version

    async def fetch_version(self) -> Version:
        data = await self.http.get_version()
        version = Response[Version].model_validate(data)
        return version.data
