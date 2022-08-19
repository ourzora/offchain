from dataclasses import dataclass
from typing import Optional

from offchain.web3.batching import BatchContactViewCaller
from offchain.web3.jsonrpc import EthereumJSONRPC


@dataclass
class RawSeeds:
    background: int
    body: int
    accessory: int
    head: int
    glasses: int


class NounsContractCaller:
    def __init__(
        self, contract_address: str, rpc: Optional[EthereumJSONRPC] = None
    ) -> None:
        self.contract_address = contract_address
        self.rpc = rpc or EthereumJSONRPC()
        self.caller = BatchContactViewCaller(rpc)

    def seeds(self, token_id: int) -> RawSeeds:
        return self.batch_seeds([token_id])[0]

    def batch_seeds(self, token_ids: list[int]) -> list[RawSeeds]:
        seeds = []

        results = self.caller.single_address_single_fn_many_args(
            self.contract_address,
            function_sig="seeds(uint256)",
            return_type=["uint48", "uint48", "uint48", "uint48", "uint48"],
            args=[[id] for id in token_ids],
        )

        for result in results:
            deserialized = RawSeeds(
                background=result[0],
                body=result[1],
                accessory=result[2],
                head=result[3],
                glasses=result[4],
            )
            seeds.append(deserialized)

        return seeds
