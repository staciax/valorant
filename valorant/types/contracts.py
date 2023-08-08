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

from typing import Dict, List, Optional, TypedDict, Union

from .object import Object
from .response import Response


class Reward(Object):
    type: str
    amount: int
    isHighlighted: bool


class Level(TypedDict):
    reward: Reward
    xp: int
    vpCost: int
    isPurchasableWithVP: bool
    doughCost: int
    isPurchasableWithDough: bool


class Chapter(TypedDict):
    isEpilogue: bool
    levels: List[Level]
    freeRewards: Optional[List[Reward]]


class Content(TypedDict):
    relationType: Optional[str]
    relationUuid: Optional[str]
    chapters: List[Chapter]
    premiumRewardScheduleUuid: Optional[str]
    premiumVPCost: int


class Contract(Object):
    displayName: Union[str, Dict[str, str]]
    displayIcon: Optional[str]
    shipIt: bool
    freeRewardScheduleUuid: str
    content: Content
    assetPath: str


Contracts = Response[List[Contract]]
ContractUUID = Response[Contract]
