import asyncio
from typing import Optional

from offchain.constants.addresses import CollectionAddress
from offchain.logger.logging import logger
from offchain.metadata.models.metadata import (
    Attribute,
    MediaDetails,
    Metadata,
    MetadataField,
    MetadataFieldType,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry


@ParserRegistry.register
class ArtblocksParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [CollectionAddress.ARTBLOCKS]

    def get_additional_fields(self, raw_data: dict) -> list[MetadataField]:  # type: ignore[type-arg]  # noqa: E501
        additional_fields = []
        if (platform := raw_data.get("platform")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="platform",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the platform for the NFT asset",
                    value=platform,
                )
            )

        if (tokenID := raw_data.get("tokenID")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="tokenID",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the token ID for the NFT asset",
                    value=tokenID,
                )
            )

        if (series := raw_data.get("series")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="series",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the series for the NFT asset",
                    value=series,
                )
            )

        if (aspect_ratio := raw_data.get("aspect_ratio")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="aspect_ratio",
                    type=MetadataFieldType.NUMBER,
                    description="This property defines the aspect ratio for the NFT asset",  # noqa: E501
                    value=aspect_ratio,
                )
            )

        if (payout_address := raw_data.get("payout_address")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="payout_address",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the payout address for the NFT asset",  # noqa: E501
                    value=payout_address,
                )
            )

        if (minted := raw_data.get("minted")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="minted",
                    type=MetadataFieldType.BOOLEAN,
                    description="This property defines the minted state for the NFT asset",  # noqa: E501
                    value=minted,
                )
            )

        if (artist := raw_data.get("artist")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="artist",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the artist for the NFT asset",
                    value=artist,
                )
            )

        if (script_type := raw_data.get("script_type")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="script_type",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the script type for the NFT asset",  # noqa: E501
                    value=script_type,
                )
            )

        if (project_id := raw_data.get("project_id")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="project_id",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the project ID for the NFT asset",  # noqa: E501
                    value=project_id,
                )
            )

        if (curation_status := raw_data.get("curation_status")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="curation_status",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the curation status for the NFT asset",  # noqa: E501
                    value=curation_status,
                )
            )

        if (generator_url := raw_data.get("generator_url")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="generator_url",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the generator URL for the NFT asset",  # noqa: E501
                    value=generator_url,
                )
            )

        if (animation_url := raw_data.get("animation_url")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="animation_url",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the animation URL for the NFT asset",  # noqa: E501
                    value=animation_url,
                )
            )

        if (royaltyInfo := raw_data.get("royaltyInfo")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="royaltyInfo",
                    type=MetadataFieldType.OBJECT,
                    description="This property defines the royalty information for the NFT asset",  # noqa: E501
                    value=royaltyInfo,
                )
            )

        if (collection_name := raw_data.get("collection_name")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="collection_name",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the collection name for the NFT asset",  # noqa: E501
                    value=collection_name,
                )
            )

        if (website := raw_data.get("website")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="website",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the website for the NFT asset",
                    value=website,
                )
            )

        if (token_hash := raw_data.get("token_hash")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="token_hash",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the token hash for the NFT asset",  # noqa: E501
                    value=token_hash,
                )
            )

        if (external_url := raw_data.get("external_url")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="external_url",
                    type=MetadataFieldType.TEXT,
                    description="This property defines an optional external URL that can reference a webpage or "  # noqa: E501
                    "external asset for the NFT",
                    value=external_url,
                )
            )

        if (features := raw_data.get("features")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="features",
                    type=MetadataFieldType.OBJECT,
                    description="This property defines the features for the NFT asset",
                    value=features,
                )
            )

        if (is_static := raw_data.get("is_static")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="is_static",
                    type=MetadataFieldType.BOOLEAN,
                    description="This property defines the static state for the NFT asset",  # noqa: E501
                    value=is_static,
                )
            )

        if (license := raw_data.get("license")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="license",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the license for the NFT asset",
                    value=license,
                )
            )

        return additional_fields

    def parse_traits(self, raw_data: dict) -> Optional[list[Attribute]]:  # type: ignore[type-arg]  # noqa: E501
        traits = raw_data.get("traits")
        if not traits or not isinstance(traits, list):
            return  # type: ignore[return-value]

        return [
            Attribute(
                trait_type=trait_dict.get("trait_type"),
                value=trait_dict.get("value"),
                display_type=None,
            )
            for trait_dict in traits
        ]

    def get_image(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[return, type-arg]  # noqa: E501
        image_uri = raw_data.get("image")
        if image_uri:
            image = MediaDetails(uri=image_uri, size=None, sha256=None, mime_type=None)
            try:
                content_type, size = self.fetcher.fetch_mime_type_and_size(image_uri)
                image.mime_type = content_type
                image.size = size
                return image
            except Exception:
                pass

    async def gen_image(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[return, type-arg]  # noqa: E501
        image_uri = raw_data.get("image")
        if image_uri:
            image = MediaDetails(uri=image_uri, size=None, sha256=None, mime_type=None)
            try:
                content_type, size = await self.fetcher.gen_fetch_mime_type_and_size(
                    image_uri
                )
                image.mime_type = content_type
                image.size = size
                return image
            except Exception as e:
                logger.error(
                    f"{self.__class__.__name__} fail to fetch image {image_uri=}. {str(e)}"
                )

    async def _gen_parse_metadata_impl(
        self, token: Token, raw_data: dict, *args, **kwargs
    ):
        token.uri = f"https://api.artblocks.io/token/{token.token_id}"
        raw_data, mime_type_and_size = await asyncio.gather(
            self.fetcher.gen_fetch_content(token.uri),
            self.fetcher.gen_fetch_mime_type_and_size(token.uri),
        )
        mime_type, _ = mime_type_and_size
        image = await self.gen_image(raw_data=raw_data)
        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=self.parse_traits(raw_data),
            name=raw_data.get("name"),
            description=raw_data.get("description"),
            mime_type=mime_type,
            image=image,
            additional_fields=self.get_additional_fields(raw_data=raw_data),
        )

    def parse_metadata(self, token: Token, raw_data: dict, *args, **kwargs) -> Optional[Metadata]:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        token.uri = f"https://api.artblocks.io/token/{token.token_id}"

        raw_data = self.fetcher.fetch_content(token.uri)  # type: ignore[assignment]
        mime_type, _ = self.fetcher.fetch_mime_type_and_size(token.uri)

        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=self.parse_traits(raw_data),
            name=raw_data.get("name"),
            description=raw_data.get("description"),
            mime_type=mime_type,
            image=self.get_image(raw_data=raw_data),
            additional_fields=self.get_additional_fields(raw_data=raw_data),
        )
