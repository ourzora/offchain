# flake8: noqa: E501
from pprint import pprint
from unittest.mock import MagicMock, Mock

from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher
from offchain.metadata.models.metadata import (
    MediaDetails,
    Metadata,
    Attribute,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers import MakersPlaceParser
from offchain.web3.contract_caller import ContractCaller


class TestMakersPlaceParser:
    token = Token(
        chain_identifier="ETHEREUM-MAINNET",
        collection_address="0x2a46f2ffd99e19a89476e2f62270e0a35bbf0756",
        token_id=68710,
        uri=None,
    )

    raw_data = {
        "attributes": [{"trait_type": "Creator", "value": "Tyrone Doyle"}],
        "description": "using python in cinema 4d",
        "imageUrl": "https://ipfsgateway.makersplace.com/ipfs/QmRP5shGPgRAuRpfJRi36ABgUd4zABGZ4XmB8s3CedipNK",
        "name": "Infinite library",
        "properties": {
            "created_at": {
                "description": "2020-12-29T10:51:53.986624+00:00",
                "type": "datetime",
            },
            "description": {
                "description": "using python in " "cinema 4d",
                "type": "string",
            },
            "digital_media_signature": {
                "description": "83bf7f1157d43054d840317a919f937ad85269fb3ec29dfdc8d8ca52813b3d10",
                "type": "string",
            },
            "digital_media_signature_type": {
                "description": "SHA-256",
                "type": "string",
            },
            "name": {"description": "Infinite library", "type": "string"},
            "preview_media_file": {
                "description": "https://ipfsgateway.makersplace.com/ipfs/QmRP5shGPgRAuRpfJRi36ABgUd4zABGZ4XmB8s3CedipNK",
                "type": "string",
            },
            "preview_media_file2": {
                "description": "https://ipfsgateway.makersplace.com/ipfs/QmUB4EhNRT3KpLrpp2Nc6ZtcQrDLg7hdGhF4Y2fe94WD12",
                "type": "string",
            },
            "preview_media_file2_type": {"description": "mp4", "type": "string"},
            "preview_media_file_type": {"description": "jpg", "type": "string"},
            "total_supply": {"description": 1, "type": "int"},
        },
        "title": "Infinite library",
        "type": "object",
    }

    def test_makersplace_parser_should_parse_token(self):
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        parser = MakersPlaceParser(fetcher=fetcher, contract_caller=contract_caller)
        assert parser.should_parse_token(token=self.token) == True

    def test_makersplace_parser_parses_metadata(self):
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        fetcher.fetch_mime_type_and_size = Mock(
            side_effect=[
                ("application/json", 0),
                ("image/jpeg", 1605069),
                ("video/mp4", 5644701),
            ]
        )
        # fix this test later
        # fetcher.fetch_content = MagicMock(return_value=self.raw_data)
        parser = MakersPlaceParser(fetcher=fetcher, contract_caller=contract_caller)
        metadata = parser.parse_metadata(token=self.token, raw_data=self.raw_data)
        assert metadata == Metadata(
            token=Token(
                collection_address="0x2a46f2ffd99e19a89476e2f62270e0a35bbf0756",
                token_id=68710,
                chain_identifier="ETHEREUM-MAINNET",
                uri="https://ipfsgateway.makersplace.com/ipfs/QmSsMzC8zTJvyVJzUifpnBx6zFGFxNvtQVhJq7H8T1oCnr",
            ),
            raw_data={
                "title": "Infinite library",
                "name": "Infinite library",
                "type": "object",
                "imageUrl": "https://ipfsgateway.makersplace.com/ipfs/QmRP5shGPgRAuRpfJRi36ABgUd4zABGZ4XmB8s3CedipNK",
                "description": "using python in cinema 4d",
                "attributes": [{"trait_type": "Creator", "value": "Tyrone Doyle"}],
                "properties": {
                    "name": {"type": "string", "description": "Infinite library"},
                    "description": {
                        "type": "string",
                        "description": "using python in cinema 4d",
                    },
                    "preview_media_file": {
                        "type": "string",
                        "description": "https://ipfsgateway.makersplace.com/ipfs/QmRP5shGPgRAuRpfJRi36ABgUd4zABGZ4XmB8s3CedipNK",
                    },
                    "preview_media_file_type": {"type": "string", "description": "jpg"},
                    "created_at": {
                        "type": "datetime",
                        "description": "2020-12-29T10:51:53.986624+00:00",
                    },
                    "total_supply": {"type": "int", "description": 1},
                    "digital_media_signature_type": {
                        "type": "string",
                        "description": "SHA-256",
                    },
                    "digital_media_signature": {
                        "type": "string",
                        "description": "83bf7f1157d43054d840317a919f937ad85269fb3ec29dfdc8d8ca52813b3d10",
                    },
                    "preview_media_file2": {
                        "type": "string",
                        "description": "https://ipfsgateway.makersplace.com/ipfs/QmUB4EhNRT3KpLrpp2Nc6ZtcQrDLg7hdGhF4Y2fe94WD12",
                    },
                    "preview_media_file2_type": {
                        "type": "string",
                        "description": "mp4",
                    },
                },
            },
            attributes=[
                Attribute(trait_type="name", value="Infinite library", display_type="string"),
                Attribute(
                    trait_type="description",
                    value="using python in cinema 4d",
                    display_type="string",
                ),
                Attribute(
                    trait_type="preview_media_file",
                    value="https://ipfsgateway.makersplace.com/ipfs/QmRP5shGPgRAuRpfJRi36ABgUd4zABGZ4XmB8s3CedipNK",
                    display_type="string",
                ),
                Attribute(
                    trait_type="preview_media_file_type",
                    value="jpg",
                    display_type="string",
                ),
                Attribute(
                    trait_type="created_at",
                    value="2020-12-29T10:51:53.986624+00:00",
                    display_type="datetime",
                ),
                Attribute(trait_type="total_supply", value="1", display_type="int"),
                Attribute(
                    trait_type="digital_media_signature_type",
                    value="SHA-256",
                    display_type="string",
                ),
                Attribute(
                    trait_type="digital_media_signature",
                    value="83bf7f1157d43054d840317a919f937ad85269fb3ec29dfdc8d8ca52813b3d10",
                    display_type="string",
                ),
                Attribute(
                    trait_type="preview_media_file2",
                    value="https://ipfsgateway.makersplace.com/ipfs/QmUB4EhNRT3KpLrpp2Nc6ZtcQrDLg7hdGhF4Y2fe94WD12",
                    display_type="string",
                ),
                Attribute(
                    trait_type="preview_media_file2_type",
                    value="mp4",
                    display_type="string",
                ),
                Attribute(trait_type="Creator", value="Tyrone Doyle", display_type=None),
            ],
            standard=None,
            name="Infinite library",
            description="using python in cinema 4d",
            mime_type="application/json",
            image=MediaDetails(
                size=1605069,
                sha256=None,
                uri="https://ipfsgateway.makersplace.com/ipfs/QmRP5shGPgRAuRpfJRi36ABgUd4zABGZ4XmB8s3CedipNK",
                mime_type="image/jpeg",
            ),
            content=MediaDetails(
                size=5644701,
                sha256=None,
                uri="https://ipfsgateway.makersplace.com/ipfs/QmUB4EhNRT3KpLrpp2Nc6ZtcQrDLg7hdGhF4Y2fe94WD12",
                mime_type="video/mp4",
            ),
            additional_fields=[],
        )
