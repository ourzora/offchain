import cgi
from typing import Tuple, Union

import requests

from adapters.base_adapter import Adapter
from fetchers.base_fetcher import BaseFetcher
from logger.logging import logger


class MetadataFetcher(BaseFetcher):
    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 0,
    ) -> None:
        self.timeout = timeout
        self.max_retries = max_retries
        self.sess = requests.Session()

    def register_adapter(self, adapter: Adapter, url_prefix: str):
        self.sess.mount(url_prefix, adapter)

    def _head(self, uri: str):
        return self.sess.head(uri, timeout=self.timeout, allow_redirects=True)

    def _get(self, uri: str):
        return self.sess.get(uri, timeout=self.timeout, allow_redirects=True)

    def fetch_mime_type_and_size(self, uri: str) -> Tuple[str, str]:
        """Fetch mime type and size for uri"""
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

    def fetch_content(self, token_uri: str) -> Union[dict, str]:
        """Fetch data at uri"""
        try:
            res = self._get(token_uri)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            raise Exception(f"Don't know how to fetch metadata for {token_uri=}. {str(e)}")
