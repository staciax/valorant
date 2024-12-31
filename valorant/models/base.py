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

from __future__ import annotations

from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel as PydanticBaseModel, Field

T = TypeVar('T')

__all__ = (
    'BaseModel',
    'BaseUUIDModel',
    'LocalizedField',
    'Response',
)


class BaseModel(PydanticBaseModel):
    """Base class for all models."""

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}>'


class BaseUUIDModel(BaseModel):
    uuid: UUID

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.uuid == other.uuid

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.uuid)


class LocalizedField(BaseModel):
    de_DE: str = Field(alias='de-DE')
    es_ES: str = Field(alias='es-ES')
    ar_AE: str = Field(alias='ar-AE')
    id_ID: str = Field(alias='id-ID')
    es_MX: str = Field(alias='es-MX')
    fr_FR: str = Field(alias='fr-FR')
    en_US: str = Field(alias='en-US')
    it_IT: str = Field(alias='it-IT')
    ja_JP: str = Field(alias='ja-JP')
    ko_KR: str = Field(alias='ko-KR')
    th_TH: str = Field(alias='th-TH')
    pl_PL: str = Field(alias='pl-PL')
    pt_BR: str = Field(alias='pt-BR')
    ru_RU: str = Field(alias='ru-RU')
    tr_TR: str = Field(alias='tr-TR')
    vi_VN: str = Field(alias='vi-VN')
    zh_TW: str = Field(alias='zh-TW')
    zh_CN: str = Field(alias='zh-CN')

    # aliases

    arabic: str = ar_AE
    german: str = de_DE
    american_english: str = en_US
    spain_spanish: str = es_ES
    spanish_mexican: str = es_MX
    french: str = fr_FR
    indonesian: str = id_ID
    italian: str = it_IT
    japanese: str = ja_JP
    korean: str = ko_KR
    polish: str = pl_PL
    brazil_portuguese: str = pt_BR
    russian: str = ru_RU
    thai: str = th_TH
    turkish: str = tr_TR
    vietnamese: str = vi_VN
    chinese: str = zh_CN
    taiwan_chinese: str = zh_TW

    def __str__(self) -> str:
        return self.en_US

    def __repr__(self) -> str:
        return f'<LocalizedField en_US={self.en_US!r}>'


class Response(BaseModel, Generic[T]):
    status: int
    data: T
