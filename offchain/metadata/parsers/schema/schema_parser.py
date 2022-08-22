from offchain.metadata.models.metadata import MetadataStandard
from offchain.metadata.parsers.base_parser import BaseParser


class SchemaParser(BaseParser):
    _METADATA_STANDARD: MetadataStandard
