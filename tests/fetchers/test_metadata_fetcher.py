from adapters.ipfs import IPFSAdapter
from fetchers.metadata_fetcher import MetadataFetcher


class TestMetadataFetcher:
    def test_metadata_fetcher_register_adapter(self):
        fetcher = MetadataFetcher()
        adapter = IPFSAdapter()
        fetcher.register_adapter(adapter, "ipfs://")
        assert fetcher.sess.adapters.get("ipfs://") == adapter
