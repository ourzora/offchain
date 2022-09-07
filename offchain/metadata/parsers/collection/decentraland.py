from typing import Optional

from offchain.constants.addresses import CollectionAddress
from offchain.metadata.models.metadata import Metadata, MetadataField, MetadataFieldType
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.parsers.catchall.default_catchall import DefaultCatchallParser
from offchain.metadata.registries.parser_registry import ParserRegistry


@ParserRegistry.register
class DecentralandParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [
        CollectionAddress.DECENTRALAND,
        CollectionAddress.DECENTRALAND_ESTATE,
    ]

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
        if (id := raw_data.get("id")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="id",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the ID for the NFT asset",
                    value=id,
                )
            )

        if (background_color := raw_data.get("background_color")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="background_color",
                    type=MetadataFieldType.TEXT,
                    description="This property defines the background color for the NFT asset",
                    value=background_color,
                )
            )
        return additional_fields

    def parse_metadata(self, token: Token, raw_data: Optional[dict], *args, **kwargs) -> Optional[Metadata]:
        if token.uri is None or raw_data is None:
            token.uri = (
                f"https://api.decentraland.org/v2/contracts/{token.collection_address.lower()}/tokens/{token.token_id}"
            )
            raw_data = self.fetcher.fetch_content(token.uri)

        metadata = DefaultCatchallParser(self.fetcher).parse_metadata(token=token, raw_data=raw_data)
        metadata.additional_fields = self.parse_additional_fields(raw_data)
        metadata.mime_type = "application/json"

        return metadata
