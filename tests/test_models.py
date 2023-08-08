import datetime

import pytest

from valorant import MISSING, AbilityType, Agent, Event, RelationType, RewardType, Season

from .conftest import BaseTest


class TestValorantAPI(BaseTest):
    @pytest.mark.asyncio
    async def test_fetch_assets(self) -> None:
        await self.client.init()

    @pytest.mark.asyncio
    async def test_agents(self) -> None:
        assert len(self.client.agents) > 0
        for agent in self.client.agents:
            # fagent = await self.client.fetch_agent(agent.uuid)
            fagent = self.client.get_agent(agent.uuid)
            assert fagent is not None
            assert fagent == agent

            assert agent.display_name is not None
            assert agent.description is not None
            assert agent.display_icon is not None
            assert agent.bust_portrait is not None
            assert agent.full_portrait is not None
            assert agent.full_portrait_v2 is not None
            assert agent.killfeed_portrait is not None
            assert agent.background is not None

            assert agent.role is not None
            assert agent.role.display_name is not None
            assert agent.role.description is not None
            assert agent.role.display_icon is not None

            assert agent.abilities is not None
            assert isinstance(agent.abilities, list)
            assert len(agent.abilities) >= 4 or len(agent.abilities) <= 5
            for ability in agent.abilities:
                assert ability is not None
                assert ability.slot is not None
                assert isinstance(ability.slot, AbilityType)
                assert ability.display_name is not None
                assert ability.description is not None
                if ability.display_icon:
                    assert ability.display_icon is not None

            assert agent.voice_line_localization is not None
            voice_line = agent.voice_line
            if voice_line is not None:
                assert agent.voice_line_localization.voice_locale == voice_line
                for voice in agent.voice_line_localization.all():
                    assert voice is not None
                    assert voice.min_duration is not None
                    assert voice.max_duration is not None
                    assert voice.media_list is not None
                    for media in voice.media_list:
                        assert media is not None
                        assert media.id is not None
                        assert media.wwise is not None
                        assert media.wave is not None

    @pytest.mark.asyncio
    async def test_buddies(self) -> None:
        assert len(self.client.buddies) > 0
        for buddy in self.client.buddies:
            assert buddy is not None
            # fbuddy = await self.client.fetch_buddy(buddy.uuid)
            fbuddy = self.client.get_buddy(buddy.uuid)
            assert fbuddy is not None
            assert fbuddy == buddy
            assert buddy is not None
            assert buddy.display_name is not None
            assert isinstance(buddy.is_hidden_if_not_owned(), bool)
            if buddy._theme_uuid is not None:
                assert buddy.theme is not None
            assert buddy.display_icon is not None
            assert buddy.asset_path is not None
            assert len(buddy.levels) > 0
            assert buddy.get_buddy_level(1) is not None

            for level in buddy.levels:
                assert level is not None
                assert level.parent is not None
                assert level.charm_level is not None
                assert level.display_name is not None
                assert level.display_icon is not None
                assert level.asset_path is not None

    @pytest.mark.asyncio
    async def test_bundles(self) -> None:
        assert len(self.client.bundles) > 0
        for bundle in self.client.bundles:
            # fbundle = await self.client.fetch_bundle(bundle.uuid)
            fbundle = self.client.get_bundle(bundle.uuid)
            assert fbundle is not None
            assert fbundle == bundle

            assert bundle is not None
            assert bundle.display_name is not None
            assert bundle.description is not None
            if bundle.display_name_sub_text:
                assert bundle.display_name_sub_text is not None
            if bundle.extra_description:
                assert bundle.extra_description is not None
            if bundle.promo_description:
                assert bundle.promo_description is not None
            assert isinstance(bundle.use_additional_context, bool)
            assert bundle.display_icon is not None
            assert bundle.display_icon_2 is not None
            if bundle.vertical_promo_image:
                assert bundle.vertical_promo_image is not None
            assert bundle.asset_path is not None

    @pytest.mark.asyncio
    async def test_ceremonies(self) -> None:
        assert len(self.client.ceremonies) > 0
        for ceremony in self.client.ceremonies:
            assert ceremony is not None
            assert ceremony.display_name is not None
            assert ceremony.asset_path is not None

    @pytest.mark.asyncio
    async def test_competitive_tiers(self) -> None:
        assert len(self.client.competitive_tiers) > 0
        for c_tier in self.client.competitive_tiers:
            assert c_tier is not None
            assert c_tier.asset_path is not None
            assert len(c_tier.tiers) > 0
            for tier in c_tier.tiers:
                assert tier is not None
                assert tier.tier is not None
                assert tier.name is not None
                assert tier.division is not None
                assert tier.division_name is not None
                assert tier.color is not None
                assert tier.background_color is not None
                if tier.small_icon:
                    assert tier.small_icon is not None
                if tier.large_icon:
                    assert tier.large_icon is not None
                if tier.rank_triangle_down_icon:
                    assert tier.rank_triangle_down_icon is not None
                if tier.rank_triangle_up_icon:
                    assert tier.rank_triangle_up_icon is not None

    @pytest.mark.asyncio
    async def test_content_tiers(self) -> None:
        assert len(self.client.content_tiers) > 0
        for content_tier in self.client.content_tiers:
            assert content_tier is not None
            assert content_tier.display_name is not None
            assert content_tier.dev_name is not None
            assert content_tier.rank is not None
            assert content_tier.juice_value is not None
            assert content_tier.juice_cost is not None
            assert content_tier.highlight_color is not None
            assert content_tier.display_icon is not None
            assert content_tier.asset_path is not None

    @pytest.mark.asyncio
    async def test_contracts(self) -> None:
        assert len(self.client.contracts) > 0
        for contract in self.client.contracts:
            assert contract is not None
            assert contract.display_name is not None
            if contract.display_icon:
                assert contract.display_icon is not None
            assert isinstance(contract.ship_it, bool)
            assert contract.free_reward_schedule_uuid is not None
            assert contract.asset_path is not None
            content = contract.content
            assert content is not None
            assert isinstance(content.relation_type, RelationType)
            assert content.premium_vp_cost is not None
            # assert content.premium_reward_schedule_uuid is not None
            if content._relation_uuid is None:
                assert content.relationship is None
            if content.relationship is not None:
                assert isinstance(content.relationship, (Agent, Event, Season))
            assert len(content.chapters) > 0
            for chapter in content.chapters:
                assert chapter is not None
                assert isinstance(chapter.is_epilogue(), bool)
                assert len(chapter.levels) > 0
                for level in chapter.levels:
                    assert level is not None
                    assert level.reward is not None
                    reward = level.reward
                    assert reward.type is not None
                    assert isinstance(reward.type, RewardType)
                    assert reward.amount is not None
                    assert isinstance(reward.amount, int)
                    item = reward.get_item()
                    assert item is not None  # if item is None, maybe game is updated new reward type
                    assert isinstance(level.xp, int)
                    assert isinstance(level.vp_cost, int)
                    assert isinstance(level.dough_cost, int)
                    assert isinstance(level.is_purchasable_with_vp(), bool)
                    assert isinstance(level.is_purchasable_with_dough(), bool)

                if chapter.free_rewards is not None:
                    assert len(chapter.free_rewards) > 0
                    for reward in chapter.free_rewards:
                        assert reward is not None
                        assert reward.type is not None
                        assert isinstance(reward.type, RewardType)
                        assert reward.amount is not None
                        assert isinstance(reward.amount, int)
                        item_free = reward.get_item()
                        assert item_free is not None  # if item is None, maybe game is updated new reward type

    @pytest.mark.asyncio
    async def test_currencies(self) -> None:
        assert len(self.client.currencies) > 0
        for currency in self.client.currencies:
            assert currency is not None
            assert currency.display_name is not None
            assert currency.display_name_singular is not None
            assert currency.display_icon is not None
            assert currency.large_icon is not None
            assert currency.asset_path is not None

    @pytest.mark.asyncio
    async def test_events(self) -> None:
        assert len(self.client.events) > 0
        for event in self.client.events:
            assert event is not None
            assert event.display_name is not None
            assert event.short_display_name is not None
            assert event.start_time is not None
            assert isinstance(event.start_time, datetime.datetime)
            assert event.end_time is not None
            assert isinstance(event.end_time, datetime.datetime)
            assert event.asset_path is not None

    @pytest.mark.asyncio
    async def test_gamemodes(self) -> None:
        assert len(self.client.game_modes) > 0
        for gm in self.client.game_modes:
            assert gm is not None
            assert gm.display_name is not None
            assert isinstance(gm.allows_match_timeouts, bool)
            assert isinstance(gm.is_team_voice_allowed(), bool)
            assert isinstance(gm.is_minimap_hidden(), bool)
            assert gm.orb_count is not None
            assert isinstance(gm.orb_count, int)
            assert gm.rounds_per_half is not None
            assert isinstance(gm.rounds_per_half, int)
            team_roles = gm.team_roles
            if team_roles is not None:
                assert isinstance(team_roles, list)
                assert len(team_roles) > 0
                for tr in team_roles:
                    assert tr is not None
                    assert isinstance(tr, str)
            feature_overrides = gm.game_feature_overrides
            if feature_overrides is not None:
                assert len(feature_overrides) > 0
                for fo in feature_overrides:
                    assert fo is not None
                    assert fo.feature_name is not None
                    assert isinstance(fo.state, bool)
            game_rule_bool_overrides = gm.game_rule_bool_overrides
            if game_rule_bool_overrides is not None:
                assert len(game_rule_bool_overrides) > 0
                for gro in game_rule_bool_overrides:
                    assert gro is not None
                    assert gro.rule_name is not None
                    assert isinstance(gro.state, bool)
            if gm.display_icon:
                assert gm.display_icon is not None
            assert gm.asset_path is not None

    @pytest.mark.asyncio
    async def test_gamemode_equippables(self) -> None:
        assert len(self.client.game_mode_equippables) > 0
        for gme in self.client.game_mode_equippables:
            assert gme is not None
            assert gme.display_name is not None
            assert gme.display_icon is not None
            assert gme.kill_stream_icon is not None
            assert gme.asset_path is not None
            # weapon = gme.get_weapon()

    @pytest.mark.asyncio
    async def test_gear(self) -> None:
        assert len(self.client.gear) > 0
        for gear in self.client.gear:
            assert gear is not None
            assert gear.display_name is not None
            assert gear.display_icon is not None
            shop_data = gear.shop_data
            assert shop_data is not None
            assert shop_data.cost is not None
            assert shop_data.category is not None
            assert shop_data.category_text is not None
            grid_position = shop_data.grid_position
            if grid_position is not None:
                assert grid_position.row is not None
                assert grid_position.column is not None
            assert shop_data.can_be_trashed is not None
            assert isinstance(shop_data.can_be_trashed, bool)
            if shop_data.new_image:
                assert shop_data.new_image is not None
            assert shop_data.new_image is not None
            if shop_data.new_image_2:
                assert shop_data.new_image_2 is not None
            assert shop_data.asset_path is not None
            assert gear.asset_path is not None

    @pytest.mark.asyncio
    async def test_level_borders(self) -> None:
        assert len(self.client.level_borders) > 0
        for border in self.client.level_borders:
            assert border is not None
            assert border.starting_level is not None
            assert border.level_number_appearance is not None
            assert border.small_player_card_appearance is not None
            assert border.asset_path is not None

    @pytest.mark.asyncio
    async def test_maps(self) -> None:
        assert len(self.client.maps) > 0
        for mp in self.client.maps:
            assert mp is not None
            assert mp.display_name is not None
            assert mp.coordinates is not None
            assert mp.display_name is not None
            assert mp.list_view_icon is not None
            assert mp.asset_path is not None
            assert mp.url is not None
            assert mp.x_multiplier is not None
            assert mp.y_multiplier is not None
            assert mp.x_scalar_to_add is not None
            assert mp.y_scalar_to_add is not None
            callouts = mp.callouts
            if callouts is not None:
                for callout in callouts:
                    assert callout.region_name is not None
                    assert callout.super_region_name is not None
                    assert callout.location is not None
                    assert callout.location.x is not None
                    assert callout.location.y is not None

    @pytest.mark.asyncio
    async def test_missions(self) -> None:
        assert len(self.client.missions) > 0
        for mission in self.client.missions:
            assert mission is not None
            if mission.display_name:
                assert mission.display_name is not None
            if mission.title:
                assert mission.title is not None
            if mission.type:
                assert mission.type is not None
            assert mission.xp_grant is not None
            assert mission.progress_to_complete is not None
            assert mission.activation_date is not None
            assert mission.expiration_date is not None
            if mission.tags is not None:
                assert len(mission.tags) > 0
            if mission.objectives:
                assert len(mission.objectives) > 0
                for objective in mission.objectives:
                    assert objective is not None
                    assert objective.value is not None
                    assert isinstance(objective.value, int)
            assert mission.asset_path is not None

    @pytest.mark.asyncio
    async def test_player_cards(self) -> None:
        assert len(self.client.player_cards) > 0
        for card in self.client.player_cards:
            assert card is not None
            assert card.display_name is not None
            assert card.display_icon is not None
            assert card.asset_path is not None
            assert isinstance(card.is_hidden_if_not_owned(), bool)
            assert card.small_art is not None
            assert card.wide_art is not None
            assert card.large_art is not None
            if card._theme_uuid is not None:
                assert card.theme is not None

    @pytest.mark.asyncio
    async def test_player_titles(self) -> None:
        assert len(self.client.player_titles) > 0
        for title in self.client.player_titles:
            assert title is not None
            assert title.display_name is not None
            assert title.text is not None
            assert isinstance(title.is_hidden_if_not_owned(), bool)
            assert title.asset_path is not None

    @pytest.mark.asyncio
    async def test_seasons(self) -> None:
        assert len(self.client.seasons) > 0
        for season in self.client.seasons:
            assert season is not None
            assert season.display_name is not None
            if season.type is not None:
                assert season.type.lower() == 'act'
            assert season.start_time is not None
            assert season.end_time is not None
            if season._parent_uuid is not None:
                assert season.parent is not None
            assert season.asset_path is not None

    @pytest.mark.asyncio
    async def test_competitive_seasons(self) -> None:
        assert len(self.client.competitive_seasons) > 0
        for cs in self.client.competitive_seasons:
            assert cs is not None
            assert cs.start_time is not None
            assert cs.end_time is not None
            assert cs.season_uuid is not None
            assert cs.competitive_tiers_uuid is not None
            if cs.borders is not None:
                for border in cs.borders:
                    assert border is not None
                    assert border.level is not None
                    assert isinstance(border.level, int)
                    assert border.wins_required is not None
                    assert isinstance(border.wins_required, int)
                    assert border.display_icon is not None
                    if border.small_icon:
                        assert border.small_icon is not None
                    assert border.asset_path is not None
            assert cs.asset_path is not None

    @pytest.mark.asyncio
    async def test_sprays(self) -> None:
        assert len(self.client.sprays) > 0
        for spray in self.client.sprays:
            assert spray is not None
            assert spray.display_name is not None
            if spray.category:
                assert spray.category is not None
            if spray._theme_uuid is not None:
                assert spray.theme is not None
            assert isinstance(spray.is_null_spray(), bool)
            assert spray.display_icon is not None
            if spray.full_icon:
                assert spray.full_icon is not None
            if spray.full_transparent_icon:
                assert spray.full_transparent_icon is not None
            if spray.animation_png:
                assert spray.animation_png is not None
            if spray.animation_gif:
                # TODO: Asset support gif
                assert spray.animation_gif is not None
            assert spray.asset_path is not None
            for level in spray.levels:
                assert level is not None
                assert level.parent is not None
                assert level.spray_level is not None
                assert level.display_name is not None
                assert level.asset_path is not None
                if level.display_icon:
                    assert level.display_icon is not None

    @pytest.mark.asyncio
    async def test_themes(self) -> None:
        assert len(self.client.themes) > 0
        for theme in self.client.themes:
            assert theme is not None
            assert theme.display_name is not None
            if theme.display_icon:
                assert theme.display_icon is not None
            if theme.store_featured_image:
                assert theme.store_featured_image is not None
            assert theme.asset_path is not None

    @pytest.mark.asyncio
    async def test_version(self) -> None:
        version = self.client.version
        assert version.manifest_id is not None
        assert version.branch is not None
        assert version.version is not None
        assert version.build_version is not None
        assert version.engine_version is not None
        assert version.riot_client_version is not None
        assert version.riot_client_build is not None
        assert version.build_date is not None

    @pytest.mark.asyncio
    async def test_weapons(self) -> None:
        assert len(self.client.weapons) > 0
        for weapon in self.client.weapons:
            assert weapon is not None
            assert weapon.display_name is not None
            assert weapon._default_skin_uuid is not None
            assert weapon.display_icon is not None
            assert weapon.kill_stream_icon is not None
            assert weapon.asset_path is not None
            stats = weapon.weapon_stats
            if stats:
                assert stats is not None
                assert stats.fire_rate is not None
                assert stats.magazine_size is not None
                assert stats.run_speed_multiplier is not None
                assert stats.equip_time_seconds is not None
                assert stats.reload_time_seconds is not None
                assert stats.first_bullet_accuracy is not None
                assert stats.wall_penetration is not None
                if stats.feature is not None:
                    assert stats.feature is not None
                if stats.fire_mode is not None:
                    assert stats.fire_mode is not None
                if stats.alt_fire_type is not None:
                    assert stats.alt_fire_type is not None

                # TODO: test all attributes of weapon stats
            if weapon.shop_data:
                assert weapon.shop_data is not None
                # TODO: test all attributes of shop data
            for skin in weapon.skins:
                assert skin is not None
                if skin._theme_uuid is not None:
                    assert skin.theme is not None
                for chroma in skin.chromas:
                    assert chroma is not None
                    assert chroma.parent is not None
                    assert chroma.display_name is not None
                    if chroma.display_icon:
                        assert chroma.display_icon is not None
                    assert chroma.full_render is not None
                    if chroma.swatch:
                        assert chroma.swatch is not None
                    if chroma.streamed_video:
                        assert chroma.streamed_video is not None
                    assert chroma.asset_path is not None

                    # helper method
                    if chroma.display_icon_fix:
                        if skin.theme is not None:
                            assert chroma.theme is not None
                        assert chroma.display_icon_fix is not None

                for index, level in enumerate(skin.levels):
                    assert level is not None
                    assert level.parent is not None
                    assert level.display_name is not None
                    assert level.level_item is not None
                    if level.display_icon:
                        assert level.display_icon is not None
                    if level.streamed_video:
                        assert level.streamed_video is not None
                    assert level.asset_path is not None

                    # helper method
                    assert level.display_icon_fix is not None
                    if skin.theme is not None:
                        assert level.theme is not None
                    assert level.level_number is not None
                    assert isinstance(level.is_level_one(), bool)
                    if index == 0:
                        assert level.is_level_one() is True

    def test_clear(self) -> None:
        self.client.clear()
        assert self.client.version is MISSING
        for key in self.client.cache.__dict__.keys():
            if key.startswith('_') and isinstance(self.client.cache.__dict__[key], dict):
                assert len(self.client.cache.__dict__[key]) == 0

    @pytest.mark.asyncio
    async def test_close(self) -> None:
        await self.client.close()
