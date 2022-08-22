from offchain.metadata.adapters.base_adapter import HTTPAdapter as BaseHTTPAdapter
from offchain.metadata.registries.adapter_registry import AdapterRegistry


@AdapterRegistry.register
class HTTPAdapter(BaseHTTPAdapter):
    pass
