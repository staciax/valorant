from __future__ import annotations

from pydantic import Field

from .base import BaseUUIDModel
from .localization import LocalizedField


class Flex(BaseUUIDModel):
    # uuid: str
    display_name: str | LocalizedField = Field(alias='displayName')
    display_name_all_caps: str | LocalizedField = Field(alias='displayNameAllCaps')
    display_icon: str = Field(alias='displayIcon')
    asset_path: str = Field(alias='assetPath')
