import asyncio
from typing import Optional
from urllib.parse import quote

from offchain.constants.addresses import CollectionAddress
from offchain.metadata.models.metadata import Attribute, MediaDetails, Metadata
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

        return results  # type: ignore[return-value]

    async def gen_attributes(self, token_id: int) -> Optional[dict[str, str]]:
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

        results = await asyncio.gather(
            *(
                self.contract_caller.rpc.async_reader.gen_call_single_function_single_address_many_args(
                    address=ADDRESS,
                    function_sig=sig,
                    return_type=["string"],
                    args=[[token_id]],
                )
                for sig in sigs
            )
        )
        return results  # type: ignore[return-value]

    def parse_attributes(self, attributes: dict) -> Optional[list[Attribute]]:  # type: ignore[type-arg]  # noqa: E501
        return [
            Attribute(
                trait_type=self.normalize_name(item),
                value=value,
                display_type=None,
            )
            for item, value in attributes.items()
        ]

    def parse_attributes_for_async(self, attributes: list) -> Optional[list[Attribute]]:  # type: ignore[type-arg]  # noqa: E501
        return [
            Attribute(
                trait_type="string",
                value=",".join(value),
                display_type=None,
            )
            for value in attributes
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

    async def gen_uri(self, token_id: int) -> Optional[str]:
        results = await self.contract_caller.rpc.async_reader.gen_call_single_function_single_address_many_args(
            ADDRESS,
            function_sig="tokenURI(uint256)",
            return_type=["string"],
            args=[[token_id]],
        )

        if len(results) < 1:
            return None

        return results[0]

    def get_image(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[type-arg]  # noqa: E501
        raw_image_uri = raw_data.get("image")
        image_uri = quote(self.fetcher.fetch_content(raw_image_uri))  # type: ignore[arg-type]  # noqa: E501

        return MediaDetails(
            uri=image_uri, size=None, sha256=None, mime_type="image/svg+xml"
        )  # noqa: E501

    async def gen_image(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[type-arg]  # noqa: E501
        raw_image_uri = raw_data.get("image")
        image_uri = quote(await self.fetcher.gen_fetch_content(raw_image_uri))  # type: ignore[arg-type]  # noqa: E501

        return MediaDetails(
            uri=image_uri, size=None, sha256=None, mime_type="image/svg+xml"
        )  # noqa: E501

    def parse_metadata(self, token: Token, raw_data: dict, *args, **kwargs) -> Metadata:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        token.uri = self.get_uri(token.token_id)

        raw_data = self.fetcher.fetch_content(token.uri)  # type: ignore[arg-type, assignment]  # noqa: E501
        mime_type, _ = self.fetcher.fetch_mime_type_and_size(token.uri)  # type: ignore[arg-type]  # noqa: E501

        attributes = self.get_attributes(token.token_id)

        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=self.parse_attributes(attributes),  # type: ignore[arg-type]
            name=raw_data.get("name"),
            description=raw_data.get("description"),
            mime_type=mime_type,
            image=self.get_image(raw_data=raw_data),
        )

    async def _gen_parse_metadata_impl(self, token: Token, raw_data: dict, *args, **kwargs) -> Metadata:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        token.uri = await self.gen_uri(token.token_id)
        raw_data, mime_type_and_size, attributes, image = await asyncio.gather(
            self.fetcher.gen_fetch_content(token.uri),  # type: ignore[arg-type, assignment]  # noqa: E501
            self.fetcher.gen_fetch_mime_type_and_size(token.uri),  # type: ignore[arg-type]  # noqa: E501
            self.gen_attributes(token.token_id),
            self.gen_image(raw_data=raw_data),
        )
        mime_type, _ = mime_type_and_size

        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=self.parse_attributes_for_async(attributes),  # type: ignore[arg-type]
            name=raw_data.get("name"),
            description=raw_data.get("description"),
            mime_type=mime_type,
            image=image,
        )
