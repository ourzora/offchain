import pytest

from offchain.concurrency import batched_parmap


@pytest.mark.parametrize("batch_size", range(1, 11))
def test_batched_parmap(batch_size):
    def square(x):
        return x * x

    args = list(range(0, 10))
    expected = [square(x) for x in args]
    result = batched_parmap(square, args, batch_size=batch_size)
    assert result == expected
