# flake8: noqa: E501

from unittest.mock import MagicMock

from adapters.ipfs import IPFSAdapter
from fetchers.metadata_fetcher import MetadataFetcher
from models.metadata import (
    Attribute,
    MediaDetails,
    Metadata,
    MetadataField,
    MetadataFieldType,
    MetadataStandard,
)
from models.token import Token
from parsers.schema.opensea import OpenseaParser


class TestOpenseaParser:
    mock_raw_data = {
        "description": "You are a WITCH of the highest order. You are borne of chaos that gives the night shape. Your magic spawns from primordial darkness. You are called oracle by those wise enough to listen. ALL THEOLOGY STEMS FROM THE TERROR OF THE FIRMAMENT!",
        "external_url": "https://www.cryptocoven.xyz/witches/1",
        "image": "https://cryptocoven.s3.amazonaws.com/nyx.png",
        "name": "nyx",
        "background_color": "",
        "attributes": [
            {"trait_type": "Background", "value": "Sepia"},
            {"trait_type": "Skin Tone", "value": "Dawn"},
            {"trait_type": "Body Shape", "value": "Lithe"},
            {"trait_type": "Top", "value": "Sheer Top (Black)"},
            {"trait_type": "Eyebrows", "value": "Medium Flat (Black)"},
            {"trait_type": "Eye Style", "value": "Nyx"},
            {"trait_type": "Eye Color", "value": "Cloud"},
            {"trait_type": "Mouth", "value": "Nyx (Mocha)"},
            {"trait_type": "Hair (Front)", "value": "Nyx"},
            {"trait_type": "Hair (Back)", "value": "Nyx Long"},
            {"trait_type": "Hair Color", "value": "Steel"},
            {"trait_type": "Hat", "value": "Witch (Black)"},
            {"trait_type": "Necklace", "value": "Moon Necklace (Silver)"},
            {"trait_type": "Archetype of Power", "value": "Witch of Woe"},
            {"trait_type": "Sun Sign", "value": "Taurus"},
            {"trait_type": "Moon Sign", "value": "Aquarius"},
            {"trait_type": "Rising Sign", "value": "Capricorn"},
            {"display_type": "number", "trait_type": "Will", "value": 9},
            {"display_type": "number", "trait_type": "Wisdom", "value": 9},
            {"display_type": "number", "trait_type": "Wonder", "value": 9},
            {"display_type": "number", "trait_type": "Woe", "value": 10},
            {"display_type": "number", "trait_type": "Wit", "value": 9},
            {"display_type": "number", "trait_type": "Wiles", "value": 9},
        ],
        "coven": {
            "id": 1,
            "name": "nyx",
            "type": "Witch of Woe",
            "description": {
                "intro": "You are a WITCH of the highest order.",
                "hobby": "You are borne of chaos that gives the night shape.",
                "magic": "Your magic spawns from primordial darkness.",
                "typeSpecific": "You are called oracle by those wise enough to listen.",
                "exclamation": "ALL THEOLOGY STEMS FROM THE TERROR OF THE FIRMAMENT!",
            },
            "skills": {
                "will": 9,
                "wisdom": 9,
                "wonder": 9,
                "woe": 10,
                "wit": 9,
                "wiles": 9,
            },
            "birthChart": {
                "sun": "taurus",
                "moon": "aquarius",
                "rising": "capricorn",
            },
            "styles": [
                {
                    "attribute": "background",
                    "name": "solid",
                    "color": "sepia",
                    "fullName": "background_solid_sepia",
                },
                {
                    "attribute": "base",
                    "name": "lithe",
                    "color": "dawn",
                    "fullName": "base_lithe_dawn",
                },
                {
                    "attribute": "body-under",
                    "name": "sheer-top",
                    "color": "black",
                    "fullName": "body-under_sheer-top_black",
                },
                {
                    "attribute": "eyebrows",
                    "name": "medium-flat",
                    "color": "black",
                    "fullName": "eyebrows_medium-flat_black",
                },
                {
                    "attribute": "eyes",
                    "name": "nyx",
                    "color": "cloud",
                    "fullName": "eyes_nyx_cloud",
                },
                {
                    "attribute": "mouth",
                    "name": "nyx",
                    "color": "mocha",
                    "fullName": "mouth_nyx_mocha",
                },
                {
                    "attribute": "hair-back",
                    "name": "nyx",
                    "color": "steel",
                    "fullName": "hair-back_nyx_steel",
                },
                {
                    "attribute": "hair-bangs",
                    "name": "nyx",
                    "color": "steel",
                    "fullName": "hair-bangs_nyx_steel",
                },
                {
                    "attribute": "hat-back",
                    "name": "witch",
                    "color": "black",
                    "fullName": "hat-back_witch_black",
                },
                {
                    "attribute": "hat-front",
                    "name": "witch",
                    "color": "black",
                    "fullName": "hat-front_witch_black",
                },
                {
                    "attribute": "necklace",
                    "name": "moon-necklace",
                    "color": "silver",
                    "fullName": "necklace_moon-necklace_silver",
                },
            ],
            "hash": "nyx",
        },
    }

    token = Token(
        chain_identifier="ETHEREUM-MAINNET",
        collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
        token_id="1",
        uri="ipfs://QmSr3vdMuP2fSxWD7S26KzzBWcAN1eNhm4hk1qaR3x3vmj/1.json",
    )

    def test_opensea_parser_should_parse_token(self):
        fetcher = MetadataFetcher()
        ipfs_adapter = IPFSAdapter()
        fetcher.register_adapter(ipfs_adapter, "ipfs://")
        parser = OpenseaParser(fetcher=fetcher)
        assert parser.should_parse_token(token=self.token, raw_data=self.mock_raw_data) == True

    def test_opensea_parser_parses_metadata(self):
        fetcher = MetadataFetcher()
        ipfs_adapter = IPFSAdapter()
        fetcher.register_adapter(ipfs_adapter, "ipfs://")
        fetcher.fetch_mime_type_and_size = MagicMock(return_value=("application/json", "3095"))
        parser = OpenseaParser(fetcher=fetcher)
        metadata = parser.parse_metadata(token=self.token, raw_data=self.mock_raw_data)
        assert metadata == Metadata(
            chain_identifier="ETHEREUM-MAINNET",
            collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
            token_id=1,
            raw_data={
                "description": "You are a WITCH of the highest order. You are borne of chaos that gives the night shape. Your magic spawns from primordial darkness. You are called oracle by those wise enough to listen. ALL THEOLOGY STEMS FROM THE TERROR OF THE FIRMAMENT!",
                "external_url": "https://www.cryptocoven.xyz/witches/1",
                "image": "https://cryptocoven.s3.amazonaws.com/nyx.png",
                "name": "nyx",
                "background_color": "",
                "attributes": [
                    {"trait_type": "Background", "value": "Sepia"},
                    {"trait_type": "Skin Tone", "value": "Dawn"},
                    {"trait_type": "Body Shape", "value": "Lithe"},
                    {"trait_type": "Top", "value": "Sheer Top (Black)"},
                    {"trait_type": "Eyebrows", "value": "Medium Flat (Black)"},
                    {"trait_type": "Eye Style", "value": "Nyx"},
                    {"trait_type": "Eye Color", "value": "Cloud"},
                    {"trait_type": "Mouth", "value": "Nyx (Mocha)"},
                    {"trait_type": "Hair (Front)", "value": "Nyx"},
                    {"trait_type": "Hair (Back)", "value": "Nyx Long"},
                    {"trait_type": "Hair Color", "value": "Steel"},
                    {"trait_type": "Hat", "value": "Witch (Black)"},
                    {"trait_type": "Necklace", "value": "Moon Necklace (Silver)"},
                    {"trait_type": "Archetype of Power", "value": "Witch of Woe"},
                    {"trait_type": "Sun Sign", "value": "Taurus"},
                    {"trait_type": "Moon Sign", "value": "Aquarius"},
                    {"trait_type": "Rising Sign", "value": "Capricorn"},
                    {"display_type": "number", "trait_type": "Will", "value": 9},
                    {"display_type": "number", "trait_type": "Wisdom", "value": 9},
                    {"display_type": "number", "trait_type": "Wonder", "value": 9},
                    {"display_type": "number", "trait_type": "Woe", "value": 10},
                    {"display_type": "number", "trait_type": "Wit", "value": 9},
                    {"display_type": "number", "trait_type": "Wiles", "value": 9},
                ],
                "coven": {
                    "id": 1,
                    "name": "nyx",
                    "type": "Witch of Woe",
                    "description": {
                        "intro": "You are a WITCH of the highest order.",
                        "hobby": "You are borne of chaos that gives the night shape.",
                        "magic": "Your magic spawns from primordial darkness.",
                        "typeSpecific": "You are called oracle by those wise enough to listen.",
                        "exclamation": "ALL THEOLOGY STEMS FROM THE TERROR OF THE FIRMAMENT!",
                    },
                    "skills": {
                        "will": 9,
                        "wisdom": 9,
                        "wonder": 9,
                        "woe": 10,
                        "wit": 9,
                        "wiles": 9,
                    },
                    "birthChart": {
                        "sun": "taurus",
                        "moon": "aquarius",
                        "rising": "capricorn",
                    },
                    "styles": [
                        {
                            "attribute": "background",
                            "name": "solid",
                            "color": "sepia",
                            "fullName": "background_solid_sepia",
                        },
                        {
                            "attribute": "base",
                            "name": "lithe",
                            "color": "dawn",
                            "fullName": "base_lithe_dawn",
                        },
                        {
                            "attribute": "body-under",
                            "name": "sheer-top",
                            "color": "black",
                            "fullName": "body-under_sheer-top_black",
                        },
                        {
                            "attribute": "eyebrows",
                            "name": "medium-flat",
                            "color": "black",
                            "fullName": "eyebrows_medium-flat_black",
                        },
                        {
                            "attribute": "eyes",
                            "name": "nyx",
                            "color": "cloud",
                            "fullName": "eyes_nyx_cloud",
                        },
                        {
                            "attribute": "mouth",
                            "name": "nyx",
                            "color": "mocha",
                            "fullName": "mouth_nyx_mocha",
                        },
                        {
                            "attribute": "hair-back",
                            "name": "nyx",
                            "color": "steel",
                            "fullName": "hair-back_nyx_steel",
                        },
                        {
                            "attribute": "hair-bangs",
                            "name": "nyx",
                            "color": "steel",
                            "fullName": "hair-bangs_nyx_steel",
                        },
                        {
                            "attribute": "hat-back",
                            "name": "witch",
                            "color": "black",
                            "fullName": "hat-back_witch_black",
                        },
                        {
                            "attribute": "hat-front",
                            "name": "witch",
                            "color": "black",
                            "fullName": "hat-front_witch_black",
                        },
                        {
                            "attribute": "necklace",
                            "name": "moon-necklace",
                            "color": "silver",
                            "fullName": "necklace_moon-necklace_silver",
                        },
                    ],
                    "hash": "nyx",
                },
            },
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
            token_uri="ipfs://QmSr3vdMuP2fSxWD7S26KzzBWcAN1eNhm4hk1qaR3x3vmj/1.json",
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
