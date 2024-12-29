from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from valorant import Client

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


@pytest.fixture(scope='session')
def anyio_backend() -> Any:
    return 'asyncio'


@pytest.fixture(scope='session')
async def client() -> AsyncGenerator[Client]:
    async with Client() as client:
        yield client
