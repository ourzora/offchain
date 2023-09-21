from offchain.base.base_model import BaseModel  # type: ignore[attr-defined]
from offchain.metadata.models.token import Token


class MetadataProcessingError(BaseModel):
    """Interface for metadata processing errors and relevant contextual information.

    Attributes:
        token (Token): a Token interface with all information required to uniquely identify an NFT
        error_type (str): the class of caught exception.
        error_message (str): the error message of the caught exception.
    """  # noqa: E501

    token: Token

    error_type: str
    error_message: str

    @staticmethod
    def from_token_and_error(token: Token, e: Exception) -> "MetadataProcessingError":
        return MetadataProcessingError(
            token=token,
            error_type=e.__class__.__name__,
            error_message=str(e),
        )
