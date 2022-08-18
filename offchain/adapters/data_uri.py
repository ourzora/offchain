from urllib.request import urlopen
from requests import PreparedRequest, Response

from offchain.adapters.base_adapter import BaseAdapter
from offchain.registries.adapter_registry import AdapterRegistry


@AdapterRegistry.register
class DataURIAdapter(BaseAdapter):
    """Requests adapter for decoding data-uris"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send(self, request: PreparedRequest, *args, **kwargs):
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
