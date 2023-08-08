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
from typing import TYPE_CHECKING, Dict, List, Optional

from .models import (
    Agent,
    Buddy,
    BuddyLevel,
    Bundle,
    Ceremony,
    CompetitiveSeason,
    CompetitiveTier,
    ContentTier,
    Contract,
    Currency,
    Event,
    GameMode,
    GameModeEquippable,
    Gear,
    LevelBorder,
    Map,
    Mission,
    PlayerCard,
    PlayerTitle,
    Season,
    Skin,
    SkinChroma,
    SkinLevel,
    Spray,
    SprayLevel,
    Theme,
    Version,
    Weapon,
)
from .utils import MISSING

if TYPE_CHECKING:
    from .enums import Locale
    from .http import HTTPClient
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

# class BaseCache(ABC):

#     @abstractmethod
#     def get(self):
#         raise NotImplementedError

#     @abstractmethod
#     def find(self):
#         raise NotImplementedError

_log = logging.getLogger(__name__)


class CacheState:
    def __init__(self, *, locale: Locale, http: HTTPClient, to_file: bool = False) -> None:
        self.locale = locale
        self.http = http
        self.cache: bool = True
        self._to_file: bool = to_file
        # -
        self._agents: Dict[str, Agent] = {}
        self._buddies: Dict[str, Buddy] = {}
        self._bundles: Dict[str, Bundle] = {}
        self._ceremonies: Dict[str, Ceremony] = {}
        self._competitive_tiers: Dict[str, CompetitiveTier] = {}
        self._content_tiers: Dict[str, ContentTier] = {}
        self._contracts: Dict[str, Contract] = {}
        self._currencies: Dict[str, Currency] = {}
        self._events: Dict[str, Event] = {}
        self._game_modes: Dict[str, GameMode] = {}
        self._game_mode_equippables: Dict[str, GameModeEquippable] = {}
        self._gear: Dict[str, Gear] = {}
        self._level_borders: Dict[str, LevelBorder] = {}
        self._maps: Dict[str, Map] = {}
        self._missions: Dict[str, Mission] = {}
        self._player_cards: Dict[str, PlayerCard] = {}
        self._player_titles: Dict[str, PlayerTitle] = {}
        self._seasons: Dict[str, Season] = {}
        self._competitive_seasons: Dict[str, CompetitiveSeason] = {}
        self._sprays: Dict[str, Spray] = {}
        self._themes: Dict[str, Theme] = {}
        self._version: Version = MISSING
        self._weapons: Dict[str, Weapon] = {}

    async def init(self) -> None:
        tasks = [
            self.http.get_agents,
            self.http.get_buddies,
            self.http.get_bundles,
            self.http.get_ceremonies,
            self.http.get_competitive_tiers,
            self.http.get_content_tiers,
            self.http.get_contracts,
            self.http.get_currencies,
            self.http.get_events,
            self.http.get_game_modes,
            self.http.get_game_mode_equippables,
            self.http.get_gear,
            self.http.get_level_borders,
            self.http.get_maps,
            self.http.get_missions,
            self.http.get_player_cards,
            self.http.get_player_titles,
            self.http.get_seasons,
            self.http.get_competitive_seasons,
            self.http.get_sprays,
            self.http.get_themes,
            self.http.get_weapons,
            self.http.get_version,
        ]
        # if self._to_file:

        #     # read from file
        #     for func in tasks:
        #         funcname = func.__name__.split('_')[1:]
        #         filename = '_'.join(funcname) + '.json'
        #         # add_to_cache = getattr(self, f'add_{funcname}')
        #         # if os.path.exists(filename):
        #         #     with open(filename, 'r') as f:
        #         #         data = json.load(f)
        #         #         continue
        #         # else:
        #         #     data = await func()
        #         #     self._add_to_file(data, filename)
        #         # add_to_cache = getattr(self, f'add_{funcname}')
        # else:
        # results = await self._fetch_data_from_api(tasks)

        results = await asyncio.gather(*(task() for task in tasks))
        for func, result in zip(tasks, results):
            assert result is not None
            funcname = func.__name__.split('_')[1:]
            funcname = '_'.join(funcname)
            parse_func = getattr(self, f'_add_{funcname}')
            parse_func(result)

    # async def _fetch_data_from_api(self, tasks: List[Callable[..., Coroutine[Any, Any, Any]]]) -> List[Any]:
    #     results = await asyncio.gather(*[task() for task in tasks])
    #     return results
    # for func, result in zip(tasks, results):
    #     assert result is not None
    #     funcname = func.__name__.split('_')[1:]
    #     funcname = '_'.join(funcname)
    #     parse_func = getattr(self, f'add_{funcname}')
    #     parse_func(result)

    # def _add_to_file(self, data: Any, filename: str) -> None:
    #     with open(filename, 'w') as f:
    #         json.dump(data, f, indent=4)

    def clear(self) -> None:
        for key in self.__dict__.keys():
            if key.startswith('_') and isinstance(self.__dict__[key], dict):
                self.__dict__[key].clear()
        self._version = MISSING

    # agents

    @property
    def agents(self) -> List[Agent]:
        return list(self._agents.values())

    def get_agent(self, uuid: Optional[str], /) -> Optional[Agent]:
        return self._agents.get(uuid)  # type: ignore

    def store_agent(self, data: agents.Agent) -> Agent:
        agent_id = data['uuid']
        self._agents[agent_id] = agent = Agent(state=self, data=data)
        return agent

    def _add_agents(self, data: agents.Agents) -> None:
        agent_data = data['data']
        for agent in agent_data:
            existing = self.get_agent(agent['uuid'])
            if existing is None:
                self.store_agent(agent)

    async def fetch_agents(self) -> List[Agent]:
        data = await self.http.get_agents()
        self._add_agents(data)
        return self.agents

    # buddies

    @property
    def buddies(self) -> List[Buddy]:
        return list(self._buddies.values())

    @property
    def buddy_levels(self) -> List[BuddyLevel]:
        levels = []
        for buddy in self.buddies:
            levels.extend(buddy.levels)
        return levels

    def get_buddy(self, uuid: Optional[str], /) -> Optional[Buddy]:
        return self._buddies.get(uuid)  # type: ignore

    def get_buddy_level(self, uuid: Optional[str], /) -> Optional[BuddyLevel]:
        for level in self.buddy_levels:
            if level.uuid == uuid:
                return level
        return None

    def store_buddy(self, data: buddies.Buddy) -> Buddy:
        buddy_id = data['uuid']
        self._buddies[buddy_id] = buddy = Buddy(state=self, data=data)
        return buddy

    def _add_buddies(self, data: buddies.Buddies) -> None:
        buddy_data = data['data']
        for buddy in buddy_data:
            buddy_existing = self.get_buddy(buddy['uuid'])
            if buddy_existing is None:
                self.store_buddy(buddy)

    async def fetch_buddies(self) -> List[Buddy]:
        data = await self.http.get_buddies()
        self._add_buddies(data)
        return self.buddies

    # bundles

    @property
    def bundles(self) -> List[Bundle]:
        return list(self._bundles.values())

    def get_bundle(self, uuid: Optional[str], /) -> Optional[Bundle]:
        return self._bundles.get(uuid)  # type: ignore

    def store_bundle(self, data: bundles.Bundle) -> Bundle:
        bundle_id = data['uuid']
        self._bundles[bundle_id] = bundle = Bundle(state=self, data=data)
        return bundle

    def _add_bundles(self, data: bundles.Bundles) -> None:
        bundle_data = data['data']
        for bundle in bundle_data:
            bundle_existing = self.get_bundle(bundle['uuid'])
            if bundle_existing is None:
                self.store_bundle(bundle)

    async def fetch_bundles(self) -> List[Bundle]:
        data = await self.http.get_bundles()
        self._add_bundles(data)
        return self.bundles

    # ceremonies

    @property
    def ceremonies(self) -> List[Ceremony]:
        return list(self._ceremonies.values())

    def get_ceremony(self, uuid: Optional[str], /) -> Optional[Ceremony]:
        return self._ceremonies.get(uuid)  # type: ignore

    def store_ceremony(self, data: ceremonies.Ceremony) -> Ceremony:
        ceremony_id = data['uuid']
        self._ceremonies[ceremony_id] = ceremony = Ceremony(state=self, data=data)
        return ceremony

    def _add_ceremonies(self, data: ceremonies.Ceremonies) -> None:
        ceremony_data = data['data']
        for ceremony in ceremony_data:
            ceremony_existing = self.get_ceremony(ceremony['uuid'])
            if ceremony_existing is None:
                self.store_ceremony(ceremony)

    async def fetch_ceremonies(self) -> List[Ceremony]:
        data = await self.http.get_ceremonies()
        self._add_ceremonies(data)
        return self.ceremonies

    # competitive tiers

    @property
    def competitive_tiers(self) -> List[CompetitiveTier]:
        return list(self._competitive_tiers.values())

    def get_competitive_tier(self, uuid: Optional[str], /) -> Optional[CompetitiveTier]:
        return self._competitive_tiers.get(uuid)  # type: ignore

    def store_competitive_tier(self, data: competitive_tiers.CompetitiveTier) -> CompetitiveTier:
        competitive_tier_id = data['uuid']
        self._competitive_tiers[competitive_tier_id] = competitive_tier = CompetitiveTier(state=self, data=data)
        return competitive_tier

    def _add_competitive_tiers(self, data: competitive_tiers.CompetitiveTiers) -> None:
        competitive_tier_data = data['data']
        for competitive_tier in competitive_tier_data:
            competitive_tier_existing = self.get_competitive_tier(competitive_tier['uuid'])
            if competitive_tier_existing is None:
                self.store_competitive_tier(competitive_tier)

    async def fetch_competitive_tiers(self) -> List[CompetitiveTier]:
        data = await self.http.get_competitive_tiers()
        self._add_competitive_tiers(data)
        return self.competitive_tiers

    # content tiers

    @property
    def content_tiers(self) -> List[ContentTier]:
        return list(self._content_tiers.values())

    def get_content_tier(self, uuid: Optional[str], /) -> Optional[ContentTier]:
        return self._content_tiers.get(uuid)  # type: ignore

    def store_content_tier(self, data: content_tiers.ContentTier) -> ContentTier:
        content_tier_id = data['uuid']
        self._content_tiers[content_tier_id] = content_tier = ContentTier(state=self, data=data)
        return content_tier

    def _add_content_tiers(self, data: content_tiers.ContentTiers) -> None:
        content_tier_data = data['data']
        for content_tier in content_tier_data:
            content_tier_existing = self.get_content_tier(content_tier['uuid'])
            if content_tier_existing is None:
                self.store_content_tier(content_tier)

    async def fetch_content_tiers(self) -> List[ContentTier]:
        data = await self.http.get_content_tiers()
        self._add_content_tiers(data)
        return self.content_tiers

    # contracts

    @property
    def contracts(self) -> List[Contract]:
        return list(self._contracts.values())

    def get_contract(self, uuid: Optional[str], /) -> Optional[Contract]:
        return self._contracts.get(uuid)  # type: ignore

    def store_contract(self, data: contracts.Contract) -> Contract:
        contract_id = data['uuid']
        self._contracts[contract_id] = contract = Contract(state=self, data=data)
        return contract

    def _add_contracts(self, data: contracts.Contracts) -> None:
        contract_data = data['data']
        for contract in contract_data:
            contract_existing = self.get_contract(contract['uuid'])
            if contract_existing is None:
                self.store_contract(contract)

    async def fetch_contracts(self) -> List[Contract]:
        data = await self.http.get_contracts()
        self._add_contracts(data)
        return self.contracts

    # currencies

    @property
    def currencies(self) -> List[Currency]:
        return list(self._currencies.values())

    def get_currency(self, uuid: Optional[str], /) -> Optional[Currency]:
        return self._currencies.get(uuid)  # type: ignore

    def store_currency(self, data: currencies.Currency) -> Currency:
        currency_id = data['uuid']
        self._currencies[currency_id] = currency = Currency(state=self, data=data)
        return currency

    def _add_currencies(self, data: currencies.Currencies) -> None:
        currency_data = data['data']
        for currency in currency_data:
            currency_existing = self.get_currency(currency['uuid'])
            if currency_existing is None:
                self.store_currency(currency)

    async def fetch_currencies(self) -> List[Currency]:
        data = await self.http.get_currencies()
        self._add_currencies(data)
        return self.currencies

    # events

    @property
    def events(self) -> List[Event]:
        return list(self._events.values())

    def get_event(self, uuid: Optional[str], /) -> Optional[Event]:
        return self._events.get(uuid)  # type: ignore

    def store_event(self, data: events.Event) -> Event:
        event_id = data['uuid']
        self._events[event_id] = event = Event(state=self, data=data)
        return event

    def _add_events(self, data: events.Events) -> None:
        event_data = data['data']
        for event in event_data:
            event_existing = self.get_event(event['uuid'])
            if event_existing is None:
                self.store_event(event)

    async def fetch_events(self) -> List[Event]:
        data = await self.http.get_events()
        self._add_events(data)
        return self.events

    # game modes

    @property
    def game_modes(self) -> List[GameMode]:
        return list(self._game_modes.values())

    @property
    def game_mode_equippables(self) -> List[GameModeEquippable]:
        return list(self._game_mode_equippables.values())

    def get_game_mode(self, uuid: Optional[str], /) -> Optional[GameMode]:
        return self._game_modes.get(uuid)  # type: ignore

    def get_game_mode_equippable(self, uuid: Optional[str], /) -> Optional[GameModeEquippable]:
        return self._game_mode_equippables.get(uuid)  # type: ignore

    def store_game_mode(self, data: gamemodes.GameMode) -> GameMode:
        game_mode_id = data['uuid']
        self._game_modes[game_mode_id] = game_mode = GameMode(state=self, data=data)
        return game_mode

    def store_game_mode_equippable(self, data: gamemodes.GameModeEquippable) -> GameModeEquippable:
        game_mode_equippable_id = data['uuid']
        self._game_mode_equippables[game_mode_equippable_id] = game_mode_equippable = GameModeEquippable(
            state=self,
            data=data,
        )
        return game_mode_equippable

    def _add_game_modes(self, data: gamemodes.GameModes) -> None:
        game_mode_data = data['data']
        for game_mode in game_mode_data:
            game_mode_existing = self.get_game_mode(game_mode['uuid'])
            if game_mode_existing is None:
                self.store_game_mode(game_mode)

    async def fetch_game_modes(self) -> List[GameMode]:
        data = await self.http.get_game_modes()
        self._add_game_modes(data)
        return self.game_modes

    def _add_game_mode_equippables(self, data: gamemodes.GameModeEquippables) -> None:
        game_mode_equippable_data = data['data']
        for game_mode_equippable in game_mode_equippable_data:
            game_mode_equippable_existing = self.get_game_mode_equippable(game_mode_equippable['uuid'])
            if game_mode_equippable_existing is None:
                self.store_game_mode_equippable(game_mode_equippable)

    async def fetch_game_mode_equippables(self) -> List[GameModeEquippable]:
        data = await self.http.get_game_mode_equippables()
        self._add_game_mode_equippables(data)
        return self.game_mode_equippables

    # gear

    @property
    def gear(self) -> List[Gear]:
        return list(self._gear.values())

    def get_gear(self, uuid: Optional[str], /) -> Optional[Gear]:
        return self._gear.get(uuid)  # type: ignore

    def store_gear(self, data: gear.Gear_) -> Gear:
        gear_id = data['uuid']
        self._gear[gear_id] = gear = Gear(state=self, data=data)
        return gear

    def _add_gear(self, data: gear.Gear) -> None:
        gear_data = data['data']
        for gear_ in gear_data:
            gear_existing = self.get_gear(gear_['uuid'])
            if gear_existing is None:
                self.store_gear(gear_)

    async def fetch_gear(self) -> List[Gear]:
        data = await self.http.get_gear()
        self._add_gear(data)
        return self.gear

    # level borders

    @property
    def level_borders(self) -> List[LevelBorder]:
        return list(self._level_borders.values())

    def get_level_border(self, uuid: Optional[str], /) -> Optional[LevelBorder]:
        return self._level_borders.get(uuid)  # type: ignore

    def store_level_border(self, data: level_borders.LevelBorder) -> LevelBorder:
        level_border_id = data['uuid']
        self._level_borders[level_border_id] = level_border = LevelBorder(state=self, data=data)
        return level_border

    def _add_level_borders(self, data: level_borders.LevelBorders) -> None:
        level_border_data = data['data']
        for level_border in level_border_data:
            level_border_existing = self.get_level_border(level_border['uuid'])
            if level_border_existing is None:
                self.store_level_border(level_border)

    async def fetch_level_borders(self) -> List[LevelBorder]:
        data = await self.http.get_level_borders()
        self._add_level_borders(data)
        return self.level_borders

    # maps

    @property
    def maps(self) -> List[Map]:
        return list(self._maps.values())

    def get_map(self, uuid: Optional[str], /) -> Optional[Map]:
        return self._maps.get(uuid)  # type: ignore

    def store_map(self, data: maps.Map) -> Map:
        map_id = data['uuid']
        self._maps[map_id] = map_ = Map(state=self, data=data)
        return map_

    def _add_maps(self, data: maps.Maps) -> None:
        map_data = data['data']
        for map_ in map_data:
            map_existing = self.get_map(map_['uuid'])
            if map_existing is None:
                self.store_map(map_)

    async def fetch_maps(self) -> List[Map]:
        data = await self.http.get_maps()
        self._add_maps(data)
        return self.maps

    # missions

    @property
    def missions(self) -> List[Mission]:
        return list(self._missions.values())

    def get_mission(self, uuid: Optional[str], /) -> Optional[Mission]:
        return self._missions.get(uuid)  # type: ignore

    def store_mission(self, data: missions.Mission) -> Mission:
        mission_id = data['uuid']
        self._missions[mission_id] = mission = Mission(state=self, data=data)
        return mission

    def _add_missions(self, data: missions.Missions) -> None:
        mission_data = data['data']
        for mission in mission_data:
            mission_existing = self.get_mission(mission['uuid'])
            if mission_existing is None:
                self.store_mission(mission)

    async def fetch_missions(self) -> List[Mission]:
        data = await self.http.get_missions()
        self._add_missions(data)
        return self.missions

    # player_cards

    @property
    def player_cards(self) -> List[PlayerCard]:
        return list(self._player_cards.values())

    def get_player_card(self, uuid: Optional[str], /) -> Optional[PlayerCard]:
        return self._player_cards.get(uuid)  # type: ignore

    def store_player_card(self, data: player_cards.PlayerCard) -> PlayerCard:
        player_card_id = data['uuid']
        self._player_cards[player_card_id] = player_card = PlayerCard(state=self, data=data)
        return player_card

    def _add_player_cards(self, data: player_cards.PlayerCards) -> None:
        player_card_data = data['data']
        for player_card in player_card_data:
            player_card_existing = self.get_player_card(player_card['uuid'])
            if player_card_existing is None:
                self.store_player_card(player_card)

    async def fetch_player_cards(self) -> List[PlayerCard]:
        data = await self.http.get_player_cards()
        self._add_player_cards(data)
        return self.player_cards

    # player_titles

    @property
    def player_titles(self) -> List[PlayerTitle]:
        return list(self._player_titles.values())

    def get_player_title(self, uuid: Optional[str], /) -> Optional[PlayerTitle]:
        return self._player_titles.get(uuid)  # type: ignore

    def store_player_title(self, data: player_titles.PlayerTitle) -> PlayerTitle:
        player_title_id = data['uuid']
        self._player_titles[player_title_id] = player_title = PlayerTitle(state=self, data=data)
        return player_title

    def _add_player_titles(self, data: player_titles.PlayerTitles) -> None:
        player_title_data = data['data']
        for player_title in player_title_data:
            player_title_existing = self.get_player_title(player_title['uuid'])
            if player_title_existing is None:
                self.store_player_title(player_title)

    async def fetch_player_titles(self) -> List[PlayerTitle]:
        data = await self.http.get_player_titles()
        self._add_player_titles(data)
        return self.player_titles

    # seasons

    @property
    def seasons(self) -> List[Season]:
        return list(self._seasons.values())

    def get_season(self, uuid: Optional[str], /) -> Optional[Season]:
        return self._seasons.get(uuid)  # type: ignore

    def store_season(self, data: seasons.Season) -> Season:
        season_id = data['uuid']
        self._seasons[season_id] = season = Season(state=self, data=data)
        return season

    def _add_seasons(self, data: seasons.Seasons) -> None:
        season_data = data['data']
        for season in season_data:
            season_existing = self.get_season(season['uuid'])
            if season_existing is None:
                self.store_season(season)

    async def fetch_seasons(self) -> List[Season]:
        data = await self.http.get_seasons()
        self._add_seasons(data)
        return self.seasons

    @property
    def competitive_seasons(self) -> List[CompetitiveSeason]:
        return list(self._competitive_seasons.values())

    def get_competitive_season(self, uuid: Optional[str], /) -> Optional[CompetitiveSeason]:
        return self._competitive_seasons.get(uuid)  # type: ignore

    def store_competitive_season(self, data: seasons.CompetitiveSeason) -> CompetitiveSeason:
        season_id = data['uuid']
        self._competitive_seasons[season_id] = season = CompetitiveSeason(state=self, data=data)
        return season

    def _add_competitive_seasons(self, data: seasons.CompetitiveSeasons) -> None:
        season_data = data['data']
        for season in season_data:
            season_existing = self.get_competitive_season(season['uuid'])
            if season_existing is None:
                self.store_competitive_season(season)

    async def fetch_competitive_seasons(self) -> List[CompetitiveSeason]:
        data = await self.http.get_competitive_seasons()
        self._add_competitive_seasons(data)
        return self.competitive_seasons

    # sprays

    @property
    def sprays(self) -> List[Spray]:
        return list(self._sprays.values())

    def get_spray(self, uuid: Optional[str], /) -> Optional[Spray]:
        return self._sprays.get(uuid)  # type: ignore

    @property
    def spray_levels(self) -> List[SprayLevel]:
        levels = []
        for spray in self.sprays:
            levels.extend(spray.levels)
        return levels

    def get_spray_level(self, uuid: Optional[str], /) -> Optional[SprayLevel]:
        for level in self.spray_levels:
            if level.uuid == uuid:
                return level
        return

    def store_spray(self, data: sprays.Spray) -> Spray:
        spray_id = data['uuid']
        self._sprays[spray_id] = spray = Spray(state=self, data=data)
        return spray

    def _add_sprays(self, data: sprays.Sprays) -> None:
        spray_data = data['data']
        for spray in spray_data:
            spray_existing = self.get_spray(spray['uuid'])
            if spray_existing is None:
                self.store_spray(spray)

    async def fetch_sprays(self) -> List[Spray]:
        data = await self.http.get_sprays()
        self._add_sprays(data)
        return self.sprays

    # themes

    @property
    def themes(self) -> List[Theme]:
        return list(self._themes.values())

    def get_theme(self, uuid: Optional[str], /) -> Optional[Theme]:
        return self._themes.get(uuid)  # type: ignore

    def store_theme(self, data: themes.Theme) -> Theme:
        theme_id = data['uuid']
        self._themes[theme_id] = theme = Theme(state=self, data=data)
        return theme

    def _add_themes(self, data: themes.Themes) -> None:
        theme_data = data['data']
        for theme in theme_data:
            theme_existing = self.get_theme(theme['uuid'])
            if theme_existing is None:
                self.store_theme(theme)

    async def fetch_themes(self) -> List[Theme]:
        data = await self.http.get_themes()
        self._add_themes(data)
        return self.themes

    # version

    @property
    def version(self) -> Version:
        return self._version

    def _add_version(self, data: version.Version) -> None:
        self._version = Version(state=self, data=data['data'])

    async def fetch_version(self) -> Version:
        data = await self.http.get_version()
        self._add_version(data)
        return self.version

    # weapons

    @property
    def weapons(self) -> List[Weapon]:
        return list(self._weapons.values())

    def get_weapon(self, uuid: Optional[str], /) -> Optional[Weapon]:
        return self._weapons.get(uuid)  # type: ignore

    @property
    def skins(self) -> List[Skin]:
        skins = []
        for weapon in self.weapons:
            skins.extend(weapon.skins)
        return skins

    def get_skin(self, uuid: Optional[str], /) -> Optional[Skin]:
        for skin in self.skins:
            if skin.uuid == uuid:
                return skin
        return None

    @property
    def skin_chromas(self) -> List[SkinChroma]:
        chromas = []
        for skin in self.skins:
            chromas.extend(skin.chromas)
        return chromas

    def get_skin_chroma(self, uuid: Optional[str], /) -> Optional[SkinChroma]:
        for chroma in self.skin_chromas:
            if chroma.uuid == uuid:
                return chroma
        return None

    @property
    def skin_levels(self) -> List[SkinLevel]:
        levels = []
        for skin in self.skins:
            levels.extend(skin.levels)
        return levels

    def get_skin_level(self, uuid: Optional[str], /) -> Optional[SkinLevel]:
        for level in self.skin_levels:
            if level.uuid == uuid:
                return level
        return None

    def store_weapon(self, data: weapons.Weapon) -> Weapon:
        weapon_id = data['uuid']
        self._weapons[weapon_id] = weapon = Weapon(state=self, data=data)
        return weapon

    def _add_weapons(self, data: weapons.Weapons) -> None:
        weapon_data = data['data']
        for weapon in weapon_data:
            weapon_existing = self.get_weapon(weapon['uuid'])
            if weapon_existing is None:
                self.store_weapon(weapon)

    async def fetch_weapons(self) -> List[Weapon]:
        data = await self.http.get_weapons()
        self._add_weapons(data)
        return self.weapons
