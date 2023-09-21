from typing import Optional

from offchain.metadata.models.metadata import (
    Attribute,
    MediaDetails,
    Metadata,
    MetadataField,
    MetadataFieldType,
    MetadataStandard,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.schema.schema_parser import SchemaParser
from offchain.metadata.registries.parser_registry import ParserRegistry


@ParserRegistry.register
class OpenseaParser(SchemaParser):
    """Parser class for the OpenSea metadata standard.

    https://docs.opensea.io/docs/metadata-standards
    """

    _METADATA_STANDARD: MetadataStandard = MetadataStandard.OPENSEA_STANDARD

    def parse_attribute(self, attribute_dict: dict) -> Attribute:  # type: ignore[type-arg]  # noqa: E501
        return Attribute(
            trait_type=attribute_dict.get("trait_type"),
            value=attribute_dict.get("value"),
            display_type=attribute_dict.get("display_type"),
        )

    def parse_additional_fields(self, raw_data: dict) -> list[MetadataField]:  # type: ignore[type-arg]  # noqa: E501
        additional_fields = []
        if (external_url := raw_data.get("external_url")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="external_url",
                    type=MetadataFieldType.TEXT,
                    description="This is the URL that will appear below the asset's image on OpenSea "  # noqa: E501
                    "and will allow users to leave OpenSea and view the item on your site.",  # noqa: E501
                    value=external_url,
                )
            )
        if (background_color := raw_data.get("background_color")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="background_color",
                    type=MetadataFieldType.TEXT,
                    description="Background color of the item on OpenSea. Must be a six-character "  # noqa: E501
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

    def parse_metadata(self, token: Token, raw_data: dict, *args, **kwargs) -> Optional[Metadata]:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        """Given a token and raw data returned from the token uri, return a normalized Metadata object.

        Args:
            token (Token): token to process metadata for.
            raw_data (dict): raw data returned from token uri.

        Returns:
            Optional[Metadata]: normalized metadata object, if successfully parsed.
        """  # noqa: E501
        mime, _ = self.fetcher.fetch_mime_type_and_size(token.uri)  # type: ignore[arg-type]  # noqa: E501

        attributes = [
            self.parse_attribute(attribute)
            for attribute in raw_data.get("attributes", [])
        ]  # noqa: E501
        image = None
        image_uri = raw_data.get("image") or raw_data.get("image_data")
        if image_uri:
            image_mime, image_size = self.fetcher.fetch_mime_type_and_size(image_uri)
            image = MediaDetails(size=image_size, uri=image_uri, mime_type=image_mime)

        content = None
        content_uri = raw_data.get("animation_url")
        if content_uri:
            content_mime, content_size = self.fetcher.fetch_mime_type_and_size(
                content_uri
            )  # noqa: E501
            content = MediaDetails(
                uri=content_uri, size=content_size, mime_type=content_mime
            )  # noqa: E501

        if image and image.mime_type:
            mime = image.mime_type

        if content and content.mime_type:
            mime = content.mime_type

        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=attributes,
            name=raw_data.get("name"),
            description=raw_data.get("description"),
            mime_type=mime,
            image=image,
            content=content,
            additional_fields=self.parse_additional_fields(raw_data),
        )

    async def _gen_parse_metadata_impl(self, token: Token, raw_data: dict, *args, **kwargs) -> Optional[Metadata]:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        """Given a token and raw data returned from the token uri, return a normalized Metadata object.

        Args:
            token (Token): token to process metadata for.
            raw_data (dict): raw data returned from token uri.

        Returns:
            Optional[Metadata]: normalized metadata object, if successfully parsed.
        """  # noqa: E501
        mime, _ = await self.fetcher.gen_fetch_mime_type_and_size(token.uri)  # type: ignore[arg-type]  # noqa: E501

        attributes = [
            self.parse_attribute(attribute)
            for attribute in raw_data.get("attributes", [])
        ]  # noqa: E501
        image = None
        image_uri = raw_data.get("image") or raw_data.get("image_data")
        if image_uri:
            image_mime, image_size = await self.fetcher.gen_fetch_mime_type_and_size(
                image_uri
            )
            image = MediaDetails(size=image_size, uri=image_uri, mime_type=image_mime)

        content = None
        content_uri = raw_data.get("animation_url")
        if content_uri:
            (
                content_mime,
                content_size,
            ) = await self.fetcher.gen_fetch_mime_type_and_size(
                content_uri
            )  # noqa: E501
            content = MediaDetails(
                uri=content_uri, size=content_size, mime_type=content_mime
            )  # noqa: E501

        if image and image.mime_type:
            mime = image.mime_type

        if content and content.mime_type:
            mime = content.mime_type

        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=attributes,
            name=raw_data.get("name"),
            description=raw_data.get("description"),
            mime_type=mime,
            image=image,
            content=content,
            additional_fields=self.parse_additional_fields(raw_data),
        )

    def should_parse_token(self, token: Token, raw_data: Optional[dict], *args, **kwargs) -> bool:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        """Return whether or not a collection parser should parse a given token.

        Args:
            token (Token): the token whose metadata needs to be parsed.
            raw_data (dict): raw data returned from token uri.

        Returns:
            bool: whether or not the collection parser handles this token.
        """
        return (
            raw_data is not None
            and isinstance(raw_data, dict)
            and (
                raw_data.get("background_color") is not None
                or raw_data.get("youtube_url") is not None
            )  # noqa: E501
        )
