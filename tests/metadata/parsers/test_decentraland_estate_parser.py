# flake8: noqa: E501
from unittest.mock import MagicMock, Mock

from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher
from offchain.metadata.models.metadata import (
    MediaDetails,
    Metadata,
    MetadataField,
    MetadataFieldType,
    Attribute,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.collection.decentraland import DecentralandParser
from offchain.web3.contract_caller import ContractCaller


class TestDecentralandEstateParser:
    token = Token(
        chain_identifier="ETHEREUM-MAINNET",
        collection_address="0x959e104e1a4db6317fa58f8295f586e1a978c297",
        token_id=4550,
    )

    raw_data = {
        "id": "4550",
        "name": "The Ocean Meta",
        "description": "",
        "image": "https://api.decentraland.org/v2/estates/4550/map.png?size=24&width=1024&height=1024",
        "external_url": "https://market.decentraland.org/contracts/0x959e104e1a4db6317fa58f8295f586e1a978c297/tokens/4550",
        "attributes": [
            {"trait_type": "Size", "value": 2, "display_type": "number"},
            {
                "trait_type": "Distance to District",
                "value": 8,
                "display_type": "number",
            },
            {"trait_type": "Distance to Road", "value": 6, "display_type": "number"},
        ],
        "background_color": "000000",
    }

    def test_decentraland_estate_parser_should_parse_token(self):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        parser = DecentralandParser(fetcher=fetcher, contract_caller=contract_caller)  # type: ignore[abstract]
        assert parser.should_parse_token(token=self.token)

    def test_decentraland_estate_parser_parses_metadata(self):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        fetcher.fetch_mime_type_and_size = Mock(side_effect=[("application/json", 0), ("image/png", 0)])  # type: ignore[assignment]
        fetcher.fetch_content = MagicMock(return_value=self.raw_data)  # type: ignore[assignment]
        parser = DecentralandParser(fetcher=fetcher, contract_caller=contract_caller)  # type: ignore[abstract]
        metadata = parser.parse_metadata(token=self.token, raw_data=self.raw_data)
        assert metadata == Metadata(
            token=Token(
                chain_identifier="ETHEREUM-MAINNET",
                collection_address="0x959e104e1a4db6317fa58f8295f586e1a978c297",
                token_id=4550,
                uri="https://api.decentraland.org/v2/contracts/0x959e104e1a4db6317fa58f8295f586e1a978c297/tokens/4550",
            ),
            raw_data={
                "id": "4550",
                "name": "The Ocean Meta",
                "description": "",
                "image": "https://api.decentraland.org/v2/estates/4550/map.png?size=24&width=1024&height=1024",
                "external_url": "https://market.decentraland.org/contracts/0x959e104e1a4db6317fa58f8295f586e1a978c297/tokens/4550",
                "attributes": [
                    {"trait_type": "Size", "value": 2, "display_type": "number"},
                    {
                        "trait_type": "Distance to District",
                        "value": 8,
                        "display_type": "number",
                    },
                    {
                        "trait_type": "Distance to Road",
                        "value": 6,
                        "display_type": "number",
                    },
                ],
                "background_color": "000000",
            },
            attributes=[
                Attribute(trait_type="Size", value="2", display_type="number"),
                Attribute(
                    trait_type="Distance to District", value="8", display_type="number"
                ),
                Attribute(
                    trait_type="Distance to Road", value="6", display_type="number"
                ),
            ],
            standard=None,
            name="The Ocean Meta",
            description="",
            mime_type="application/json",
            image=MediaDetails(
                size=0,
                sha256=None,
                uri="https://api.decentraland.org/v2/estates/4550/map.png?size=24&width=1024&height=1024",
                mime_type="image/png",
            ),
            additional_fields=[
                MetadataField(
                    field_name="external_url",
                    type=MetadataFieldType.TEXT,
                    description="This property defines an optional external URL that can reference a webpage or external asset for the NFT",
                    value="https://market.decentraland.org/contracts/0x959e104e1a4db6317fa58f8295f586e1a978c297/tokens/4550",
                ),
                MetadataField(
                    field_name="id",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the ID for the NFT asset",
                    value="4550",
                ),
                MetadataField(
                    field_name="background_color",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the background color for the NFT asset",
                    value="000000",
                ),
            ],
        )
