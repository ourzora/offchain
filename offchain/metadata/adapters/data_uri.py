from urllib.request import urlopen
from requests import PreparedRequest, Response

from offchain.metadata.adapters.base_adapter import BaseAdapter
from offchain.metadata.registries.adapter_registry import AdapterRegistry


@AdapterRegistry.register
class DataURIAdapter(BaseAdapter):
    """Provides an interface for Requests sessions to handle data uris."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send(self, request: PreparedRequest, *args, **kwargs):
        """Handle data uri request.

        Args:
            request (PreparedRequest): incoming request

        Returns:
            Response: encoded data uri response.
        """
        newResponse = Response()
        newResponse.request = request
        newResponse.url = request.url
        newResponse.connection = self
        try:
            response = urlopen(request.url)
            newResponse.status_code = 200
            newResponse.headers = response.headers
            newResponse.raw = response
            newResponse.encoding = "utf-8"
            self.response = response
        finally:
            return newResponse

    def close(self):
        self.response.close()
