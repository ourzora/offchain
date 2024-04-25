# flake8: noqa: E501

from unittest.mock import MagicMock

import pytest
import base64

from offchain.metadata.adapters.ipfs import IPFSAdapter
from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher
from offchain.metadata.models.metadata import (
    Attribute,
    MediaDetails,
    Metadata,
    MetadataField,
    MetadataFieldType,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.schema.opensea import OpenseaParser


class TestOpenseaParser:
    token = Token(
        chain_identifier="ETHEREUM-MAINNET",
        collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
        token_id=1,
        uri="ipfs://QmSr3vdMuP2fSxWD7S26KzzBWcAN1eNhm4hk1qaR3x3vmj/1.json",
    )

    metadata_with_content_raw = {
        "name": "Glass House #996",
        "description": "Glass House is a collection from Daniel Allan’s forthcoming four-track EP. It’s meant to embody the calming nature of being at home, represented through 1000 unique tokens. It’s debuted first through web3, and available on all streaming platforms in September.",
        "external_url": "https://danielallan.xyz",
        "image": "ipfs://bafybeigyjbnmnifzzkl5a7nywllmu2aoqedazz6dlos5mfqovvrcnn562a/996.jpeg",
        "animation_url": "ipfs://bafybeihfcqvofl3qlf747wg2jxghumqzrnu2w5x6zunnqfj3mssp7v5og4/996.mp4",
        "attributes": [
            {"trait_type": "Background", "value": "Flower"},
            {"trait_type": "Rings", "value": "None"},
            {"trait_type": "Antenna", "value": "In"},
            {"trait_type": "Butterfly", "value": "Green"},
            {"trait_type": "Track", "value": "Chasing Paradise"},
        ],
        "edition": 996,
    }

    def test_opensea_parser_should_parse_token(self, raw_crypto_coven_metadata):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        ipfs_adapter = IPFSAdapter()
        fetcher.register_adapter(ipfs_adapter, "ipfs://")
        parser = OpenseaParser(fetcher=fetcher)  # type: ignore[abstract]
        assert (
            parser.should_parse_token(
                token=self.token, raw_data=raw_crypto_coven_metadata
            )
            == True
        )

    def test_opensea_parser_should_parse_token_raw_data_string(self):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        ipfs_adapter = IPFSAdapter()
        fetcher.register_adapter(ipfs_adapter, "ipfs://")
        parser = OpenseaParser(fetcher=fetcher)  # type: ignore[abstract]
        assert parser.should_parse_token(token=self.token, raw_data="test") == False  # type: ignore[arg-type]

    def test_opensea_parser_parses_metadata(self, raw_crypto_coven_metadata):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        ipfs_adapter = IPFSAdapter()
        fetcher.register_adapter(ipfs_adapter, "ipfs://")
        fetcher.fetch_mime_type_and_size = MagicMock(return_value=("application/json", "3095"))  # type: ignore[assignment]
        parser = OpenseaParser(fetcher=fetcher)  # type: ignore[abstract]
        metadata = parser.parse_metadata(
            token=self.token, raw_data=raw_crypto_coven_metadata
        )
        assert metadata == Metadata(
            token=self.token,
            raw_data=raw_crypto_coven_metadata,
            standard=None,
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

    def test_opensea_parser_parses_metadata_with_content(self):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        ipfs_adapter = IPFSAdapter()
        fetcher.register_adapter(ipfs_adapter, "ipfs://")
        fetcher.fetch_mime_type_and_size = MagicMock(return_value=("application/json", "3095"))  # type: ignore[assignment]
        parser = OpenseaParser(fetcher=fetcher)  # type: ignore[abstract]
        token = Token(
            chain_identifier="ETHEREUM-MAINNET",
            collection_address="0x719c6d392fc659f4fe9b0576cbc46e18939687a7",
            token_id=996,
            uri="ipfs://bafybeighjepdqehd2jq3i3q7363r3o24zcoam62ki5bmp6ddsvzwhnktyu/996",
        )
        metadata = parser.parse_metadata(
            token=token, raw_data=self.metadata_with_content_raw
        )
        assert metadata == Metadata(
            token=Token(
                chain_identifier="ETHEREUM-MAINNET",
                collection_address="0x719c6d392fc659f4fe9b0576cbc46e18939687a7",
                token_id=996,
                uri="ipfs://bafybeighjepdqehd2jq3i3q7363r3o24zcoam62ki5bmp6ddsvzwhnktyu/996",
            ),
            raw_data={
                "name": "Glass House #996",
                "description": "Glass House is a collection from Daniel Allan’s forthcoming four-track EP. It’s meant to embody the calming nature of being at home, represented through 1000 unique tokens. It’s debuted first through web3, and available on all streaming platforms in September.",
                "external_url": "https://danielallan.xyz",
                "image": "ipfs://bafybeigyjbnmnifzzkl5a7nywllmu2aoqedazz6dlos5mfqovvrcnn562a/996.jpeg",
                "animation_url": "ipfs://bafybeihfcqvofl3qlf747wg2jxghumqzrnu2w5x6zunnqfj3mssp7v5og4/996.mp4",
                "attributes": [
                    {"trait_type": "Background", "value": "Flower"},
                    {"trait_type": "Rings", "value": "None"},
                    {"trait_type": "Antenna", "value": "In"},
                    {"trait_type": "Butterfly", "value": "Green"},
                    {"trait_type": "Track", "value": "Chasing Paradise"},
                ],
                "edition": 996,
            },
            attributes=[
                Attribute(trait_type="Background", value="Flower", display_type=None),
                Attribute(trait_type="Rings", value="None", display_type=None),
                Attribute(trait_type="Antenna", value="In", display_type=None),
                Attribute(trait_type="Butterfly", value="Green", display_type=None),
                Attribute(
                    trait_type="Track", value="Chasing Paradise", display_type=None
                ),
            ],
            standard=None,
            name="Glass House #996",
            description="Glass House is a collection from Daniel Allan’s forthcoming four-track EP. It’s meant to embody the calming nature of being at home, represented through 1000 unique tokens. It’s debuted first through web3, and available on all streaming platforms in September.",
            mime_type="application/json",
            image=MediaDetails(
                size=3095,
                sha256=None,
                uri="ipfs://bafybeigyjbnmnifzzkl5a7nywllmu2aoqedazz6dlos5mfqovvrcnn562a/996.jpeg",
                mime_type="application/json",
            ),
            content=MediaDetails(
                size=3095,
                sha256=None,
                uri="ipfs://bafybeihfcqvofl3qlf747wg2jxghumqzrnu2w5x6zunnqfj3mssp7v5og4/996.mp4",
                mime_type="application/json",
            ),
            additional_fields=[
                MetadataField(
                    field_name="external_url",
                    type=MetadataFieldType.TEXT,
                    description="This is the URL that will appear below the asset's image on OpenSea and will allow users to leave OpenSea and view the item on your site.",
                    value="https://danielallan.xyz",
                ),
                MetadataField(
                    field_name="animation_url",
                    type=MetadataFieldType.TEXT,
                    description="A URL to a multi-media attachment for the item.",
                    value="ipfs://bafybeihfcqvofl3qlf747wg2jxghumqzrnu2w5x6zunnqfj3mssp7v5og4/996.mp4",
                ),
            ],
        )

    @pytest.mark.asyncio
    async def test_opensea_parser_gen_parses_metadata(self, raw_crypto_coven_metadata):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        parser = OpenseaParser(fetcher=fetcher)  # type: ignore[abstract]
        metadata = await parser.gen_parse_metadata(
            token=self.token, raw_data=raw_crypto_coven_metadata
        )
        assert metadata

    @pytest.mark.asyncio
    async def test_opensea_parser_parses_token_with_xml_image(self):
        parser = OpenseaParser(fetcher=MetadataFetcher())  # type: ignore[abstract]
        token = Token(
            chain_identifier="BASE-MAINNET",
            collection_address="0x00000000001594c61dd8a6804da9ab58ed2483ce",
            token_id=91107139416293979998100172630436458595092238971,
            uri="https://metadata.nfts2me.com/api/ownerTokenURI/8453/91107139416293979998100172630436458595092238971/574759207385280074438303243253258373278259074888/10000/",
        )
        raw_data = {
            "name": "NFTs2Me Collection Owner - drako",
            "description": "Represents **Ownership of the NFTs2Me Collection** with address '[0x0fF562Ab42325222cF72971d32ED9CDF373b927B](https://0x0fF562Ab42325222cF72971d32ED9CDF373b927B_8453.nfts2.me/)'.\n\nTransferring this NFT implies changing the owner of the collection, as well as who will receive 100% of the profits from primary and secondary sales.\n\n[NFTs2Me](https://nfts2me.com/) is a showcase of unique digital creations from talented creators who have used the tool to generate their own NFT projects. These projects range from digital art and collectibles to gaming items and more, all with the added value of being verified on the blockchain. With a wide range of styles and themes, the [NFTs2Me](https://nfts2me.com/) tool offers something for every fan of the growing NFT space.",
            "image_data": '<svg viewBox="0 0 499.99998 499.99998" width="500" height="500" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="background: white;"><style type="text/css">.st0{fill:#6CB7E6;}.st1{fill:#147ABF;}</style><g transform="matrix(2.002645,0,0,2.002645,40.953902,-319.12168)"><circle class="st0" cx="105.05" cy="204.58" r="8.1800003"/><path class="st0" d="M 80.05,327.28 54.21,312.9 V 253.94 L 86.54,236.99 V 356.55 L 36.4,325.86 c 0,0 -3.28,-1.71 -3.28,-6.2 0,-4.49 0,-71.78 0,-71.78 0,0 -0.57,-4.27 3.85,-6.76 4.42,-2.49 60.67,-35.39 60.67,-35.39 l 2.07,5.04 c 0,0 -53.67,31.08 -57.95,33.85 -1.78,1.15 -3.15,2.11 -3.15,4.98 0,2.98 -0.01,54.64 -0.01,67.42 0,2.51 0.22,3.4 2.27,5.19 1.9,1.64 39.16,24.28 39.16,24.28 z"/><circle class="st0" cx="103.73" cy="363.79001" r="8.1800003"/><path class="st0" d="m 128.72,241.09 25.85,14.38 v 58.96 l -32.33,16.95 V 211.82 l 50.13,30.69 c 0,0 3.28,1.71 3.28,6.2 0,4.49 0,71.78 0,71.78 0,0 0.57,4.27 -3.85,6.76 -4.41,2.49 -60.67,35.39 -60.67,35.39 l -2.07,-5.04 c 0,0 53.67,-31.08 57.95,-33.85 1.78,-1.15 3.15,-2.11 3.15,-4.98 0,-2.98 0.01,-54.64 0.01,-67.42 0,-2.51 -0.22,-3.4 -2.27,-5.19 -1.9,-1.64 -39.16,-24.28 -39.16,-24.28 z"/></g> <g transform="matrix(2.002645,0,0,2.002645,-601.56128,-329.35424)"><polygon class="st1" points="122.24,331.38 86.53,291.04 86.53,236.99 122.24,277.39" transform="translate(320.83329,5.1095282)"/></g> <path d="m 113.85595,58.83376 h 272.2881 a 36.305083,22.490145 0 0 1 36.30509,22.490149 V 418.67609 a 36.305083,22.490145 0 0 1 -36.30509,22.49015 H 113.85595 A 36.305083,22.490145 0 0 1 77.55086,418.67609 V 81.323909 A 36.305083,22.490145 0 0 1 113.85595,58.83376 Z" style="fill:none;stroke:#147ABF;stroke-width:3;stroke-opacity:1"/> <path id="text-path" d="m 109.75187,53.071033 h 280.49626 a 37.399504,23.168113 0 0 1 37.39951,23.168117 v 347.5217 a 37.399504,23.168113 0 0 1 -37.39951,23.16812 H 109.75187 A 37.399504,23.168113 0 0 1 72.35236,423.76085 V 76.23915 a 37.399504,23.168113 0 0 1 37.39951,-23.168117 z" style="fill:none;"/><text text-rendering="optimizeSpeed"><textPath startOffset="-100%" fill="black" font-family="\'Courier New\', monospace" font-size="16px" xlink:href="#text-path">COLLECTION • drako <animate additive="sum" attributeName="startOffset" from="0%" to="100%" begin="0s" dur="30s" repeatCount="indefinite"/> </textPath> <textPath startOffset="0%" fill="black" font-family="\'Courier New\', monospace" font-size="16px" xlink:href="#text-path">COLLECTION • drako <animate additive="sum" attributeName="startOffset" from="0%" to="100%" begin="0s" dur="30s" repeatCount="indefinite"/> </textPath> <textPath startOffset="50%" fill="black" font-family="\'Courier New\', monospace" font-size="16px" xlink:href="#text-path">OWNER • 0x64Ad181f69466bD4D15076aC1d33a22c6Cc9d748 <animate additive="sum" attributeName="startOffset" from="0%" to="100%" begin="0s" dur="30s" repeatCount="indefinite"/> </textPath> <textPath startOffset="-50%" fill="black" font-family="\'Courier New\', monospace" font-size="16px" xlink:href="#text-path">OWNER • 0x64Ad181f69466bD4D15076aC1d33a22c6Cc9d748 <animate additive="sum" attributeName="startOffset" from="0%" to="100%" begin="0s" dur="30s" repeatCount="indefinite"/> </textPath> </text></svg>',
            "background_color": "#FFFFFF",
            "attributes": [
                {"trait_type": "Collection Name", "value": "drako"},
                {
                    "trait_type": "Collection Address",
                    "value": "0x0fF562Ab42325222cF72971d32ED9CDF373b927B",
                },
                {
                    "trait_type": "Owner Address",
                    "value": "0x64Ad181f69466bD4D15076aC1d33a22c6Cc9d748",
                },
                {"display_type": "number", "trait_type": "Revenue", "value": 100},
            ],
            "external_url": "https://0x0fF562Ab42325222cF72971d32ED9CDF373b927B_8453.nfts2.me/",
        }
        metadata = await parser._gen_parse_metadata_impl(token=token, raw_data=raw_data)
        svg_encoded = base64.b64encode(
            raw_data.get("image_data").encode("utf-8")
        ).decode("utf-8")
        expected_image_uri = f"data:image/svg+xml;base64,{svg_encoded}"
        assert metadata
        assert metadata.image == MediaDetails(
            size=3256,
            sha256=None,
            uri=expected_image_uri,
            mime_type="image/svg+xml",
        )
