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

import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum

else:
    from enum import Enum

    class StrEnum(str, Enum): ...


__all__ = (
    'AbilitySlot',
    'DivisionTier',
    'GameFeature',
    'GameRule',
    'Language',
    'MissionTag',
    'MissionType',
    'RelationType',
    'RewardType',
    'SeasonType',
    'ShopCategory',
    'WeaponCategory',
)


class AbilitySlot(StrEnum):
    passive = 'Passive'
    grenade = 'Grenade'
    ability_1 = 'Ability1'
    ability_2 = 'Ability2'
    ultimate = 'Ultimate'


class DivisionTier(StrEnum):
    unranked = 'ECompetitiveDivision::UNRANKED'
    invalid = 'ECompetitiveDivision::INVALID'
    iron = 'ECompetitiveDivision::IRON'
    bronze = 'ECompetitiveDivision::BRONZE'
    silver = 'ECompetitiveDivision::SILVER'
    gold = 'ECompetitiveDivision::GOLD'
    platinum = 'ECompetitiveDivision::PLATINUM'
    diamond = 'ECompetitiveDivision::DIAMOND'
    ascendant = 'ECompetitiveDivision::ASCENDANT'
    immortal = 'ECompetitiveDivision::IMMORTAL'
    radiant = 'ECompetitiveDivision::RADIANT'


class GameFeature(StrEnum):
    allow_shopping_while_dead = 'EGameFeatureToggleName::AllowShoppingWhileDead'
    deathmatch_encourage_far_spawning = 'EGameFeatureToggleName::DeathmatchEncourageFarSpawning'
    disable_fog_of_war = 'EGameFeatureToggleName::DisableFogOfWar'
    equippable_cache_recycling = 'EGameFeatureToggleName::EquippableCacheRecycling'
    # reuse_actor_on_respawn = 'EGameFeatureToggleName::ReuseActorOnRespawn'
    remove_deleted_fx_cs_from_pool = 'EGameFeatureToggleName::RemoveDeletedFXCsFromPool'
    use_mesh_material_manager_alt = 'EGameFeatureToggleName::UseMeshMaterialManagerAlt'
    use_server_authoritative_drop_out = 'EGameFeatureToggleName::UseServerAuthoritativeDropOut'


class GameRule(StrEnum):
    accolades_enabled = 'EGameRuleBoolName::AccoladesEnabled'
    allow_drop_out = 'EGameRuleBoolName::AllowDropOut'
    assign_random_agents = 'EGameRuleBoolName::AssignRandomAgents'
    combat_report_only_show_last_life = 'EGameRuleBoolName::CombatReportOnlyShowLastLife'
    context_aware_module_enabled = 'EGameRuleBoolName::ContextAwareModuleEnabled'
    destroy_abilities_on_death = 'EGameRuleBoolName::DestroyAbilitiesOnDeath'
    disable_shop_selling = 'EGameRuleBoolName::DisableShopSelling'
    downed_characters_can_give_up = 'EGameRuleBoolName::DownedCharactersCanGiveUp'
    fill_with_bots = 'EGameRuleBoolName::FillWithBots'
    is_overtime_win_by_two = 'EGameRuleBoolName::IsOvertimeWinByTwo'
    majority_vote_agents = 'EGameRuleBoolName::MajorityVoteAgents'
    pip_ability_casting = 'EGameRuleBoolName::PipAbilityCasting'
    prevent_ability_recharge = 'EGameRuleBoolName::PreventAbilityRecharge'
    skip_pregame = 'EGameRuleBoolName::SkipPregame'
    use_all_ability_cooldowns = 'EGameRuleBoolName::UseAllAbilityCooldowns'
    use_in_dev_weapons = 'EGameRuleBoolName::UseInDevWeapons'


class MissionType(StrEnum):
    daily = 'EAresMissionType::Daily'
    weekly = 'EAresMissionType::Weekly'
    tutorial = 'EAresMissionType::Tutorial'
    npe = 'EAresMissionType::NPE'
    bte = 'EAresMissionType::BTE'


class MissionTag(StrEnum):
    econ = 'EAresMissionTag::Econ'
    combat = 'EAresMissionTag::Combat'


class RelationType(StrEnum):
    agent = 'Agent'
    event = 'Event'
    season = 'Season'


class RewardType(StrEnum):
    currency = 'Currency'
    equippable_charm_level = 'EquippableCharmLevel'  # buddy level
    equippable_skin_level = 'EquippableSkinLevel'  # skin level
    player_card = 'PlayerCard'
    player_title = 'Title'
    spray = 'Spray'
    totem = 'Totem'  # flex


class SeasonType(StrEnum):
    act = 'EAresSeasonType::Act'


class ShopCategory(StrEnum):
    armor = 'Armor'
    pistols = 'Pistols'
    smgs = 'SMGs'
    shotguns = 'Shotguns'
    heavy_weapons = 'Heavy Weapons'
    rifles = 'Rifles'
    sniper_rifles = 'Sniper Rifles'


class WeaponCategory(StrEnum):
    melee = 'EEquippableCategory::Melee'
    sidearm = 'EEquippableCategory::Sidearm'
    smg = 'EEquippableCategory::SMG'
    shotgun = 'EEquippableCategory::Shotgun'
    heavy = 'EEquippableCategory::Heavy'
    rifle = 'EEquippableCategory::Rifle'
    sniper = 'EEquippableCategory::Sniper'


class Language(StrEnum):
    arabic = 'ar-AE'
    german = 'de-DE'
    american_english = 'en-US'
    spain_spanish = 'es-ES'
    spanish_mexican = 'es-MX'
    french = 'fr-FR'
    indonesian = 'id-ID'
    italian = 'it-IT'
    japanese = 'ja-JP'
    korean = 'ko-KR'
    polish = 'pl-PL'
    brazil_portuguese = 'pt-BR'
    russian = 'ru-RU'
    thai = 'th-TH'
    turkish = 'tr-TR'
    vietnamese = 'vi-VN'
    chinese = 'zh-CN'
    taiwan_chinese = 'zh-TW'
