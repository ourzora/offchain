from offchain.base.types import StringEnum

from .base_parser import BaseParser
from .collection.collection_parser import CollectionParser
from .collection.ens import ENSParser
from .schema.opensea import OpenseaParser
from .schema.unknown import UnknownParser
from .schema.schema_parser import SchemaParser


class ParserType(StringEnum):
    ENSParser = ENSParser.__name__
    OpenseaParser = OpenseaParser.__name__
    UnknownParser = UnknownParser.__name__
