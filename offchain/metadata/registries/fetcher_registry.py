from typing import Type

from offchain.metadata.fetchers.base_fetcher import BaseFetcher
from offchain.metadata.registries.base_registry import BaseRegistry


class FetcherRegistry(BaseRegistry):
    __fetcher_registry: dict[str, BaseFetcher] = {}

    @staticmethod
    def get_all() -> list[BaseFetcher]:  # type: ignore[override]
        return list(FetcherRegistry.__fetcher_registry.values())

    @staticmethod
    def validate(fetcher_cls: Type[BaseFetcher]):  # type: ignore[no-untyped-def, override]  # noqa: E501
        assert (
            fetcher_cls.__name__ not in FetcherRegistry.__fetcher_registry
        ), f"{fetcher_cls.__name__} already exists in registry."

    @staticmethod
    def add(fetcher_cls: Type[BaseFetcher]):  # type: ignore[no-untyped-def, override]
        FetcherRegistry.__fetcher_registry[fetcher_cls.__name__] = fetcher_cls  # type: ignore[assignment]  # noqa: E501
