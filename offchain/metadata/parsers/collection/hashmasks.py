from typing import Optional

from offchain.constants.addresses import CollectionAddress
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

ADDRESS = CollectionAddress.HASHMASKS


@ParserRegistry.register
class HashmasksParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [ADDRESS]

    def get_name(self, token_id: int) -> Optional[str]:
        results = self.contract_caller.single_address_single_fn_many_args(
            address=ADDRESS,
            function_sig="tokenNameByIndex(uint256)",
            return_type=["string"],
            args=[[token_id]],
        )

        if len(results) < 1:
            return None

        return results[0]

    def get_additional_fields(self, raw_data: dict) -> list[MetadataField]:
        additional_fields = []
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

    def parse_attributes(self, raw_data: dict) -> Optional[list[Attribute]]:
        attributes = raw_data.get("attributes")
        if not attributes or not isinstance(attributes, list):
            return

        return [
            Attribute(
                trait_type=attribute_dict.get("trait_type"),
                value=attribute_dict.get("value"),
                display_type=None,
            )
            for attribute_dict in attributes
        ]

    def get_image(self, raw_data: dict) -> Optional[MediaDetails]:
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

    def parse_metadata(self, token: Token, raw_data: dict, *args, **kwargs) -> Optional[Metadata]:
        token.uri = f"https://hashmap.azurewebsites.net/getMask/{token.token_id}"

        raw_data = self.fetcher.fetch_content(token.uri)
        mime_type, _ = self.fetcher.fetch_mime_type_and_size(token.uri)

        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=self.parse_attributes(raw_data) or [],
            name=self.get_name(token.token_id),
            description=raw_data.get("description"),
            mime_type=mime_type,
            image=self.get_image(raw_data=raw_data),
            additional_fields=self.get_additional_fields(raw_data=raw_data),
        )
