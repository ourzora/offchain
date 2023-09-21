import pytest

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
