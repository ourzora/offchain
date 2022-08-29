# flake8: noqa: E501

from unittest.mock import MagicMock

from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher
from offchain.metadata.models.metadata import (
    MediaDetails,
    Metadata,
    MetadataField,
    MetadataFieldType,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers import SuperRareParser
from offchain.web3.contract_caller import ContractCaller


class TestSuperRareParser:
    token = Token(
        chain_identifier="ETHEREUM-MAINNET",
        collection_address="0xb932a70a57673d89f4acffbe830e8ed7f75fb9e0",
        token_id=8724,
        uri="https://ipfs.pixura.io/ipfs/QmRhDdj22ZkcrHzaxTixew8k9uNC6kpum6SDeWmDgPMqRX/metadata.json",
    )

    raw_data = {
        "name": "Path Tracer",
        "createdBy": "Scott Darby",
        "yearCreated": "2020",
        "description": "Path Tracer",
        "image": "https://ipfs.pixura.io/ipfs/QmV1F4gXFtpAueQcQxQUx96cc1GQK5BNtgmAt48rJSAxCm/yarn.jpg",
        "media": {
            "uri": "https://ipfs.pixura.io/ipfs/QmcdWQmrRsBkNAjQWQ9AGYdaL6zHeAajx9wg46Nnq3YWMA/PathTracer.mp4",
            "dimensions": "1024x1024",
            "size": "19444353",
            "mimeType": "video/mp4",
        },
        "tags": [
            "3d",
            "procedural",
            "generative",
            "light",
            "glass",
            "trail",
            "trace",
            "animation",
            "scottdarby",
            "abstract",
            "loop",
            "blue",
            "flow",
        ],
    }

    def test_superrare_parser_should_parse_token(self):
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        parser = SuperRareParser(fetcher=fetcher, contract_caller=contract_caller)
        assert parser.should_parse_token(token=self.token) == True

    def test_superrare_parser_parses_metadata(self):
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        fetcher.fetch_mime_type_and_size = MagicMock(return_value=("application/json", 0))
        fetcher.fetch_content = MagicMock(return_value=self.raw_data)
        parser = SuperRareParser(fetcher=fetcher, contract_caller=contract_caller)
        metadata = parser.parse_metadata(token=self.token, raw_data=self.raw_data)
        assert metadata == Metadata(
            token=self.token,
            raw_data=self.raw_data,
            attributes=[],
            standard=None,
            name="Path Tracer",
            description="Path Tracer",
            mime_type="application/json",
            image=MediaDetails(
                size=0,
                sha256=None,
                uri="https://ipfs.pixura.io/ipfs/QmV1F4gXFtpAueQcQxQUx96cc1GQK5BNtgmAt48rJSAxCm/yarn.jpg",
                mime_type="application/json",
            ),
            content=MediaDetails(
                size=19444353,
                sha256=None,
                uri="https://ipfs.pixura.io/ipfs/QmcdWQmrRsBkNAjQWQ9AGYdaL6zHeAajx9wg46Nnq3YWMA/PathTracer.mp4",
                mime_type="video/mp4",
            ),
            additional_fields=[
                MetadataField(
                    field_name="created_by",
                    type=MetadataFieldType.TEXT,
                    description="The creator of an NFT.",
                    value="Scott Darby",
                ),
                MetadataField(
                    field_name="year_created",
                    type=MetadataFieldType.NUMBER,
                    description="The year in which an NFT was created.",
                    value="2020",
                ),
                MetadataField(
                    field_name="tags",
                    type=MetadataFieldType.LIST,
                    description="List of tags associated with an NFT.",
                    value=[
                        "3d",
                        "procedural",
                        "generative",
                        "light",
                        "glass",
                        "trail",
                        "trace",
                        "animation",
                        "scottdarby",
                        "abstract",
                        "loop",
                        "blue",
                        "flow",
                    ],
                ),
            ],
        )
