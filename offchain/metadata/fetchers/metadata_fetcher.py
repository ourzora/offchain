import cgi
import requests
from typing import Tuple, Union

from offchain.metadata.adapters.base_adapter import Adapter
from offchain.metadata.fetchers.base_fetcher import BaseFetcher
from offchain.logger.logging import logger
from offchain.metadata.registries.fetcher_registry import FetcherRegistry


@FetcherRegistry.register
class MetadataFetcher(BaseFetcher):
    """Fetcher class that makes network requests for metadata-related information.

    Attributes:
        timeout (int): request timeout in seconds.
        max_retries (int): maximum number of request retries.
        sess (requests.Session): a requests Session object.
    """

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 0,
    ) -> None:
        self.timeout = timeout
        self.max_retries = max_retries
        self.sess = requests.Session()

    def register_adapter(self, adapter: Adapter, url_prefix: str):
        """Register an adapter to a url prefix.

        Args:
            adapter (Adapter): an Adapter instance to register.
            url_prefix (str): the url prefix to which the adapter should be registered.
        """
        self.sess.mount(url_prefix, adapter)

    def set_max_retries(self, max_retries: int):
        """Setter function for max retries

        Args:
            max_retries (int): new maximum number of request retries.
        """
        self.max_retries = max_retries

    def set_timeout(self, timeout: int):
        """Setter function for timeout

        Args:
            timeout (int): new request timeout in seconds.
        """
        self.timeout = timeout

    def _head(self, uri: str):
        return self.sess.head(uri, timeout=self.timeout, allow_redirects=True)

    def _get(self, uri: str):
        return self.sess.get(uri, timeout=self.timeout, allow_redirects=True)

    def fetch_mime_type_and_size(self, uri: str) -> Tuple[str, int]:
        """Fetch the mime type and size of the content at a given uri.

        Args:
            uri (str): uri from which to fetch content mime type and size.

        Returns:
            tuple[str, int]: mime type and size
        """
        try:
            res = self._head(uri)
            # For any error status, try a get
            if 300 <= res.status_code < 600:
                res = self._get(uri)
            res.raise_for_status()
            headers = res.headers
            size = headers.get("content-length", 0)
            content_type = headers.get("content-type") or headers.get("Content-Type")
            if content_type is not None:
                content_type, _ = cgi.parse_header(content_type)

            return content_type, size
        except Exception as e:
            logger.error(f"Failed to fetch content-type and size from uri {uri}. Error: {e}")
            raise

    def fetch_content(self, uri: str) -> Union[dict, str]:
        """Fetch the content at a given uri

        Args:
            uri (str): uri from which to fetch content.

        Returns:
            Union[dict, str]: content fetched from uri
        """
        try:
            res = self._get(uri)
            res.raise_for_status()
            if res.text.startswith("{"):
                return res.json()
            else:
                return res.text
        except Exception as e:
            raise Exception(f"Don't know how to fetch metadata for {uri=}. {str(e)}")
