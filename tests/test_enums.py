from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from valorant.enums import (
    AbilitySlot,
    DivisionTier,
    GameFeature,
    GameRule,
    MissionTag,
    MissionType,
    RelationType,
    RewardType,
    SeasonType,
    ShopCategory,
    WeaponCategory,
)

if TYPE_CHECKING:
    from valorant import Client


@pytest.mark.anyio
async def test_ability_slot(client: Client) -> None:
    agents = await client.fetch_agents()
    # fmt: off
    used_ability_slots = {
        ability.slot
        for agent in agents
        for ability in agent.abilities
    }
    # fmt: on
    all_ability_slots = set(AbilitySlot)
    assert used_ability_slots == all_ability_slots


@pytest.mark.anyio
async def test_division_tier(client: Client) -> None:
    competitive_tiers = await client.fetch_competitive_tiers()
    # fmt: off
    used_division_tiers = {
        division.division
        for competitive_tier in competitive_tiers
        for division in competitive_tier.tiers
    }
    # fmt: on
    all_division_tiers = set(DivisionTier)
    assert used_division_tiers == all_division_tiers


@pytest.mark.anyio
async def test_game_feature(client: Client) -> None:
    game_modes = await client.fetch_game_modes()
    # fmt: off
    used_game_features = {
        feature.feature_name
        for game_mode in game_modes if game_mode.game_feature_overrides is not None
        for feature in game_mode.game_feature_overrides
    }
    # fmt: on
    all_game_features = set(GameFeature)
    assert used_game_features == all_game_features


@pytest.mark.anyio
async def test_game_rule(client: Client) -> None:
    game_modes = await client.fetch_game_modes()
    # fmt: off
    used_game_rules = {
        rule.rule_name
        for game_mode in game_modes if game_mode.game_rule_bool_overrides is not None
        for rule in game_mode.game_rule_bool_overrides
    }
    # fmt: on
    all_game_rules = set(GameRule)
    assert used_game_rules == all_game_rules


@pytest.mark.anyio
async def test_mission_type(client: Client) -> None:
    missions = await client.fetch_missions()
    used_mission_types = {mission.type for mission in missions if mission.type is not None}
    all_mission_types = set(MissionType)
    assert used_mission_types == all_mission_types


@pytest.mark.anyio
async def test_mission_tag(client: Client) -> None:
    missions = await client.fetch_missions()
    # fmt: off
    used_mission_tags = {
        tag
        for mission in missions if mission.tags is not None
        for tag in mission.tags
    }
    # fmt: on
    all_mission_tags = set(MissionTag)
    assert used_mission_tags == all_mission_tags


@pytest.mark.anyio
async def test_relation_type(client: Client) -> None:
    contracts = await client.fetch_contracts()
    # fmt: off
    used_relation_types = {
        contract.content.relation_type
        for contract in contracts if contract.content.relation_type is not None
    }
    # fmt: on
    all_relation_types = set(RelationType)
    assert used_relation_types == all_relation_types


@pytest.mark.anyio
async def test_reward_type(client: Client) -> None:
    contracts = await client.fetch_contracts()
    # fmt: off
    used_reward_types = {
        level.reward.type
        for contract in contracts
        for chapter in contract.content.chapters
        for level in chapter.levels
    }
    # fmt: on
    all_reward_types = set(RewardType)
    assert used_reward_types == all_reward_types


@pytest.mark.anyio
async def test_season_type(client: Client) -> None:
    seasons = await client.fetch_seasons()
    used_season_types = {season.type for season in seasons if season.type is not None}
    all_season_types = set(SeasonType)
    assert used_season_types == all_season_types


@pytest.mark.anyio
async def test_shop_category(client: Client) -> None:
    gears = await client.fetch_gears()
    weapons = await client.fetch_weapons()

    gear_used_shop_categories = {gear.shop_data.category for gear in gears}
    weapon_used_shop_categories = {weapon.shop_data.category for weapon in weapons if weapon.shop_data is not None}
    used_shop_categories = gear_used_shop_categories | weapon_used_shop_categories

    all_shop_categories = set(ShopCategory)
    assert used_shop_categories == all_shop_categories


@pytest.mark.anyio
async def test_weapon_category(client: Client) -> None:
    weapons = await client.fetch_weapons()
    used_categories = {weapon.category for weapon in weapons}
    all_categories = set(WeaponCategory)
    assert used_categories == all_categories
