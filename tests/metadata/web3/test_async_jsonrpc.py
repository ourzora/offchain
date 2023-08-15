import pytest

from unittest.mock import AsyncMock
from offchain.web3.jsonrpc import AsyncEthereumJSONRPC


@pytest.mark.asyncio
async def test_chunking_batch_calls():
    rpc = AsyncEthereumJSONRPC()
    rpc.call_batch = AsyncMock()
    params = [i for i in range(5)]
    await rpc.call_batch_chunked("test", params, chunk_size=1)
    assert rpc.call_batch.call_count == 5
    assert (
        str(rpc.call_batch.call_args_list)
        == "[call('test', [0]),\n call('test', [1]),\n call('test', [2]),\n call('test', [3]),\n call('test', [4])]"
    )
