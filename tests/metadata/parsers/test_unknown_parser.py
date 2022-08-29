# flake8: noqa: E501

from unittest.mock import MagicMock

from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher
from offchain.metadata.models.metadata import (
    Metadata,
    MetadataStandard,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.schema.unknown import UnknownParser


class TestUnknownParser:
    token = Token(
        chain_identifier="ETHEREUM-MAINNET",
        collection_address="0x74cb086a1611cc9ca672f458b7742dd4159ac9db",
        token_id="80071",
        uri="https://api.dego.finance/gego-token-v2/80071",
    )
    raw_data = {
        "status": 10000,
        "result": {
            "data": {
                "name": "KuCoin Mining Tram",
                "description": "Without it, you cannot even find the door",
                "i18n_name": "nft_0022",
                "i18n_description": "nft_0023",
                "small_image": "https://dego.finance/upload/small/kucoin_1.png",
                "big_image": "https://dego.finance/upload/big/kucoin_1.png",
                "auction_image": "",
                "video": "",
                "id": "80071",
                "external_url": "https://api.dego.finance/gego-token-v2/80071",
                "attributes": {
                    "grade": "1",
                    "quality": "1969",
                    "amount": "29400000000000000000",
                    "resBaseId": "2",
                    "tLevel": "1",
                    "ruleId": "1",
                    "nftType": "2",
                    "author": "0x5528711420D3Cf07043C536e419c13218D7BaB30",
                    "erc20": "0x88EF27e69108B2633F8E1C184CC37940A075cC02",
                    "createdTime": "1603588635",
                    "blockNum": "11122588",
                    "resId": "10000121",
                    "erc20_value": "29.4 DEGO",
                },
            }
        },
    }

    def test_unknown_parser_should_parse_token(self):
        fetcher = MetadataFetcher()
        parser = UnknownParser(fetcher=fetcher)
        assert parser.should_parse_token(token=self.token, raw_data=self.raw_data) == True

    def test_unknown_parser_parses_metadata(self):
        fetcher = MetadataFetcher()
        fetcher.fetch_mime_type_and_size = MagicMock(return_value=(None, 0))
        parser = UnknownParser(fetcher=fetcher)
        metadata = parser.parse_metadata(token=self.token, raw_data=self.raw_data)
        assert metadata == Metadata(
            token=self.token,
            raw_data={
                "status": 10000,
                "result": {
                    "data": {
                        "name": "KuCoin Mining Tram",
                        "description": "Without it, you cannot even find the door",
                        "i18n_name": "nft_0022",
                        "i18n_description": "nft_0023",
                        "small_image": "https://dego.finance/upload/small/kucoin_1.png",
                        "big_image": "https://dego.finance/upload/big/kucoin_1.png",
                        "auction_image": "",
                        "video": "",
                        "id": "80071",
                        "external_url": "https://api.dego.finance/gego-token-v2/80071",
                        "attributes": {
                            "grade": "1",
                            "quality": "1969",
                            "amount": "29400000000000000000",
                            "resBaseId": "2",
                            "tLevel": "1",
                            "ruleId": "1",
                            "nftType": "2",
                            "author": "0x5528711420D3Cf07043C536e419c13218D7BaB30",
                            "erc20": "0x88EF27e69108B2633F8E1C184CC37940A075cC02",
                            "createdTime": "1603588635",
                            "blockNum": "11122588",
                            "resId": "10000121",
                            "erc20_value": "29.4 DEGO",
                        },
                    }
                },
            },
            standard=MetadataStandard.UNKNOWN,
            attributes=[],
            name=None,
            description=None,
            mime_type=None,
            image=None,
            content=None,
            additional_fields=[],
        )
