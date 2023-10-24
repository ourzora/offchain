# flake8: noqa: E501

from typing import Tuple
from unittest.mock import AsyncMock, MagicMock

import pytest

from offchain.metadata.adapters.http_adapter import HTTPAdapter
from offchain.metadata.adapters.ipfs import IPFSAdapter
from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher
from offchain.metadata.models.metadata import (
    Attribute,
    MediaDetails,
    Metadata,
    MetadataField,
    MetadataFieldType,
    MetadataStandard,
)
from offchain.metadata.models.metadata_processing_error import MetadataProcessingError
from offchain.metadata.models.token import Token
from offchain.metadata.pipelines.metadata_pipeline import (  # type: ignore[attr-defined]
    AdapterConfig,
    MetadataPipeline,
)
from offchain.web3.contract_caller import ContractCaller
from offchain.web3.jsonrpc import EthereumJSONRPC


class TestMetadataPipeline:
    def test_metadata_pipeline_mounts_adapters(self):  # type: ignore[no-untyped-def]
        pipeline = MetadataPipeline(
            adapter_configs=[
                AdapterConfig(
                    adapter_cls=HTTPAdapter,
                    mount_prefixes=["https://", "http://"],
                    kwargs={
                        "pool_connections": 100,
                        "pool_maxsize": 1000,
                        "max_retries": 0,
                    },
                )
            ]
        )
        assert isinstance(
            pipeline.fetcher.sess.get_adapter(  # type: ignore[attr-defined]
                "https://api.sorare.com/api/v1/cards/91116343315175353437320038031158839194898416502213211151306930097337986202850"
            ),
            HTTPAdapter,
        )
        ipfs_adapter = IPFSAdapter(
            pool_connections=100, pool_maxsize=1000, max_retries=0
        )
        pipeline.mount_adapter(
            ipfs_adapter,
            ["ipfs://"],
        )
        assert (
            pipeline.fetcher.sess.get_adapter("ipfs://QmQZaQ8pgRAWN7TE9QZdYBd43VG7b54m42XmhBFW5ZZKMy/150.json")  # type: ignore[attr-defined]
            == ipfs_adapter
        )

    def test_metadata_pipeline_fetch_token_uri(self, raw_crypto_coven_metadata):  # type: ignore[no-untyped-def]
        token = Token(
            chain_identifier="ETHEREUM-MAINNET",
            collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
            token_id="1",
        )

        fetcher = MetadataFetcher()
        fetcher.fetch_content = MagicMock(return_value=raw_crypto_coven_metadata)  # type: ignore[assignment]
        fetcher.fetch_mime_type_and_size = MagicMock(return_value=("application/json", "3095"))  # type: ignore[assignment]

        pipeline = MetadataPipeline(fetcher=fetcher)
        mock_fetch_token_uri = MagicMock()
        pipeline.fetch_token_uri = mock_fetch_token_uri  # type: ignore[assignment]
        pipeline.run([token])
        mock_fetch_token_uri.assert_called_once_with(token)

    def test_metadata_pipeline_fetch_token_metadata(self, raw_crypto_coven_metadata):  # type: ignore[no-untyped-def]
        token = Token(
            chain_identifier="ETHEREUM-MAINNET",
            collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
            token_id="1",
            uri="ipfs://QmSr3vdMuP2fSxWD7S26KzzBWcAN1eNhm4hk1qaR3x3vmj/1.json",
        )

        fetcher = MetadataFetcher()
        fetcher.fetch_content = MagicMock(return_value=raw_crypto_coven_metadata)  # type: ignore[assignment]
        fetcher.fetch_mime_type_and_size = MagicMock(return_value=("application/json", "3095"))  # type: ignore[assignment]

        pipeline = MetadataPipeline(fetcher=fetcher)
        pipeline.fetch_token_metadata(token=token) == Metadata(
            token=token,
            raw_data=raw_crypto_coven_metadata,
            standard=MetadataStandard.OPENSEA_STANDARD,
            attributes=[
                Attribute(trait_type="Background", value="Sepia", display_type=None),
                Attribute(trait_type="Skin Tone", value="Dawn", display_type=None),
                Attribute(trait_type="Body Shape", value="Lithe", display_type=None),
                Attribute(
                    trait_type="Top", value="Sheer Top (Black)", display_type=None
                ),
                Attribute(
                    trait_type="Eyebrows",
                    value="Medium Flat (Black)",
                    display_type=None,
                ),
                Attribute(trait_type="Eye Style", value="Nyx", display_type=None),
                Attribute(trait_type="Eye Color", value="Cloud", display_type=None),
                Attribute(trait_type="Mouth", value="Nyx (Mocha)", display_type=None),
                Attribute(trait_type="Hair (Front)", value="Nyx", display_type=None),
                Attribute(
                    trait_type="Hair (Back)", value="Nyx Long", display_type=None
                ),
                Attribute(trait_type="Hair Color", value="Steel", display_type=None),
                Attribute(trait_type="Hat", value="Witch (Black)", display_type=None),
                Attribute(
                    trait_type="Necklace",
                    value="Moon Necklace (Silver)",
                    display_type=None,
                ),
                Attribute(
                    trait_type="Archetype of Power",
                    value="Witch of Woe",
                    display_type=None,
                ),
                Attribute(trait_type="Sun Sign", value="Taurus", display_type=None),
                Attribute(trait_type="Moon Sign", value="Aquarius", display_type=None),
                Attribute(
                    trait_type="Rising Sign", value="Capricorn", display_type=None
                ),
                Attribute(trait_type="Will", value="9", display_type="number"),
                Attribute(trait_type="Wisdom", value="9", display_type="number"),
                Attribute(trait_type="Wonder", value="9", display_type="number"),
                Attribute(trait_type="Woe", value="10", display_type="number"),
                Attribute(trait_type="Wit", value="9", display_type="number"),
                Attribute(trait_type="Wiles", value="9", display_type="number"),
            ],
            name="nyx",
            description="You are a WITCH of the highest order. You are borne of chaos that gives the night shape. Your magic spawns from primordial darkness. You are called oracle by those wise enough to listen. ALL THEOLOGY STEMS FROM THE TERROR OF THE FIRMAMENT!",
            mime_type="application/json",
            image=MediaDetails(
                size=3095,
                sha256=None,
                uri="https://cryptocoven.s3.amazonaws.com/nyx.png",
                mime_type="application/json",
            ),
            content=None,
            additional_fields=[
                MetadataField(
                    field_name="external_url",
                    type=MetadataFieldType.TEXT,
                    description="This is the URL that will appear below the asset's image on OpenSea and will allow users to leave OpenSea and view the item on your site.",
                    value="https://www.cryptocoven.xyz/witches/1",
                ),
                MetadataField(
                    field_name="background_color",
                    type=MetadataFieldType.TEXT,
                    description="Background color of the item on OpenSea. Must be a six-character hexadecimal without a pre-pended #.",
                    value="",
                ),
            ],
        )

    @pytest.mark.asyncio
    async def test_metadata_pipeline_async_fetch_video_mime_type_and_size(
        self, mock_video_rawdata
    ):
        token = Token(
            chain_identifier="ZORA-MAINNET",
            collection_address="0x7d256d82b32d8003d1ca1a1526ed211e6e0da9e2",
            token_id="11539",
            uri="https://a.y.at/nft_transfers/metadata/11539",
        )

        fetcher = MetadataFetcher()
        fetcher.gen_fetch_content = AsyncMock(return_value=mock_video_rawdata)

        def mock_video_mime_type_and_size(uri: str) -> Tuple[str, int]:
            if uri == "https://a.y.at/nft_transfers/metadata/11539":
                return ("application/json", 0)
            elif (
                uri
                == "https://y.at/viz/money-mouth/money-mouth.point.heart-eyes.crown.ring-2ba3b7.mp4"
            ):
                return ("video/mp4", 5065775)
            else:
                return ("image/png", 207474)

        fetcher.gen_fetch_mime_type_and_size = AsyncMock(
            side_effect=mock_video_mime_type_and_size
        )
        pipeline = MetadataPipeline(fetcher=fetcher)
        metadata = await pipeline.async_run(tokens=[token])

        assert metadata[0].mime_type == "video/mp4"
        assert metadata[0].content.mime_type == "video/mp4"
        assert metadata[0].content.size == 5065775
        assert metadata[0].image.mime_type == "image/png"
        assert metadata[0].image.size == 207474

    @pytest.mark.asyncio
    async def test_metadata_pipeline_async_fetch_image_mime_type_and_size(
        self, mock_image_rawdata
    ):
        token = Token(
            chain_identifier="ZORA-MAINNET",
            collection_address="0x2781b28934943f51a8a08375d6f95e0208d7150e",
            token_id="929",
            uri="https://ipfs.io/ipfs/QmRVtPDV4JSsPRhec2djxr2qpx6ex6xrgYTWKKfAbS3u3b",
        )

        fetcher = MetadataFetcher()
        fetcher.gen_fetch_content = AsyncMock(return_value=mock_image_rawdata)

        def mock_image_mime_type_and_size(uri: str) -> Tuple[str, int]:
            if (
                uri
                == "https://ipfs.io/ipfs/QmRVtPDV4JSsPRhec2djxr2qpx6ex6xrgYTWKKfAbS3u3b"
            ):
                return ("application/json", 0)
            else:
                return ("image/png", 2887641)

        fetcher.gen_fetch_mime_type_and_size = AsyncMock(
            side_effect=mock_image_mime_type_and_size
        )
        pipeline = MetadataPipeline(fetcher=fetcher)
        metadata = await pipeline.async_run(tokens=[token])

        assert metadata[0].mime_type == "image/png"
        assert metadata[0].image.mime_type == "image/png"
        assert metadata[0].image.size == 2887641

    def test_metadata_pipeline_run(self, raw_crypto_coven_metadata):  # type: ignore[no-untyped-def]
        token = Token(
            chain_identifier="ETHEREUM-MAINNET",
            collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
            token_id="1",
            uri="ipfs://QmSr3vdMuP2fSxWD7S26KzzBWcAN1eNhm4hk1qaR3x3vmj/1.json",
        )

        fetcher = MetadataFetcher()
        fetcher.fetch_content = MagicMock(return_value=raw_crypto_coven_metadata)  # type: ignore[assignment]
        fetcher.fetch_mime_type_and_size = MagicMock(return_value=("application/json", "3095"))  # type: ignore[assignment]

        pipeline = MetadataPipeline(fetcher=fetcher)
        assert pipeline.run(tokens=[token]) == [
            Metadata(
                token=token,
                raw_data=raw_crypto_coven_metadata,
                standard=MetadataStandard.OPENSEA_STANDARD,
                attributes=[
                    Attribute(
                        trait_type="Background", value="Sepia", display_type=None
                    ),
                    Attribute(trait_type="Skin Tone", value="Dawn", display_type=None),
                    Attribute(
                        trait_type="Body Shape", value="Lithe", display_type=None
                    ),
                    Attribute(
                        trait_type="Top", value="Sheer Top (Black)", display_type=None
                    ),
                    Attribute(
                        trait_type="Eyebrows",
                        value="Medium Flat (Black)",
                        display_type=None,
                    ),
                    Attribute(trait_type="Eye Style", value="Nyx", display_type=None),
                    Attribute(trait_type="Eye Color", value="Cloud", display_type=None),
                    Attribute(
                        trait_type="Mouth", value="Nyx (Mocha)", display_type=None
                    ),
                    Attribute(
                        trait_type="Hair (Front)", value="Nyx", display_type=None
                    ),
                    Attribute(
                        trait_type="Hair (Back)", value="Nyx Long", display_type=None
                    ),
                    Attribute(
                        trait_type="Hair Color", value="Steel", display_type=None
                    ),
                    Attribute(
                        trait_type="Hat", value="Witch (Black)", display_type=None
                    ),
                    Attribute(
                        trait_type="Necklace",
                        value="Moon Necklace (Silver)",
                        display_type=None,
                    ),
                    Attribute(
                        trait_type="Archetype of Power",
                        value="Witch of Woe",
                        display_type=None,
                    ),
                    Attribute(trait_type="Sun Sign", value="Taurus", display_type=None),
                    Attribute(
                        trait_type="Moon Sign", value="Aquarius", display_type=None
                    ),
                    Attribute(
                        trait_type="Rising Sign", value="Capricorn", display_type=None
                    ),
                    Attribute(trait_type="Will", value="9", display_type="number"),
                    Attribute(trait_type="Wisdom", value="9", display_type="number"),
                    Attribute(trait_type="Wonder", value="9", display_type="number"),
                    Attribute(trait_type="Woe", value="10", display_type="number"),
                    Attribute(trait_type="Wit", value="9", display_type="number"),
                    Attribute(trait_type="Wiles", value="9", display_type="number"),
                ],
                name="nyx",
                description="You are a WITCH of the highest order. You are borne of chaos that gives the night shape. Your magic spawns from primordial darkness. You are called oracle by those wise enough to listen. ALL THEOLOGY STEMS FROM THE TERROR OF THE FIRMAMENT!",
                mime_type="application/json",
                image=MediaDetails(
                    size=3095,
                    sha256=None,
                    uri="https://cryptocoven.s3.amazonaws.com/nyx.png",
                    mime_type="application/json",
                ),
                content=None,
                additional_fields=[
                    MetadataField(
                        field_name="external_url",
                        type=MetadataFieldType.TEXT,
                        description="This is the URL that will appear below the asset's image on OpenSea and will allow users to leave OpenSea and view the item on your site.",
                        value="https://www.cryptocoven.xyz/witches/1",
                    ),
                    MetadataField(
                        field_name="background_color",
                        type=MetadataFieldType.TEXT,
                        description="Background color of the item on OpenSea. Must be a six-character hexadecimal without a pre-pended #.",
                        value="",
                    ),
                ],
            )
        ]

    @pytest.mark.asyncio
    async def test_metadata_pipeline_async_run(self, raw_crypto_coven_metadata):  # type: ignore[no-untyped-def]
        token = Token(
            chain_identifier="ETHEREUM-MAINNET",
            collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
            token_id="1",
            uri="ipfs://QmSr3vdMuP2fSxWD7S26KzzBWcAN1eNhm4hk1qaR3x3vmj/1.json",
        )

        fetcher = MetadataFetcher()

        pipeline = MetadataPipeline(fetcher=fetcher)
        metadata = await pipeline.async_run(tokens=[token])
        assert metadata == [
            Metadata(
                token=token,
                raw_data=raw_crypto_coven_metadata,
                standard=MetadataStandard.OPENSEA_STANDARD,
                attributes=[
                    Attribute(
                        trait_type="Background", value="Sepia", display_type=None
                    ),
                    Attribute(trait_type="Skin Tone", value="Dawn", display_type=None),
                    Attribute(
                        trait_type="Body Shape", value="Lithe", display_type=None
                    ),
                    Attribute(
                        trait_type="Top", value="Sheer Top (Black)", display_type=None
                    ),
                    Attribute(
                        trait_type="Eyebrows",
                        value="Medium Flat (Black)",
                        display_type=None,
                    ),
                    Attribute(trait_type="Eye Style", value="Nyx", display_type=None),
                    Attribute(trait_type="Eye Color", value="Cloud", display_type=None),
                    Attribute(
                        trait_type="Mouth", value="Nyx (Mocha)", display_type=None
                    ),
                    Attribute(
                        trait_type="Hair (Front)", value="Nyx", display_type=None
                    ),
                    Attribute(
                        trait_type="Hair (Back)", value="Nyx Long", display_type=None
                    ),
                    Attribute(
                        trait_type="Hair Color", value="Steel", display_type=None
                    ),
                    Attribute(
                        trait_type="Hat", value="Witch (Black)", display_type=None
                    ),
                    Attribute(
                        trait_type="Necklace",
                        value="Moon Necklace (Silver)",
                        display_type=None,
                    ),
                    Attribute(
                        trait_type="Archetype of Power",
                        value="Witch of Woe",
                        display_type=None,
                    ),
                    Attribute(trait_type="Sun Sign", value="Taurus", display_type=None),
                    Attribute(
                        trait_type="Moon Sign", value="Aquarius", display_type=None
                    ),
                    Attribute(
                        trait_type="Rising Sign", value="Capricorn", display_type=None
                    ),
                    Attribute(trait_type="Will", value="9", display_type="number"),
                    Attribute(trait_type="Wisdom", value="9", display_type="number"),
                    Attribute(trait_type="Wonder", value="9", display_type="number"),
                    Attribute(trait_type="Woe", value="10", display_type="number"),
                    Attribute(trait_type="Wit", value="9", display_type="number"),
                    Attribute(trait_type="Wiles", value="9", display_type="number"),
                ],
                name="nyx",
                description="You are a WITCH of the highest order. You are borne of chaos that gives the night shape. Your magic spawns from primordial darkness. You are called oracle by those wise enough to listen. ALL THEOLOGY STEMS FROM THE TERROR OF THE FIRMAMENT!",
                mime_type="image/png",
                image=MediaDetails(
                    size=1365782,
                    sha256=None,
                    uri="https://cryptocoven.s3.amazonaws.com/nyx.png",
                    mime_type="image/png",
                ),
                content=None,
                additional_fields=[
                    MetadataField(
                        field_name="external_url",
                        type=MetadataFieldType.TEXT,
                        description="This is the URL that will appear below the asset's image on OpenSea and will allow users to leave OpenSea and view the item on your site.",
                        value="https://www.cryptocoven.xyz/witches/1",
                    ),
                    MetadataField(
                        field_name="background_color",
                        type=MetadataFieldType.TEXT,
                        description="Background color of the item on OpenSea. Must be a six-character hexadecimal without a pre-pended #.",
                        value="",
                    ),
                ],
            )
        ]

    @pytest.mark.asyncio
    async def test_metadata_pipeline_async_run_with_custom_adapters(self, raw_crypto_coven_metadata):  # type: ignore[no-untyped-def]
        token = Token(
            chain_identifier="ETHEREUM-MAINNET",
            collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
            token_id="1",
            uri="ipfs://QmSr3vdMuP2fSxWD7S26KzzBWcAN1eNhm4hk1qaR3x3vmj/1.json",
        )

        fetcher = MetadataFetcher()
        pipeline = MetadataPipeline(
            fetcher=fetcher,
            adapter_configs=[
                AdapterConfig(
                    adapter_cls=IPFSAdapter,
                    mount_prefixes=[
                        "ipfs://",
                        "https://gateway.pinata.cloud/",
                        "https://ipfs.io/",
                    ],
                    host_prefixes=["https://gateway.pinata.cloud/"],
                    kwargs={
                        "pool_connections": 100,
                        "pool_maxsize": 1000,
                        "max_retries": 0,
                    },
                )
            ],
        )
        metadata = await pipeline.async_run(tokens=[token])
        assert metadata[0].token == token

    def test_metadata_pipeline_errors_with_no_parser(self):  # type: ignore[no-untyped-def]
        token = Token(
            chain_identifier="ETHEREUM-MAINNET",
            collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
            token_id="1",
            uri="ipfs://QmSr3vdMuP2fSxWD7S26KzzBWcAN1eNhm4hk1qaR3x3vmj/1.json",
        )
        fetcher = MetadataFetcher()
        fetcher.fetch_content = MagicMock(return_value={})  # type: ignore[assignment]
        fetcher.fetch_mime_type_and_size = MagicMock(return_value=("application/json", "3095"))  # type: ignore[assignment]

        pipeline = MetadataPipeline(fetcher=fetcher, parsers=[])
        assert pipeline.run(tokens=[token]) == [
            MetadataProcessingError(
                token=token,
                error_type="Exception",
                error_message=f"({token.chain_identifier}-{token.collection_address}-{token.token_id}) No parsers found.",
            )
        ]
