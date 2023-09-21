from typing import Any, Optional, TypedDict

import requests
import requests.adapters
from tenacity import retry, stop_after_attempt, wait_exponential

from offchain.concurrency import parmap
from offchain.constants.providers import RPCProvider
from offchain.logger.logging import logger
from offchain.web3.read_async import AsyncContractReader

MAX_REQUEST_BATCH_SIZE = 100


class RPCPayload(TypedDict):
    method: str
    params: list[dict]  # type: ignore[type-arg]
    id: int
    jsonrpc: str


class EthereumJSONRPC:
    def __init__(
        self,
        provider_url: Optional[str] = None,
    ) -> None:
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=100, pool_maxsize=1000, max_retries=10
        )  # noqa: E501
        self.sess = requests.Session()
        self.sess.mount("https://", adapter)
        self.sess.mount("http://", adapter)
        self.sess.headers = {"Content-Type": "application/json"}
        self.url = provider_url or RPCProvider.LLAMA_NODES_MAINNET
        self.async_reader = AsyncContractReader(rpc_url=self.url)

    def __payload_factory(self, method: str, params: list[Any], id: int) -> RPCPayload:
        return {"method": method, "params": params, "id": id, "jsonrpc": "2.0"}

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=1, max=5),
    )
    def call(self, method: str, params: list[dict]) -> dict:  # type: ignore[type-arg]
        try:
            payload = self.__payload_factory(method, params, 1)
            resp = self.sess.post(self.url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data  # type: ignore[no-any-return]
        except Exception as e:
            logger.error(
                f"Caught exception while making rpc call. Method: {method}. Params: {params}. Retrying. Error: {e}"  # noqa: E501
            )
            raise

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=1, max=5),
    )
    def call_batch(self, method: str, params: list[list[Any]]) -> list[dict]:  # type: ignore[type-arg]  # noqa: E501
        try:
            payload = [
                self.__payload_factory(method, param, i)
                for i, param in enumerate(params)
            ]  # noqa: E501
            resp = self.sess.post(self.url, json=payload)
            resp.raise_for_status()
            result = resp.json()
            return result  # type: ignore[no-any-return]
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
    ) -> list[dict]:  # type: ignore[type-arg]
        size = len(params)
        if size < chunk_size:  # type: ignore[operator]
            return self.call_batch(method, params)

        prev_offset, curr_offset = 0, chunk_size

        chunks = []
        while prev_offset < size:
            chunks.append(params[prev_offset:curr_offset])
            prev_offset = curr_offset  # type: ignore[assignment]
            curr_offset = min(curr_offset + chunk_size, size)  # type: ignore[operator]

        results = parmap(lambda chunk: self.call_batch(method, chunk), chunks)
        return [i for res in results for i in res]
