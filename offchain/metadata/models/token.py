from pydantic import validator
import re
from typing import Optional

from offchain.base.base_model import BaseModel  # type: ignore[attr-defined]


class Token(BaseModel):
    """Token interface with all information required to uniquely identify an NFT.


    Attributes:
        chain_identifier (str): identifier for network and chain of token,
            formatted as NETWORK_NAME-CHAIN_NAME (e.g. "ETHEREUM-MAINNET").
        collection_address (str): collection address of token.
        token_id (int): unique identifier of token.
        uri (str, optional): the uri where the metadata is stored.
    """

    collection_address: str
    token_id: int
    chain_identifier: str = "ETHEREUM-MAINNET"
    uri: Optional[str] = None

    @validator("chain_identifier")
    def validate_chain_identifier(cls, chain_identifier):  # type: ignore[no-untyped-def]  # noqa: E501
        if not re.match("^[A-Z]*-[A-Z]*$", chain_identifier):
            raise ValueError(
                "Expected chain identifier to be formatted as NETWORKNAME-CHAINNAME, e.g. ETHEREUM-MAINNET"  # noqa: E501
            )

        return chain_identifier
