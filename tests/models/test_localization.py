import pytest

from valorant.models.localization import LocalizedField


@pytest.fixture
def data() -> dict[str, str]:
    return {
        'de-DE': 'Deutsch',
        'es-ES': 'Español',
        'ar-AE': 'العربية',
        'id-ID': 'Indonesia',
        'es-MX': 'Español (México)',
        'fr-FR': 'Français',
        'en-US': 'English',
        'it-IT': 'Italiano',
        'ja-JP': '日本語',
        'ko-KR': '한국어',
        'th-TH': 'ไทย',
        'pl-PL': 'Polski',
        'pt-BR': 'Português (Brasil)',
        'ru-RU': 'Русский',
        'tr-TR': 'Türkçe',
        'vi-VN': 'Tiếng Việt',
        'zh-TW': '繁體中文',
        'zh-CN': '简体中文',
    }


def test_creation_with_aliases(data: dict[str, str]) -> None:
    field = LocalizedField(**data)

    assert field.de_DE == 'Deutsch'
    assert field.en_US == 'English'
    assert field.zh_CN == '简体中文'


def test_language_aliases(data: dict[str, str]) -> None:
    field = LocalizedField(**data)

    assert field.arabic == field.ar_AE
    assert field.german == field.de_DE
    assert field.american_english == field.en_US
    assert field.spain_spanish == field.es_ES
    assert field.spanish_mexican == field.es_MX
    assert field.french == field.fr_FR
    assert field.indonesian == field.id_ID
    assert field.italian == field.it_IT
    assert field.japanese == field.ja_JP
    assert field.korean == field.ko_KR
    assert field.polish == field.pl_PL
    assert field.brazil_portuguese == field.pt_BR
    assert field.russian == field.ru_RU
    assert field.thai == field.th_TH
    assert field.turkish == field.tr_TR
    assert field.vietnamese == field.vi_VN
    assert field.chinese == field.zh_CN
    assert field.taiwan_chinese == field.zh_TW


def test_str_method(data: dict[str, str]) -> None:
    field = LocalizedField(**data)
    assert str(field) == 'English'


def test_repr_method(data: dict[str, str]) -> None:
    field = LocalizedField(**data)
    assert repr(field) == "<LocalizedField en_US='English'>"
