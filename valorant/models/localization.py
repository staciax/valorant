from __future__ import annotations

from pydantic import Field

from .base import BaseModel


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
