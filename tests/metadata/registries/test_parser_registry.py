import pytest

from offchain.metadata.parsers import (
    ENSParser,
    FoundationParser,
    OpenseaParser,
    SuperRareParser,
    PunksParser,
    AutoglyphsParser,
    UnknownParser,
)
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.parsers.priority import Priority
from offchain.metadata.parsers.schema.schema_parser import SchemaParser
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

    def test_parser_priority(self):
        class LowPriorityCollectionParser(CollectionParser):
            _COLLECTION_ADDRESSES = ["test"]
            _PARSER_PRIORITY = Priority.LOW
            pass

        class HighPriorityCollectionParser(CollectionParser):
            _COLLECTION_ADDRESSES = ["test"]
            _PARSER_PRIORITY = Priority.HIGH
            pass

        parser_registry = ParserRegistry()

        parser_registry.register(LowPriorityCollectionParser)
        parser_registry.register(HighPriorityCollectionParser)

        low_priority = 0
        high_priority = 0

        parsers = parser_registry.get_all()

        for i, parser in enumerate(parsers):
            if issubclass(parser, HighPriorityCollectionParser):
                high_priority = i
            elif issubclass(parser, LowPriorityCollectionParser):
                low_priority = i

        parser_registry.remove(LowPriorityCollectionParser)
        parser_registry.remove(HighPriorityCollectionParser)

        # low priority should be a higher number, meaning it comes later in the iteration
        assert high_priority < low_priority

    def test_parser_registry_has_all_parsers(self):
        parser_registry = ParserRegistry()
        assert set(parser_registry.get_all()) == set(
            [
                ENSParser,
                FoundationParser,
                OpenseaParser,
                SuperRareParser,
                PunksParser,
                AutoglyphsParser,
                UnknownParser,
            ]
        )
