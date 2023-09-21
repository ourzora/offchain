from typing import Optional

from offchain.constants.addresses import CollectionAddress
from offchain.logger.logging import logger
from offchain.metadata.adapters.ipfs import build_request_url
from offchain.metadata.models.metadata import MediaDetails, Metadata
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.catchall.default_catchall import DefaultCatchallParser
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry

ADDRESS = CollectionAddress.MAKERSPLACE


@ParserRegistry.register
class MakersPlaceParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [ADDRESS]

    def get_uri(self, index: int) -> Optional[str]:
        results = self.contract_caller.single_address_single_fn_many_args(
            address=ADDRESS,
            function_sig="tokenURI(uint256)",
            return_type=["string"],
            args=[[index]],
        )

        if len(results) < 1:
            return None

        return results[0]

    async def gen_uri(self, index: int) -> Optional[str]:
        results = await self.contract_caller.rpc.async_reader.gen_call_single_function_single_address_many_args(
            address=ADDRESS,
            function_sig="tokenURI(uint256)",
            return_type=["string"],
            args=[[index]],
        )

        if len(results) < 1:
            return None

        return results[0]

    def get_content_details(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[type-arg]  # noqa: E501
        properties = raw_data.get("properties", None)
        if properties is None:
            return None

        if (
            "preview_media_file2" not in properties
            and "preview_media_file2_type" not in properties
        ):  # noqa: E501
            return None

        if properties.get("preview_media_file2_type").get("description") != "mp4":
            return None

        url = properties.get("preview_media_file2").get("description")
        details = MediaDetails(uri=url, size=None, sha256=None, mime_type=None)
        try:
            content_type, size = self.fetcher.fetch_mime_type_and_size(url)
            details.mime_type = content_type
            details.size = size
        except Exception:
            pass

        return details

    async def gen_content_details(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[type-arg]  # noqa: E501
        properties = raw_data.get("properties", None)
        if properties is None:
            return None

        if (
            "preview_media_file2" not in properties
            and "preview_media_file2_type" not in properties
        ):  # noqa: E501
            return None

        if properties.get("preview_media_file2_type").get("description") != "mp4":
            return None

        url = properties.get("preview_media_file2").get("description")
        details = MediaDetails(uri=url, size=None, sha256=None, mime_type=None)
        try:
            content_type, size = await self.fetcher.gen_fetch_mime_type_and_size(url)
            details.mime_type = content_type
            details.size = size
        except Exception as e:
            logger.error(
                f"{self.__class__.__name__} fail to fetch content detail {url=}. {str(e)}"
            )

        return details

    def parse_metadata(self, token: Token, raw_data: Optional[dict], *args, **kwargs) -> Optional[Metadata]:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        if token.uri is None or raw_data is None:
            token.uri = build_request_url(
                gateway="https://ipfsgateway.makersplace.com/ipfs",
                request_url=self.get_uri(token.token_id),  # type: ignore[arg-type]
            )
            raw_data = self.fetcher.fetch_content(token.uri)  # type: ignore[assignment]

        metadata = DefaultCatchallParser(self.fetcher).parse_metadata(token=token, raw_data=raw_data)  # type: ignore[arg-type]  # noqa: E501
        metadata.content = self.get_content_details(raw_data)  # type: ignore[arg-type, union-attr]  # noqa: E501
        metadata.mime_type = "application/json"  # type: ignore[union-attr]
        metadata.standard = None  # type: ignore[union-attr]

        return metadata

    async def _gen_parse_metadata_impl(self, token: Token, raw_data: Optional[dict], *args, **kwargs) -> Optional[Metadata]:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        if token.uri is None or raw_data is None:
            token.uri = build_request_url(
                gateway="https://ipfsgateway.makersplace.com/ipfs",
                request_url=await self.gen_uri(token.token_id),  # type: ignore[arg-type]
            )
            raw_data = await self.fetcher.gen_fetch_content(token.uri)  # type: ignore[assignment]

        metadata = await DefaultCatchallParser(self.fetcher).gen_parse_metadata(token=token, raw_data=raw_data)  # type: ignore[arg-type]  # noqa: E501
        metadata.content = await self.gen_content_details(raw_data)  # type: ignore[arg-type, union-attr]  # noqa: E501
        metadata.mime_type = "application/json"  # type: ignore[union-attr]
        metadata.standard = None  # type: ignore[union-attr]

        return metadata
