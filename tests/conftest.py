from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from valorant import Client

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator
    from pathlib import Path


@pytest.fixture(scope='session')
def anyio_backend() -> Any:
    return 'asyncio'


@pytest.fixture(scope='session')
def cache_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return tmp_path_factory.mktemp('test_valorant_cache')


@pytest.fixture(scope='session')
async def client(cache_path: Path) -> AsyncGenerator[Client]:
    async with Client(cache_path=cache_path) as client:
        yield client
