from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from valorant.errors import NotFound

if TYPE_CHECKING:
    from valorant import Client


@pytest.mark.anyio
async def test_agents(client: Client) -> None:
    agents = await client.fetch_agents()
    assert len(agents) > 0

    agent_id = agents[0].uuid
    agent = await client.fetch_agent(str(agent_id))
    assert agent is not None
    assert agent_id == agent.uuid

    with pytest.raises(NotFound):
        await client.fetch_agent('fake-agent-id')


@pytest.mark.anyio
async def test_buddies(client: Client) -> None:
    buddies = await client.fetch_buddies()
    assert len(buddies) > 0

    buddy_id = buddies[0].uuid
    buddy = await client.fetch_buddy(str(buddy_id))
    assert buddy is not None
    assert buddy_id == buddy.uuid

    with pytest.raises(NotFound):
        await client.fetch_buddy('fake-buddy-id')


@pytest.mark.anyio
async def test_buddy_levels(client: Client) -> None:
    buddy_levels = await client.fetch_buddy_levels()
    assert len(buddy_levels) > 0

    buddy_level_id = buddy_levels[0].uuid
    buddy_level = await client.fetch_buddy_level(str(buddy_level_id))
    assert buddy_level is not None
    assert buddy_level_id == buddy_level.uuid

    with pytest.raises(NotFound):
        await client.fetch_buddy_level('fake-buddy-level-id')


@pytest.mark.anyio
async def test_bundles(client: Client) -> None:
    bundles = await client.fetch_bundles()
    assert len(bundles) > 0

    bundle_id = bundles[0].uuid
    bundle = await client.fetch_bundle(str(bundle_id))
    assert bundle is not None
    assert bundle_id == bundle.uuid

    with pytest.raises(NotFound):
        await client.fetch_bundle('fake-bundle-id')


@pytest.mark.anyio
async def test_ceremonies(client: Client) -> None:
    ceremonies = await client.fetch_ceremonies()
    assert len(ceremonies) > 0

    ceremony_id = ceremonies[0].uuid
    ceremony = await client.fetch_ceremony(str(ceremony_id))
    assert ceremony is not None
    assert ceremony_id == ceremony.uuid

    with pytest.raises(NotFound):
        await client.fetch_ceremony('fake-ceremony-id')


@pytest.mark.anyio
async def test_competitive_tiers(client: Client) -> None:
    competitive_tiers = await client.fetch_competitive_tiers()
    assert len(competitive_tiers) > 0

    competitive_tier_id = competitive_tiers[0].uuid
    competitive_tier = await client.fetch_competitive_tier(str(competitive_tier_id))
    assert competitive_tier is not None
    assert competitive_tier_id == competitive_tier.uuid

    with pytest.raises(NotFound):
        await client.fetch_competitive_tier('fake-competitive-tier-id')


@pytest.mark.anyio
async def test_content_tiers(client: Client) -> None:
    content_tiers = await client.fetch_content_tiers()
    assert len(content_tiers) > 0

    content_tier_id = content_tiers[0].uuid
    content_tier = await client.fetch_content_tier(str(content_tier_id))
    assert content_tier is not None
    assert content_tier_id == content_tier.uuid

    with pytest.raises(NotFound):
        await client.fetch_content_tier('fake-content-tier-id')


@pytest.mark.anyio
async def test_contracts(client: Client) -> None:
    contracts = await client.fetch_contracts()
    assert len(contracts) > 0

    contract_id = contracts[0].uuid
    contract = await client.fetch_contract(str(contract_id))
    assert contract is not None
    assert contract_id == contract.uuid

    with pytest.raises(NotFound):
        await client.fetch_contract('fake-contract-id')


@pytest.mark.anyio
async def test_currencies(client: Client) -> None:
    currencies = await client.fetch_currencies()
    assert len(currencies) > 0

    currency_id = currencies[0].uuid
    currency = await client.fetch_currency(str(currency_id))
    assert currency is not None
    assert currency_id == currency.uuid

    with pytest.raises(NotFound):
        await client.fetch_currency('fake-currency-id')


@pytest.mark.anyio
async def test_events(client: Client) -> None:
    events = await client.fetch_events()
    assert len(events) > 0

    event_id = events[0].uuid
    event = await client.fetch_event(str(event_id))
    assert event is not None
    assert event_id == event.uuid

    with pytest.raises(NotFound):
        await client.fetch_event('fake-event-id')


@pytest.mark.anyio
async def test_game_modes(client: Client) -> None:
    game_modes = await client.fetch_game_modes()
    assert len(game_modes) > 0

    game_mode_id = game_modes[0].uuid
    game_mode = await client.fetch_game_mode(str(game_mode_id))
    assert game_mode is not None
    assert game_mode_id == game_mode.uuid

    with pytest.raises(NotFound):
        await client.fetch_game_mode('fake-game-mode-id')


@pytest.mark.anyio
async def test_game_mode_equippables(client: Client) -> None:
    game_mode_equippables = await client.fetch_game_mode_equippables()
    assert len(game_mode_equippables) > 0

    game_mode_equippable_id = game_mode_equippables[0].uuid
    game_mode_equippable = await client.fetch_game_mode_equippable(str(game_mode_equippable_id))
    assert game_mode_equippable is not None
    assert game_mode_equippable_id == game_mode_equippable.uuid

    with pytest.raises(NotFound):
        await client.fetch_game_mode_equippable('fake-game-mode-equippable-id')


@pytest.mark.anyio
async def test_gears(client: Client) -> None:
    gears = await client.fetch_gears()
    assert len(gears) > 0

    gear_id = gears[0].uuid
    gear = await client.fetch_gear(str(gear_id))
    assert gear is not None
    assert gear_id == gear.uuid

    with pytest.raises(NotFound):
        await client.fetch_gear('fake-gear-id')


@pytest.mark.anyio
async def test_level_borders(client: Client) -> None:
    level_borders = await client.fetch_level_borders()
    assert len(level_borders) > 0

    level_border_id = level_borders[0].uuid
    level_border = await client.fetch_level_border(str(level_border_id))
    assert level_border is not None
    assert level_border_id == level_border.uuid

    with pytest.raises(NotFound):
        await client.fetch_level_border('fake-level-border-id')


@pytest.mark.anyio
async def test_maps(client: Client) -> None:
    maps = await client.fetch_maps()
    assert len(maps) > 0

    map_id = maps[0].uuid
    map_ = await client.fetch_map(str(map_id))
    assert map_ is not None
    assert map_id == map_.uuid

    with pytest.raises(NotFound):
        await client.fetch_map('fake-map-id')


@pytest.mark.anyio
async def test_missions(client: Client) -> None:
    missions = await client.fetch_missions()
    assert len(missions) > 0

    mission_id = missions[0].uuid
    mission = await client.fetch_mission(str(mission_id))
    assert mission is not None
    assert mission_id == mission.uuid

    with pytest.raises(NotFound):
        await client.fetch_mission('fake-mission-id')


@pytest.mark.anyio
async def test_player_cards(client: Client) -> None:
    player_cards = await client.fetch_player_cards()
    assert len(player_cards) > 0

    player_card_id = player_cards[0].uuid
    player_card = await client.fetch_player_card(str(player_card_id))
    assert player_card is not None
    assert player_card_id == player_card.uuid

    with pytest.raises(NotFound):
        await client.fetch_player_card('fake-player-card-id')


@pytest.mark.anyio
async def test_player_titles(client: Client) -> None:
    player_titles = await client.fetch_player_titles()
    assert len(player_titles) > 0

    player_title_id = player_titles[0].uuid
    player_title = await client.fetch_player_title(str(player_title_id))
    assert player_title is not None
    assert player_title_id == player_title.uuid

    with pytest.raises(NotFound):
        await client.fetch_player_title('fake-player-title-id')


@pytest.mark.anyio
async def test_seasons(client: Client) -> None:
    seasons = await client.fetch_seasons()
    assert len(seasons) > 0

    season_id = seasons[0].uuid
    season = await client.fetch_season(str(season_id))
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
async def test_sprays(client: Client) -> None:
    sprays = await client.fetch_sprays()
    assert len(sprays) > 0

    spray_id = sprays[0].uuid
    spray = await client.fetch_spray(str(spray_id))
    assert spray is not None
    assert spray_id == spray.uuid

    with pytest.raises(NotFound):
        await client.fetch_spray('fake-spray-id')


@pytest.mark.anyio
async def test_spray_levels(client: Client) -> None:
    spray_levels = await client.fetch_spray_levels()
    assert len(spray_levels) > 0

    spray_level_id = spray_levels[0].uuid
    spray_level = await client.fetch_spray_level(str(spray_level_id))
    assert spray_level is not None
    assert spray_level_id == spray_level.uuid

    with pytest.raises(NotFound):
        await client.fetch_spray_level('fake-spray-level-id')


@pytest.mark.anyio
async def test_themes(client: Client) -> None:
    themes = await client.fetch_themes()
    assert len(themes) > 0

    theme_id = themes[0].uuid
    theme = await client.fetch_theme(str(theme_id))
    assert theme is not None
    assert theme_id == theme.uuid

    with pytest.raises(NotFound):
        await client.fetch_theme('fake-theme-id')


@pytest.mark.anyio
async def test_weapons(client: Client) -> None:
    weapons = await client.fetch_weapons()
    assert len(weapons) > 0

    weapon_id = weapons[0].uuid
    weapon = await client.fetch_weapon(str(weapon_id))
    assert weapon is not None
    assert weapon_id == weapon.uuid

    with pytest.raises(NotFound):
        await client.fetch_weapon('fake-weapon-id')


@pytest.mark.anyio
async def test_weapon_skins(client: Client) -> None:
    weapon_skins = await client.fetch_skins()
    assert len(weapon_skins) > 0

    weapon_skin_id = weapon_skins[0].uuid
    weapon_skin = await client.fetch_skin(str(weapon_skin_id))
    assert weapon_skin is not None
    assert weapon_skin_id == weapon_skin.uuid

    with pytest.raises(NotFound):
        await client.fetch_skin('fake-weapon-skin-id')


@pytest.mark.anyio
async def test_weapon_skin_chromas(client: Client) -> None:
    weapon_skin_chromas = await client.fetch_skin_chromas()
    assert len(weapon_skin_chromas) > 0

    weapon_skin_chroma_id = weapon_skin_chromas[0].uuid
    weapon_skin_chroma = await client.fetch_skin_chroma(str(weapon_skin_chroma_id))
    assert weapon_skin_chroma is not None
    assert weapon_skin_chroma_id == weapon_skin_chroma.uuid

    with pytest.raises(NotFound):
        await client.fetch_skin_chroma('fake-weapon-skin-chroma-id')


@pytest.mark.anyio
async def test_weapon_skin_levels(client: Client) -> None:
    weapon_skin_levels = await client.fetch_skin_levels()
    assert len(weapon_skin_levels) > 0

    weapon_skin_level_id = weapon_skin_levels[0].uuid
    weapon_skin_level = await client.fetch_skin_level(str(weapon_skin_level_id))
    assert weapon_skin_level is not None
    assert weapon_skin_level_id == weapon_skin_level.uuid

    with pytest.raises(NotFound):
        await client.fetch_skin_level('fake-weapon-skin-level-id')


@pytest.mark.anyio
async def test_version(client: Client) -> None:
    version = await client.fetch_version()
    assert version is not None
