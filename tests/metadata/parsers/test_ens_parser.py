# flake8: noqa: E501

from unittest.mock import MagicMock

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
from offchain.metadata.parsers import ENSParser  # type: ignore[attr-defined]
from offchain.web3.contract_caller import ContractCaller


class TestENSParser:
    token = Token(
        chain_identifier="ETHEREUM-MAINNET",
        collection_address="0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85",
        token_id=10110056301157368922112380646085332716736091604887080310048917803187113883396,
    )

    raw_data = {
        "is_normalized": True,
        "name": "steev.eth",
        "description": "steev.eth, an ENS name.",
        "attributes": [
            {
                "trait_type": "Created Date",
                "display_type": "date",
                "value": 1633123738000,
            },
            {"trait_type": "Length", "display_type": "number", "value": 5},
            {"trait_type": "Segment Length", "display_type": "number", "value": 5},
            {
                "trait_type": "Character Set",
                "display_type": "string",
                "value": "letter",
            },
            {
                "trait_type": "Registration Date",
                "display_type": "date",
                "value": 1633123738000,
            },
            {
                "trait_type": "Expiration Date",
                "display_type": "date",
                "value": 1822465450000,
            },
        ],
        "name_length": 5,
        "segment_length": 5,
        "url": "https://app.ens.domains/name/steev.eth",
        "version": 0,
        "background_image": "https://metadata.ens.domains/mainnet/avatar/steev.eth",
        "image": "https://metadata.ens.domains/mainnet/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/0x165a16ce2915e51295772b6a67bfc8ceee2c1c7caa85591fba107af4ee24f704/image",
        "image_url": "https://metadata.ens.domains/mainnet/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/0x165a16ce2915e51295772b6a67bfc8ceee2c1c7caa85591fba107af4ee24f704/image",
    }

    def test_ens_parser_should_parse_token(self):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        parser = ENSParser(fetcher=fetcher, contract_caller=contract_caller)  # type: ignore[abstract]
        assert parser.should_parse_token(token=self.token) == True

    def test_ens_parser_parses_metadata(self):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        fetcher.fetch_mime_type_and_size = MagicMock(return_value=("application/json", 0))  # type: ignore[assignment]
        fetcher.fetch_content = MagicMock(return_value=self.raw_data)  # type: ignore[assignment]
        parser = ENSParser(fetcher=fetcher, contract_caller=contract_caller)  # type: ignore[abstract]
        metadata = parser.parse_metadata(token=self.token, raw_data=None)  # type: ignore[arg-type]
        assert metadata == Metadata(
            token=Token(
                chain_identifier="ETHEREUM-MAINNET",
                collection_address="0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85",
                token_id=10110056301157368922112380646085332716736091604887080310048917803187113883396,
                uri="https://metadata.ens.domains/mainnet/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/10110056301157368922112380646085332716736091604887080310048917803187113883396/",
            ),
            raw_data={
                "is_normalized": True,
                "name": "steev.eth",
                "description": "steev.eth, an ENS name.",
                "attributes": [
                    {
                        "trait_type": "Created Date",
                        "display_type": "date",
                        "value": 1633123738000,
                    },
                    {"trait_type": "Length", "display_type": "number", "value": 5},
                    {
                        "trait_type": "Segment Length",
                        "display_type": "number",
                        "value": 5,
                    },
                    {
                        "trait_type": "Character Set",
                        "display_type": "string",
                        "value": "letter",
                    },
                    {
                        "trait_type": "Registration Date",
                        "display_type": "date",
                        "value": 1633123738000,
                    },
                    {
                        "trait_type": "Expiration Date",
                        "display_type": "date",
                        "value": 1822465450000,
                    },
                ],
                "name_length": 5,
                "segment_length": 5,
                "url": "https://app.ens.domains/name/steev.eth",
                "version": 0,
                "background_image": "https://metadata.ens.domains/mainnet/avatar/steev.eth",
                "image": "https://metadata.ens.domains/mainnet/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/0x165a16ce2915e51295772b6a67bfc8ceee2c1c7caa85591fba107af4ee24f704/image",
                "image_url": "https://metadata.ens.domains/mainnet/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/0x165a16ce2915e51295772b6a67bfc8ceee2c1c7caa85591fba107af4ee24f704/image",
            },
            attributes=[
                Attribute(
                    trait_type="Created Date",
                    value="1633123738000",
                    display_type="date",
                ),
                Attribute(trait_type="Length", value="5", display_type="number"),
                Attribute(
                    trait_type="Segment Length", value="5", display_type="number"
                ),
                Attribute(
                    trait_type="Character Set", value="letter", display_type="string"
                ),
                Attribute(
                    trait_type="Registration Date",
                    value="1633123738000",
                    display_type="date",
                ),
                Attribute(
                    trait_type="Expiration Date",
                    value="1822465450000",
                    display_type="date",
                ),
            ],
            standard=None,
            name="steev.eth",
            description="steev.eth, an ENS name.",
            mime_type="application/json",
            image=MediaDetails(
                size=0,
                sha256=None,
                uri="https://metadata.ens.domains/mainnet/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/0x165a16ce2915e51295772b6a67bfc8ceee2c1c7caa85591fba107af4ee24f704/image",
                mime_type="application/json",
            ),
            content=MediaDetails(
                size=0,
                sha256=None,
                uri="https://metadata.ens.domains/mainnet/avatar/steev.eth",
                mime_type="application/json",
            ),
            additional_fields=[
                MetadataField(
                    field_name="name_length",
                    type=MetadataFieldType.TEXT,
                    description="Character length of ens name",
                    value=5,
                ),
                MetadataField(
                    field_name="url",
                    type=MetadataFieldType.TEXT,
                    description="ENS App URL of the name",
                    value="https://app.ens.domains/name/steev.eth",
                ),
            ],
        )

    @pytest.mark.asyncio
    async def test_ens_parser_gen_parses_metadata(self):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        parser = ENSParser(fetcher=fetcher, contract_caller=contract_caller)  # type: ignore[abstract]
        metadata = await parser.gen_parse_metadata(token=self.token, raw_data=None)  # type: ignore[arg-type]
        assert metadata
