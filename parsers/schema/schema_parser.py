from models.metadata import MetadataStandard
from parsers.base_parser import BaseParser


class SchemaParser(BaseParser):
    _METADATA_STANDARD: MetadataStandard
