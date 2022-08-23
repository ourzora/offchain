from offchain.metadata.web3.batching import BatchContractViewCaller

ADDRESS = "0x335eeef8e93a7a757d9e7912044d9cd264e2b2d8"


class TestBatchContractViewCaller:
    batcher = BatchContractViewCaller()

    def test__single_address_single_fn_many_args(self):
        ids = self.batcher.single_address_single_fn_many_args(
            ADDRESS, "tokenByIndex(uint256)", ["uint256"], [[0], [2], [3]]
        )
        assert ids == [1, 3, 4]

    def test__single_address_many_fns_many_args(self):
        results = self.batcher.single_address_many_fns_many_args(
            ADDRESS,
            function_sigs=["tokenByIndex(uint256)", "tokenURI(uint256)"],
            return_types=[["uint256"], ["string"]],
            args=[[0], [8403]],
        )
        assert results == {
            "tokenByIndex(uint256)": 1,
            "tokenURI(uint256)": "https://meta.sadgirlsbar.io/8403.json",
        }
