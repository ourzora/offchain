from offchain.metadata.adapters.base_adapter import HTTPAdapter as BaseHTTPAdapter
from offchain.metadata.registries.adapter_registry import AdapterRegistry


@AdapterRegistry.register
class HTTPAdapter(BaseHTTPAdapter):
    """Provides an interface for Requests sessions to contact HTTP and HTTPS urls."""

    pass
