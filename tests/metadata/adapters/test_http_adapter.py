import httpx
import pytest
from pytest_httpx import HTTPXMock

from offchain.metadata.adapters import HTTPAdapter  # type: ignore[attr-defined]


class TestHTTPAdapter:
    @pytest.mark.asyncio
    async def test_gen_head(self, httpx_mock: HTTPXMock):
        # mocker responds to HEAD requests only
        httpx_mock.add_response(method="HEAD")

        adapter = HTTPAdapter()
        url = "https://meta.sadgirlsbar.io/8403.json"  # noqa
        async with httpx.AsyncClient() as client:
            await adapter.gen_head(url=url, sess=client)
        outgoing_get_request = httpx_mock.get_request(method="GET")
        assert not outgoing_get_request
        outgoing_head_request = httpx_mock.get_request(method="HEAD")
        assert outgoing_head_request

    @pytest.mark.asyncio
    async def test_gen_send(self, httpx_mock: HTTPXMock):
        # mocker responds to GET requests only
        httpx_mock.add_response(method="GET")

        adapter = HTTPAdapter()
        url = "https://meta.sadgirlsbar.io/8403.json"  # noqa
        async with httpx.AsyncClient() as client:
            await adapter.gen_send(url=url, sess=client)
        outgoing_get_request = httpx_mock.get_request(method="GET")
        assert outgoing_get_request
        outgoing_head_request = httpx_mock.get_request(method="HEAD")
        assert not outgoing_head_request
