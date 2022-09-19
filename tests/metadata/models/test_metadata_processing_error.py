from offchain.metadata.models.token import Token
from offchain.metadata.models.metadata_processing_error import MetadataProcessingError


def test_metadata_processing_error():
    token = Token(
        collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
        token_id=9559,
        chain_identifier="ETHEREUM-MAINNET",
    )

    metadata_processing_error = MetadataProcessingError(
        token=token,
        error_type="ClientError",
        error_message="404 ClientError: Could not find NFT.",
    )
    assert metadata_processing_error.token == token
    assert metadata_processing_error.error_type == "ClientError"
    assert metadata_processing_error.error_message == "404 ClientError: Could not find NFT."
