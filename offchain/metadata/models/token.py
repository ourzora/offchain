from typing import Optional
from offchain.base.base_model import BaseModel


class Token(BaseModel):
    """Information required to uniquely identify an NFT.


    Attributes:
        chain_identifier (str): identifier for network and chain of token,
            formatted as NETWORK_NAME-CHAIN_NAME (e.g. "ETHEREUM-MAINNET").
        collection_address (str): collection address of token.
        token_id (int): unique identifier of token.
        uri (str, optional): the uri where the metadata is stored.
    """

    chain_identifier: str
    collection_address: str
    token_id: int
    uri: Optional[str] = None
