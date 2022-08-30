from typing import Optional

from offchain.constants.addresses import CollectionAddress
from offchain.metadata.models.metadata import (
    MediaDetails,
    Metadata,
    MetadataField,
    MetadataFieldType,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry


@ParserRegistry.register
class SuperRareParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [CollectionAddress.SUPERRARE]

    def get_image_details(self, raw_data: dict) -> Optional[MediaDetails]:
        image_uri = raw_data.get("image")
        if not image_uri:
            return None
        details = MediaDetails(uri=image_uri, size=None, sha256=None, mime_type=None)
        try:
            content_type, size = self.fetcher.fetch_mime_type_and_size(image_uri)
            details.mime_type = content_type
            details.size = size
        except Exception:
            pass
        return details

    def get_content_details(self, raw_data: dict) -> Optional[MediaDetails]:
        media = raw_data.get("media")
        if not media or not isinstance(media, dict):
            return
        content_uri = media.get("uri")
        if not content_uri:
            return
        details = MediaDetails(
            uri=content_uri,
            size=media.get("size"),
            sha256=None,
            mime_type=media.get("mimeType"),
        )
        if not details.mime_type:
            try:
                content_type, size = self.fetcher.fetch_mime_type_and_size(content_uri)
                details.mime_type = content_type
                details.size = size
            except Exception:
                pass

        return details

    def parse_additional_fields(self, raw_data: dict) -> list[MetadataField]:
        additional_fields = []
        if created_by := raw_data.get("createdBy"):
            additional_fields.append(
                MetadataField(
                    field_name="created_by",
                    type=MetadataFieldType.TEXT,
                    description="The creator of an NFT.",
                    value=created_by,
                )
            )
        if year_created := raw_data.get("yearCreated"):
            additional_fields.append(
                MetadataField(
                    field_name="year_created",
                    type=MetadataFieldType.NUMBER,
                    description="The year in which an NFT was created.",
                    value=year_created,
                )
            )
        if tags := raw_data.get("tags"):
            additional_fields.append(
                MetadataField(
                    field_name="tags",
                    type=MetadataFieldType.LIST,
                    description="List of tags associated with an NFT.",
                    value=tags,
                )
            )
        return additional_fields

    def parse_metadata(self, token: Token, raw_data: Optional[dict], *args, **kwargs) -> Optional[Metadata]:

        mime_type, _ = self.fetcher.fetch_mime_type_and_size(token.uri)

        return Metadata(
            token=token,
            raw_data=raw_data,
            name=raw_data.get("name"),
            description=raw_data.get("description"),
            mime_type=mime_type,
            image=self.get_image_details(raw_data),
            content=self.get_content_details(raw_data),
            additional_fields=self.parse_additional_fields(raw_data),
            attributes=[],
        )
