from typing import Optional

from offchain.base.base_model import BaseModel
from offchain.metadata.models.token import Token


class MetadataProcessingError(BaseModel):
    """Class for storing relevant information for metadata processing errors.

    Attributes:
        chain_identifier (str): identifier for the network and chain, e.g. "ETHEREUM-MAINNET".
        collection_address (str): collection address of the token .
        token_id (int): token id of the token.
        uri (str): metadata uri of the token.
        error_type (str): the class of caught exception.
        error_message (str): the error message of the caught exception.
    """

    chain_identifier: str
    collection_address: str
    token_id: int
    uri: Optional[str]

    error_type: str
    error_message: str

    @staticmethod
    def from_token_and_error(token: Token, e: Exception) -> "MetadataProcessingError":
        return MetadataProcessingError(
            chain_identifier=token.chain_identifier,
            collection_address=token.collection_address,
            token_id=token.token_id,
            uri=token.uri,
            error_type=e.__class__.__name__,
            error_message=str(e),
        )
