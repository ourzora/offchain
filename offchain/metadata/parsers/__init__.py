from offchain.base.types import StringEnum

from .base_parser import BaseParser
from .collection.collection_parser import CollectionParser
from .collection.nouns_parser import NounsParser
from .schema.opensea import OpenseaParser
from .schema.unknown import UnknownParser
from .schema.schema_parser import SchemaParser


class ParserType(StringEnum):
    OpenseaParser = OpenseaParser.__name__
    NounsParser = NounsParser.__name__
    UnknownParser = UnknownParser.__name__
