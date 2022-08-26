from typing import Optional

from offchain.constants.addresses import CollectionAddress
from offchain.metadata.constants.nouns import Seeds
from offchain.metadata.models.metadata import Metadata, MediaDetails, Attribute
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry


@ParserRegistry.register
class NounsParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [
        CollectionAddress.NOUNS,
        CollectionAddress.LIL_NOUNS,
    ]

    def seeds(self, token_id: int) -> Optional[Seeds]:
        results = self.caller.single_address_single_fn_many_args(
            self.contract_address,
            function_sig="seeds(uint256)",
            return_type=["uint48", "uint48", "uint48", "uint48", "uint48"],
            args=[[token_id]],
        )

        if len(results) < 1:
            return None

        result = results[0]

        seeds = Seeds.from_raw(
            background_index=result[0],
            body_index=result[1],
            accessory_index=result[2],
            head_index=result[3],
            glasses_index=result[4],
        )

        return seeds

    def get_seed_attributes(self, token_id: int) -> list[Attribute]:
        attributes = []

        def normalize_value(value: str) -> str:
            return value.replace("-", " ")

        seeds = self.seeds(token_id)
        for trait, value in seeds.__dict__.values():
            attribute = Attribute(
                trait_type=trait,
                value=normalize_value(value),
                display_type=None,
            )
            attributes.append(attribute)

        return attributes

    def parse_metadata(self, token: Token, raw_data: dict, *args, **kwargs) -> Metadata:
        mime, _ = self.fetcher.fetch_mime_type_and_size(token.uri)

        image = None
        image_uri = raw_data.get("image") or raw_data.get("image_data")
        if image_uri:
            image_mime, image_size = self.fetcher.fetch_mime_type_and_size(image_uri)
            image = MediaDetails(size=image_size, uri=image_uri, mime_type=image_mime)

        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=self.parse_attributes(token.token_id),
            name=raw_data.get("name"),
            description=raw_data.get("description"),
            mime_type=mime,
            image=image,
        )
