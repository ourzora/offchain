import httpx
import pytest
from pytest_httpx import HTTPXMock

from offchain.metadata.adapters import ARWeaveAdapter  # type: ignore[attr-defined]


class TestARWeaveAdapter:
    def test_arweave_adapter_make_request_url(self):  # type: ignore[no-untyped-def]
        adapter = ARWeaveAdapter()
        arweave_url = "ar://-G92LjB-wFj-FCGx040NgniW_Ypy_Cbh3Jq1HUD6l7A"  # noqa
        assert (
            adapter.parse_ar_url(arweave_url)
            == "https://arweave.net/-G92LjB-wFj-FCGx040NgniW_Ypy_Cbh3Jq1HUD6l7A"
        )

    @pytest.mark.asyncio
    async def test_gen_head(self, httpx_mock: HTTPXMock):
        # mocker responds to HEAD requests only
        httpx_mock.add_response(method="HEAD")

        adapter = ARWeaveAdapter()
        arweave_url = "ar://-G92LjB-wFj-FCGx040NgniW_Ypy_Cbh3Jq1HUD6l7A"  # noqa
        async with httpx.AsyncClient() as client:
            await adapter.gen_head(url=arweave_url, sess=client)
        outgoing_get_request = httpx_mock.get_request(method="GET")
        assert not outgoing_get_request
        outgoing_head_request = httpx_mock.get_request(method="HEAD")
        assert outgoing_head_request

    @pytest.mark.asyncio
    async def test_gen_send(self, httpx_mock: HTTPXMock):
        # mocker responds to GET requests only
        httpx_mock.add_response(method="GET")

        adapter = ARWeaveAdapter()
        arweave_url = "ar://-G92LjB-wFj-FCGx040NgniW_Ypy_Cbh3Jq1HUD6l7A"  # noqa
        async with httpx.AsyncClient() as client:
            await adapter.gen_send(url=arweave_url, sess=client)
        outgoing_get_request = httpx_mock.get_request(method="GET")
        assert outgoing_get_request
        outgoing_head_request = httpx_mock.get_request(method="HEAD")
        assert not outgoing_head_request
