# flake8: noqa: E501
from unittest.mock import MagicMock

from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher
from offchain.metadata.models.metadata import (
    MediaDetails,
    Metadata,
    MetadataField,
    MetadataFieldType,
    Attribute,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.collection.hashmasks import HashmasksParser
from offchain.web3.contract_caller import ContractCaller


class TestHashmasksParser:
    token = Token(
        chain_identifier="ETHEREUM-MAINNET",
        collection_address="0xc2c747e0f7004f9e8817db2ca4997657a7746928",
        token_id=553,
    )

    raw_data = {
        "image": "https://hashmasksstore.blob.core.windows.net/hashmasks/10694.jpg",
        "description": "Hashmask #553",
        "external_url": "https://www.thehashmasks.com/detail/553",
        "attributes": [
            {"trait_type": "Character", "value": "Male"},
            {"trait_type": "Mask", "value": "Basic"},
            {"trait_type": "Skin Color", "value": "Blue"},
            {"trait_type": "Eye Color", "value": "Green"},
            {"trait_type": "Item", "value": "Book"},
            {"trait_type": "Background", "value": "Pixel"},
        ],
    }

    def test_hashmasks_parser_should_parse_token(self):
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        parser = HashmasksParser(fetcher=fetcher, contract_caller=contract_caller)
        assert parser.should_parse_token(token=self.token)

    def test_hashmasks_parser_parses_metadata(self):
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        fetcher.fetch_mime_type_and_size = MagicMock(return_value=("application/json", 712674))
        fetcher.fetch_content = MagicMock(return_value=self.raw_data)
        parser = HashmasksParser(fetcher=fetcher, contract_caller=contract_caller)
        metadata = parser.parse_metadata(token=self.token, raw_data=self.raw_data)
        assert metadata == Metadata(
            token=Token(
                chain_identifier="ETHEREUM-MAINNET",
                collection_address="0xc2c747e0f7004f9e8817db2ca4997657a7746928",
                token_id=553,
                uri="https://hashmap.azurewebsites.net/getMask/553",
            ),
            raw_data={
                "description": "Hashmask #553",
                "external_url": "https://www.thehashmasks.com/detail/553",
                "image": "https://hashmasksstore.blob.core.windows.net/hashmasks/10694.jpg",
                "attributes": [
                    {"trait_type": "Character", "value": "Male"},
                    {"trait_type": "Mask", "value": "Basic"},
                    {"trait_type": "Skin Color", "value": "Blue"},
                    {"trait_type": "Eye Color", "value": "Green"},
                    {"trait_type": "Item", "value": "Book"},
                    {"trait_type": "Background", "value": "Pixel"},
                ],
            },
            attributes=[
                Attribute(trait_type="Character", value="Male", display_type=None),
                Attribute(trait_type="Mask", value="Basic", display_type=None),
                Attribute(trait_type="Skin Color", value="Blue", display_type=None),
                Attribute(trait_type="Eye Color", value="Green", display_type=None),
                Attribute(trait_type="Item", value="Book", display_type=None),
                Attribute(trait_type="Background", value="Pixel", display_type=None),
            ],
            standard=None,
            name="Satoshi Hashmaskmoto",
            description="Hashmask #553",
            mime_type="application/json",
            image=MediaDetails(
                size=712674,
                sha256=None,
                uri="https://hashmasksstore.blob.core.windows.net/hashmasks/10694.jpg",
                mime_type="application/json",
            ),
            additional_fields=[
                MetadataField(
                    field_name="external_url",
                    type=MetadataFieldType.TEXT,
                    description="This property defines an optional external URL that can reference a webpage or external asset for the NFT",
                    value="https://www.thehashmasks.com/detail/553",
                ),
            ],
        )
