# flake8: noqa: E501

from unittest.mock import MagicMock

from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher
from offchain.metadata.models.metadata import (
    MediaDetails,
    Metadata,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers import FoundationParser
from offchain.web3.contract_caller import ContractCaller


class TestFoundationParser:
    token = Token(
        chain_identifier="ETHEREUM-MAINNET",
        collection_address="0x3b3ee1931dc30c1957379fac9aba94d1c48a5405",
        token_id=113384,
        uri=None,
    )

    raw_data = {
        "name": "Experiment #0004",
        "description": "They rise again!",
        "image": "https://d1hiserqh6k9o1.cloudfront.net/Ax/kk/QmWwB2LXk7VKu5KtDrtUYdwpHK1NvJ49XrQvFRJxqiAxkk/nft.png",
        "animation_url": "ipfs://QmWwB2LXk7VKu5KtDrtUYdwpHK1NvJ49XrQvFRJxqiAxkk/nft.glb",
        "external_url": "https://foundation.app/@pw_3Dlab/foundation/113384",
    }

    def test_foundation_parser_should_parse_token(self):
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        parser = FoundationParser(fetcher=fetcher, contract_caller=contract_caller)
        assert parser.should_parse_token(token=self.token) == True

    def test_foundation_parser_parses_metadata(self):
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        fetcher.fetch_mime_type_and_size = MagicMock(return_value=("application/json", 0))
        fetcher.fetch_content = MagicMock(return_value=self.raw_data)
        parser = FoundationParser(fetcher=fetcher, contract_caller=contract_caller)
        metadata = parser.parse_metadata(token=self.token, raw_data=self.raw_data)
        assert metadata == Metadata(
            token=Token(
                chain_identifier="ETHEREUM-MAINNET",
                collection_address="0x3b3ee1931dc30c1957379fac9aba94d1c48a5405",
                token_id=113384,
                uri="https://api.foundation.app/opensea/113384",
            ),
            raw_data={
                "name": "Experiment #0004",
                "description": "They rise again!",
                "image": "https://d1hiserqh6k9o1.cloudfront.net/Ax/kk/QmWwB2LXk7VKu5KtDrtUYdwpHK1NvJ49XrQvFRJxqiAxkk/nft.png",
                "animation_url": "ipfs://QmWwB2LXk7VKu5KtDrtUYdwpHK1NvJ49XrQvFRJxqiAxkk/nft.glb",
                "external_url": "https://foundation.app/@pw_3Dlab/foundation/113384",
            },
            attributes=[],
            standard=None,
            name="Experiment #0004",
            description="They rise again!",
            mime_type="application/json",
            image=MediaDetails(
                size=0,
                sha256=None,
                uri="https://d1hiserqh6k9o1.cloudfront.net/Ax/kk/QmWwB2LXk7VKu5KtDrtUYdwpHK1NvJ49XrQvFRJxqiAxkk/nft.png",
                mime_type="application/json",
            ),
            content=MediaDetails(
                size=0,
                sha256=None,
                uri="ipfs://QmWwB2LXk7VKu5KtDrtUYdwpHK1NvJ49XrQvFRJxqiAxkk/nft.glb",
                mime_type="model/gltf-binary",
            ),
            additional_fields=[],
        )
