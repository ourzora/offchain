import asyncio
from typing import Optional

from offchain.logger.logging import logger
from offchain.metadata.models.metadata import Attribute, MediaDetails, Metadata
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.catchall.catchall_parser import CatchallParser
from offchain.metadata.registries.parser_registry import ParserRegistry


@ParserRegistry.register
class DefaultCatchallParser(CatchallParser):
    """A catch-all metadata parser that does a best effort pass at parsing metadata of any format.
    This parser should always be run last in the pipeline.
    """  # noqa: E501

    def get_name(self, raw_data: dict):  # type: ignore[no-untyped-def, type-arg]
        if isinstance(raw_data.get("name"), str):
            return raw_data.get("name")
        return None

    def get_description(self, raw_data: dict):  # type: ignore[no-untyped-def, type-arg]
        if isinstance(raw_data.get("description"), str):
            return raw_data.get("description")
        return None

    def get_attributes(self, raw_data: dict) -> list[Attribute]:  # type: ignore[type-arg]  # noqa: E501
        attributes: list[Attribute] = []

        if isinstance(raw_data.get("properties"), dict):
            for key, value in raw_data["properties"].items():
                if isinstance(value, str):
                    attributes.append(
                        Attribute(trait_type=key, value=value, display_type=None)
                    )
                elif isinstance(value, dict):
                    attributes.append(
                        Attribute(
                            trait_type=key,
                            value=value.get("description"),
                            display_type=value.get("type"),
                        )
                    )

        if isinstance(raw_data.get("attributes"), list):
            attributes += [
                Attribute(
                    trait_type=attribute.get("trait_type"),
                    value=attribute.get("value"),
                    display_type=attribute.get("display_type"),
                )
                for attribute in raw_data["attributes"]
            ]

        if isinstance(raw_data.get("traits"), list):
            attributes += [
                Attribute(
                    trait_type=attribute.get("trait_type"),
                    value=attribute.get("value"),
                    display_type=attribute.get("display_type"),
                )
                for attribute in raw_data["traits"]
            ]

        return attributes

    def get_image_uri(self, raw_data: dict):  # type: ignore[no-untyped-def, type-arg]
        if isinstance(raw_data.get("image"), str):
            return raw_data["image"]
        if isinstance(raw_data.get("image_url"), str):
            return raw_data["image_url"]
        if isinstance(raw_data.get("imageUrl"), str):
            return raw_data["imageUrl"]
        return None

    def get_image_details(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[type-arg]  # noqa: E501
        image_uri = self.get_image_uri(raw_data=raw_data)
        if not image_uri:
            return None
        details = MediaDetails(uri=image_uri, size=None, sha256=None, mime_type=None)
        try:
            content_type, size = self.fetcher.fetch_mime_type_and_size(image_uri)
            details.size = size
            details.mime_type = content_type
        except Exception:
            pass

        if isinstance(raw_data.get("image_details"), dict):
            details.size = raw_data["image_details"].get("size")
            details.sha256 = raw_data["image_details"].get("sha256")
        return details

    async def gen_image_details(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[type-arg]  # noqa: E501
        image_uri = self.get_image_uri(raw_data=raw_data)
        if not image_uri:
            return None
        details = MediaDetails(uri=image_uri, size=None, sha256=None, mime_type=None)
        try:
            content_type, size = await self.fetcher.gen_fetch_mime_type_and_size(
                image_uri
            )
            details.size = size
            details.mime_type = content_type
        except Exception as e:
            logger.error(
                f"{self.__class__.__name__} fail to fetch image {image_uri=}. {str(e)}"
            )

        if isinstance(raw_data.get("image_details"), dict):
            details.size = raw_data["image_details"].get("size")
            details.sha256 = raw_data["image_details"].get("sha256")
        return details

    def get_content_uri(self, raw_data: dict):  # type: ignore[no-untyped-def, type-arg]
        if isinstance(raw_data.get("animation_url"), str):
            return raw_data["animation_url"]
        if isinstance(raw_data.get("animation"), str):
            return raw_data["animation"]
        return None

    def get_content_details(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[type-arg]  # noqa: E501
        content_uri = self.get_content_uri(raw_data)
        if not content_uri:
            return None
        details = MediaDetails(uri=content_uri, size=None, sha256=None, mime_type=None)
        try:
            content_type, size = self.fetcher.fetch_mime_type_and_size(content_uri)
            details.size = size
            details.mime_type = content_type
        except Exception:
            pass
        if isinstance(raw_data.get("animation_details"), dict):
            details.size = raw_data["animation_details"].get("size")
            details.sha256 = raw_data["animation_details"].get("sha256")
        return details

    async def gen_content_details(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[type-arg]  # noqa: E501
        content_uri = self.get_content_uri(raw_data)
        if not content_uri:
            return None
        details = MediaDetails(uri=content_uri, size=None, sha256=None, mime_type=None)
        try:
            content_type, size = await self.fetcher.gen_fetch_mime_type_and_size(
                content_uri
            )
            details.size = size
            details.mime_type = content_type
        except Exception as e:
            logger.error(
                f"{self.__class__.__name__} fail to fetch mime_type_and_size "
                f"{content_uri=}. {str(e)}"
            )
        if isinstance(raw_data.get("animation_details"), dict):
            details.size = raw_data["animation_details"].get("size")
            details.sha256 = raw_data["animation_details"].get("sha256")
        return details

    def parse_metadata(  # type: ignore[no-untyped-def]
        self, token: Token, raw_data: dict, *args, **kwargs  # type: ignore[type-arg]
    ) -> Optional[Metadata]:
        """Given a token and raw data returned from the token uri, return a normalized Metadata object.

        Args:
            token (Token): token to process metadata for.
            raw_data (dict): raw data returned from token uri.

        Returns:
            Optional[Metadata]: normalized metadata object, if successfully parsed.
        """  # noqa: E501
        mime, _ = self.fetcher.fetch_mime_type_and_size(
            token.uri  # type:ignore [arg-type]
        )

        content = self.get_content_details(raw_data=raw_data)
        image = self.get_image_details(raw_data=raw_data)

        if image and image.mime_type:
            mime = image.mime_type

        if content and content.mime_type:
            mime = content.mime_type

        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=self.get_attributes(raw_data=raw_data),
            name=self.get_name(raw_data=raw_data),
            description=self.get_description(raw_data=raw_data),
            mime_type=mime,
            image=image,
            content=content,
            additional_fields=[],
        )

    async def _gen_parse_metadata_impl(  # type: ignore[no-untyped-def]
        self, token: Token, raw_data: dict, *args, **kwargs  # type: ignore[type-arg]
    ) -> Optional[Metadata]:
        """Given a token and raw data returned from the token uri, return a normalized Metadata object.

        Args:
            token (Token): token to process metadata for.
            raw_data (dict): raw data returned from token uri.

        Returns:
            Optional[Metadata]: normalized metadata object, if successfully parsed.
        """  # noqa: E501
        mime_type_and_size, content, image = await asyncio.gather(
            self.fetcher.gen_fetch_mime_type_and_size(
                token.uri  # type:ignore [arg-type]
            ),
            self.gen_content_details(raw_data=raw_data),
            self.gen_image_details(raw_data=raw_data),
        )
        mime, _ = mime_type_and_size
        if image and image.mime_type:
            mime = image.mime_type

        if content and content.mime_type:
            mime = content.mime_type

        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=self.get_attributes(raw_data=raw_data),
            name=self.get_name(raw_data=raw_data),
            description=self.get_description(raw_data=raw_data),
            mime_type=mime,
            image=image,
            content=content,
            additional_fields=[],
        )

    def should_parse_token(  # type: ignore[no-untyped-def]
        self, token: Token, raw_data: Optional[dict], *args, **kwargs  # type: ignore[type-arg]  # noqa: E501
    ) -> bool:
        """Return whether or not a collection parser should parse a given token.

        Args:
            token (Token): the token whose metadata needs to be parsed.
            raw_data (dict): raw data returned from token uri.

        Returns:
            bool: whether or not the collection parser handles this token.
        """
        return bool(token.uri and raw_data)
