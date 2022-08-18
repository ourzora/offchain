from offchain.models.metadata import MetadataStandard
from offchain.parsers.base_parser import BaseParser


class SchemaParser(BaseParser):
    _METADATA_STANDARD: MetadataStandard
