from offchain.adapters.base_adapter import HTTPAdapter as BaseHTTPAdapter
from offchain.registries.adapter_registry import AdapterRegistry


@AdapterRegistry.register
class HTTPAdapter(BaseHTTPAdapter):
    pass
