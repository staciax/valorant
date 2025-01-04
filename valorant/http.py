"""
The MIT License (MIT).

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

import logging
import sys
from typing import TYPE_CHECKING, Any, ClassVar, TypeVar
from urllib.parse import quote as _uriquote

import aiohttp

from . import __version__, utils
from .errors import BadRequest, HTTPException, InternalServerError, NotFound, RateLimited

if TYPE_CHECKING:
    from collections.abc import Coroutine

    T = TypeVar('T')
    Response = Coroutine[Any, Any, T]

_log = logging.getLogger(__name__)


# http-client inspired by https://github.com/Rapptz/discord.py/blob/master/discord/http.py


async def to_json(response: aiohttp.ClientResponse) -> dict[str, Any] | str:
    text = await response.text(encoding='utf-8')
    return utils._from_json(text)  # type: ignore[no-any-return]


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
            url = url.format_map({k: _uriquote(v, safe='') if isinstance(v, str) else v for k, v in parameters.items()})

        self.url: str = url


class HTTPClient:
    def __init__(self, session: aiohttp.ClientSession | None = None) -> None:
        self.__session: aiohttp.ClientSession | None = session
        user_agent = 'valorantx (https://github.com/staciax/valorant {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
        self.user_agent: str = user_agent.format(__version__, sys.version_info, aiohttp.__version__)

    async def start(self) -> None:
        if self.__session is None:
            self.__session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=0))

    async def request(self, route: Route, **kwargs: Any) -> Any:
        assert self.__session is not None, 'Session is not initialized'

        method = route.method
        url = route.url
        kwargs['headers'] = {'User-Agent': self.user_agent}

        response: aiohttp.ClientResponse | None = None
        data: dict[str, Any] | str | None = None

        async with self.__session.request(method, url, **kwargs) as response:  # noqa: F811
            _log.debug('%s %s with returned %s', method, url, response.status)

            data = await to_json(response)

            if 300 > response.status >= 200:
                _log.debug('%s %s has received %s', method, url, data)
                return data

            if response.status == 400:
                raise BadRequest(response, data)

            if response.status == 429:
                raise RateLimited(response, data)

            if response.status == 404:
                raise NotFound(response, data)

            if response.status >= 500:
                raise InternalServerError(response, data)

            raise HTTPException(response, data)

    async def close(self) -> None:
        if self.__session is not None:
            await self.__session.close()

    def clear(self) -> None:
        if self.__session and self.__session.closed:
            self.__session = None

    # valorant-api.com

    def get_agents(self, *, language: str | None = None, is_playable_character: bool = True) -> Response[Any]:
        params = {'isPlayableCharacter': str(is_playable_character)}
        if language is not None:
            params['language'] = language
        return self.request(Route('GET', '/agents'), params=params)

    def get_agent(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language is not None:
            params['language'] = language
        return self.request(Route('GET', '/agents/{uuid}', uuid=uuid), params=params)

    # # -

    def get_buddies(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/buddies'), params=params)

    def get_buddy(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/buddies/{uuid}', uuid=uuid), params=params)

    def get_buddy_levels(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/buddies/levels'), params=params)

    def get_buddy_level(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/buddies/levels/{uuid}', uuid=uuid), params=params)

    # -

    def get_bundles(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/bundles'), params=params)

    def get_bundle(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/bundles/{uuid}', uuid=uuid), params=params)

    # -

    def get_ceremonies(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/ceremonies'), params=params)

    def get_ceremony(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/ceremonies/{uuid}', uuid=uuid), params=params)

    # -

    def get_competitive_tiers(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/competitivetiers'), params=params)

    def get_competitive_tier(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/competitivetiers/{uuid}', uuid=uuid), params=params)

    # -

    def get_content_tiers(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/contenttiers'), params=params)

    def get_content_tier(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/contenttiers/{uuid}', uuid=uuid), params=params)

    # -

    def get_contracts(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/contracts'), params=params)

    def get_contract(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/contracts/{uuid}', uuid=uuid), params=params)

    # -

    def get_currencies(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/currencies'), params=params)

    def get_currency(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/currencies/{uuid}', uuid=uuid), params=params)

    # -

    def get_events(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/events'), params=params)

    def get_event(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/events/{uuid}', uuid=uuid), params=params)

    # -

    def get_game_modes(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/gamemodes'), params=params)

    def get_game_mode(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/gamemodes/{uuid}', uuid=uuid), params=params)

    def get_game_mode_equippables(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/gamemodes/equippables'), params=params)

    def get_game_mode_equippable(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/gamemodes/equippables/{uuid}', uuid=uuid), params=params)

    # -

    def get_all_gear(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/gear'), params=params)

    def get_gear(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/gear/{uuid}', uuid=uuid), params=params)

    # -

    def get_level_borders(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/levelborders'), params=params)

    def get_level_border(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/levelborders/{uuid}', uuid=uuid), params=params)

    # -

    def get_maps(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/maps'), params=params)

    def get_map(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/maps/{uuid}', uuid=uuid), params=params)

    # -

    def get_missions(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/missions'), params=params)

    def get_mission(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/missions/{uuid}', uuid=uuid), params=params)

    # -

    def get_player_cards(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/playercards'), params=params)

    def get_player_card(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/playercards/{uuid}', uuid=uuid), params=params)

    # -

    def get_player_titles(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/playertitles'), params=params)

    def get_player_title(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/playertitles/{uuid}', uuid=uuid), params=params)

    # -

    def get_seasons(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/seasons'), params=params)

    def get_season(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/seasons/{uuid}', uuid=uuid), params=params)

    def get_competitive_seasons(self) -> Response[Any]:
        return self.request(Route('GET', '/seasons/competitive'))

    def get_competitive_season(self, uuid: str) -> Response[Any]:
        return self.request(Route('GET', '/seasons/competitive/{uuid}', uuid=uuid))

    # -

    def get_sprays(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/sprays'), params=params)

    def get_spray(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/sprays/{uuid}', uuid=uuid), params=params)

    def get_spray_levels(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/sprays/levels'), params=params)

    def get_spray_level(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/sprays/levels/{uuid}', uuid=uuid), params=params)

    # -

    def get_themes(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/themes'), params=params)

    def get_theme(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/themes/{uuid}', uuid=uuid), params=params)

    # -

    def get_weapons(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/weapons'), params=params)

    def get_weapon(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/weapons/{uuid}', uuid=uuid), params=params)

    def get_weapon_skins(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/weapons/skins'), params=params)

    def get_weapon_skin(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/weapons/skins/{uuid}', uuid=uuid), params=params)

    def get_weapon_skin_chromas(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/weapons/skinchromas'), params=params)

    def get_weapon_skin_chroma(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/weapons/skinchromas/{uuid}', uuid=uuid), params=params)

    def get_weapon_skin_levels(self, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/weapons/skinlevels'), params=params)

    def get_weapon_skin_level(self, uuid: str, *, language: str | None = None) -> Response[Any]:
        params = {}
        if language:
            params['language'] = language
        return self.request(Route('GET', '/weapons/skinlevels/{uuid}', uuid=uuid), params=params)

    # -

    def get_version(self) -> Response[Any]:
        return self.request(Route('GET', '/version'))
