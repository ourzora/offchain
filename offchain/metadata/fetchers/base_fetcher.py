from typing import Optional, Protocol, Union

from offchain.metadata.adapters.base_adapter import Adapter, AdapterConfig


class BaseFetcher(Protocol):
    """Base protocol for fetcher classes

    Attributes:
        timeout (int): request timeout in seconds.
        max_retries (int): maximum number of request retries.
    """

    timeout: int
    max_retries: int
    async_adapter_configs: Optional[list[AdapterConfig]] = None

    def __init__(
        self,
        timeout: int,
        max_retries: int,
        async_adapter_configs: Optional[list[AdapterConfig]] = None,
    ) -> None:
        pass

    def set_timeout(self, new_timeout: int):  # type: ignore[no-untyped-def]
        """Setter function for timeout

        Args:
            new_timeout (int): new request timeout in seconds.
        """
        pass

    def set_max_retries(self, new_max_retries: int):  # type: ignore[no-untyped-def]
        """Setter function for max retries

        Args:
            new_max_retries (int): new maximum number of request retries.
        """
        pass

    def register_adapter(self, adapter: Adapter, url_prefix: str):  # type: ignore[no-untyped-def]  # noqa: E501
        """Register an adapter to a url prefix. Note this only affects synchronous http
        requests (via the requests library).

        Args:
            adapter (Adapter): an Adapter instance to register.
            url_prefix (str): the url prefix to which the adapter should be registered.
        """
        pass

    def fetch_mime_type_and_size(self, uri: str) -> tuple[str, int]:
        """Fetch the mime type and size of the content at a given uri.

        Args:
            uri (str): uri from which to fetch content mime type and size.

        Returns:
            tuple[str, int]: mime type and size
        """
        pass

    async def gen_fetch_mime_type_and_size(self, uri: str) -> tuple[str, int]:
        """Fetch the mime type and size of the content at a given uri.

        Args:
            uri (str): uri from which to fetch content mime type and size.

        Returns:
            tuple[str, int]: mime type and size
        """
        pass

    def fetch_content(self, uri: str) -> Union[dict, str]:  # type: ignore[type-arg]
        """Fetch the content at a given uri

        Args:
            uri (str): uri from which to fetch content.

        Returns:
            Union[dict, str]: content fetched from uri
        """
        pass

    async def gen_fetch_content(self, uri: str) -> Union[dict, str]:  # type: ignore[type-arg]  # noqa: E501
        """Async fetch the content at a given uri

        Args:
            uri (str): uri from which to fetch content.

        Returns:
            Union[dict, str]: content fetched from uri
        """
        pass
