import pytest

from fetchers.metadata_fetcher import MetadataFetcher
from registries.fetcher_registry import FetcherRegistry


class TestFetcherRegistry:
    def test_fetcher_registry_no_duplicate_class_names(self):
        fetcher_registry = FetcherRegistry()
        with pytest.raises(AssertionError):
            fetcher_registry.register(MetadataFetcher)

    def test_fetcher_registry_has_all_fetchers(self):
        fetcher_registry = FetcherRegistry()
        assert fetcher_registry.get_all() == [MetadataFetcher]
