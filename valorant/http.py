"""
The MIT License (MIT)

Copyright (c) 2015-present Rapptz
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
import sys
from typing import TYPE_CHECKING, Any, ClassVar, Coroutine, Dict, Optional, TypeVar, Union
from urllib.parse import quote as _uriquote

import aiohttp

from . import __version__, utils
from .errors import BadRequest, Forbidden, HTTPException, InternalServerError, NotFound, RateLimited

MISSING = utils.MISSING

if TYPE_CHECKING:
    from .types import (
        agents,
        buddies,
        bundles,
        ceremonies,
        competitive_tiers,
        content_tiers,
        contracts,
        currencies,
        events,
        gamemodes,
        gear,
        level_borders,
        maps,
        missions,
        player_cards,
        player_titles,
        seasons,
        sprays,
        themes,
        version,
        weapons,
    )

    T = TypeVar('T')
    Response = Coroutine[Any, Any, T]

_log = logging.getLogger(__name__)

# http-client inspired by https://github.com/Rapptz/discord.py/blob/master/discord/http.pyS


async def to_json(response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str]:
    text = await response.text(encoding='utf-8')
    return utils._from_json(text)


class Route:
    BASE: ClassVar[str] = 'https://valorant-api.com/v1'

    def __init__(
        self,
        method: str,
        path: str,
        **parameters: Any,
    ) -> None:
        self.method = method
        self.path = path
        self.parameters = parameters

        url = Route.BASE + path

        if parameters:
            url = url.format_map({k: _uriquote(v) if isinstance(v, str) else v for k, v in parameters.items()})

        self.url: str = url


class HTTPClient:
    def __init__(self, session: aiohttp.ClientSession = MISSING) -> None:
        self.__session: aiohttp.ClientSession = session
        user_agent = 'valorantx (https://github.com/staciax/valorant {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
        self.user_agent: str = user_agent.format(__version__, sys.version_info, aiohttp.__version__)

    async def init(self) -> None:
        if self.__session is MISSING:
            self.__session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=0))

    async def request(self, route: Route, **kwargs: Any) -> Any:
        method = route.method
        url = route.url
        kwargs['headers'] = {'User-Agent': self.user_agent}

        response: Optional[aiohttp.ClientResponse] = None
        data: Optional[Union[Dict[str, Any], str]] = None

        for tries in range(5):
            try:
                async with self.__session.request(method, url, **kwargs) as response:
                    _log.debug('%s %s with %s has returned %s', method, url, kwargs.get('data'), response.status)
                    data = await to_json(response)
                    if 300 > response.status >= 200:
                        _log.debug('%s %s has received %s', method, url, data)
                        return data

                    if response.status == 400:
                        raise BadRequest(response, data)

                    # we are being rate limited
                    if response.status == 429:
                        if not response.headers.get('Via') or isinstance(data, str):
                            # Banned by Cloudflare more than likely.
                            raise HTTPException(response, data)
                        raise RateLimited(response, data)
                    elif response.status == 403:
                        raise Forbidden(response, data)
                    elif response.status == 404:
                        raise NotFound(response, data)
                    elif response.status >= 500:
                        raise InternalServerError(response, data)
                    else:
                        raise HTTPException(response, data)

            except OSError as e:
                # Connection reset by peer
                if tries < 4 and e.errno in (54, 10054):
                    await asyncio.sleep(1 + tries * 2)
                    continue
                raise

        if response is not None:
            # We've run out of retries, raise.
            if response.status >= 500:
                raise InternalServerError(response, data)

            raise HTTPException(response, data)

        raise RuntimeError('Unreachable code in HTTP handling')

    async def close(self) -> None:
        if self.__session is not MISSING:
            await self.__session.close()

    def clear(self) -> None:
        if self.__session and self.__session.closed:
            self.__session = MISSING

    async def read_from_url(self, url: str) -> bytes:
        async with self.__session.get(url) as resp:
            if resp.status == 200:
                return await resp.read()
            elif resp.status == 403:
                raise Forbidden(resp, 'cannot retrieve asset')
            elif resp.status == 404:
                raise NotFound(resp, 'asset not found')
            else:
                raise HTTPException(resp, 'failed to get asset')

    async def text_from_url(self, url: str) -> str:
        async with self.__session.get(url) as resp:
            if resp.status == 200:
                return await resp.text()
            elif resp.status == 404:
                raise NotFound(resp, 'asset not found')
            elif resp.status == 403:
                raise Forbidden(resp, 'cannot retrieve asset')
            else:
                raise HTTPException(resp, 'failed to get asset')

    # valorant-api.com

    def get_agents(self, *, language: Optional[str] = 'all', is_playable_character: bool = True) -> Response[agents.Agents]:
        params = {'isPlayableCharacter': str(is_playable_character), 'language': language}
        return self.request(Route('GET', '/agents'), params=params)

    def get_agent(self, uuid: str, *, language: Optional[str] = 'all') -> Response[agents.AgentUUID]:
        params = {'language': language}
        return self.request(Route('GET', '/agents/{uuid}', uuid=uuid), params=params)

    # -

    def get_buddies(self, *, language: Optional[str] = 'all') -> Response[buddies.Buddies]:
        return self.request(Route('GET', '/buddies'), params={'language': language})

    def get_buddy(self, uuid: str, *, language: Optional[str] = 'all') -> Response[buddies.BuddyUUID]:
        return self.request(Route('GET', '/buddies/{uuid}', uuid=uuid), params={'language': language})

    def get_buddy_levels(self, *, language: Optional[str] = 'all') -> Response[buddies.BuddyLevels]:
        return self.request(Route('GET', '/buddies/levels'), params={'language': language})

    def get_buddy_level(self, uuid: str, *, language: Optional[str] = 'all') -> Response[buddies.BuddyLevelUUID]:
        return self.request(Route('GET', '/buddies/levels/{uuid}', uuid=uuid), params={'language': language})

    # -

    def get_bundles(self, *, language: Optional[str] = 'all') -> Response[bundles.Bundles]:
        return self.request(Route('GET', '/bundles'), params={'language': language})

    def get_bundle(self, uuid: str, *, language: Optional[str] = 'all') -> Response[bundles.BundleUUID]:
        return self.request(Route('GET', '/bundles/{uuid}', uuid=uuid), params={'language': language})

    # -

    def get_ceremonies(self, *, language: Optional[str] = 'all') -> Response[ceremonies.Ceremonies]:
        return self.request(Route('GET', '/ceremonies'), params={'language': language})

    def get_ceremony(self, uuid: str, *, language: Optional[str] = 'all') -> Response[ceremonies.CeremonyUUID]:
        return self.request(Route('GET', '/ceremonies/{uuid}', uuid=uuid), params={'language': language})

    # -

    def get_competitive_tiers(self, *, language: Optional[str] = 'all') -> Response[competitive_tiers.CompetitiveTiers]:
        return self.request(Route('GET', '/competitivetiers'), params={'language': language})

    def get_competitive_tier(
        self, uuid: str, *, language: Optional[str] = 'all'
    ) -> Response[competitive_tiers.CompetitiveTierUUID]:
        return self.request(Route('GET', '/competitivetiers/{uuid}', uuid=uuid), params={'language': language})

    # -

    def get_content_tiers(self, *, language: Optional[str] = 'all') -> Response[content_tiers.ContentTiers]:
        return self.request(Route('GET', '/contenttiers'), params={'language': language})

    def get_content_tier(self, uuid: str, *, language: Optional[str] = 'all') -> Response[content_tiers.ContentTierUUID]:
        return self.request(Route('GET', '/contenttiers/{uuid}', uuid=uuid), params={'language': language})

    # -

    def get_contracts(self, *, language: Optional[str] = 'all') -> Response[contracts.Contracts]:
        return self.request(Route('GET', '/contracts'), params={'language': language})

    def get_contract(self, uuid: str, *, language: Optional[str] = 'all') -> Response[contracts.ContractUUID]:
        return self.request(Route('GET', '/contracts/{uuid}', uuid=uuid), params={'language': language})

    # -

    def get_currencies(self, *, language: Optional[str] = 'all') -> Response[currencies.Currencies]:
        return self.request(Route('GET', '/currencies'), params={'language': language})

    def get_currency(self, uuid: str, *, language: Optional[str] = 'all') -> Response[currencies.CurrencyUUID]:
        return self.request(Route('GET', '/currencies/{uuid}', uuid=uuid), params={'language': language})

    # -

    def get_events(self, *, language: Optional[str] = 'all') -> Response[events.Events]:
        return self.request(Route('GET', '/events'), params={'language': language})

    def get_event(self, uuid: str, *, language: Optional[str] = 'all') -> Response[events.EventUUID]:
        return self.request(Route('GET', '/events/{uuid}', uuid=uuid), params={'language': language})

    # -

    def get_game_modes(self, *, language: Optional[str] = 'all') -> Response[gamemodes.GameModes]:
        return self.request(Route('GET', '/gamemodes'), params={'language': language})

    def get_game_mode(self, uuid: str, *, language: Optional[str] = 'all') -> Response[gamemodes.GameModeUUID]:
        return self.request(Route('GET', '/gamemodes/{uuid}', uuid=uuid), params={'language': language})

    def get_game_mode_equippables(self, *, language: Optional[str] = 'all') -> Response[gamemodes.GameModeEquippables]:
        return self.request(Route('GET', '/gamemodes/equippables'), params={'language': language})

    def get_game_mode_equippable(
        self, uuid: str, *, language: Optional[str] = 'all'
    ) -> Response[gamemodes.GameModeEquippableUUID]:
        return self.request(
            Route('GET', '/gamemodes/equippables/{uuid}', uuid=uuid),
            params={'language': language},
        )

    # -

    def get_gear(self, *, language: Optional[str] = 'all') -> Response[gear.Gear]:
        return self.request(Route('GET', '/gear'), params={'language': language})

    def get_gear_(self, uuid: str, *, language: Optional[str] = 'all') -> Response[gear.GearUUID]:
        return self.request(Route('GET', '/gear/{uuid}', uuid=uuid), params={'language': language})

    # -

    def get_level_borders(self) -> Response[level_borders.LevelBorders]:
        return self.request(Route('GET', '/levelborders'))

    def get_level_border(self, uuid: str) -> Response[level_borders.LevelBorderUUID]:
        return self.request(Route('GET', '/levelborders/{uuid}', uuid=uuid))

    # -

    def get_maps(self, *, language: Optional[str] = 'all') -> Response[maps.Maps]:
        return self.request(Route('GET', '/maps'), params={'language': language})

    def get_map(self, uuid: str, *, language: Optional[str] = 'all') -> Response[maps.MapUUID]:
        return self.request(Route('GET', '/maps/{uuid}', uuid=uuid), params={'language': language})

    # -

    def get_missions(self, *, language: Optional[str] = 'all') -> Response[missions.Missions]:
        return self.request(Route('GET', '/missions'), params={'language': language})

    def get_mission(self, uuid: str, *, language: Optional[str] = 'all') -> Response[missions.MissionUUID]:
        return self.request(Route('GET', '/missions/{uuid}', uuid=uuid), params={'language': language})

    # -

    def get_player_cards(self, *, language: Optional[str] = 'all') -> Response[player_cards.PlayerCards]:
        return self.request(Route('GET', '/playercards'), params={'language': language})

    def get_player_card(self, uuid: str, *, language: Optional[str] = 'all') -> Response[player_cards.PlayerCardUUID]:
        return self.request(Route('GET', '/playercards/{uuid}', uuid=uuid), params={'language': language})

    # -

    def get_player_titles(self, *, language: Optional[str] = 'all') -> Response[player_titles.PlayerTitles]:
        return self.request(Route('GET', '/playertitles'), params={'language': language})

    def get_player_title(self, uuid: str, *, language: Optional[str] = 'all') -> Response[player_titles.PlayerTitleUUID]:
        return self.request(Route('GET', '/playertitles/{uuid}', uuid=uuid), params={'language': language})

    # -

    def get_seasons(self, *, language: Optional[str] = 'all') -> Response[seasons.Seasons]:
        return self.request(Route('GET', '/seasons'), params={'language': language})

    def get_season(self, uuid: str, *, language: Optional[str] = 'all') -> Response[seasons.SeasonUUID]:
        return self.request(Route('GET', '/seasons/{uuid}', uuid=uuid), params={'language': language})

    def get_competitive_seasons(self) -> Response[seasons.CompetitiveSeasons]:
        return self.request(Route('GET', '/seasons/competitive'))

    def get_competitive_season(self, uuid: str) -> Response[seasons.CompetitiveSeasonUUID]:
        return self.request(Route('GET', '/seasons/competitive/{uuid}', uuid=uuid))

    # -

    def get_sprays(self, *, language: Optional[str] = 'all') -> Response[sprays.Sprays]:
        return self.request(Route('GET', '/sprays'), params={'language': language})

    def get_spray(self, uuid: str, *, language: Optional[str] = 'all') -> Response[sprays.SprayUUID]:
        return self.request(Route('GET', '/sprays/{uuid}', uuid=uuid), params={'language': language})

    def get_spray_levels(self, *, language: Optional[str] = 'all') -> Response[sprays.SprayLevels]:
        return self.request(Route('GET', '/sprays/levels'), params={'language': language})

    def get_spray_level(self, uuid: str, *, language: Optional[str] = 'all') -> Response[sprays.SprayLevelUUID]:
        return self.request(Route('GET', '/sprays/levels/{uuid}', uuid=uuid), params={'language': language})

    # -

    def get_themes(self, *, language: Optional[str] = 'all') -> Response[themes.Themes]:
        return self.request(Route('GET', '/themes'), params={'language': language})

    def get_theme(self, uuid: str, *, language: Optional[str] = 'all') -> Response[themes.ThemeUUID]:
        return self.request(Route('GET', '/themes/{uuid}', uuid=uuid), params={'language': language})

    # -

    def get_weapons(self, *, language: Optional[str] = 'all') -> Response[weapons.Weapons]:
        return self.request(Route('GET', '/weapons'), params={'language': language})

    def get_weapon(self, uuid: str, *, language: Optional[str] = 'all') -> Response[weapons.WeaponUUID]:
        return self.request(Route('GET', '/weapons/{uuid}', uuid=uuid), params={'language': language})

    def get_weapon_skins(self, *, language: Optional[str] = 'all') -> Response[weapons.Skins]:
        return self.request(Route('GET', '/weapons/skins'), params={'language': language})

    def get_weapon_skin(self, uuid: str, *, language: Optional[str] = 'all') -> Response[weapons.SkinUUID]:
        return self.request(Route('GET', '/weapons/skins/{uuid}', uuid=uuid), params={'language': language})

    def get_weapon_skin_chromas(self, *, language: Optional[str] = 'all') -> Response[weapons.SkinChromas]:
        return self.request(Route('GET', '/weapons/skinchromas'), params={'language': language})

    def get_weapon_skin_chroma(self, uuid: str, *, language: Optional[str] = 'all') -> Response[weapons.SkinChromaUUID]:
        return self.request(Route('GET', '/weapons/skinchromas/{uuid}', uuid=uuid), params={'language': language})

    def get_weapon_skin_levels(self, *, language: Optional[str] = 'all') -> Response[weapons.SkinLevels]:
        return self.request(Route('GET', '/weapons/skinlevels'), params={'language': language})

    def get_weapon_skin_level(self, uuid: str, *, language: Optional[str] = 'all') -> Response[weapons.SkinLevelUUID]:
        return self.request(Route('GET', '/weapons/skinlevels/{uuid}', uuid=uuid), params={'language': language})

    # -

    def get_version(self) -> Response[version.Version]:
        return self.request(Route('GET', '/version'))
