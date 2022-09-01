from dataclasses import dataclass
from typing import Optional
from urllib.parse import quote

from offchain.constants.addresses import CollectionAddress
from offchain.metadata.constants.nouns import BACKGROUND, BODY, ACCESSORY, HEAD, GLASSES
from offchain.metadata.models.metadata import Metadata, MediaDetails, Attribute
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry


@dataclass
class Seeds:
    background: str
    body: str
    accessory: str
    head: str
    glasses: str

    @classmethod
    def from_raw(
        cls,
        background_index: int,
        body_index: int,
        accessory_index: int,
        head_index: int,
        glasses_index: int,
    ):
        background = BACKGROUND[background_index]
        body = BODY[body_index]
        accessory = ACCESSORY[accessory_index]
        head = HEAD[head_index]
        glasses = GLASSES[glasses_index]

        return Seeds(background, body, accessory, head, glasses)


@ParserRegistry.register
class NounsParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [
        CollectionAddress.NOUNS,
        CollectionAddress.LIL_NOUNS,
    ]

    def get_image(self, raw_data: dict) -> Optional[MediaDetails]:
        raw_image_uri = raw_data.get("image")
        image_uri = quote(self.fetcher.fetch_content(raw_image_uri))

        return MediaDetails(uri=image_uri, size=None, sha256=None, mime_type="image/svg+xml")

    def seeds(self, token: Token) -> Optional[Seeds]:
        results = self.contract_caller.single_address_single_fn_many_args(
            address=token.collection_address,
            function_sig="seeds(uint256)",
            return_type=["uint48", "uint48", "uint48", "uint48", "uint48"],
            args=[[token.token_id]],
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

    def get_uri(self, token: Token) -> Optional[str]:
        results = self.contract_caller.single_address_single_fn_many_args(
            token.collection_address,
            function_sig="tokenURI(uint256)",
            return_type=["string"],
            args=[[token.token_id]],
        )

        if len(results) < 1:
            return None

        return results[0]

    def get_seed_attributes(self, token: Token) -> list[Attribute]:
        seeds = self.seeds(token)

        def normalize_value(value: str) -> str:
            return value.replace("-", " ")

        return [
            Attribute(
                trait_type=trait,
                value=normalize_value(value),
                display_type=None,
            )
            for trait, value in seeds.__dict__.items()
        ]

    def parse_metadata(self, token: Token, raw_data: dict, *args, **kwargs) -> Metadata:
        token.uri = self.get_uri(token)

        raw_data = self.fetcher.fetch_content(token.uri)
        mime_type, _ = self.fetcher.fetch_mime_type_and_size(token.uri)

        return Metadata(
            token=token,
            raw_data=raw_data,
            name=raw_data.get("name"),
            description=raw_data.get("description"),
            mime_type=mime_type,
            image=self.get_image(raw_data),
            attributes=self.get_seed_attributes(token),
        )
