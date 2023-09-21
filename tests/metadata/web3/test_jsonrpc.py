from unittest.mock import MagicMock

from offchain.web3.jsonrpc import EthereumJSONRPC


def test_chunking_batch_calls():  # type: ignore[no-untyped-def]
    rpc = EthereumJSONRPC()
    rpc.call_batch = MagicMock()  # type: ignore[assignment]
    params = [i for i in range(5)]
    rpc.call_batch_chunked("test", params, chunk_size=1)  # type: ignore[arg-type]
    assert rpc.call_batch.call_count == 5
    assert (
        str(rpc.call_batch.call_args_list)
        == "[call('test', [0]),\n call('test', [1]),\n call('test', [2]),\n call('test', [3]),\n call('test', [4])]"  # noqa: E501
    )
