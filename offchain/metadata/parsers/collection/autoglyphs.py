from typing import Optional

from offchain.constants.addresses import CollectionAddress
from offchain.metadata.constants.autoglyphs import get_symbol_by_index
from offchain.metadata.models.metadata import (
    Metadata,
    Attribute,
    MetadataField,
    MetadataFieldType,
    MediaDetails,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry

ADDRESS = CollectionAddress.AUTOGLYPHS


@ParserRegistry.register
class AutoglyphsParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [ADDRESS]

    @staticmethod
    def create_raw_data(token_id: int) -> dict:
        return {
            "title": f"Autoglyph #{token_id}",
            "name": f"Autoglyph #{token_id}",
            "image": f"https://www.larvalabs.com/autoglyphs/glyphimage?index={token_id}",
            "description": 'Autoglyphs are the first "on-chain" generative art on the Ethereum blockchain. A '
            "completely self-contained mechanism for the creation and ownership of an artwork.",
            "external_url": f"https://www.larvalabs.com/autoglyphs/glyph?index={token_id}",
        }

    @staticmethod
    def encode_uri_data(uri: str) -> str:
        start = uri.index(",") + 1
        return uri[start:]

    def get_symbol_scheme(self, index: int) -> Optional[int]:
        results = self.contract_caller.single_address_single_fn_many_args(
            address=ADDRESS,
            function_sig="symbolScheme(uint256)",
            return_type=["uint8"],
            args=[[index]],
        )

        if len(results) < 1:
            return None

        return results[0]

    def get_raw_content(self, index: int) -> Optional[str]:
        results = self.contract_caller.single_address_single_fn_many_args(
            address=ADDRESS,
            function_sig="draw(uint256)",
            return_type=["string"],
            args=[[index]],
        )

        if len(results) < 1:
            return None

        return results[0]

    def get_image_details(self, raw_data: dict) -> Optional[MediaDetails]:
        image_uri = raw_data.get("image")
        details = MediaDetails(uri=image_uri, size=None, sha256=None, mime_type=None)
        try:
            content_type, size = self.fetcher.fetch_mime_type_and_size(image_uri)
            details.mime_type = content_type
            details.size = size
        except Exception:
            pass
        return details

    def get_content_details(self, index: int) -> Optional[MediaDetails]:
        raw_uri = self.get_raw_content(index)
        content_uri = self.encode_uri_data(raw_uri)
        return MediaDetails(uri=content_uri, size=None, sha256=None, mime_type="text/plain")

    def parse_additional_fields(self, raw_data: dict) -> list[MetadataField]:
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
        if (title := raw_data.get("title")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="title",
                    type=MetadataFieldType.TEXT,
                    description="This property defines an the title for the NFT asset",
                    value=title,
                )
            )
        return additional_fields

    def parse_attributes(self, token_id: int) -> list[Attribute]:
        attributes = []

        scheme = get_symbol_by_index(self.get_symbol_scheme(token_id))
        if scheme is None:
            scheme = "Unknown"

        scheme_attribute = Attribute(
            trait_type="Symbol Scheme",
            value=scheme,
            display_type=None,
        )
        attributes.append(scheme_attribute)

        return attributes

    def parse_metadata(self, token: Token, raw_data: dict, *args, **kwargs) -> Metadata:
        raw_data = self.create_raw_data(token.token_id)

        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=self.parse_attributes(token.token_id),
            name=raw_data.get("name"),
            description=raw_data.get("description"),
            mime_type="application/json",
            image=self.get_image_details(raw_data),
            content=self.get_content_details(token.token_id),
            additional_fields=self.parse_additional_fields(raw_data),
        )
