from typing import Optional

from offchain.constants.addresses import CollectionAddress
from offchain.metadata.models.metadata import (
    Metadata,
    MediaDetails,
    MetadataField,
    MetadataFieldType,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.catchall.default_catchall import DefaultCatchallParser
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry

ADDRESS = CollectionAddress.ZORA_MEDIA


@ParserRegistry.register
class ZoraParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [ADDRESS]

    def parse_additional_fields(self, raw_data: dict) -> list[MetadataField]:
        additional_fields = []
        if version := raw_data.get("version"):
            additional_fields.append(
                MetadataField(
                    field_name="version",
                    type=MetadataFieldType.TEXT,
                    description="Zora Metadata version",
                    value=version,
                )
            )

        return additional_fields

    def get_uri(self, token_id: int) -> Optional[str]:
        results = self.contract_caller.single_address_single_fn_many_args(
            ADDRESS,
            function_sig="tokenMetadataURI(uint256)",
            return_type=["string"],
            args=[[token_id]],
        )

        if len(results) < 1:
            return None

        return results[0]

    def get_content_uri(self, token_id: int) -> Optional[str]:
        results = self.contract_caller.single_address_single_fn_many_args(
            ADDRESS,
            function_sig="tokenURI(uint256)",
            return_type=["string"],
            args=[[token_id]],
        )

        if len(results) < 1:
            return None

        return results[0]

    def get_content_details(self, uri: str) -> Optional[MediaDetails]:
        try:
            content_type, size = self.fetcher.fetch_mime_type_and_size(uri)
            return MediaDetails(uri=uri, size=size, sha256=None, mime_type=content_type)
        except Exception:
            pass

        return None

    def parse_metadata(self, token: Token, raw_data: Optional[dict], *args, **kwargs) -> Optional[Metadata]:
        if token.uri is None or raw_data is None:
            token.uri = self.get_uri(token.token_id)
            raw_data = self.fetcher.fetch_content(token.uri)

        metadata = DefaultCatchallParser(self.fetcher).parse_metadata(token=token, raw_data=raw_data)

        content_uri = self.get_content_uri(token.token_id)
        content = self.get_content_details(content_uri)

        # if we have an image, make sure we set
        # the image field, otherwise fallback to content
        if content.mime_type.startswith("image"):
            metadata.image = content
        else:
            metadata.content = content

        metadata.additional_fields = self.parse_additional_fields(raw_data)
        metadata.mime_type = "application/json"

        return metadata
