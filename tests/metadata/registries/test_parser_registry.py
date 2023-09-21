import pytest

from offchain.metadata.parsers import (  # type: ignore[attr-defined]
    ENSParser,
    FoundationParser,
    OpenseaParser,
    SuperRareParser,
    PunksParser,
    ArtblocksParser,
    AutoglyphsParser,
    HashmasksParser,
    ChainRunnersParser,
    LootParser,
    NounsParser,
    ZoraParser,
    MakersPlaceParser,
    DecentralandParser,
    DefaultCatchallParser,
)
from offchain.metadata.parsers.schema.schema_parser import SchemaParser
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry


class TestParserRegistry:
    def test_parser_registry_no_duplicate_class_names(self):  # type: ignore[no-untyped-def]  # noqa: E501
        parser_registry = ParserRegistry()
        with pytest.raises(AssertionError):
            parser_registry.register(OpenseaParser)  # type: ignore[type-abstract]

    def test_collection_parser_must_specify_collection_addresses(self):  # type: ignore[no-untyped-def]  # noqa: E501
        class BadCollectionParser(CollectionParser):
            pass

        parser_registry = ParserRegistry()
        with pytest.raises(AssertionError):
            parser_registry.register(BadCollectionParser)  # type: ignore[type-abstract]

    def test_schema_parser_must_specify_metadata_standard(self):  # type: ignore[no-untyped-def]  # noqa: E501
        class BadSchemaParser(SchemaParser):
            pass

        parser_registry = ParserRegistry()
        with pytest.raises(AssertionError):
            parser_registry.register(BadSchemaParser)  # type: ignore[type-abstract]

    def test_parser_registry_has_all_parsers(self):  # type: ignore[no-untyped-def]
        parser_registry = ParserRegistry()
        assert set(parser_registry.get_all()) == set(
            [
                ENSParser,
                FoundationParser,
                OpenseaParser,
                SuperRareParser,
                PunksParser,
                AutoglyphsParser,
                HashmasksParser,
                ChainRunnersParser,
                LootParser,
                ArtblocksParser,
                DecentralandParser,
                ZoraParser,
                NounsParser,
                MakersPlaceParser,
                DefaultCatchallParser,
            ]
        )

    def test_parser_registry_has_collection_parsers(self):  # type: ignore[no-untyped-def]  # noqa: E501
        parser_registry = ParserRegistry()
        assert set(parser_registry.get_all_collection_parsers()) == set(
            [
                ENSParser,
                FoundationParser,
                SuperRareParser,
                ArtblocksParser,
                PunksParser,
                AutoglyphsParser,
                ChainRunnersParser,
                LootParser,
                NounsParser,
                DecentralandParser,
                ZoraParser,
                MakersPlaceParser,
                HashmasksParser,
            ]
        )

    def test_parser_registry_has_schema_parsers(self):  # type: ignore[no-untyped-def]
        parser_registry = ParserRegistry()
        assert set(parser_registry.get_all_schema_parsers()) == set(
            [
                OpenseaParser,
            ]
        )

    def test_parser_registry_has_catchall_parsers(self):  # type: ignore[no-untyped-def]
        parser_registry = ParserRegistry()
        assert set(parser_registry.get_all_catchall_parsers()) == set(
            [
                DefaultCatchallParser,
            ]
        )
