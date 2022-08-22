from typing import Any, Optional

from offchain.base.types import StringEnum
from offchain.models.base_model import BaseModel


class MetadataStandard(StringEnum):
    ERC721_STANDARD = "ERC721_STANDARD"
    ERC1155_STANDARD = "ERC1155_STANDARD"
    OPENSEA_STANDARD = "OPENSEA_STANDARD"
    UNKNOWN = "UNKNOWN"


class MetadataFieldType(StringEnum):
    BOOLEAN = "BOOLEAN"
    LIST = "LIST"
    NUMBER = "NUMBER"
    OBJECT = "OBJECT"
    TEXT = "TEXT"


class Attribute(BaseModel):
    trait_type: Optional[str] = None
    value: Optional[str] = None
    display_type: Optional[str] = None


class MediaDetails(BaseModel):
    size: Optional[int] = None
    sha256: Optional[str] = None
    uri: Optional[str] = None
    mime_type: Optional[str] = None


class MetadataField(BaseModel):
    field_name: str
    type: MetadataFieldType
    description: str
    value: Any


class Metadata(BaseModel):
    chain_identifier: str
    collection_address: str
    token_id: int

    raw_data: dict
    standard: MetadataStandard
    attributes: list[Attribute]
    name: Optional[str] = None
    description: Optional[str] = None
    mime_type: Optional[str] = None
    token_uri: Optional[str] = None

    image: Optional[MediaDetails] = None
    content: Optional[MediaDetails] = None

    additional_fields: Optional[list[MetadataField]] = None
