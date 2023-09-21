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
from offchain.metadata.parsers.collection.autoglyphs import AutoglyphsParser
from offchain.web3.contract_caller import ContractCaller


class TestAutoglyphsParser:
    token = Token(
        chain_identifier="ETHEREUM-MAINNET",
        collection_address="0xd4e4078ca3495de5b1d4db434bebc5a986197782",
        token_id=35,
        uri=None,
    )

    raw_data = {
        "title": "Autoglyph #35",
        "name": "Autoglyph #35",
        "image": "https://www.larvalabs.com/autoglyphs/glyphimage?index=35",
        "description": 'Autoglyphs are the first "on-chain" generative art on the Ethereum blockchain. A '
        "completely self-contained mechanism for the creation and ownership of an artwork.",
        "external_url": "https://www.larvalabs.com/autoglyphs/glyph?index=35",
    }

    def test_autoglyphs_parser_should_parse_token(self):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        parser = AutoglyphsParser(fetcher=fetcher, contract_caller=contract_caller)  # type: ignore[abstract]
        assert parser.should_parse_token(token=self.token)

    def test_autoglyphs_parser_parses_metadata(self):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        fetcher.fetch_mime_type_and_size = MagicMock(return_value=("image/svg+xml", 0))  # type: ignore[assignment]
        fetcher.fetch_content = MagicMock(return_value=self.raw_data)  # type: ignore[assignment]
        parser = AutoglyphsParser(fetcher=fetcher, contract_caller=contract_caller)  # type: ignore[abstract]
        metadata = parser.parse_metadata(token=self.token, raw_data=self.raw_data)
        assert metadata == Metadata(
            token=Token(
                chain_identifier="ETHEREUM-MAINNET",
                collection_address="0xd4e4078ca3495de5b1d4db434bebc5a986197782",
                token_id=35,
                uri=None,
            ),
            raw_data={
                "title": "Autoglyph #35",
                "name": "Autoglyph #35",
                "image": "https://www.larvalabs.com/autoglyphs/glyphimage?index=35",
                "description": 'Autoglyphs are the first "on-chain" generative art on the Ethereum blockchain. A '
                "completely self-contained mechanism for the creation and ownership of an artwork.",
                "external_url": "https://www.larvalabs.com/autoglyphs/glyph?index=35",
            },
            attributes=[
                Attribute(trait_type="Symbol Scheme", value=" X/\\", display_type=None),
            ],
            standard=None,
            name="Autoglyph #35",
            description='Autoglyphs are the first "on-chain" generative art on the Ethereum blockchain. A completely self-contained mechanism for the creation and ownership of an artwork.',
            mime_type="application/json",
            image=MediaDetails(
                size=0,
                sha256=None,
                uri="https://www.larvalabs.com/autoglyphs/glyphimage?index=35",
                mime_type="image/svg+xml",
            ),
            content=MediaDetails(
                size=None,
                sha256=None,
                uri="..../......\\......\\.X....\\.../..\\.X.\\..\\.../..\\...\\......\\.X....%0A.......X\\.......\\.X.......X\\.......\\./......./\\.......\\./.......%0A.....X..\\...../.X..\\...../.X..\\...../.X......../.X......../.....%0A..../....X.....X...\\....../....X/....X...\\.\\..../...../....X....%0A/../......./../......\\.../......\\..\\..X....\\..\\..X..X....\\..X..X%0A..X../............/.../..\\X..\\X../.../...X...X.......\\...\\X../..%0A.........XX...X....XX...X..../....X..../...//...\\/...//...\\\\...\\%0A.X.....\\../.....\\..X.....\\/./.....\\X.X....../.......\\X......../.%0A.\\\\.....//\\....XXX.....................\\\\\\....///.....XX........%0A...X..X./.\\..\\.........X./../......X..X./.\\..\\.........X./../.\\.%0A......X/\\\\...........X/\\.................X/\\............X/\\.....%0A\\.../......../.../.../.../.../....X...X...X...X.\\.X.....\\..X....%0A..................\\..\\../.X/..X\\./\\.X/.X........................%0A.........\\./.X..\\./....\\.X..........\\./....\\.X..../.X..........\\%0A.././.X.......X\\X........../.......\\X\\.......\\././......./.X.X..%0A...X....X.....\\../..../..X.....\\....\\./..X....X.....\\../.\\../...%0A.\\X....\\X....\\X....\\X..../X..../X..../X..../...../...../...../..%0A........X../.../..\\.........X..X/../...\\..\\.....X...X../...\\..\\\\%0A\\X.../......\\/...\\......./...........\\X...\\......\\X...\\...X.../.%0A..\\\\..XX........\\..XX......../\\...X........//...........//......%0AX.....X.........X..X..X..XX./../X.\\X.//../../../..\\..\\.../.\\\\../%0A....\\.....X/\\.........../......X/\\.....X.....\\\\.....X/\\.........%0A...../..../..../....X....X....X../..../..../....X....X.\\..X.\\...%0A.........X\\..\\........../\\..\\..........X\\............./\\........%0A......X...../.......././.....\\........\\.X.X...\\....X...\\./.....\\%0A\\././\\.\\././.X.X/./.X.X\\.\\.X.X\\.\\././\\.\\././.X.X/./.X.X....X.X..%0A.X./.X./....X...X...X.........\\...\\...\\..../.\\./.\\./....X./.X./.%0A.\\X........././..........X.........\\../.........\\X\\X........./.\\%0A......././.......X../..\\......X../..\\......X../..\\....X.X..\\..\\.%0A/....\\/..../......./....\\X...........\\/....\\X......\\X...\\X.....X%0A..\\..X......X......\\..X..\\\\.X....../...../\\......../....../.....%0A...X........\\..\\/X../X................\\.../X../X...........\\/..\\%0A\\../\\...........X/..X/...\\................X/..X/\\..\\........X...%0A...../....../........\\/...../......X.\\\\..X..\\......X......X..\\..%0AX.....X\\...X\\......X\\..../\\...........X\\..../......./..../\\..../%0A.\\..\\..X.X....\\../..X......\\../..X......\\../..X......././.......%0A\\./.........X\\X\\........./..\\.........X.........././.........X\\.%0A./.X./.X..../.\\./.\\./....\\...\\...\\.........X...X...X..../.X./.X.%0A..X.X....X.X././X.X././.\\.\\/./.\\.\\X.X.\\.\\X.X././X.X././.\\.\\/./.\\%0A\\...../.\\...X....\\...X.X.\\........\\....././......../.....X......%0A........\\/.............\\X..........\\..\\/..........\\..\\X.........%0A...\\.X..\\.X....X..../..../..../..X....X....X..../..../..../.....%0A.........\\/X.....\\\\.....X.....\\/X....../...........\\/X.....\\....%0A/..\\\\./...\\..\\../../../..//.X\\.X/../.XX..X..X..X.........X.....X%0A......//...........//........X...\\/........XX..\\........XX..\\\\..%0A./...X...\\...X\\......\\...X\\.........../.......\\.../\\....../...X\\%0A\\\\..\\.../..X...X.....\\..\\.../../X..X.........\\../.../..X........%0A../...../...../...../....X/....X/....X/....X\\....X\\....X\\....X\\.%0A.../..\\./..\\.....X....X../.\\....\\.....X../..../..\\.....X....X...%0A..X.X./......././.\\.......\\X\\......./..........X\\X.......X././..%0A\\..........X./....X.\\..../.\\..........X.\\..../.\\..X./.\\.........%0A........................X./X.\\/.\\X../X./..\\..\\..................%0A....X..\\.....X.\\.X...X...X...X..../.../.../.../.../......../...\\%0A.....\\/X............\\/X.................\\/X...........\\\\/X......%0A.\\./../.X.........\\..\\./.X..X....../../.X.........\\..\\./.X..X...%0A........XX.....///....\\\\\\.....................XXX....\\//.....\\\\.%0A./........X\\......./......X.X\\....././\\.....X..\\...../..\\.....X.%0A\\...\\\\...//.../\\...//.../....X..../....X...XX....X...XX.........%0A../..X\\...\\.......X...X.../.../..X\\..X\\../.../............/..X..%0AX..X..\\....X..X..\\..\\....X..\\..\\....../...\\....../../......./../%0A....X..../...../....\\.\\...X..../X..../......\\...X.....X..../....%0A...../........X./........X./.....\\..X./.....\\..X./.....\\..X.....%0A......./.\\.......\\/......./.\\.......\\X.......X.\\.......\\X.......%0A....X.\\......\\...\\../...\\..\\.X.\\../...\\....X.\\......\\....../....%0A",
                mime_type="text/plain",
            ),
            additional_fields=[
                MetadataField(
                    field_name="external_url",
                    type=MetadataFieldType.TEXT,
                    description="This property defines an optional external URL that can reference a webpage or external asset for the NFT",
                    value="https://www.larvalabs.com/autoglyphs/glyph?index=35",
                ),
                MetadataField(
                    field_name="title",
                    type=MetadataFieldType.TEXT,
                    description="This property defines an the title for the NFT asset",
                    value="Autoglyph #35",
                ),
            ],
        )

    @pytest.mark.asyncio
    async def test_autoglyphs_parser_gen_parses_metadata(self):  # type: ignore[no-untyped-def]
        fetcher = MetadataFetcher()
        contract_caller = ContractCaller()
        parser = AutoglyphsParser(fetcher=fetcher, contract_caller=contract_caller)  # type: ignore[abstract]
        metadata = await parser.gen_parse_metadata(
            token=self.token, raw_data=self.raw_data
        )
        assert metadata
