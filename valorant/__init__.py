"""
Valorant API Wrapper
~~~~~~~~~~~~~~~~~~~
A basic wrapper for the Valorant API.
:copyright: (c) 2023-present STACiA
:license: MIT, see LICENSE for more details.
"""

__title__ = 'valorant'
__author__ = 'STACiA'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023-present STACiA'
__version__ = '1.0.8a'

from typing import Literal, NamedTuple

from . import models as models, utils as utils
from .asset import Asset as Asset
from .client import Client as Client
from .enums import *
from .localization import Localization as Localization
from .models import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    release: Literal['alpha', 'beta', 'final']


version_info: VersionInfo = VersionInfo(major=1, minor=0, micro=7, release='alpha')

del NamedTuple, Literal, VersionInfo
