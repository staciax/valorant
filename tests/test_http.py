from __future__ import annotations

import aiohttp
import pytest

from valorant.http import HTTPClient


@pytest.mark.anyio
async def test_http_client_start_close() -> None:
    http_client = HTTPClient(enable_cache=False)
    assert http_client._session is None

    await http_client.start()
    assert http_client._session is not None
    assert not http_client._session.closed

    await http_client.close()
    await http_client.close()
    assert http_client._session.closed


@pytest.mark.anyio
async def test_http_client_clear() -> None:
    http_client = HTTPClient(enable_cache=False)
    await http_client.start()
    await http_client.close()

    assert http_client._session is not None
    assert http_client._session.closed

    http_client.clear()
    assert http_client._session is None


@pytest.mark.anyio
async def test_http_client_clear_with_open_session() -> None:
    http_client = HTTPClient(enable_cache=False)
    await http_client.start()

    assert http_client._session is not None
    assert not http_client._session.closed

    http_client.clear()
    assert http_client._session is not None

    await http_client.close()


@pytest.mark.anyio
async def test_http_client_with_custom_session() -> None:
    custom_session = aiohttp.ClientSession()
    http_client = HTTPClient(session=custom_session, enable_cache=False)

    assert http_client._session is custom_session

    await http_client.start()
    assert http_client._session is custom_session

    await http_client.close()
    assert http_client._session.closed
