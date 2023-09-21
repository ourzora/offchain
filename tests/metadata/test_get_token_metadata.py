# flake8: noqa: E501

from unittest import mock
from offchain import Metadata, Token  # type: ignore[attr-defined]
from offchain.metadata.get_token_metadata import get_token_metadata
from offchain.metadata.models.metadata import (
    Attribute,
    MediaDetails,
    MetadataField,
    MetadataFieldType,
    MetadataStandard,
)


@mock.patch(
    "offchain.metadata.fetchers.metadata_fetcher.MetadataFetcher.fetch_mime_type_and_size"
)
@mock.patch("offchain.metadata.fetchers.metadata_fetcher.MetadataFetcher.fetch_content")
def test_get_token_metadata(mock_fetch_content, mock_fetch_mime_type_and_size, raw_crypto_coven_metadata):  # type: ignore[no-untyped-def]
    mock_fetch_content.return_value = raw_crypto_coven_metadata
    mock_fetch_mime_type_and_size.return_value = ("application/json", "3095")
    assert get_token_metadata(
        collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
        token_id=1,
        uri="ipfs://QmSr3vdMuP2fSxWD7S26KzzBWcAN1eNhm4hk1qaR3x3vmj/1.json",
    ) == Metadata(
        token=Token(
            collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
            token_id=1,
            uri="ipfs://QmSr3vdMuP2fSxWD7S26KzzBWcAN1eNhm4hk1qaR3x3vmj/1.json",
            chain_identifier="ETHEREUM-MAINNET",
        ),
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
