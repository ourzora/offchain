from typing import Optional, Type

from offchain.metadata.parsers.base_parser import BaseParser
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.parsers.schema.schema_parser import SchemaParser
from offchain.metadata.registries.base_registry import BaseRegistry, Priority


class ParserRegistry(BaseRegistry):
    __parser_registry: dict[str, BaseParser] = {}

    @staticmethod
    def get_all() -> list[BaseParser]:
        return sorted(ParserRegistry.__parser_registry.values(), key=ParserRegistry.get_priority_by_cls)

    @staticmethod
    def get_all_collection_parsers() -> list[CollectionParser]:
        return sorted(
            [parser for parser in ParserRegistry.__parser_registry.values() if issubclass(parser, CollectionParser)],
            key=ParserRegistry.get_priority_by_cls,
        )

    @staticmethod
    def get_all_schema_parsers() -> list[SchemaParser]:
        return sorted(
            [parser for parser in ParserRegistry.__parser_registry.values() if issubclass(parser, SchemaParser)],
            key=ParserRegistry.get_priority_by_cls,
        )

    @staticmethod
    def get_priority_by_cls(parser_cls: Type[BaseParser]) -> Priority:
        if (
            hasattr(parser_cls, "_PARSER_PRIORITY")
            and parser_cls._PARSER_PRIORITY is not None
            and isinstance(parser_cls._PARSER_PRIORITY, Priority)
        ):
            return parser_cls._PARSER_PRIORITY

        # normal is default sort
        return Priority.NORMAL

    @staticmethod
    def get_parser_cls_by_name(cls_name: str) -> Optional[BaseParser]:
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
        elif issubclass(parser_cls, SchemaParser):
            assert (
                hasattr(parser_cls, "_METADATA_STANDARD")
                and parser_cls._METADATA_STANDARD is not None
                and isinstance(parser_cls._METADATA_STANDARD, str)
            )

    @staticmethod
    def add(parser_cls: Type[BaseParser]):
        ParserRegistry.__parser_registry[parser_cls.__name__] = parser_cls

    @staticmethod
    def remove(parser_cls: Type[BaseParser]):
        if parser_cls.__name__ in ParserRegistry.__parser_registry:
            del ParserRegistry.__parser_registry[parser_cls.__name__]
