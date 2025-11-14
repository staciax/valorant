from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from aiohttp import ClientSession
from aiohttp_client_cache.session import CachedSession

from valorant.http import IS_CACHE_ENABLED, HTTPClient

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.anyio
@pytest.mark.skipif(not IS_CACHE_ENABLED, reason='aiohttp-client-cache not available')
@pytest.mark.parametrize('enable_cache', [True, False])
async def test_cache(enable_cache: bool, tmp_path: Path) -> None:
    cache_path = tmp_path / 'test_cache'
    http_client = HTTPClient(enable_cache=enable_cache, cache_path=cache_path)

    try:
        await http_client.start()
        assert http_client._session is not None

        if enable_cache:
            assert isinstance(http_client._session, CachedSession)
        else:
            assert isinstance(http_client._session, ClientSession)

    finally:
        await http_client.close()


@pytest.mark.anyio
@pytest.mark.skipif(not IS_CACHE_ENABLED, reason='aiohttp-client-cache not available')
async def test_custom_cache_path(tmp_path: Path) -> None:
    cache_path = tmp_path / 'test_custom_cache'
    http_client = HTTPClient(enable_cache=True, cache_path=cache_path)

    try:
        await http_client.start()

        assert (cache_path / '.gitignore').exists(), 'Cache .gitignore file should exist'

        # try to request for initialize the cache
        await http_client.get_agent('add6443a-41bd-e414-f6ad-e58d267f4e95')  # Jett

        session = http_client._session
        assert isinstance(session, CachedSession)

        assert (cache_path / 'aiohttp-requests.db').exists(), 'Cache database should exist after initialization'

    finally:
        await http_client.close()
