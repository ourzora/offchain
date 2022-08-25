from offchain.base.base_model import BaseModel


class Token(BaseModel):
    """Information required to uniquely identify an NFT.

    Attributes:
        chain_identifier (str): identifier for network and chain of token, e.g. "ETHEREUM-MAINNET".
        collection_address (str): collection address of token.
        token_id (int): token_id of token.
        token_uri (str, optional): the uri at which the metadata lives.
    """

    chain_identifier: str
    collection_address: str
    token_id: int
    uri: str
