from typing import Any, Optional

from offchain.base.types import StringEnum
from offchain.base.base_model import BaseModel  # type: ignore[attr-defined]
from offchain.metadata.models.token import Token


class MetadataStandard(StringEnum):
    """Standards for NFT metadata formats"""

    COLLECTION_STANDARD = "COLLECTION_STANDARD"
    OPENSEA_STANDARD = "OPENSEA_STANDARD"
    UNKNOWN_STANDARD = "UNKNOWN_STANDARD"


class MetadataFieldType(StringEnum):
    """Valid metadata field types"""

    BOOLEAN = "BOOLEAN"
    LIST = "LIST"
    NUMBER = "NUMBER"
    OBJECT = "OBJECT"
    TEXT = "TEXT"


class Attribute(BaseModel):
    """NFT metadata atttribute

    Attributes:
        trait_type (str, optional): the attribute key.
        value (str, optional): the attribute value.
        display_type (str, optional): informs how the attribute is displayed.
    """

    trait_type: Optional[str] = None
    value: Optional[str] = None
    display_type: Optional[str] = None


class MediaDetails(BaseModel):
    """Metadata media information

    Attributes:
        size (int, optional): size of the media.
        sha256 (str, optional): the SHA256 hash of the media.
        uri (str, optional): the uri at which the media was found.
        mime_type (str, optional): the mime type of the media.
    """

    size: Optional[int] = None
    sha256: Optional[str] = None
    uri: Optional[str] = None
    mime_type: Optional[str] = None


class MetadataField(BaseModel):
    """Additional metadata field that does not fit within the defined Metadata entity

    Some metadata standards will have standardized additional metadata fields that are not
    captured in our metadata schema. For example, OpenSea allows for an 'external_url' field.

    Attributes:
        field_name (str): name of the metadata field.
        type (MetadataFieldType): metadata field type.
        description (str, optional): a description of what this metadata field represents.
        value (any): the value of the metadata field.
    """  # noqa: E501

    field_name: str
    type: MetadataFieldType
    description: str
    value: Any


class Metadata(BaseModel):
    """A standard metadata interface

    This aims to be a relatively comprehensive definition of NFT metadata, but not all
    metadata will fit cleanly into this shape.

    Attributes:
        token (Token): a Token interface with all information required to uniquely identify an NFT

        raw_data (dict): raw metadata object fetched from token uri.
        standard (MetadataStandard): accepted metadata standard based on the format of the metadata.
        attributes (list[Attribute]): list of token metadata attributes.
        name (str, optional): token name.
        description (str, optional): token description.
        mime_type (str, optional): metadata mime type, e.g. "image/png".

        image (str, optional): nested image in the metadata.
        content (str, optional): nested content, e.g. video, audio, etc., in the metadata.

        additional_fields (list[MetadataField], optional): any additional metadata fields
            that don't fit in the defined schema.

    """  # noqa: E501

    token: Token

    raw_data: dict  # type: ignore[type-arg]
    attributes: list[Attribute]
    standard: Optional[MetadataStandard] = None
    name: Optional[str] = None
    description: Optional[str] = None
    mime_type: Optional[str] = None

    image: Optional[MediaDetails] = None
    content: Optional[MediaDetails] = None

    additional_fields: Optional[list[MetadataField]] = None
