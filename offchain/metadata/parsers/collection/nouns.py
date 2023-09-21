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
    def from_raw(  # type: ignore[no-untyped-def]
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

    def get_image(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[type-arg]  # noqa: E501
        raw_image_uri = raw_data.get("image")
        image_uri = quote(self.fetcher.fetch_content(raw_image_uri))  # type: ignore[arg-type]  # noqa: E501

        return MediaDetails(
            uri=image_uri, size=None, sha256=None, mime_type="image/svg+xml"
        )  # noqa: E501

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
            background_index=result[0],  # type: ignore[index]
            body_index=result[1],  # type: ignore[index]
            accessory_index=result[2],  # type: ignore[index]
            head_index=result[3],  # type: ignore[index]
            glasses_index=result[4],  # type: ignore[index]
        )

        return seeds  # type: ignore[no-any-return]

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

    def parse_metadata(self, token: Token, raw_data: dict, *args, **kwargs) -> Metadata:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        token.uri = self.get_uri(token)

        raw_data = self.fetcher.fetch_content(token.uri)  # type: ignore[arg-type, assignment]  # noqa: E501
        mime_type, _ = self.fetcher.fetch_mime_type_and_size(token.uri)  # type: ignore[arg-type]  # noqa: E501

        return Metadata(
            token=token,
            raw_data=raw_data,
            name=raw_data.get("name"),
            description=raw_data.get("description"),
            mime_type=mime_type,
            image=self.get_image(raw_data),
            attributes=self.get_seed_attributes(token),
        )
