from typing import Type

from offchain.metadata.fetchers.base_fetcher import BaseFetcher
from offchain.metadata.registries.base_registry import BaseRegistry


class FetcherRegistry(BaseRegistry):
    __fetcher_registry: dict[str, BaseFetcher] = {}

    @staticmethod
    def get_all() -> list[BaseFetcher]:
        return list(FetcherRegistry.__fetcher_registry.values())

    @staticmethod
    def validate(fetcher_cls: Type[BaseFetcher]):
        assert (
            fetcher_cls.__name__ not in FetcherRegistry.__fetcher_registry
        ), f"{fetcher_cls.__name__} already exists in registry."

    @staticmethod
    def add(fetcher_cls: Type[BaseFetcher]):
        FetcherRegistry.__fetcher_registry[fetcher_cls.__name__] = fetcher_cls
