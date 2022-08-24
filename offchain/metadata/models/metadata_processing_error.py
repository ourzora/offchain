from offchain.base.base_model import BaseModel
from offchain.metadata.models.token import Token


class MetadataProcessingError(BaseModel):
    chain_identifier: str
    collection_address: str
    token_id: int
    uri: str

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
