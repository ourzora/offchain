from typing import Type

from parsers.base_parser import BaseParser
from parsers.collection.collection_parser import CollectionParser
from parsers.schema.schema_parser import SchemaParser
from registries.base_registry import BaseRegistry


class ParserRegistry(BaseRegistry):
    __parser_registry: dict[str, BaseParser] = {}

    @staticmethod
    def get_all() -> list[BaseParser]:
        return list(ParserRegistry.__parser_registry.values())

    @staticmethod
    def get_all_collection_parsers() -> list[CollectionParser]:
        return [parser for parser in ParserRegistry.__parser_registry.values() if isinstance(parser, CollectionParser)]

    @staticmethod
    def get_all_schema_parsers() -> list[SchemaParser]:
        return [parser for parser in ParserRegistry.__parser_registry.values() if isinstance(parser, SchemaParser)]

    @staticmethod
    def validate(parser_cls: Type[BaseParser]):
        assert (
            parser_cls.__name__ not in ParserRegistry.__parser_registry
        ), f"{parser_cls.__name__} already exists in registry."

        if issubclass(parser_cls, CollectionParser):
            assert (
                hasattr(parser_cls, "_COLLECTION_ADDRESSES")
                and parser_cls._COLLECTION_ADDRESSES is not None
                and isinstance(parser_cls._COLLECTION_ADDRESSES, list)
                and len(parser_cls._COLLECTION_ADDRESSES) > 0
            )
        elif issubclass(parser_cls, SchemaParser):
            assert (
                hasattr(parser_cls, "_METADATA_STANDARD")
                and parser_cls._METADATA_STANDARD is not None
                and isinstance(parser_cls._METADATA_STANDARD, str)
            )

    @staticmethod
    def add(parser_cls: Type[BaseParser]):
        ParserRegistry.__parser_registry[parser_cls.__name__] = parser_cls
