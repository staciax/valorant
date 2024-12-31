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
from typing import TYPE_CHECKING, Literal

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

if TYPE_CHECKING:
    from types import TracebackType
    from typing import TypeAlias

    from aiohttp import ClientSession
    from typing_extensions import Self

    from .enums import Language

    LanguageOption: TypeAlias = Language | Literal['all']


class Client:
    def __init__(
        self,
        language: LanguageOption | None = None,
        *,
        session: ClientSession | None = None,
    ) -> None:
        self.language = language
        self.http = HTTPClient(session)
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

    async def fetch_agent(self, uuid: str, /, *, language: LanguageOption | None = None) -> Agent | None:
        data = await self.http.get_agent(uuid, language=language or self.language)
        agent = Response[Agent].model_validate(data)
        return agent.data

    async def fetch_agents(self, *, language: LanguageOption | None = None) -> list[Agent]:
        data = await self.http.get_agents(language=language or self.language)
        agents = Response[list[Agent]].model_validate(data)
        return agents.data

    # buddies

    async def fetch_buddy(self, uuid: str, /, *, language: LanguageOption | None = None) -> Buddy | None:
        data = await self.http.get_buddy(uuid, language=language or self.language)
        buddy = Response[Buddy].model_validate(data)
        return buddy.data

    async def fetch_buddies(self, *, language: LanguageOption | None = None) -> list[Buddy]:
        data = await self.http.get_buddies(language=language or self.language)
        buddies = Response[list[Buddy]].model_validate(data)
        return buddies.data

    async def fetch_buddy_level(self, uuid: str, /, *, language: LanguageOption | None = None) -> BuddyLevel | None:
        data = await self.http.get_buddy_level(uuid, language=language or self.language)
        buddy_level = Response[BuddyLevel].model_validate(data)
        return buddy_level.data

    async def fetch_buddy_levels(self, *, language: LanguageOption | None = None) -> list[BuddyLevel]:
        data = await self.http.get_buddy_levels(language=language or self.language)
        buddy_levels = Response[list[BuddyLevel]].model_validate(data)
        return buddy_levels.data

    # bundles

    async def fetch_bundle(self, uuid: str, /, *, language: LanguageOption | None = None) -> Bundle | None:
        data = await self.http.get_bundle(uuid, language=language or self.language)
        bundle = Response[Bundle].model_validate(data)
        return bundle.data

    async def fetch_bundles(self, *, language: LanguageOption | None = None) -> list[Bundle]:
        data = await self.http.get_bundles(language=language or self.language)
        bundles = Response[list[Bundle]].model_validate(data)
        return bundles.data

    # ceremonies

    async def fetch_ceremony(self, uuid: str, /, *, language: LanguageOption | None = None) -> Ceremony | None:
        data = await self.http.get_ceremony(uuid, language=language or self.language)
        ceremony = Response[Ceremony].model_validate(data)
        return ceremony.data

    async def fetch_ceremonies(self, *, language: LanguageOption | None = None) -> list[Ceremony]:
        data = await self.http.get_ceremonies(language=language or self.language)
        ceremonies = Response[list[Ceremony]].model_validate(data)
        return ceremonies.data

    # competitive_tiers

    async def fetch_competitive_tier(
        self, uuid: str, /, *, language: LanguageOption | None = None
    ) -> CompetitiveTier | None:
        data = await self.http.get_competitive_tier(uuid, language=language or self.language)
        competitive_tier = Response[CompetitiveTier].model_validate(data)
        return competitive_tier.data

    async def fetch_competitive_tiers(self, *, language: LanguageOption | None = None) -> list[CompetitiveTier]:
        data = await self.http.get_competitive_tiers(language=language or self.language)
        competitive_tiers = Response[list[CompetitiveTier]].model_validate(data)
        return competitive_tiers.data

    # content_tiers

    async def fetch_content_tier(self, uuid: str, /, *, language: LanguageOption | None = None) -> ContentTier | None:
        data = await self.http.get_content_tier(uuid, language=language or self.language)
        content_tier = Response[ContentTier].model_validate(data)
        return content_tier.data

    async def fetch_content_tiers(self, *, language: LanguageOption | None = None) -> list[ContentTier]:
        data = await self.http.get_content_tiers(language=language or self.language)
        content_tiers = Response[list[ContentTier]].model_validate(data)
        return content_tiers.data

    # contracts

    async def fetch_contract(self, uuid: str, /, *, language: LanguageOption | None = None) -> Contract | None:
        data = await self.http.get_contract(uuid, language=language or self.language)
        contract = Response[Contract].model_validate(data)
        return contract.data

    async def fetch_contracts(self, *, language: LanguageOption | None = None) -> list[Contract]:
        data = await self.http.get_contracts(language=language or self.language)
        contracts = Response[list[Contract]].model_validate(data)
        return contracts.data

    # currencies

    async def fetch_currency(self, uuid: str, /, *, language: LanguageOption | None = None) -> Currency | None:
        data = await self.http.get_currency(uuid, language=language or self.language)
        currency = Response[Currency].model_validate(data)
        return currency.data

    async def fetch_currencies(self, *, language: LanguageOption | None = None) -> list[Currency]:
        data = await self.http.get_currencies(language=language or self.language)
        currencies = Response[list[Currency]].model_validate(data)
        return currencies.data

    # events

    async def fetch_event(self, uuid: str, /, *, language: LanguageOption | None = None) -> Event | None:
        data = await self.http.get_event(uuid, language=language or self.language)
        event = Response[Event].model_validate(data)
        return event.data

    async def fetch_events(self, *, language: LanguageOption | None = None) -> list[Event]:
        data = await self.http.get_events(language=language or self.language)
        events = Response[list[Event]].model_validate(data)
        return events.data

    # game_modes

    async def fetch_game_mode(self, uuid: str, /, *, language: LanguageOption | None = None) -> GameMode | None:
        data = await self.http.get_game_mode(uuid, language=language or self.language)
        game_mode = Response[GameMode].model_validate(data)
        return game_mode.data

    async def fetch_game_modes(self, *, language: LanguageOption | None = None) -> list[GameMode]:
        data = await self.http.get_game_modes(language=language or self.language)
        game_modes = Response[list[GameMode]].model_validate(data)
        return game_modes.data

    async def fetch_game_mode_equippable(
        self, uuid: str, /, *, language: LanguageOption | None = None
    ) -> GameModeEquippable | None:
        data = await self.http.get_game_mode_equippable(uuid, language=language or self.language)
        game_mode_equippable = Response[GameModeEquippable].model_validate(data)
        return game_mode_equippable.data

    async def fetch_game_mode_equippables(self, *, language: LanguageOption | None = None) -> list[GameModeEquippable]:
        data = await self.http.get_game_mode_equippables(language=language or self.language)
        game_mode_equippables = Response[list[GameModeEquippable]].model_validate(data)
        return game_mode_equippables.data

    # gear

    async def fetch_gear(self, uuid: str, /, *, language: LanguageOption | None = None) -> Gear | None:
        data = await self.http.get_gear(uuid, language=language or self.language)
        gear = Response[Gear].model_validate(data)
        return gear.data

    async def fetch_gears(self, *, language: LanguageOption | None = None) -> list[Gear]:
        data = await self.http.get_all_gear(language=language or self.language)
        gears = Response[list[Gear]].model_validate(data)
        return gears.data

    # level_borders

    async def fetch_level_border(self, uuid: str, /, *, language: LanguageOption | None = None) -> LevelBorder | None:
        data = await self.http.get_level_border(uuid, language=language or self.language)
        level_border = Response[LevelBorder].model_validate(data)
        return level_border.data

    async def fetch_level_borders(self, *, language: LanguageOption | None = None) -> list[LevelBorder]:
        data = await self.http.get_level_borders(language=language or self.language)
        level_borders = Response[list[LevelBorder]].model_validate(data)
        return level_borders.data

    # maps

    async def fetch_map(self, uuid: str, /, *, language: LanguageOption | None = None) -> Map | None:
        data = await self.http.get_map(uuid, language=language or self.language)
        map_ = Response[Map].model_validate(data)
        return map_.data

    async def fetch_maps(self, *, language: LanguageOption | None = None) -> list[Map]:
        data = await self.http.get_maps(language=language or self.language)
        maps = Response[list[Map]].model_validate(data)
        return maps.data

    # missions

    async def fetch_mission(self, uuid: str, /, *, language: LanguageOption | None = None) -> Mission | None:
        data = await self.http.get_mission(uuid, language=language or self.language)
        mission = Response[Mission].model_validate(data)
        return mission.data

    async def fetch_missions(self, *, language: LanguageOption | None = None) -> list[Mission]:
        data = await self.http.get_missions(language=language or self.language)
        missions = Response[list[Mission]].model_validate(data)
        return missions.data

    # player cards

    async def fetch_player_card(self, uuid: str, /, *, language: LanguageOption | None = None) -> PlayerCard | None:
        data = await self.http.get_player_card(uuid, language=language or self.language)
        player_card = Response[PlayerCard].model_validate(data)
        return player_card.data

    async def fetch_player_cards(self, *, language: LanguageOption | None = None) -> list[PlayerCard]:
        data = await self.http.get_player_cards(language=language or self.language)
        player_cards = Response[list[PlayerCard]].model_validate(data)
        return player_cards.data

    # player titles

    async def fetch_player_title(self, uuid: str, /, *, language: LanguageOption | None = None) -> PlayerTitle | None:
        data = await self.http.get_player_title(uuid, language=language or self.language)
        player_title = Response[PlayerTitle].model_validate(data)
        return player_title.data

    async def fetch_player_titles(self, *, language: LanguageOption | None = None) -> list[PlayerTitle]:
        data = await self.http.get_player_titles(language=language or self.language)
        player_titles = Response[list[PlayerTitle]].model_validate(data)
        return player_titles.data

    # seasons

    async def fetch_season(self, uuid: str, /, *, language: LanguageOption | None = None) -> Season | None:
        data = await self.http.get_season(uuid, language=language or self.language)
        season = Response[Season].model_validate(data)
        return season.data

    async def fetch_seasons(self, *, language: LanguageOption | None = None) -> list[Season]:
        data = await self.http.get_seasons(language=language or self.language)
        seasons = Response[list[Season]].model_validate(data)
        return seasons.data

    async def fetch_competitive_season(self, uuid: str, /) -> CompetitiveSeason | None:
        data = await self.http.get_competitive_season(uuid)
        competitive_season = Response[CompetitiveSeason].model_validate(data)
        return competitive_season.data

    async def fetch_competitive_seasons(self) -> list[CompetitiveSeason]:
        data = await self.http.get_competitive_seasons()
        competitive_seasons = Response[list[CompetitiveSeason]].model_validate(data)
        return competitive_seasons.data

    # sprays

    async def fetch_spray(self, uuid: str, /, *, language: LanguageOption | None = None) -> Spray | None:
        data = await self.http.get_spray(uuid, language=language or self.language)
        spray = Response[Spray].model_validate(data)
        return spray.data

    async def fetch_sprays(self, *, language: LanguageOption | None = None) -> list[Spray]:
        data = await self.http.get_sprays(language=language or self.language)
        sprays = Response[list[Spray]].model_validate(data)
        return sprays.data

    async def fetch_spray_level(self, uuid: str, /, *, language: LanguageOption | None = None) -> SprayLevel | None:
        data = await self.http.get_spray_level(uuid, language=language or self.language)
        spray_level = Response[SprayLevel].model_validate(data)
        return spray_level.data

    async def fetch_spray_levels(self, *, language: LanguageOption | None = None) -> list[SprayLevel]:
        data = await self.http.get_spray_levels(language=language or self.language)
        spray_levels = Response[list[SprayLevel]].model_validate(data)
        return spray_levels.data

    # themes

    async def fetch_theme(self, uuid: str, /, *, language: LanguageOption | None = None) -> Theme | None:
        data = await self.http.get_theme(uuid, language=language or self.language)
        theme = Response[Theme].model_validate(data)
        return theme.data

    async def fetch_themes(self, *, language: LanguageOption | None = None) -> list[Theme]:
        data = await self.http.get_themes(language=language or self.language)
        themes = Response[list[Theme]].model_validate(data)
        return themes.data

    # weapons

    async def fetch_weapon(self, uuid: str, /, *, language: LanguageOption | None = None) -> Weapon | None:
        data = await self.http.get_weapon(uuid, language=language or self.language)
        weapon = Response[Weapon].model_validate(data)
        return weapon.data

    async def fetch_weapons(self, *, language: LanguageOption | None = None) -> list[Weapon]:
        data = await self.http.get_weapons(language=language or self.language)
        weapons = Response[list[Weapon]].model_validate(data)
        return weapons.data

    async def fetch_skin(self, uuid: str, /, *, language: LanguageOption | None = None) -> Skin | None:
        data = await self.http.get_weapon_skin(uuid, language=language or self.language)
        skin = Response[Skin].model_validate(data)
        return skin.data

    async def fetch_skins(self, *, language: LanguageOption | None = None) -> list[Skin]:
        data = await self.http.get_weapon_skins(language=language or self.language)
        skins = Response[list[Skin]].model_validate(data)
        return skins.data

    async def fetch_skin_chroma(self, uuid: str, /, *, language: LanguageOption | None = None) -> SkinChroma | None:
        data = await self.http.get_weapon_skin_chroma(uuid, language=language or self.language)
        skin_chroma = Response[SkinChroma].model_validate(data)
        return skin_chroma.data

    async def fetch_skin_chromas(self, *, language: LanguageOption | None = None) -> list[SkinChroma]:
        data = await self.http.get_weapon_skin_chromas(language=language or self.language)
        skin_chromas = Response[list[SkinChroma]].model_validate(data)
        return skin_chromas.data

    async def fetch_skin_level(self, uuid: str, /, *, language: LanguageOption | None = None) -> SkinLevel | None:
        data = await self.http.get_weapon_skin_level(uuid, language=language or self.language)
        skin_level = Response[SkinLevel].model_validate(data)
        return skin_level.data

    async def fetch_skin_levels(self, *, language: LanguageOption | None = None) -> list[SkinLevel]:
        data = await self.http.get_weapon_skin_levels(language=language or self.language)
        skin_levels = Response[list[SkinLevel]].model_validate(data)
        return skin_levels.data

    # version

    async def fetch_version(self) -> Version:
        data = await self.http.get_version()
        version = Response[Version].model_validate(data)
        return version.data
