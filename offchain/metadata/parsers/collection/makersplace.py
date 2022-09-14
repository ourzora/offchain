from typing import Optional

from offchain.constants.addresses import CollectionAddress
from offchain.metadata.adapters.ipfs import build_request_url
from offchain.metadata.models.metadata import Metadata, MediaDetails
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.parsers.catchall.default_catchall import DefaultCatchallParser
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

    def get_content_details(self, raw_data: dict) -> Optional[MediaDetails]:
        properties = raw_data.get("properties", None)
        if properties is None:
            return None

        if "preview_media_file2" not in properties and "preview_media_file2_type" not in properties:
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

    def parse_metadata(self, token: Token, raw_data: Optional[dict], *args, **kwargs) -> Optional[Metadata]:
        if token.uri is None or raw_data is None:
            token.uri = build_request_url(
                gateway="https://ipfsgateway.makersplace.com/ipfs",
                request_url=self.get_uri(token.token_id),
            )
            raw_data = self.fetcher.fetch_content(token.uri)

        metadata = DefaultCatchallParser(self.fetcher).parse_metadata(token=token, raw_data=raw_data)
        metadata.content = self.get_content_details(raw_data)
        metadata.mime_type = "application/json"
        metadata.standard = None

        return metadata
