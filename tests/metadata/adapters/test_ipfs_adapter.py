import httpx
import pytest
from pytest_httpx import HTTPXMock

from offchain.metadata.adapters import IPFSAdapter  # type: ignore[attr-defined]


class TestIPFSAdapter:
    def test_ipfs_adapter_requires_trailing_slashes(self):  # type: ignore[no-untyped-def]  # noqa: E501
        with pytest.raises(AssertionError):
            IPFSAdapter(host_prefixes=["https://gateway.pinata.cloud"])

    def test_ipfs_adapter_make_request_url(self):  # type: ignore[no-untyped-def]
        adapter = IPFSAdapter()
        for url in [
            "https://tunes.mypinata.cloud/ipfs/QmSr3vdMuP2fSxWD7S26KzzBWcAN1eNhm4hk1qaR3x3vmj/1.json",
            "ipfs://ipfs/QmSr3vdMuP2fSxWD7S26KzzBWcAN1eNhm4hk1qaR3x3vmj/1.json",
            "ipfs://QmSr3vdMuP2fSxWD7S26KzzBWcAN1eNhm4hk1qaR3x3vmj/1.json",
        ]:
            assert (
                adapter.make_request_url(url)
                == "https://gateway.pinata.cloud/ipfs/QmSr3vdMuP2fSxWD7S26KzzBWcAN1eNhm4hk1qaR3x3vmj/1.json"
            )

    @pytest.mark.asyncio
    async def test_gen_head(self, httpx_mock: HTTPXMock):
        # mocker responds to HEAD requests only
        httpx_mock.add_response(method="HEAD")

        adapter = IPFSAdapter()
        ipfs_url = (
            "ipfs://bafkreiboyxwytfyufln3uzyzaixslzvmrqs5ezjo2cio2fymfqf6u57u6u"  # noqa
        )
        async with httpx.AsyncClient() as client:
            await adapter.gen_head(url=ipfs_url, sess=client)
        outgoing_get_request = httpx_mock.get_request(method="GET")
        assert not outgoing_get_request
        outgoing_head_request = httpx_mock.get_request(method="HEAD")
        assert outgoing_head_request

    @pytest.mark.asyncio
    async def test_gen_send(self, httpx_mock: HTTPXMock):
        # mocker responds to GET requests only
        httpx_mock.add_response(method="GET")

        adapter = IPFSAdapter()
        ipfs_url = (
            "ipfs://bafkreiboyxwytfyufln3uzyzaixslzvmrqs5ezjo2cio2fymfqf6u57u6u"  # noqa
        )
        async with httpx.AsyncClient() as client:
            await adapter.gen_send(url=ipfs_url, sess=client)
        outgoing_get_request = httpx_mock.get_request(method="GET")
        assert outgoing_get_request
        outgoing_head_request = httpx_mock.get_request(method="HEAD")
        assert not outgoing_head_request
