# flake8: noqa: E501

from unittest.mock import MagicMock

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
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.schema.opensea import OpenseaParser


class TestOpenseaParser:
    token = Token(
        chain_identifier="ETHEREUM-MAINNET",
        collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
        token_id="1",
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

    def test_opensea_parser_should_parse_token(self, raw_crypto_coven_metadata):
        fetcher = MetadataFetcher()
        ipfs_adapter = IPFSAdapter()
        fetcher.register_adapter(ipfs_adapter, "ipfs://")
        parser = OpenseaParser(fetcher=fetcher)
        assert parser.should_parse_token(token=self.token, raw_data=raw_crypto_coven_metadata) == True

    def test_opensea_parser_parses_metadata(self, raw_crypto_coven_metadata):
        fetcher = MetadataFetcher()
        ipfs_adapter = IPFSAdapter()
        fetcher.register_adapter(ipfs_adapter, "ipfs://")
        fetcher.fetch_mime_type_and_size = MagicMock(return_value=("application/json", "3095"))
        parser = OpenseaParser(fetcher=fetcher)
        metadata = parser.parse_metadata(token=self.token, raw_data=raw_crypto_coven_metadata)
        assert metadata == Metadata(
            token=self.token,
            raw_data=raw_crypto_coven_metadata,
            standard=MetadataStandard.OPENSEA_STANDARD,
            attributes=[
                Attribute(trait_type="Background", value="Sepia", display_type=None),
                Attribute(trait_type="Skin Tone", value="Dawn", display_type=None),
                Attribute(trait_type="Body Shape", value="Lithe", display_type=None),
                Attribute(trait_type="Top", value="Sheer Top (Black)", display_type=None),
                Attribute(
                    trait_type="Eyebrows",
                    value="Medium Flat (Black)",
                    display_type=None,
                ),
                Attribute(trait_type="Eye Style", value="Nyx", display_type=None),
                Attribute(trait_type="Eye Color", value="Cloud", display_type=None),
                Attribute(trait_type="Mouth", value="Nyx (Mocha)", display_type=None),
                Attribute(trait_type="Hair (Front)", value="Nyx", display_type=None),
                Attribute(trait_type="Hair (Back)", value="Nyx Long", display_type=None),
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
                Attribute(trait_type="Rising Sign", value="Capricorn", display_type=None),
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

    def test_opensea_parser_parses_metadata_with_content(self):
        fetcher = MetadataFetcher()
        ipfs_adapter = IPFSAdapter()
        fetcher.register_adapter(ipfs_adapter, "ipfs://")
        fetcher.fetch_mime_type_and_size = MagicMock(return_value=("application/json", "3095"))
        parser = OpenseaParser(fetcher=fetcher)
        token = Token(
            chain_identifier="ETHEREUM-MAINNET",
            collection_address="0x719c6d392fc659f4fe9b0576cbc46e18939687a7",
            token_id=996,
            uri="ipfs://bafybeighjepdqehd2jq3i3q7363r3o24zcoam62ki5bmp6ddsvzwhnktyu/996",
        )
        metadata = parser.parse_metadata(token=token, raw_data=self.metadata_with_content_raw)
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
                Attribute(trait_type="Track", value="Chasing Paradise", display_type=None),
            ],
            standard=MetadataStandard.OPENSEA_STANDARD,
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
