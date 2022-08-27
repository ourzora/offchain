from typing import Optional

from offchain.metadata.fetchers import BaseFetcher
from offchain.metadata.models.metadata import (
    Metadata,
    MediaDetails,
    MetadataField,
    MetadataFieldType,
    MetadataStandard,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry


@ParserRegistry.register
class ZoraParser(CollectionParser):
    _METADATA_STANDARD: MetadataStandard = MetadataStandard.ZORA_STANDARD

    def __init__(self, fetcher: BaseFetcher) -> None:
        self.fetcher = fetcher

    def get_additional_fields(self, raw_data: dict) -> list[MetadataField]:
        additional_fields = []
        if version := raw_data.get("version"):
            additional_fields.append(
                MetadataField(
                    field_name="version",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the calendar version of the schema so that consumers can "
                    "correctly parse the json",
                    value=version,
                )
            )

        if (animation_url := raw_data.get("animation_url")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="animation_url",
                    type=MetadataFieldType.TEXT,
                    description="A URL to a multi-media attachment for the item. The file extensions GLTF, GLB, WEBM, "
                    "MP4, M4V, OGV, and OGG are supported, along with the audio-only extensions MP3, WAV, "
                    "and OGA. Animation_url also supports HTML pages, allowing you to build rich "
                    "experiences using JavaScript canvas, WebGL, and more. Access to browser extensions "
                    "is not supported",
                    value=animation_url,
                )
            )

        if (external_url := raw_data.get("external_url")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="external_url",
                    type=MetadataFieldType.TEXT,
                    description="This property defines an optional external URL that can reference a webpage or "
                    "external asset for the NFT",
                    value=external_url,
                )
            )
        return additional_fields

    def parse_metadata(
        self, token: Token, raw_data: dict, *args, **kwargs
    ) -> Optional[Metadata]:
        """Given a token and raw data returned from the token uri, return a normalized Metadata object.

        Args:
            token (Token): token to process metadata for.
            raw_data (dict): raw data returned from token uri.

        Returns:
            Optional[Metadata]: normalized metadata object, if successfully parsed.
        """

        mime, size = self.fetcher.fetch_mime_type_and_size(token.uri)
        raw_content = self.fetcher.fetch_content(token.uri)

        content = None
        if raw_content:
            content = MediaDetails(size=size, uri=token.uri, mime_type=mime)

        attributes = [
            self.parse_attribute(attribute)
            for attribute in raw_data.get("attributes", [])
        ]

        image = None
        image_uri = raw_data.get("image") or raw_data.get("image_data")
        if image_uri:
            image_mime, image_size = self.fetcher.fetch_mime_type_and_size(image_uri)
            image = MediaDetails(size=image_size, uri=image_uri, mime_type=image_mime)

        return Metadata(
            token=token,
            raw_data=raw_data,
            standard=ZoraParser._METADATA_STANDARD,
            attributes=attributes,
            name=raw_data.get("name"),
            description=raw_data.get("description"),
            mime_type=mime,
            image=image,
            content=content,
            additional_fields=self.parse_additional_fields(raw_data),
        )

    def should_parse_token(self, token: Token, raw_data: dict, *args, **kwargs) -> bool:
        """Return whether or not a schema parser should parse a given token.

        Args:
            token (Token): the token whose metadata needs to be parsed.
            raw_data (dict): raw data returned from token metadata uri.

        Returns:
            bool: whether or not the schema parser handles this token.
        """
        return isinstance(raw_data.get("attributes"), list)