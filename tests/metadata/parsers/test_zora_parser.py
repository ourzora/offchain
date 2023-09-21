# flake8: noqa: E501
from unittest.mock import Mock, MagicMock

from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher
from offchain.metadata.models.metadata import (
    MediaDetails,
    Metadata,
    MetadataField,
    MetadataFieldType,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.collection.zora import ZoraParser
from offchain.web3.contract_caller import ContractCaller


class TestZoraParser:
    token = Token(
        chain_identifier="ETHEREUM-MAINNET",
        collection_address="0xabefbc9fd2f806065b4f3c237d4b59d9a97bcac7",
        token_id=5769,
    )

    raw_data = {
        "description": "A Lonely Soul,\n\nI've felt lonely lately. Somewhere deep inside, detached. \n\nThere must be plenty of lost souls wandering the globe. Looking to belong; to understand their purpose.\n\nI know my purpose, but I fear I've burned up surviving to the moment.\n\nDoes this count?\nAm I still pushing forward?\n\nI hope so...\n\nDo I still have time?\nAm I just floating?\n\nPlease, don't give up.\n\nAge 23 (2021)\n4096x4096px",
        "mimeType": "image/jpeg",
        "name": "Reform: A Lonely Soul",
        "version": "zora-20210101",
    }

    def test_zora_parser_should_parse_token(self):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        parser = ZoraParser(fetcher=fetcher, contract_caller=contract_caller)  # type: ignore[abstract]
        assert parser.should_parse_token(token=self.token)

    def test_zora_parser_parses_metadata(self):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        fetcher.fetch_mime_type_and_size = Mock(side_effect=[("application/json", 0), ("image/jpeg", 13548199)])  # type: ignore[assignment]
        fetcher.fetch_content = MagicMock(return_value=self.raw_data)  # type: ignore[assignment]
        parser = ZoraParser(fetcher=fetcher, contract_caller=contract_caller)  # type: ignore[abstract]
        metadata = parser.parse_metadata(token=self.token, raw_data=self.raw_data)
        assert metadata == Metadata(
            token=Token(
                chain_identifier="ETHEREUM-MAINNET",
                collection_address="0xabefbc9fd2f806065b4f3c237d4b59d9a97bcac7",
                token_id=5769,
                uri="https://zora-dev.mypinata.cloud/ipfs/bafkreigux6jujn5hvlmptgzgok4reaie2gkuvsk2kynnalsyfgr4g35dkm",
            ),
            raw_data={
                "description": "A Lonely Soul,\n\nI've felt lonely lately. Somewhere deep inside, detached. \n\nThere must be plenty of lost souls wandering the globe. Looking to belong; to understand their purpose.\n\nI know my purpose, but I fear I've burned up surviving to the moment.\n\nDoes this count?\nAm I still pushing forward?\n\nI hope so...\n\nDo I still have time?\nAm I just floating?\n\nPlease, don't give up.\n\nAge 23 (2021)\n4096x4096px",
                "mimeType": "image/jpeg",
                "name": "Reform: A Lonely Soul",
                "version": "zora-20210101",
            },
            attributes=[],
            standard=None,
            name="Reform: A Lonely Soul",
            description="A Lonely Soul,\n\nI've felt lonely lately. Somewhere deep inside, detached. \n\nThere must be plenty of lost souls wandering the globe. Looking to belong; to understand their purpose.\n\nI know my purpose, but I fear I've burned up surviving to the moment.\n\nDoes this count?\nAm I still pushing forward?\n\nI hope so...\n\nDo I still have time?\nAm I just floating?\n\nPlease, don't give up.\n\nAge 23 (2021)\n4096x4096px",
            mime_type="application/json",
            image=MediaDetails(
                size=13548199,
                sha256=None,
                uri="https://zora-dev.mypinata.cloud/ipfs/bafybeiffwxjez2axebcprj2h7wkohr2pdbvuv37f7uxyptuw7o6t5fvppu",
                mime_type="image/jpeg",
            ),
            content=None,
            additional_fields=[
                MetadataField(
                    field_name="version",
                    type=MetadataFieldType.TEXT,
                    description="Zora Metadata version",
                    value="zora-20210101",
                )
            ],
        )
