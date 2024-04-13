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

from typing import Dict, Optional, Union

from . import utils
from .enums import Locale

# fmt: off
__all__ = (
    'Localization',
)
# fmt: on


class Localization:
    def __init__(
        self,
        untranslated: Optional[Union[str, Dict[str, str]]],
        locale: Union[str, Locale] = Locale.american_english,
    ) -> None:
        self.untranslated = untranslated
        self._locale = locale
        if self.untranslated is None:
            self.untranslated = {}
        if isinstance(self.untranslated, str):
            self.untranslated = {str(self._locale): self.untranslated}
        default = self.untranslated.get(str(self._locale), '')
        self.ar_AE: str = self.untranslated.get('ar-AE', default)
        self.de_DE: str = self.untranslated.get('de-DE', default)
        self.en_US: str = self.untranslated.get('en-US', default)
        self.es_ES: str = self.untranslated.get('es-ES', default)
        self.es_MX: str = self.untranslated.get('es-MX', default)
        self.fr_FR: str = self.untranslated.get('fr-FR', default)
        self.id_ID: str = self.untranslated.get('id-ID', default)
        self.it_IT: str = self.untranslated.get('it-IT', default)
        self.ja_JP: str = self.untranslated.get('ja-JP', default)
        self.ko_KR: str = self.untranslated.get('ko-KR', default)
        self.pl_PL: str = self.untranslated.get('pl-PL', default)
        self.pt_BR: str = self.untranslated.get('pt-BR', default)
        self.ru_RU: str = self.untranslated.get('ru-RU', default)
        self.th_TH: str = self.untranslated.get('th-TH', default)
        self.tr_TR: str = self.untranslated.get('tr-TR', default)
        self.vi_VN: str = self.untranslated.get('vi-VN', default)
        self.zh_CN: str = self.untranslated.get('zh-CN', default)
        self.zh_TW: str = self.untranslated.get('zh-TW', default)

    def __str__(self) -> str:
        """Return the default locale."""
        return self.locale

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Localization) and self.untranslated == other.untranslated

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.untranslated)

    def __lt__(self, other: Localization) -> bool:
        return self.locale < other.locale

    def __le__(self, other: Localization) -> bool:
        return self.locale <= other.locale

    def __gt__(self, other: Localization) -> bool:
        return self.locale > other.locale

    def __ge__(self, other: Localization) -> bool:
        return self.locale >= other.locale

    @property
    def arabic(self) -> str:
        """:class:`str`: Returns the Arabic locale."""
        return utils.string_escape(self.ar_AE)

    @property
    def german(self) -> str:
        """:class:`str`: Returns the German locale."""
        return utils.string_escape(self.de_DE)

    @property
    def english(self) -> str:
        """:class:`str`: Returns the English locale."""
        return utils.string_escape(self.en_US)

    @property
    def american_english(self) -> str:
        """:class:`str`: Returns the American English locale."""
        return utils.string_escape(self.en_US)

    @property
    def british_english(self) -> str:
        """:class:`str`: Returns the British English locale."""
        return utils.string_escape(self.en_US)

    @property
    def spanish(self) -> str:
        """:class:`str`: Returns the Spanish locale."""
        return utils.string_escape(self.es_ES)

    @property
    def spanish_mexican(self) -> str:
        """:class:`str`: Returns the Spanish Mexican locale."""
        return utils.string_escape(self.es_MX)

    @property
    def french(self) -> str:
        """:class:`str`: Returns the French locale."""
        return utils.string_escape(self.fr_FR)

    @property
    def indonesian(self) -> str:
        """:class:`str`: Returns the Indonesian locale."""
        return utils.string_escape(self.id_ID)

    @property
    def italian(self) -> str:
        """:class:`str`: Returns the Italian locale."""
        return utils.string_escape(self.it_IT)

    @property
    def japanese(self) -> str:
        """:class:`str`: Returns the Japanese locale."""
        return utils.string_escape(self.ja_JP)

    @property
    def korean(self) -> str:
        """:class:`str`: Returns the Korean locale."""
        return utils.string_escape(self.ko_KR)

    @property
    def polish(self) -> str:
        """:class:`str`: Returns the Polish locale."""
        return utils.string_escape(self.pl_PL)

    @property
    def portuguese_brazil(self) -> str:
        """:class:`str`: Returns the Portuguese Brazil locale."""
        return utils.string_escape(self.pt_BR)

    @property
    def russian(self) -> str:
        """:class:`str`: Returns the Russian locale."""
        return utils.string_escape(self.ru_RU)

    @property
    def thai(self) -> str:
        """:class:`str`: Returns the Thai locale."""
        return utils.string_escape(self.th_TH)

    @property
    def turkish(self) -> str:
        """:class:`str`: Returns the Turkish locale."""
        return utils.string_escape(self.tr_TR)

    @property
    def vietnamese(self) -> str:
        """:class:`str`: Returns the Vietnamese locale."""
        return utils.string_escape(self.vi_VN)

    @property
    def chinese_simplified(self) -> str:
        """:class:`str`: Returns the Chinese Simplified locale."""
        return utils.string_escape(self.zh_CN)

    @property
    def chinese_traditional(self) -> str:
        """:class:`str`: Returns the Chinese Traditional locale."""
        return utils.string_escape(self.zh_TW)

    @property
    def default(self) -> str:
        """:class:`str`: Returns the english locale is default."""
        if isinstance(self.untranslated, str):
            return self.untranslated
        elif isinstance(self.untranslated, dict):
            return self.untranslated.get('en-US', '')
        return ''

    @property
    def locale(self) -> str:
        """:class:`str`: Returns from your current locale."""
        if isinstance(self.untranslated, dict):
            return self.untranslated.get(str(self._locale), self.default)
        return self.default

    def from_locale(self, locale: Optional[Union[Locale, str]] = None) -> str:
        """:class:`str`: Returns the locale from the locale code."""
        if locale is None:
            return self.locale
        if isinstance(locale, Locale):
            locale = str(locale)

        if hasattr(self, locale.replace('-', '_')):
            return getattr(self, locale.replace('-', '_'))
        elif isinstance(self.untranslated, dict):
            return self.untranslated.get(locale, self.default)
        return self.default
