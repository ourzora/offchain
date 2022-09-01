# flake8: noqa: E501
from unittest.mock import MagicMock

from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher
from offchain.metadata.models.metadata import (
    MediaDetails,
    Metadata,
    Attribute,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers import ChainRunnersParser
from offchain.web3.contract_caller import ContractCaller


class TestChainRunnersParser:
    token = Token(
        chain_identifier="ETHEREUM-MAINNET",
        collection_address="0x97597002980134bea46250aa0510c9b90d87a587",
        token_id=484,
        uri=None,
    )

    raw_data = {
        "name": "Runner #484",
        "description": "Chain Runners are Mega City renegades 100% generated on chain.",
        "attributes": [
            {"trait_type": "Background", "value": "Peach Blue Vert"},
            {"trait_type": "Race", "value": "Human"},
            {"trait_type": "Mouth", "value": "Teethy Grin"},
            {"trait_type": "Nose", "value": "Downturned"},
            {"trait_type": "Eyes", "value": "Beady Variant 1"},
            {"trait_type": "Ear Accessory", "value": "Gold Stud Earrings"},
            {"trait_type": "Face Accessory", "value": "Oni Mask Red"},
            {"trait_type": "Head Below", "value": "Cornrows Dark Topknot Hair"},
        ],
        "image": "https://img.chainrunners.xyz/api/v1/tokens/png/484",
    }

    def test_chainrunners_parser_should_parse_token(self):
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        parser = ChainRunnersParser(fetcher=fetcher, contract_caller=contract_caller)
        assert parser.should_parse_token(token=self.token) == True

    def test_chainrunners_parser_parses_metadata(self):
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        fetcher.fetch_mime_type_and_size = MagicMock(return_value=("application/json", 0))
        fetcher.fetch_content = MagicMock(return_value=self.raw_data)
        parser = ChainRunnersParser(fetcher=fetcher, contract_caller=contract_caller)
        metadata = parser.parse_metadata(token=self.token, raw_data=self.raw_data)
        assert metadata == Metadata(
            token=Token(
                chain_identifier="ETHEREUM-MAINNET",
                collection_address="0x97597002980134bea46250aa0510c9b90d87a587",
                token_id=484,
                uri="https://api.chainrunners.xyz/tokens/metadata/484"
                "?dna=25123093727902066427844701658307416778734511262743439751758719408481279775970",
            ),
            raw_data={
                "name": "Runner #484",
                "description": "Chain Runners are Mega City renegades 100% generated on chain.",
                "attributes": [
                    {"trait_type": "Background", "value": "Peach Blue Vert"},
                    {"trait_type": "Race", "value": "Human"},
                    {"trait_type": "Mouth", "value": "Teethy Grin"},
                    {"trait_type": "Nose", "value": "Downturned"},
                    {"trait_type": "Eyes", "value": "Beady Variant 1"},
                    {"trait_type": "Ear Accessory", "value": "Gold Stud Earrings"},
                    {"trait_type": "Face Accessory", "value": "Oni Mask Red"},
                    {"trait_type": "Head Below", "value": "Cornrows Dark Topknot Hair"},
                ],
                "image": "https://img.chainrunners.xyz/api/v1/tokens/png/484",
            },
            attributes=[
                Attribute(trait_type="Background", value="Peach Blue Vert", display_type=None),
                Attribute(trait_type="Race", value="Human", display_type=None),
                Attribute(trait_type="Mouth", value="Teethy Grin", display_type=None),
                Attribute(trait_type="Nose", value="Downturned", display_type=None),
                Attribute(trait_type="Eyes", value="Beady Variant 1", display_type=None),
                Attribute(
                    trait_type="Ear Accessory",
                    value="Gold Stud Earrings",
                    display_type=None,
                ),
                Attribute(trait_type="Face Accessory", value="Oni Mask Red", display_type=None),
                Attribute(
                    trait_type="Head Below",
                    value="Cornrows Dark Topknot Hair",
                    display_type=None,
                ),
            ],
            standard=None,
            name="Runner #484",
            description="Chain Runners are Mega City renegades 100% generated on chain.",
            mime_type="application/json",
            image=MediaDetails(
                size=0,
                sha256=None,
                uri="https://img.chainrunners.xyz/api/v1/tokens/png/484",
                mime_type="application/json",
            ),
            additional_fields=[],
        )
