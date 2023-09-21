# flake8: noqa: E501
from unittest.mock import MagicMock, Mock

import pytest

from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher
from offchain.metadata.models.metadata import (
    Attribute,
    MediaDetails,
    Metadata,
    MetadataField,
    MetadataFieldType,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.collection.decentraland import DecentralandParser
from offchain.web3.contract_caller import ContractCaller


class TestDecentralandParser:
    token = Token(
        chain_identifier="ETHEREUM-MAINNET",
        collection_address="0xf87e31492faf9a91b02ee0deaad50d51d56d5d4d",
        token_id=14632141777600353928925108119566033092594,
    )

    raw_data = {
        "attributes": [
            {"display_type": "number", "trait_type": "X", "value": 42},
            {"display_type": "number", "trait_type": "Y", "value": -14},
            {"display_type": "number", "trait_type": "Distance to Road", "value": 6},
        ],
        "background_color": "000000",
        "description": "very close to the center",
        "external_url": "https://market.decentraland.org/contracts/0xf87e31492faf9a91b02ee0deaad50d51d56d5d4d/tokens/14632141777600353928925108119566033092594",
        "id": "14632141777600353928925108119566033092594",
        "image": "https://api.decentraland.org/v2/parcels/42/-14/map.png?size=24&width=1024&height=1024",
        "name": "Dream land",
    }

    def test_decentraland_parser_should_parse_token(self):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        parser = DecentralandParser(fetcher=fetcher, contract_caller=contract_caller)  # type: ignore[abstract]
        assert parser.should_parse_token(token=self.token)

    def test_decentraland_parser_parses_metadata(self):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        fetcher.fetch_mime_type_and_size = Mock(side_effect=[("application/json", 0), ("image/png", 0)])  # type: ignore[assignment]
        fetcher.fetch_content = MagicMock(return_value=self.raw_data)  # type: ignore[assignment]
        parser = DecentralandParser(fetcher=fetcher, contract_caller=contract_caller)  # type: ignore[abstract]
        metadata = parser.parse_metadata(token=self.token, raw_data=self.raw_data)
        assert metadata == Metadata(
            token=Token(
                chain_identifier="ETHEREUM-MAINNET",
                collection_address="0xf87e31492faf9a91b02ee0deaad50d51d56d5d4d",
                token_id=14632141777600353928925108119566033092594,
                uri="https://api.decentraland.org/v2/contracts/0xf87e31492faf9a91b02ee0deaad50d51d56d5d4d/tokens/14632141777600353928925108119566033092594",
            ),
            raw_data={
                "attributes": [
                    {"display_type": "number", "trait_type": "X", "value": 42},
                    {"display_type": "number", "trait_type": "Y", "value": -14},
                    {
                        "display_type": "number",
                        "trait_type": "Distance to Road",
                        "value": 6,
                    },
                ],
                "background_color": "000000",
                "description": "very close to the center",
                "external_url": "https://market.decentraland.org/contracts/0xf87e31492faf9a91b02ee0deaad50d51d56d5d4d/tokens/14632141777600353928925108119566033092594",
                "id": "14632141777600353928925108119566033092594",
                "image": "https://api.decentraland.org/v2/parcels/42/-14/map.png?size=24&width=1024&height=1024",
                "name": "Dream land",
            },
            attributes=[
                Attribute(trait_type="X", value="42", display_type="number"),
                Attribute(trait_type="Y", value="-14", display_type="number"),
                Attribute(
                    trait_type="Distance to Road", value="6", display_type="number"
                ),
            ],
            standard=None,
            name="Dream land",
            description="very close to the center",
            mime_type="application/json",
            image=MediaDetails(
                size=0,
                sha256=None,
                uri="https://api.decentraland.org/v2/parcels/42/-14/map.png?size=24&width=1024&height=1024",
                mime_type="image/png",
            ),
            additional_fields=[
                MetadataField(
                    field_name="external_url",
                    type=MetadataFieldType.TEXT,
                    description="This property defines an optional external URL that can reference a webpage or external asset for the NFT",
                    value="https://market.decentraland.org/contracts/0xf87e31492faf9a91b02ee0deaad50d51d56d5d4d/tokens/14632141777600353928925108119566033092594",
                ),
                MetadataField(
                    field_name="id",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the ID for the NFT asset",
                    value="14632141777600353928925108119566033092594",
                ),
                MetadataField(
                    field_name="background_color",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the background color for the NFT asset",
                    value="000000",
                ),
            ],
        )

    @pytest.mark.asyncio
    async def test_decentraland_parser_gen_parses_metadata(self):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        parser = DecentralandParser(fetcher=fetcher, contract_caller=contract_caller)  # type: ignore[abstract]
        metadata = await parser.gen_parse_metadata(
            token=self.token, raw_data=self.raw_data
        )
        assert metadata
