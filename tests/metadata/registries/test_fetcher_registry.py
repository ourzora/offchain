import pytest

from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher
from offchain.metadata.registries.fetcher_registry import FetcherRegistry


class TestFetcherRegistry:
    def test_fetcher_registry_no_duplicate_class_names(self):  # type: ignore[no-untyped-def]  # noqa: E501
        fetcher_registry = FetcherRegistry()
        with pytest.raises(AssertionError):
            fetcher_registry.register(MetadataFetcher)

    def test_fetcher_registry_has_all_fetchers(self):  # type: ignore[no-untyped-def]
        fetcher_registry = FetcherRegistry()
        assert fetcher_registry.get_all() == [MetadataFetcher]  # type: ignore[comparison-overlap]  # noqa: E501
