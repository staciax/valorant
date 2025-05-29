from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import pytest

from valorant.enums import Language
from valorant.errors import NotFound

if TYPE_CHECKING:
    from valorant import Client
    from valorant.client import LanguageOption


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
@pytest.mark.parametrize(
    ('is_playable_character'),
    [True, None],
)
async def test_agents(
    client: Client, language: LanguageOption | None, is_playable_character: Literal[True] | None
) -> None:
    agents = await client.fetch_agents(language=language, is_playable_character=is_playable_character)
    assert len(agents) > 0

    agent_id = agents[0].uuid
    agent = await client.fetch_agent(str(agent_id), language=language)
    assert agent is not None
    assert agent_id == agent.uuid

    with pytest.raises(NotFound):
        await client.fetch_agent('fake-agent-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_buddies(client: Client, language: LanguageOption | None) -> None:
    buddies = await client.fetch_buddies(language=language)
    assert len(buddies) > 0

    buddy_id = buddies[0].uuid
    buddy = await client.fetch_buddy(str(buddy_id), language=language)
    assert buddy is not None
    assert buddy_id == buddy.uuid

    with pytest.raises(NotFound):
        await client.fetch_buddy('fake-buddy-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_buddy_levels(client: Client, language: LanguageOption | None) -> None:
    buddy_levels = await client.fetch_buddy_levels(language=language)
    assert len(buddy_levels) > 0

    buddy_level_id = buddy_levels[0].uuid
    buddy_level = await client.fetch_buddy_level(str(buddy_level_id), language=language)
    assert buddy_level is not None
    assert buddy_level_id == buddy_level.uuid

    with pytest.raises(NotFound):
        await client.fetch_buddy_level('fake-buddy-level-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), (None)],
)
async def test_bundles(client: Client, language: LanguageOption | None) -> None:
    bundles = await client.fetch_bundles(language=language)
    assert len(bundles) > 0

    bundle_id = bundles[0].uuid
    bundle = await client.fetch_bundle(str(bundle_id), language=language)
    assert bundle is not None
    assert bundle_id == bundle.uuid

    with pytest.raises(NotFound):
        await client.fetch_bundle('fake-bundle-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), (None)],
)
async def test_ceremonies(client: Client, language: LanguageOption | None) -> None:
    ceremonies = await client.fetch_ceremonies(language=language)
    assert len(ceremonies) > 0

    ceremony_id = ceremonies[0].uuid
    ceremony = await client.fetch_ceremony(str(ceremony_id), language=language)
    assert ceremony is not None
    assert ceremony_id == ceremony.uuid

    with pytest.raises(NotFound):
        await client.fetch_ceremony('fake-ceremony-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_competitive_tiers(client: Client, language: LanguageOption | None) -> None:
    competitive_tiers = await client.fetch_competitive_tiers(language=language)
    assert len(competitive_tiers) > 0

    competitive_tier_id = competitive_tiers[0].uuid
    competitive_tier = await client.fetch_competitive_tier(str(competitive_tier_id), language=language)
    assert competitive_tier is not None
    assert competitive_tier_id == competitive_tier.uuid

    with pytest.raises(NotFound):
        await client.fetch_competitive_tier('fake-competitive-tier-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_content_tiers(client: Client, language: LanguageOption | None) -> None:
    content_tiers = await client.fetch_content_tiers(language=language)
    assert len(content_tiers) > 0

    content_tier_id = content_tiers[0].uuid
    content_tier = await client.fetch_content_tier(str(content_tier_id), language=language)
    assert content_tier is not None
    assert content_tier_id == content_tier.uuid

    with pytest.raises(NotFound):
        await client.fetch_content_tier('fake-content-tier-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_contracts(client: Client, language: LanguageOption | None) -> None:
    contracts = await client.fetch_contracts(language=language)
    assert len(contracts) > 0

    contract_id = contracts[0].uuid
    contract = await client.fetch_contract(str(contract_id), language=language)
    assert contract is not None
    assert contract_id == contract.uuid

    with pytest.raises(NotFound):
        await client.fetch_contract('fake-contract-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_currencies(client: Client, language: LanguageOption | None) -> None:
    currencies = await client.fetch_currencies(language=language)
    assert len(currencies) > 0

    currency_id = currencies[0].uuid
    currency = await client.fetch_currency(str(currency_id), language=language)
    assert currency is not None
    assert currency_id == currency.uuid

    with pytest.raises(NotFound):
        await client.fetch_currency('fake-currency-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_events(client: Client, language: LanguageOption | None) -> None:
    events = await client.fetch_events(language=language)
    assert len(events) > 0

    event_id = events[0].uuid
    event = await client.fetch_event(str(event_id), language=language)
    assert event is not None
    assert event_id == event.uuid

    with pytest.raises(NotFound):
        await client.fetch_event('fake-event-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_flexes(client: Client, language: LanguageOption | None) -> None:
    flexes = await client.fetch_flexes(language=language)
    assert len(flexes) > 0

    flex_id = flexes[0].uuid
    flex = await client.fetch_flex(str(flex_id), language=language)
    assert flex is not None
    assert flex_id == flex.uuid

    with pytest.raises(NotFound):
        await client.fetch_flex('fake-flex-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_game_modes(client: Client, language: LanguageOption | None) -> None:
    game_modes = await client.fetch_game_modes(language=language)
    assert len(game_modes) > 0

    game_mode_id = game_modes[0].uuid
    game_mode = await client.fetch_game_mode(str(game_mode_id), language=language)
    assert game_mode is not None
    assert game_mode_id == game_mode.uuid

    with pytest.raises(NotFound):
        await client.fetch_game_mode('fake-game-mode-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_game_mode_equippables(client: Client, language: LanguageOption | None) -> None:
    game_mode_equippables = await client.fetch_game_mode_equippables(language=language)
    assert len(game_mode_equippables) > 0

    game_mode_equippable_id = game_mode_equippables[0].uuid
    game_mode_equippable = await client.fetch_game_mode_equippable(str(game_mode_equippable_id), language=language)
    assert game_mode_equippable is not None
    assert game_mode_equippable_id == game_mode_equippable.uuid

    with pytest.raises(NotFound):
        await client.fetch_game_mode_equippable('fake-game-mode-equippable-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_gears(client: Client, language: LanguageOption | None) -> None:
    gears = await client.fetch_gears(language=language)
    assert len(gears) > 0

    gear_id = gears[0].uuid
    gear = await client.fetch_gear(str(gear_id), language=language)
    assert gear is not None
    assert gear_id == gear.uuid

    with pytest.raises(NotFound):
        await client.fetch_gear('fake-gear-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_level_borders(client: Client, language: LanguageOption | None) -> None:
    level_borders = await client.fetch_level_borders(language=language)
    assert len(level_borders) > 0

    level_border_id = level_borders[0].uuid
    level_border = await client.fetch_level_border(str(level_border_id), language=language)
    assert level_border is not None
    assert level_border_id == level_border.uuid

    with pytest.raises(NotFound):
        await client.fetch_level_border('fake-level-border-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_maps(client: Client, language: LanguageOption | None) -> None:
    maps = await client.fetch_maps(language=language)
    assert len(maps) > 0

    map_id = maps[0].uuid
    map_ = await client.fetch_map(str(map_id), language=language)
    assert map_ is not None
    assert map_id == map_.uuid

    with pytest.raises(NotFound):
        await client.fetch_map('fake-map-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_missions(client: Client, language: LanguageOption | None) -> None:
    missions = await client.fetch_missions(language=language)
    assert len(missions) > 0

    mission_id = missions[0].uuid
    mission = await client.fetch_mission(str(mission_id), language=language)
    assert mission is not None
    assert mission_id == mission.uuid

    with pytest.raises(NotFound):
        await client.fetch_mission('fake-mission-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_player_cards(client: Client, language: LanguageOption | None) -> None:
    player_cards = await client.fetch_player_cards(language=language)
    assert len(player_cards) > 0

    player_card_id = player_cards[0].uuid
    player_card = await client.fetch_player_card(str(player_card_id), language=language)
    assert player_card is not None
    assert player_card_id == player_card.uuid

    with pytest.raises(NotFound):
        await client.fetch_player_card('fake-player-card-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_player_titles(client: Client, language: LanguageOption | None) -> None:
    player_titles = await client.fetch_player_titles(language=language)
    assert len(player_titles) > 0

    player_title_id = player_titles[0].uuid
    player_title = await client.fetch_player_title(str(player_title_id), language=language)
    assert player_title is not None
    assert player_title_id == player_title.uuid

    with pytest.raises(NotFound):
        await client.fetch_player_title('fake-player-title-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_seasons(client: Client, language: LanguageOption | None) -> None:
    seasons = await client.fetch_seasons(language=language)
    assert len(seasons) > 0

    season_id = seasons[0].uuid
    season = await client.fetch_season(str(season_id), language=language)
    assert season is not None
    assert season_id == season.uuid

    with pytest.raises(NotFound):
        await client.fetch_season('fake-season-id')


@pytest.mark.anyio
async def test_competitive_seasons(client: Client) -> None:
    competitive_seasons = await client.fetch_competitive_seasons()
    assert len(competitive_seasons) > 0

    competitive_season_id = competitive_seasons[0].uuid
    competitive_season = await client.fetch_competitive_season(str(competitive_season_id))
    assert competitive_season is not None
    assert competitive_season_id == competitive_season.uuid

    with pytest.raises(NotFound):
        await client.fetch_competitive_season('fake-competitive-season-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_sprays(client: Client, language: LanguageOption | None) -> None:
    sprays = await client.fetch_sprays(language=language)
    assert len(sprays) > 0

    spray_id = sprays[0].uuid
    spray = await client.fetch_spray(str(spray_id), language=language)
    assert spray is not None
    assert spray_id == spray.uuid

    with pytest.raises(NotFound):
        await client.fetch_spray('fake-spray-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_spray_levels(client: Client, language: LanguageOption | None) -> None:
    spray_levels = await client.fetch_spray_levels(language=language)
    assert len(spray_levels) > 0

    spray_level_id = spray_levels[0].uuid
    spray_level = await client.fetch_spray_level(str(spray_level_id), language=language)
    assert spray_level is not None
    assert spray_level_id == spray_level.uuid

    with pytest.raises(NotFound):
        await client.fetch_spray_level('fake-spray-level-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_themes(client: Client, language: LanguageOption | None) -> None:
    themes = await client.fetch_themes(language=language)
    assert len(themes) > 0

    theme_id = themes[0].uuid
    theme = await client.fetch_theme(str(theme_id), language=language)
    assert theme is not None
    assert theme_id == theme.uuid

    with pytest.raises(NotFound):
        await client.fetch_theme('fake-theme-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_weapons(client: Client, language: LanguageOption | None) -> None:
    weapons = await client.fetch_weapons(language=language)
    assert len(weapons) > 0

    weapon_id = weapons[0].uuid
    weapon = await client.fetch_weapon(str(weapon_id), language=language)
    assert weapon is not None
    assert weapon_id == weapon.uuid

    with pytest.raises(NotFound):
        await client.fetch_weapon('fake-weapon-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_weapon_skins(client: Client, language: LanguageOption | None) -> None:
    weapon_skins = await client.fetch_skins(language=language)
    assert len(weapon_skins) > 0

    weapon_skin_id = weapon_skins[0].uuid
    weapon_skin = await client.fetch_skin(str(weapon_skin_id), language=language)
    assert weapon_skin is not None
    assert weapon_skin_id == weapon_skin.uuid

    with pytest.raises(NotFound):
        await client.fetch_skin('fake-weapon-skin-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_weapon_skin_chromas(client: Client, language: LanguageOption | None) -> None:
    weapon_skin_chromas = await client.fetch_skin_chromas(language=language)
    assert len(weapon_skin_chromas) > 0

    weapon_skin_chroma_id = weapon_skin_chromas[0].uuid
    weapon_skin_chroma = await client.fetch_skin_chroma(str(weapon_skin_chroma_id), language=language)
    assert weapon_skin_chroma is not None
    assert weapon_skin_chroma_id == weapon_skin_chroma.uuid

    with pytest.raises(NotFound):
        await client.fetch_skin_chroma('fake-weapon-skin-chroma-id')


@pytest.mark.anyio
@pytest.mark.parametrize(
    ('language'),
    [(Language.american_english), ('all'), (None)],
)
async def test_weapon_skin_levels(client: Client, language: LanguageOption | None) -> None:
    weapon_skin_levels = await client.fetch_skin_levels(language=language)
    assert len(weapon_skin_levels) > 0

    weapon_skin_level_id = weapon_skin_levels[0].uuid
    weapon_skin_level = await client.fetch_skin_level(str(weapon_skin_level_id), language=language)
    assert weapon_skin_level is not None
    assert weapon_skin_level_id == weapon_skin_level.uuid

    with pytest.raises(NotFound):
        await client.fetch_skin_level('fake-weapon-skin-level-id')


@pytest.mark.anyio
async def test_version(client: Client) -> None:
    version = await client.fetch_version()
    assert version is not None
