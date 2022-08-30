from typing import Optional, TypedDict, Any

import requests
import requests.adapters

from offchain.concurrency import parmap
from offchain.constants.providers import RPCProvider
from tenacity import retry, stop_after_attempt, wait_exponential

from offchain.logger.logging import logger

MAX_REQUEST_BATCH_SIZE = 100


class RPCPayload(TypedDict):
    method: str
    params: list[dict]
    id: int
    jsonrpc: str


class EthereumJSONRPC:
    def __init__(
        self,
        provider_url: Optional[str] = None,
    ) -> None:
        adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=1000, max_retries=10)
        self.sess = requests.Session()
        self.sess.mount("https://", adapter)
        self.sess.mount("http://", adapter)
        self.sess.headers = {"Content-Type": "application/json"}
        self.url = provider_url or RPCProvider.CLOUDFLARE_MAINNET

    def __payload_factory(self, method: str, params: list[Any], id: int) -> RPCPayload:
        return {"method": method, "params": params, "id": id, "jsonrpc": "2.0"}

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=1, max=5),
    )
    def call(self, method: str, params: list[dict]) -> dict:
        try:
            payload = self.__payload_factory(method, params, 1)
            resp = self.sess.post(self.url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data
        except Exception as e:
            logger.error(
                f"Caught exception while making rpc call. Method: {method}. Params: {params}. Retrying. Error: {e}"
            )
            raise

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=1, max=5),
    )
    def call_batch(self, method: str, params: list[list[Any]]) -> list[dict]:
        try:
            payload = [self.__payload_factory(method, param, i) for i, param in enumerate(params)]
            resp = self.sess.post(self.url, json=payload)
            resp.raise_for_status()
            result = resp.json()
            return result
        except Exception as e:
            logger.error(
                f"Caught exception while making batch rpc call. "
                f"Method: {method}. Params: {params}. Retrying. Error: {e}"
                # noqa
            )
            raise

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=1, max=5),
    )
    def call_batch_chunked(
        self,
        method: str,
        params: list[list[Any]],
        chunk_size: Optional[int] = MAX_REQUEST_BATCH_SIZE,
    ) -> list[dict]:
        size = len(params)
        if size < chunk_size:
            return self.call_batch(method, params)

        prev_offset, curr_offset = 0, chunk_size

        chunks = []
        while prev_offset < size:
            chunks.append(params[prev_offset:curr_offset])
            prev_offset = curr_offset
            curr_offset = min(curr_offset + chunk_size, size)

        results = parmap(lambda chunk: self.call_batch(method, chunk), chunks)
        return [i for res in results for i in res]
