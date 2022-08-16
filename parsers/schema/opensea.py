from metazerse.fetchers.base_fetcher import BaseFetcher
from metazerse.models.metadata import (
    Attribute,
    MediaDetails,
    Metadata,
    MetadataField,
    MetadataFieldType,
    MetadataStandard,
)
from metazerse.models.token import Token
from metazerse.parsers.schema.schema_parser import SchemaParser


class OpenseaParser(SchemaParser):
    _METADATA_STANDARD: MetadataStandard = MetadataStandard.OPENSEA_STANDARD

    def __init__(self, fetcher: BaseFetcher) -> None:
        self.fetcher = fetcher

    def parse_attribute(self, attribute_dict: dict) -> Attribute:
        return Attribute(
            trait_type=attribute_dict.get("trait_type"),
            value=attribute_dict.get("value"),
            display_type=attribute_dict.get("display_type"),
        )

    def parse_additional_fields(self, raw_data: dict) -> list[MetadataField]:
        additional_fields = []
        if (external_url := raw_data.get("external_url")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="external_url",
                    type=MetadataFieldType.TEXT,
                    description="This is the URL that will appear below the asset's image on OpenSea "
                    "and will allow users to leave OpenSea and view the item on your site.",
                    value=external_url,
                )
            )
        if (background_color := raw_data.get("background_color")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="background_color",
                    type=MetadataFieldType.TEXT,
                    description="Background color of the item on OpenSea. Must be a six-character "
                    "hexadecimal without a pre-pended #.",
                    value=background_color,
                )
            )
        if (animation_url := raw_data.get("animation_url")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="animation_url",
                    type=MetadataFieldType.TEXT,
                    description="A URL to a multi-media attachment for the item.",
                    value=animation_url,
                )
            )
        if (youtube_url := raw_data.get("youtube_url")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="youtube_url",
                    type=MetadataFieldType.TEXT,
                    description="A URL to a YouTube video.",
                    value=youtube_url,
                )
            )
        return additional_fields

    def parse_metadata(self, token: Token) -> Metadata:
        mime, _ = self.fetcher.fetch_mime_type_and_size(token.uri)
        raw_data = self.fetcher.fetch_content(token.uri)
        attributes = [
            self.parse_attribute(attribute) for attribute in raw_data.get("attributes", [])
        ]
        image_uri = raw_data.get("image") or raw_data.get("image_data")
        if image_uri:
            image_mime, image_size = self.fetcher.fetch_mime_type_and_size(image_uri)
            image = MediaDetails(size=image_size, uri=image_uri, mime_type=image_mime)

        return Metadata(
            collection_address=token.collection_address,
            token_id=token.token_id,
            token_uri=token.uri,
            raw_data=raw_data,
            standard=OpenseaParser._METADATA_STANDARD,
            attributes=attributes,
            name=raw_data.get("name"),
            description=raw_data.get("description"),
            mime_type=mime,
            image=image,
            additional_fields=self.parse_additional_fields(raw_data),
        )
