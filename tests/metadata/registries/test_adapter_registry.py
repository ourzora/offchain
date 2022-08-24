import pytest

from offchain.metadata.adapters import (
    ARWeaveAdapter,
    DataURIAdapter,
    HTTPAdapter,
    IPFSAdapter,
)
from offchain.metadata.registries.adapter_registry import AdapterRegistry


class TestAdapterRegistry:
    def test_adapter_registry_no_duplicate_class_names(self):
        adapter_registry = AdapterRegistry()
        with pytest.raises(AssertionError):
            adapter_registry.register(IPFSAdapter)

    def test_adapter_registry_has_all_adapters(self):
        adapter_registry = AdapterRegistry()
        assert adapter_registry.get_all() == [
            ARWeaveAdapter,
            DataURIAdapter,
            HTTPAdapter,
            IPFSAdapter,
        ]
