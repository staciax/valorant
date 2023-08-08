from __future__ import annotations

import asyncio

import pytest
import pytest_asyncio

import valorant
from valorant import Client

try:
    import uvloop  # type: ignore
except ImportError:
    pass
else:
    uvloop.install()


@pytest.fixture(scope='session')
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # policy = asyncio.get_event_loop_policy()
        # loop = policy.new_event_loop()
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='class')
def client_class(request) -> None:
    client = Client(locale=valorant.Locale.american_english)
    request.cls.client = client


@pytest.mark.usefixtures('client_class')
class BaseTest:
    client: Client

    def test_client(self) -> None:
        assert self.client is not None
        assert self.client.is_ready() is False


class BaseAuthTest(BaseTest):
    @pytest.mark.asyncio
    async def test_authorize(self) -> None:
        assert self.client is not None
        assert self.client.is_ready() is False
        await self.client.wait_until_ready()
        assert self.client.is_ready() is True
