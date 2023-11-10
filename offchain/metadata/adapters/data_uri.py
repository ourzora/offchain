import base64
from email.message import Message
from urllib.request import urlopen

import httpx
from requests import PreparedRequest, Response

from offchain.metadata.adapters.base_adapter import BaseAdapter
from offchain.metadata.registries.adapter_registry import AdapterRegistry


def decode_data_url(data_url):  # type: ignore[no-untyped-def]
    data_parts = data_url.split(",")
    data = data_parts[1]

    if ";base64" in data_parts[0]:
        decoded_data = base64.b64decode(data)
        decoded_text = decoded_data.decode("utf-8")
        return decoded_text

    return None


@AdapterRegistry.register
class DataURIAdapter(BaseAdapter):
    """Provides an interface for Requests sessions to handle data uris."""

    def __init__(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        super().__init__(*args, **kwargs)  # type: ignore[no-untyped-call]

    async def gen_send(self, url: str, *args, **kwargs) -> httpx.Response:  # type: ignore[no-untyped-def]  # noqa: E501
        """Handle async data uri `GET` request.

        Args:
            url (str): url

        Returns:
            httpx.Response: encoded data uri response.
        """
        response = httpx.Response(
            status_code=200,
            text=decode_data_url(url),  # type: ignore[no-untyped-call]
            request=httpx.Request(method="GET", url=url),
        )
        return response

    def send(self, request: PreparedRequest, *args, **kwargs):  # type: ignore[no-untyped-def]  # noqa: E501
        """Handle data uri `GET` request.

        Args:
            request (PreparedRequest): incoming request

        Returns:
            Response: encoded data uri response.
        """
        newResponse = Response()
        newResponse.request = request
        newResponse.url = request.url  # type: ignore[assignment]
        newResponse.connection = self  # type: ignore[attr-defined]
        try:
            response = urlopen(request.url)  # type: ignore[arg-type]
            newResponse.status_code = 200
            newResponse.headers = response.headers
            newResponse.raw = response
            newResponse._content = response.read()
            newResponse.encoding = response.info().get_param("charset") or "utf-8"
            self.response = response
        finally:
            return newResponse

    async def gen_head(self, url: str, *args, **kwargs) -> httpx.Response:  # type: ignore[no-untyped-def]  # noqa: E501
        """Handle async data uri `HEAD` request.

        Args:
            url (str): url

        Returns:
            httpx.Response: encoded data uri response.
        """
        response_headers = {}
        with urlopen(url) as r:
            message: Message = r.info()
            response_headers = dict(message._headers)  # type: ignore[attr-defined]
        response = httpx.Response(
            status_code=200,
            headers=response_headers,
            request=httpx.Request(method="HEAD", url=url),
        )
        return response

    def close(self):  # type: ignore[no-untyped-def]
        self.response.close()
