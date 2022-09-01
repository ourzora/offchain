from typing import Optional
from urllib.parse import quote

from offchain.constants.addresses import CollectionAddress
from offchain.metadata.models.metadata import (
    Attribute,
    MediaDetails,
    Metadata,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry

ADDRESS = CollectionAddress.LOOT


@ParserRegistry.register
class LootParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [ADDRESS]

    @staticmethod
    def normalize_name(name: str) -> str:
        # converts getChest(uint256) -> Chest
        return name.replace("get", "").replace("(uint256)", "")

    def get_attributes(self, token_id: int) -> Optional[dict[str, str]]:
        sigs = [
            "getChest(uint256)",
            "getFoot(uint256)",
            "getHand(uint256)",
            "getHead(uint256)",
            "getNeck(uint256)",
            "getRing(uint256)",
            "getWaist(uint256)",
            "getWeapon(uint256)",
        ]

        results = self.contract_caller.single_address_many_fns_many_args(
            address=ADDRESS,
            function_sigs=sigs,
            return_types=[["string"] for _ in sigs],
            args=[[token_id] for _ in sigs],
        )

        return results

    def parse_attributes(self, attributes: dict) -> Optional[list[Attribute]]:
        return [
            Attribute(
                trait_type=self.normalize_name(item),
                value=value,
                display_type=None,
            )
            for item, value in attributes.items()
        ]

    def get_uri(self, token_id: int) -> Optional[str]:
        results = self.contract_caller.single_address_single_fn_many_args(
            ADDRESS,
            function_sig="tokenURI(uint256)",
            return_type=["string"],
            args=[[token_id]],
        )

        if len(results) < 1:
            return None

        return results[0]

    def get_image(self, raw_data: dict) -> Optional[MediaDetails]:
        raw_image_uri = raw_data.get("image")
        image_uri = quote(self.fetcher.fetch_content(raw_image_uri))

        return MediaDetails(uri=image_uri, size=None, sha256=None, mime_type="image/svg+xml")

    def parse_metadata(self, token: Token, raw_data: dict, *args, **kwargs) -> Metadata:
        token.uri = self.get_uri(token.token_id)

        raw_data = self.fetcher.fetch_content(token.uri)
        mime_type, _ = self.fetcher.fetch_mime_type_and_size(token.uri)

        attributes = self.get_attributes(token.token_id)

        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=self.parse_attributes(attributes),
            name=raw_data.get("name"),
            description=raw_data.get("description"),
            mime_type=mime_type,
            image=self.get_image(raw_data=raw_data),
        )
