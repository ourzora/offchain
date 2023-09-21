# flake8: noqa: E501
from unittest.mock import AsyncMock, MagicMock, Mock

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
from offchain.metadata.parsers.collection.artblocks import ArtblocksParser
from offchain.web3.contract_caller import ContractCaller


class TestArtblocksParser:
    token = Token(
        chain_identifier="ETHEREUM-MAINNET",
        collection_address="0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270",
        token_id=265000125,
    )

    raw_data = {
        "platform": "Art Blocks Factory",
        "tokenID": "265000125",
        "series": "N/A",
        "aspect_ratio": 1,
        "payout_address": "0x6C093Fe8bc59e1e0cAe2Ec10F0B717D3D182056B",
        "name": "Tentura #125",
        "minted": True,
        "artist": "Stranger in the Q",
        "description": "Tentura - fundamental device of time and being.\n\nThe essence of the Tentura's work is that it breaks the connection between the body and soul of every living being under its influence.\nThe subject becomes bound to a global variable, which is calculated and controlled by the Tentura itself.\nThis is the work of Tentura, with the amendment that the object of its control is reality.\n\nClick/tap to play/pause animation",
        "script_type": "p5js",
        "project_id": "265",
        "curation_status": "factory",
        "image": "https://media.artblocks.io/265000125.png",
        "generator_url": "https://generator.artblocks.io/265000125",
        "animation_url": "https://generator.artblocks.io/265000125",
        "royaltyInfo": {
            "artistAddress": "0xe0324d6981ccb5b62bdd235366dee6172e0ef116",
            "additionalPayee": "0x0000000000000000000000000000000000000000",
            "additionalPayeePercentage": "0",
            "royaltyFeeByID": 5,
        },
        "collection_name": "Tentura by Stranger in the Q",
        "website": "https://strangerintheq.github.io/tentura",
        "token_hash": "0x70c4c5ca361b259f56babbbbed29e1cb72921f99e5d45ed99eee65f2279a1307",
        "external_url": "https://artblocks.io/collections/factory/projects/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/265/tokens/265000125",
        "features": {
            "Fog": "Yes",
            "Mask": "Edges",
            "Mode": "Partial",
            "Beams": "Less",
            "Shape": "Two lines",
            "Layout": "Bent",
            "Palette": "Dawn",
            "Grayscale": "None",
            "Background": "Lighten",
            "Distribution": "Circle",
        },
        "traits": [
            {"trait_type": "Tentura", "value": "All Tenturas"},
            {"trait_type": "Tentura", "value": "Fog: Yes"},
            {"trait_type": "Tentura", "value": "Mask: Edges"},
            {"trait_type": "Tentura", "value": "Mode: Partial"},
            {"trait_type": "Tentura", "value": "Beams: Less"},
            {"trait_type": "Tentura", "value": "Shape: Two lines"},
            {"trait_type": "Tentura", "value": "Layout: Bent"},
            {"trait_type": "Tentura", "value": "Palette: Dawn"},
            {"trait_type": "Tentura", "value": "Grayscale: None"},
            {"trait_type": "Tentura", "value": "Background: Lighten"},
            {"trait_type": "Tentura", "value": "Distribution: Circle"},
        ],
        "is_static": False,
        "license": "CC BY-NC 4.0",
    }

    def test_artblocks_parser_should_parse_token(self):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        parser = ArtblocksParser(fetcher=fetcher, contract_caller=contract_caller)  # type: ignore[abstract]
        assert parser.should_parse_token(token=self.token)

    def test_artblocks_parser_parses_metadata(self):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        fetcher.fetch_mime_type_and_size = Mock(side_effect=[("application/json", 0), ("image/png", 3295933)])  # type: ignore[assignment]
        fetcher.fetch_content = MagicMock(return_value=self.raw_data)  # type: ignore[assignment]
        parser = ArtblocksParser(fetcher=fetcher, contract_caller=contract_caller)  # type: ignore[abstract]
        metadata = parser.parse_metadata(token=self.token, raw_data=self.raw_data)
        assert metadata == Metadata(
            token=Token(
                chain_identifier="ETHEREUM-MAINNET",
                collection_address="0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270",
                token_id=265000125,
                uri="https://api.artblocks.io/token/265000125",
            ),
            raw_data={
                "platform": "Art Blocks Factory",
                "tokenID": "265000125",
                "series": "N/A",
                "aspect_ratio": 1,
                "payout_address": "0x6C093Fe8bc59e1e0cAe2Ec10F0B717D3D182056B",
                "name": "Tentura #125",
                "minted": True,
                "artist": "Stranger in the Q",
                "description": "Tentura - fundamental device of time and being.\n\nThe essence of the Tentura's work is that it breaks the connection between the body and soul of every living being under its influence.\nThe subject becomes bound to a global variable, which is calculated and controlled by the Tentura itself.\nThis is the work of Tentura, with the amendment that the object of its control is reality.\n\nClick/tap to play/pause animation",
                "script_type": "p5js",
                "project_id": "265",
                "curation_status": "factory",
                "image": "https://media.artblocks.io/265000125.png",
                "generator_url": "https://generator.artblocks.io/265000125",
                "animation_url": "https://generator.artblocks.io/265000125",
                "royaltyInfo": {
                    "artistAddress": "0xe0324d6981ccb5b62bdd235366dee6172e0ef116",
                    "additionalPayee": "0x0000000000000000000000000000000000000000",
                    "additionalPayeePercentage": "0",
                    "royaltyFeeByID": 5,
                },
                "collection_name": "Tentura by Stranger in the Q",
                "website": "https://strangerintheq.github.io/tentura",
                "token_hash": "0x70c4c5ca361b259f56babbbbed29e1cb72921f99e5d45ed99eee65f2279a1307",
                "external_url": "https://artblocks.io/collections/factory/projects/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/265/tokens/265000125",
                "features": {
                    "Fog": "Yes",
                    "Mask": "Edges",
                    "Mode": "Partial",
                    "Beams": "Less",
                    "Shape": "Two lines",
                    "Layout": "Bent",
                    "Palette": "Dawn",
                    "Grayscale": "None",
                    "Background": "Lighten",
                    "Distribution": "Circle",
                },
                "traits": [
                    {"trait_type": "Tentura", "value": "All Tenturas"},
                    {"trait_type": "Tentura", "value": "Fog: Yes"},
                    {"trait_type": "Tentura", "value": "Mask: Edges"},
                    {"trait_type": "Tentura", "value": "Mode: Partial"},
                    {"trait_type": "Tentura", "value": "Beams: Less"},
                    {"trait_type": "Tentura", "value": "Shape: Two lines"},
                    {"trait_type": "Tentura", "value": "Layout: Bent"},
                    {"trait_type": "Tentura", "value": "Palette: Dawn"},
                    {"trait_type": "Tentura", "value": "Grayscale: None"},
                    {"trait_type": "Tentura", "value": "Background: Lighten"},
                    {"trait_type": "Tentura", "value": "Distribution: Circle"},
                ],
                "is_static": False,
                "license": "CC BY-NC 4.0",
            },
            attributes=[
                Attribute(
                    trait_type="Tentura", value="All Tenturas", display_type=None
                ),
                Attribute(trait_type="Tentura", value="Fog: Yes", display_type=None),
                Attribute(trait_type="Tentura", value="Mask: Edges", display_type=None),
                Attribute(
                    trait_type="Tentura", value="Mode: Partial", display_type=None
                ),
                Attribute(trait_type="Tentura", value="Beams: Less", display_type=None),
                Attribute(
                    trait_type="Tentura", value="Shape: Two lines", display_type=None
                ),
                Attribute(
                    trait_type="Tentura", value="Layout: Bent", display_type=None
                ),
                Attribute(
                    trait_type="Tentura", value="Palette: Dawn", display_type=None
                ),
                Attribute(
                    trait_type="Tentura", value="Grayscale: None", display_type=None
                ),
                Attribute(
                    trait_type="Tentura", value="Background: Lighten", display_type=None
                ),
                Attribute(
                    trait_type="Tentura",
                    value="Distribution: Circle",
                    display_type=None,
                ),
            ],
            standard=None,
            name="Tentura #125",
            description="Tentura - fundamental device of time and being.\n\nThe essence of the Tentura's work is that it breaks the connection between the body and soul of every living being under its influence.\nThe subject becomes bound to a global variable, which is calculated and controlled by the Tentura itself.\nThis is the work of Tentura, with the amendment that the object of its control is reality.\n\nClick/tap to play/pause animation",
            mime_type="application/json",
            image=MediaDetails(
                size=3295933,
                sha256=None,
                uri="https://media.artblocks.io/265000125.png",
                mime_type="image/png",
            ),
            content=None,
            additional_fields=[
                MetadataField(
                    field_name="platform",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the platform for the NFT asset",
                    value="Art Blocks Factory",
                ),
                MetadataField(
                    field_name="tokenID",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the token ID for the NFT asset",
                    value="265000125",
                ),
                MetadataField(
                    field_name="series",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the series for the NFT asset",
                    value="N/A",
                ),
                MetadataField(
                    field_name="aspect_ratio",
                    type=MetadataFieldType.NUMBER,
                    description="This property defines the aspect ratio for the NFT asset",
                    value=1,
                ),
                MetadataField(
                    field_name="payout_address",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the payout address for the NFT asset",
                    value="0x6C093Fe8bc59e1e0cAe2Ec10F0B717D3D182056B",
                ),
                MetadataField(
                    field_name="minted",
                    type=MetadataFieldType.BOOLEAN,
                    description="This property defines the minted state for the NFT asset",
                    value=True,
                ),
                MetadataField(
                    field_name="artist",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the artist for the NFT asset",
                    value="Stranger in the Q",
                ),
                MetadataField(
                    field_name="script_type",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the script type for the NFT asset",
                    value="p5js",
                ),
                MetadataField(
                    field_name="project_id",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the project ID for the NFT asset",
                    value="265",
                ),
                MetadataField(
                    field_name="curation_status",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the curation status for the NFT asset",
                    value="factory",
                ),
                MetadataField(
                    field_name="generator_url",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the generator URL for the NFT asset",
                    value="https://generator.artblocks.io/265000125",
                ),
                MetadataField(
                    field_name="animation_url",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the animation URL for the NFT asset",
                    value="https://generator.artblocks.io/265000125",
                ),
                MetadataField(
                    field_name="royaltyInfo",
                    type=MetadataFieldType.OBJECT,
                    description="This property defines the royalty information for the NFT asset",
                    value={
                        "artistAddress": "0xe0324d6981ccb5b62bdd235366dee6172e0ef116",
                        "additionalPayee": "0x0000000000000000000000000000000000000000",
                        "additionalPayeePercentage": "0",
                        "royaltyFeeByID": 5,
                    },
                ),
                MetadataField(
                    field_name="collection_name",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the collection name for the NFT asset",
                    value="Tentura by Stranger in the Q",
                ),
                MetadataField(
                    field_name="website",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the website for the NFT asset",
                    value="https://strangerintheq.github.io/tentura",
                ),
                MetadataField(
                    field_name="token_hash",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the token hash for the NFT asset",
                    value="0x70c4c5ca361b259f56babbbbed29e1cb72921f99e5d45ed99eee65f2279a1307",
                ),
                MetadataField(
                    field_name="external_url",
                    type=MetadataFieldType.TEXT,
                    description="This property defines an optional external URL that can reference a webpage or external asset for the NFT",
                    value="https://artblocks.io/collections/factory/projects/0xa7d8d9ef8d8ce8992df33d8b8cf4aebabd5bd270/265/tokens/265000125",
                ),
                MetadataField(
                    field_name="features",
                    type=MetadataFieldType.OBJECT,
                    description="This property defines the features for the NFT asset",
                    value={
                        "Fog": "Yes",
                        "Mask": "Edges",
                        "Mode": "Partial",
                        "Beams": "Less",
                        "Shape": "Two lines",
                        "Layout": "Bent",
                        "Palette": "Dawn",
                        "Grayscale": "None",
                        "Background": "Lighten",
                        "Distribution": "Circle",
                    },
                ),
                MetadataField(
                    field_name="is_static",
                    type=MetadataFieldType.BOOLEAN,
                    description="This property defines the static state for the NFT asset",
                    value=False,
                ),
                MetadataField(
                    field_name="license",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the license for the NFT asset",
                    value="CC BY-NC 4.0",
                ),
            ],
        )

    @pytest.mark.asyncio
    async def test_artblocks_parser_gen_parses_metadata(self):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        parser = ArtblocksParser(fetcher=fetcher, contract_caller=contract_caller)  # type: ignore[abstract]
        metadata = await parser.gen_parse_metadata(
            token=self.token, raw_data=self.raw_data
        )
        assert metadata
