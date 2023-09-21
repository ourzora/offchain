from typing import Optional, Type

from offchain.metadata.adapters.base_adapter import Adapter
from offchain.metadata.registries.base_registry import BaseRegistry


class AdapterRegistry(BaseRegistry):
    __adapter_registry: dict[str, Adapter] = {}

    @staticmethod
    def get_all() -> list[Adapter]:  # type: ignore[override]
        return list(AdapterRegistry.__adapter_registry.values())

    @staticmethod
    def get_adapter_cls_by_name(adapter_name: str) -> Optional[Adapter]:
        return AdapterRegistry.__adapter_registry.get(adapter_name)

    @staticmethod
    def validate(adapter_cls: Type[Adapter]):  # type: ignore[no-untyped-def, override]
        assert (
            adapter_cls.__name__ not in AdapterRegistry.__adapter_registry
        ), f"{adapter_cls.__name__} already exists in registry."

    @staticmethod
    def add(adapter_cls: Type[Adapter]):  # type: ignore[no-untyped-def, override]
        AdapterRegistry.__adapter_registry[adapter_cls.__name__] = adapter_cls  # type: ignore[assignment]  # noqa: E501
