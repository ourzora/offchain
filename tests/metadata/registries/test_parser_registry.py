import pytest

from offchain.metadata.parsers import (
    ENSParser,
    FoundationParser,
    OpenseaParser,
    UnknownParser,
)
from offchain.metadata.parsers.schema.schema_parser import SchemaParser
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry


class TestParserRegistry:
    def test_parser_registry_no_duplicate_class_names(self):
        parser_registry = ParserRegistry()
        with pytest.raises(AssertionError):
            parser_registry.register(OpenseaParser)

    def test_collection_parser_must_specify_collection_addresses(self):
        class BadCollectionParser(CollectionParser):
            pass

        parser_registry = ParserRegistry()
        with pytest.raises(AssertionError):
            parser_registry.register(BadCollectionParser)

    def test_schema_parser_must_specify_metadata_standard(self):
        class BadSchemaParser(SchemaParser):
            pass

        parser_registry = ParserRegistry()
        with pytest.raises(AssertionError):
            parser_registry.register(BadSchemaParser)

    def test_parser_registry_has_all_parsers(self):
        parser_registry = ParserRegistry()
        assert set(parser_registry.get_all()) == set(
            [
                ENSParser,
                FoundationParser,
                OpenseaParser,
                UnknownParser,
            ]
        )
