import pytest

from .conftest import BaseTest


class TestInGameAPI(BaseTest):
    @pytest.mark.asyncio
    async def test_client_init(self) -> None:
        assert self.client is not None
        await self.client.init()

    @pytest.mark.asyncio
    async def test_client(self) -> None:
        assert self.client is not None
        assert self.client.is_ready() is True
        assert self.client.is_closed() is False

        for key in self.client.cache.__dict__.keys():
            if key.startswith('_') and isinstance(self.client.cache.__dict__[key], dict):
                assert len(self.client.cache.__dict__[key]) > 0

        await self.client.close()
        assert self.client.is_closed() is True
        self.client.clear()

        for key in self.client.cache.__dict__.keys():
            if key.startswith('_') and isinstance(self.client.cache.__dict__[key], dict):
                assert len(self.client.cache.__dict__[key]) == 0

        assert self.client.is_ready() is False
        assert self.client.is_closed() is False

    @pytest.mark.asyncio
    async def test_close(self) -> None:
        await self.client.close()
