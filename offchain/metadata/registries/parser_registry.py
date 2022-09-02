from typing import Optional, Type

from offchain.metadata.parsers.base_parser import BaseParser
from offchain.metadata.parsers.catchall.catchall_parser import CatchallParser
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.parsers.schema.schema_parser import SchemaParser
from offchain.metadata.registries.base_registry import BaseRegistry


class ParserRegistry(BaseRegistry):
    __parser_registry: dict[str, BaseParser] = {}

    @staticmethod
    def get_all() -> list[Type[BaseParser]]:
        return list(ParserRegistry.__parser_registry.values())

    @staticmethod
    def get_all_collection_parsers() -> list[Type[CollectionParser]]:
        return [parser for parser in ParserRegistry.__parser_registry.values() if issubclass(parser, CollectionParser)]

    @staticmethod
    def get_all_schema_parsers() -> list[Type[SchemaParser]]:
        return [parser for parser in ParserRegistry.__parser_registry.values() if issubclass(parser, SchemaParser)]

    @staticmethod
    def get_all_catchall_parsers() -> list[Type[CatchallParser]]:
        return [parser for parser in ParserRegistry.__parser_registry.values() if issubclass(parser, CatchallParser)]

    @staticmethod
    def get_parser_cls_by_name(cls_name: str) -> Optional[Type[BaseParser]]:
        return ParserRegistry.__parser_registry.get(cls_name)

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
        assert (
            hasattr(parser_cls, "_METADATA_STANDARD")
            and parser_cls._METADATA_STANDARD is not None
            and isinstance(parser_cls._METADATA_STANDARD, str)
        )

    @staticmethod
    def add(parser_cls: Type[BaseParser]):
        ParserRegistry.__parser_registry[parser_cls.__name__] = parser_cls
