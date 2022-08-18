from dataclasses import dataclass
from typing import Callable, Optional, Union

from offchain.adapters import ARWeaveAdapter, DataURIAdapter, HTTPAdapter, IPFSAdapter
from offchain.adapters.base_adapter import Adapter
from offchain.concurrency import batched_parmap
from offchain.fetchers.base_fetcher import BaseFetcher
from offchain.fetchers.metadata_fetcher import MetadataFetcher
from offchain.models.metadata import Metadata
from offchain.models.metadata_processing_error import MetadataProcessingError
from offchain.models.token import Token
from offchain.parsers import OpenseaParser
from offchain.parsers.base_parser import BaseParser
from offchain.pipelines.base_pipeline import BasePipeline


@dataclass
class AdapterConfig:
    adapter: Adapter
    mount_prefixes: list[str]


DEFAULT_ADAPTER_CONFIGS: list[AdapterConfig] = [
    AdapterConfig(
        adapter=ARWeaveAdapter(pool_connections=100, pool_maxsize=1000, max_retries=0),
        mount_prefixes=["ar://"],
    ),
    AdapterConfig(adapter=DataURIAdapter(), mount_prefixes=["data:"]),
    AdapterConfig(
        adapter=HTTPAdapter(pool_connections=100, pool_maxsize=1000, max_retries=0),
        mount_prefixes=["https://", "http://"],
    ),
    AdapterConfig(
        adapter=IPFSAdapter(pool_connections=100, pool_maxsize=1000, max_retries=0),
        mount_prefixes=[
            "ipfs://",
            "https://gateway.pinata.cloud/",
            "https://ipfs.io/",
        ],
    ),
]

DEFAULT_PARSER_CLASSES = [OpenseaParser]


class MetadataPipeline(BasePipeline):
    def __init__(
        self,
        fetcher: Optional[BaseFetcher] = None,
        parsers: Optional[list[BaseParser]] = None,
        adapter_configs: Optional[list[AdapterConfig]] = None,
    ) -> None:
        self.fetcher = fetcher or MetadataFetcher()
        if adapter_configs is None:
            adapter_configs = DEFAULT_ADAPTER_CONFIGS
        for adapter_config in adapter_configs:
            self.mount_adapter(
                adapter=adapter_config.adapter,
                url_prefixes=adapter_config.mount_prefixes,
            )
        if parsers is None:
            parsers = [parser_cls(fetcher=self.fetcher) for parser_cls in DEFAULT_PARSER_CLASSES]
        self.parsers = parsers

    def mount_adapter(
        self,
        adapter: Adapter,
        url_prefixes: list[str],
    ):
        for prefix in url_prefixes:
            self.fetcher.register_adapter(adapter, prefix)

    def fetch_token_metadata(
        self,
        token: Token,
        metadata_selector_fn: Optional[Callable] = None,
    ) -> Union[Metadata, MetadataProcessingError]:
        raw_data = self.fetcher.fetch_content(token.uri)
        possible_metadatas = []
        for parser in self.parsers:
            if parser.should_parse_token(token=token, raw_data=raw_data):
                try:
                    metadata_or_error = parser.parse_metadata(token=token, raw_data=raw_data)
                    if metadata_selector_fn is None:
                        return metadata_or_error
                except Exception as e:
                    metadata_or_error = MetadataProcessingError.from_token_and_error(token=token, e=e)
                possible_metadatas.append(metadata_or_error)
        if len(possible_metadatas) == 0:
            possible_metadatas.append(
                MetadataProcessingError.from_token_and_error(token=token, e=Exception("No parsers found."))
            )

        if metadata_selector_fn:
            return metadata_selector_fn(possible_metadatas)
        return possible_metadatas[0]

    def run(
        self,
        tokens: list[Token],
        parallelize: bool = True,
        select_metadata_fn: Optional[Callable] = None,
        *args,
        **kwargs,
    ) -> list[Union[Metadata, MetadataProcessingError]]:
        if len(tokens) == 0:
            return []

        if parallelize:
            metadatas_or_errors = batched_parmap(lambda t: self.fetch_token_metadata(t, select_metadata_fn), tokens, 15)
        else:
            metadatas_or_errors = list(map(lambda t: self.fetch_token_metadata(t, select_metadata_fn), tokens))

        return metadatas_or_errors
