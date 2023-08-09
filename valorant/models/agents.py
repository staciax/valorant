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

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from ..asset import Asset
from ..enums import AbilityType, Locale, try_enum
from ..localization import Localization
from .abc import BaseModel

if TYPE_CHECKING:
    from ..cache import CacheState
    from ..types.agents import (
        Ability as AbilityPayload,
        Agent as AgentPayload,
        Media as MediaPayload,
        Role as RolePayload,
        VoiceLine as VoiceLinePayload,
    )

# fmt: off
__all__ = (
    'Ability',
    'Agent',
    'Media',
    'Role',
    'VoiceLine',
    'VoiceLineLocalization',
)
# fmt: on


class Role(BaseModel):
    def __init__(self, state: CacheState, data: RolePayload) -> None:
        super().__init__(data['uuid'])
        self._state = state
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self._description: Union[str, Dict[str, str]] = data['description']
        self._display_icon: str = data['displayIcon']
        self.asset_path: str = data['assetPath']
        self._display_name_localized: Localization = Localization(self._description, locale=self._state.locale)
        self._description_localized: Localization = Localization(self._display_name, locale=self._state.locale)

    def __repr__(self) -> str:
        return f'<Role display_name={self.display_name!r}>'

    def __str__(self) -> str:
        return self.display_name.locale

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    def description_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._description_localized.from_locale(locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the agent role's name."""
        return self._display_name_localized

    @property
    def description(self) -> Localization:
        """:class: `str` Returns the agent role's description."""
        return self._description_localized

    @property
    def display_icon(self) -> Asset:
        """:class: `Asset` Returns the agent role's display icon."""
        return Asset._from_url(state=self._state, url=self._display_icon)


class Ability:
    def __init__(self, state: CacheState, data: AbilityPayload, agent: Agent) -> None:
        self._state = state
        self.agent: Agent = agent
        self.slot: AbilityType = try_enum(AbilityType, data['slot'])
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self._description: Union[str, Dict[str, str]] = data['description']
        self._display_icon: Optional[str] = data['displayIcon']
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)
        self._description_localized: Localization = Localization(self._description, locale=self._state.locale)

    def __repr__(self) -> str:
        return f'<Ability display_name={self.display_name!r}>'

    def __str__(self) -> str:
        return self.display_name.locale

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Ability) and other.slot == self.slot

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    def description_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._description_localized.from_locale(locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the agent role's name."""
        return self._display_name_localized

    @property
    def description(self) -> Localization:
        """:class: `str` Returns the agent role's description."""
        return self._description_localized

    @property
    def display_icon(self) -> Optional[Asset]:
        """:class: `Asset` Returns the agent role's display icon."""
        if self._display_icon is None:
            return None
        return Asset._from_url(state=self._state, url=self._display_icon)


class Media:
    def __init__(self, data: MediaPayload) -> None:
        self.id: int = data['id']
        self.wwise: str = data['wwise']
        self.wave: str = data['wave']

    def __repr__(self) -> str:
        return f'<Media id={self.id!r} wwise={self.wwise!r} wave={self.wave!r}>'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Media) and other.id == self.id

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.id)


class VoiceLine:
    def __init__(self, data: VoiceLinePayload) -> None:
        self.min_duration: float = data['minDuration']
        self.max_duration: float = data['maxDuration']
        self.media_list: List[Media] = [Media(media) for media in data['mediaList']]

    def __repr__(self) -> str:
        return f'<AgentVoiceLine min_duration={self.min_duration!r} max_duration={self.max_duration!r}>'

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, VoiceLine)
            and other.min_duration == self.min_duration
            and other.max_duration == self.max_duration
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.min_duration, self.max_duration))


class VoiceLineLocalization:
    def __init__(
        self,
        untranslated: Any,
        locale: Locale = Locale.american_english,
    ) -> None:
        self.ut = untranslated
        self._locale = locale

        # locale code
        self.ar_AE: Optional[VoiceLine] = VoiceLine(self.ut['ar-AE']) if self.ut.get('ar-AE') else None
        self.de_DE: Optional[VoiceLine] = VoiceLine(self.ut['de-DE']) if self.ut.get('de-DE') else None
        self.en_US: Optional[VoiceLine] = VoiceLine(self.ut['en-US']) if self.ut.get('en-US') else None
        self.es_ES: Optional[VoiceLine] = VoiceLine(self.ut['es-ES']) if self.ut.get('es-ES') else None
        self.es_MX: Optional[VoiceLine] = VoiceLine(self.ut['es-MX']) if self.ut.get('es-MX') else None
        self.fr_FR: Optional[VoiceLine] = VoiceLine(self.ut['fr-FR']) if self.ut.get('fr-FR') else None
        self.id_ID: Optional[VoiceLine] = VoiceLine(self.ut['id-ID']) if self.ut.get('id-ID') else None
        self.it_IT: Optional[VoiceLine] = VoiceLine(self.ut['it-IT']) if self.ut.get('it-IT') else None
        self.ja_JP: Optional[VoiceLine] = VoiceLine(self.ut['ja-JP']) if self.ut.get('ja-JP') else None
        self.ko_KR: Optional[VoiceLine] = VoiceLine(self.ut['ko-KR']) if self.ut.get('ko-KR') else None
        self.pl_PL: Optional[VoiceLine] = VoiceLine(self.ut['pl-PL']) if self.ut.get('pl-PL') else None
        self.pt_BR: Optional[VoiceLine] = VoiceLine(self.ut['pt-BR']) if self.ut.get('pt-BR') else None
        self.ru_RU: Optional[VoiceLine] = VoiceLine(self.ut['ru-RU']) if self.ut.get('ru-RU') else None
        self.th_TH: Optional[VoiceLine] = VoiceLine(self.ut['th-TH']) if self.ut.get('th-TH') else None
        self.tr_TR: Optional[VoiceLine] = VoiceLine(self.ut['tr-TR']) if self.ut.get('tr-TR') else None
        self.vi_VN: Optional[VoiceLine] = VoiceLine(self.ut['vi-VN']) if self.ut.get('vi-VN') else None
        self.zh_CN: Optional[VoiceLine] = VoiceLine(self.ut['zh-CN']) if self.ut.get('zh-CN') else None
        self.zh_TW: Optional[VoiceLine] = VoiceLine(self.ut['zh-TW']) if self.ut.get('zh-TW') else None

    def __repr__(self) -> str:
        attrs = [
            ('ar_AE', self.ar_AE),
            ('de_DE', self.de_DE),
            ('en_US', self.en_US),
            ('es_ES', self.es_ES),
            ('es_MX', self.es_MX),
            ('fr_FR', self.fr_FR),
            ('id_ID', self.id_ID),
            ('it_IT', self.it_IT),
            ('ja_JP', self.ja_JP),
            ('ko_KR', self.ko_KR),
            ('pl_PL', self.pl_PL),
            ('pt_BR', self.pt_BR),
            ('ru_RU', self.ru_RU),
            ('th_TH', self.th_TH),
            ('tr_TR', self.tr_TR),
            ('vi_VN', self.vi_VN),
            ('zh_CN', self.zh_CN),
            ('zh_TW', self.zh_TW),
        ]
        joined = ' '.join('%s=%r' % t for t in attrs)
        return f'<{self.__class__.__name__} {joined}>'

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Localization) and self.ut == other.untranslated

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.ut)

    def _dict(self) -> Dict[Locale, Optional[VoiceLine]]:
        """:class:`Dict[Locale, VoiceLine]`: Returns all locales as a dictionary."""
        voices = {
            Locale.arabic: self.ar_AE,
            Locale.german: self.de_DE,
            Locale.american_english: self.en_US,
            Locale.british_english: self.en_US,
            Locale.english: self.en_US,
            Locale.spain_spanish: self.es_ES,
            Locale.spanish_mexican: self.es_MX,
            Locale.french: self.fr_FR,
            Locale.indonesian: self.id_ID,
            Locale.italian: self.it_IT,
            Locale.japanese: self.ja_JP,
            Locale.korean: self.ko_KR,
            Locale.polish: self.pl_PL,
            Locale.brazil_portuguese: self.pt_BR,
            Locale.russian: self.ru_RU,
            Locale.thai: self.th_TH,
            Locale.turkish: self.tr_TR,
            Locale.vietnamese: self.vi_VN,
            Locale.chinese: self.zh_CN,
            Locale.taiwan_chinese: self.zh_TW,
        }
        return voices

    def all(self) -> List[VoiceLine]:
        """:class:`List[VoiceLine]`: Returns all locales as a list."""
        return list([v for v in self._dict().values() if v is not None])

    @property
    def voice_locale(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the voice locale of the current locale."""
        return self._dict().get(self._locale)

    @property
    def arabic(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the Arabic locale."""
        return self.ar_AE

    @property
    def german(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the German locale."""
        return self.de_DE

    @property
    def english(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the English locale."""
        return self.en_US

    @property
    def american_english(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the American English locale."""
        return self.en_US

    @property
    def british_english(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the British English locale."""
        return self.en_US

    @property
    def spanish(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the Spanish locale."""
        return self.es_ES

    @property
    def spanish_mexican(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the Spanish Mexican locale."""
        return self.es_MX

    @property
    def french(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the French locale."""
        return self.fr_FR

    @property
    def indonesian(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the Indonesian locale."""
        return self.id_ID

    @property
    def italian(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the Italian locale."""
        return self.it_IT

    @property
    def japanese(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the Japanese locale."""
        return self.ja_JP

    @property
    def korean(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the Korean locale."""
        return self.ko_KR

    @property
    def polish(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the Polish locale."""
        return self.pl_PL

    @property
    def portuguese_brazil(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the Portuguese Brazil locale."""
        return self.pt_BR

    @property
    def russian(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the Russian locale."""
        return self.ru_RU

    @property
    def thai(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the Thai locale."""
        return self.th_TH

    @property
    def turkish(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the Turkish locale."""
        return self.tr_TR

    @property
    def vietnamese(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the Vietnamese locale."""
        return self.vi_VN

    @property
    def chinese_simplified(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the Chinese Simplified locale."""
        return self.zh_CN

    @property
    def chinese_traditional(self) -> Optional[VoiceLine]:
        """:class:`Optional[VoiceLine]`: Returns the Chinese Traditional locale."""
        return self.zh_TW


class Agent(BaseModel):
    def __init__(self, *, state: CacheState, data: AgentPayload) -> None:
        super().__init__(data['uuid'])
        self._state: CacheState = state
        self._display_name: Union[str, Dict[str, str]] = data['displayName']
        self._description: Union[str, Dict[str, str]] = data['description']
        self.developer_name: str = data['developerName']
        self.character_tags: Optional[List[Union[str, Dict[str, str]]]] = data['characterTags']
        self._display_icon: str = data['displayIcon']
        self._display_icon_small: str = data['displayIconSmall']
        self._bust_portrait: str = data['bustPortrait']
        self._full_portrait: str = data['fullPortrait']
        self._full_portrait_v2: str = data['fullPortraitV2']
        self._killfeed_portrait: str = data['killfeedPortrait']
        self._background: str = data['background']
        self.background_gradient_colors: List[str] = data['backgroundGradientColors']
        self.asset_path: str = data['assetPath']
        self._is_full_portrait_right_facing: bool = data['isFullPortraitRightFacing']
        self._is_playable_character: bool = data['isPlayableCharacter']
        self._is_available_for_test: bool = data['isAvailableForTest']
        self._is_base_content: bool = data['isBaseContent']
        self._roles: Role = Role(state=self._state, data=data['role'])
        self._abilities: Dict[str, Ability] = {
            ability['slot'].lower(): Ability(state=self._state, data=ability, agent=self) for ability in data['abilities']
        }
        self._voice_line: Union[VoiceLinePayload, Dict[str, Optional[VoiceLinePayload]]] = data['voiceLine']
        self._display_name_localized: Localization = Localization(self._display_name, locale=self._state.locale)
        self._description_localized: Localization = Localization(self._description, locale=self._state.locale)

    def __str__(self) -> str:
        return self.display_name.locale

    def __repr__(self) -> str:
        return f'<Agent display_name={self.display_name!r}>'

    def display_name_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._display_name_localized.from_locale(locale)

    def description_localized(self, locale: Optional[Union[Locale, str]] = None) -> str:
        return self._description_localized.from_locale(locale)

    @property
    def display_name(self) -> Localization:
        """:class: `str` Returns the agent's name."""
        return self._display_name_localized

    @property
    def description(self) -> Localization:
        """:class: `str` Returns the agent's description."""
        return self._description_localized

    @property
    def display_icon(self) -> Asset:
        """:class: `Asset` Returns the agent's display icon."""
        return Asset._from_url(state=self._state, url=self._display_icon)

    @property
    def display_icon_small(self) -> Asset:
        """:class: `Asset` Returns the agent's display icon small."""
        return Asset._from_url(state=self._state, url=self._display_icon_small)

    @property
    def bust_portrait(self) -> Asset:
        """:class: `Asset` Returns the agent's bust portrait."""
        return Asset._from_url(state=self._state, url=self._bust_portrait)

    @property
    def full_portrait(self) -> Asset:
        """:class: `Asset` Returns the agent's full portrait."""
        return Asset._from_url(state=self._state, url=self._full_portrait)

    @property
    def full_portrait_v2(self) -> Asset:
        """:class: `Asset` Returns the agent's full portrait v2."""
        return Asset._from_url(state=self._state, url=self._full_portrait_v2)

    @property
    def killfeed_portrait(self) -> Asset:
        """:class: `Asset` Returns the agent's killfeed portrait."""
        return Asset._from_url(state=self._state, url=self._killfeed_portrait)

    @property
    def background(self) -> Asset:
        """:class: `Asset` Returns the agent's background."""
        return Asset._from_url(state=self._state, url=self._background)

    @property
    def role(self) -> Role:
        """:class: `AgentRole` Returns the agent's role."""
        return self._roles

    @property
    def abilities(self) -> List[Ability]:
        """:class: `List[AgentAbility]` Returns the agent's abilities."""
        return list(self._abilities.values())

    @property
    def voice_line(self) -> Optional[VoiceLine]:
        """:class: `AgentVoiceLineLocalization` Returns the agent's voice line."""
        return self.voice_line_localization.voice_locale

    @property
    def voice_line_localization(self) -> VoiceLineLocalization:
        """:class: `AgentVoiceLineLocalization` Returns the agent's voice line."""
        return VoiceLineLocalization(self._voice_line)

    def get_ability(self, ability_type: AbilityType) -> Optional[Ability]:
        """:class: `AgentAbility` Returns the agent's ability from the slot."""
        return self._abilities.get(ability_type.value.lower())

    def is_full_portrait_right_facing(self) -> bool:
        """:class: `bool` Returns whether the agent's full portrait is right facing."""
        return self._is_full_portrait_right_facing

    def is_playable_character(self) -> bool:
        """:class: `bool` Returns whether the agent is a playable character."""
        return self._is_playable_character

    def is_available_for_test(self) -> bool:
        """:class: `bool` Returns whether the agent is available for test."""
        return self._is_available_for_test

    def is_base_content(self) -> bool:
        """:class: `bool` Returns whether the agent is base content."""
        return self._is_base_content
