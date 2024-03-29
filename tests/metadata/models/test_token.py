import pytest

from offchain import Token  # type: ignore[attr-defined]


class TestToken:
    def test_token_validates_chain_identifier_is_uppercase(self):  # type: ignore[no-untyped-def]  # noqa: E501
        with pytest.raises(ValueError):
            Token(
                collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
                token_id=9559,
                chain_identifier="ethereum-mainnet",
            )

    def test_token_validates_chain_identifier_is_separated_by_hyphen(self):  # type: ignore[no-untyped-def]  # noqa: E501
        with pytest.raises(ValueError):
            Token(
                collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
                token_id=9559,
                chain_identifier="ETHEREUMMAINNET",
            )

    def test_token_validates_chain_identifier_starts_and_ends_correctly(self):  # type: ignore[no-untyped-def]  # noqa: E501
        with pytest.raises(ValueError):
            Token(
                collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
                token_id=9559,
                chain_identifier="aETHEREUM-MAINNETa",
            )
