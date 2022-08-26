from offchain.metadata.models.metadata import MetadataStandard
from offchain.metadata.parsers.base_parser import BaseParser


class SchemaParser(BaseParser):
    """Base class for schema parsers

    All parsers that handle schema-based metadata parsing will need to inherit from this base class.

    Attributes:
        _METADATA_STANDARD (MetadataStandard): the metadata standard that this parser supports.
    """

    _METADATA_STANDARD: MetadataStandard
