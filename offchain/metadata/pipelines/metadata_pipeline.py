import asyncio
from typing import Callable, Optional, Union

from offchain.concurrency import batched_parmap
from offchain.logger.logging import logger
from offchain.metadata.adapters import (  # type: ignore[attr-defined]
    ARWeaveAdapter,
    DataURIAdapter,
    HTTPAdapter,
    IPFSAdapter,
)
from offchain.metadata.adapters.base_adapter import Adapter, AdapterConfig
from offchain.metadata.fetchers.base_fetcher import BaseFetcher
from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher
from offchain.metadata.models.metadata import Metadata
from offchain.metadata.models.metadata_processing_error import MetadataProcessingError
from offchain.metadata.models.token import Token
from offchain.metadata.parsers import (  # type: ignore[attr-defined]  # noqa: E501
    BaseParser,
    DefaultCatchallParser,
)
from offchain.metadata.pipelines.base_pipeline import BasePipeline
from offchain.metadata.registries.parser_registry import ParserRegistry
from offchain.web3.contract_caller import ContractCaller

# TODO(luke): move the data repo's usage of this symbol to the new file, then remove this
DEFAULT_ADAPTER_CONFIGS: list[AdapterConfig] = [
    AdapterConfig(
        adapter_cls=ARWeaveAdapter,
        mount_prefixes=["ar://"],
        host_prefixes=["https://arweave.net/"],
        kwargs={"pool_connections": 100, "pool_maxsize": 1000, "max_retries": 0},
    ),
    AdapterConfig(adapter_cls=DataURIAdapter, mount_prefixes=["data:"]),
    AdapterConfig(
        adapter_cls=IPFSAdapter,
        mount_prefixes=[
            "ipfs://",
            "https://gateway.pinata.cloud/",
            "https://ipfs.io/",
        ],
        host_prefixes=["https://gateway.pinata.cloud/ipfs/"],
        kwargs={"pool_connections": 100, "pool_maxsize": 1000, "max_retries": 0},
    ),
    AdapterConfig(
        adapter_cls=HTTPAdapter,
        mount_prefixes=["https://", "http://"],
        kwargs={"pool_connections": 100, "pool_maxsize": 1000, "max_retries": 0},
    ),
]

DEFAULT_PARSERS = (
    ParserRegistry.get_all_collection_parsers()
    + ParserRegistry.get_all_schema_parsers()
    + [DefaultCatchallParser]
)


class MetadataPipeline(BasePipeline):
    """Pipeline for processing NFT metadata.

    By default, the parsers are run in order and we will early return when of them returns a valid metadata object.

    Attributes:
        contract_caller (ContractCaller, optional): a contract caller instance for fetching data from contracts.
        fetcher (BaseFetcher, optional): a fetcher instance responsible for fetching content,
            mime type, and size by making network requests.
        parsers (list[BaseParser], optional): a list of parser instances for parsing token metadata.
        adapter_configs: (list[AdapterConfig], optional): a list of adapter configs used to register adapters
            to specified url prefixes. This configuration affects both sync and async requests.
    """  # noqa: E501

    def __init__(
        self,
        contract_caller: Optional[ContractCaller] = None,
        fetcher: Optional[BaseFetcher] = None,
        parsers: Optional[list[BaseParser]] = None,
        adapter_configs: Optional[list[AdapterConfig]] = None,
    ) -> None:
        self.contract_caller = contract_caller or ContractCaller()
        self.fetcher = fetcher or MetadataFetcher(async_adapter_configs=adapter_configs)
        if adapter_configs is None:
            # TODO(luke): move the line below to the file's import section once this
            #  file's DEFAULT_ADAPTER_CONFIGS is gone
            from offchain.metadata.adapters import DEFAULT_ADAPTER_CONFIGS

            adapter_configs = DEFAULT_ADAPTER_CONFIGS
        for adapter_config in adapter_configs:
            self.mount_adapter(
                adapter=adapter_config.adapter_cls(
                    host_prefixes=adapter_config.host_prefixes, **adapter_config.kwargs
                ),
                url_prefixes=adapter_config.mount_prefixes,
            )
        if parsers is None:
            parsers = [
                parser_cls(fetcher=self.fetcher, contract_caller=self.contract_caller)
                for parser_cls in DEFAULT_PARSERS
            ]
        self.parsers = parsers

    def mount_adapter(  # type: ignore[no-untyped-def]
        self,
        adapter: Adapter,
        url_prefixes: list[str],
    ):
        """Given an adapter and list of url prefixes, register the adapter to each of the prefixes.

        Example Usage: mount_adapter(IPFSAdapter, ["ipfs://", "https://gateway.pinata.cloud/"])

        Args:
            adapter (Adapter): Adapter instance
            url_prefixes (list[str]): list of url prefixes to which to mount the adapter.
        """  # noqa: E501
        for prefix in url_prefixes:
            self.fetcher.register_adapter(adapter, prefix)

    def fetch_token_uri(
        self, token: Token, function_signature: str = "tokenURI(uint256)"
    ) -> Optional[str]:
        """Given a token, fetch the token uri from the contract using a specified function signature.

        Args:
            token (Token): token whose uri we want to fetch.
            function_signature (str, optional): token uri contract function signature. Defaults to "tokenURI(uint256)".

        Returns:
            Optional[str]: the token uri, if found.
        """  # noqa: E501

        res = self.contract_caller.single_address_single_fn_many_args(
            address=token.collection_address,
            function_sig=function_signature,
            return_type=["string"],
            args=[[token.token_id]],
        )
        return res[0] if res and len(res) > 0 else None

    async def gen_fetch_token_uri(
        self, token: Token, function_signature: str = "tokenURI(uint256)"
    ) -> Optional[str]:
        """Given a token, fetch the token uri from the contract using a specified function signature.

        Args:
            token (Token): token whose uri we want to fetch.
            function_signature (str, optional): token uri contract function signature. Defaults to "tokenURI(uint256)".

        Returns:
            Optional[str]: the token uri, if found.
        """  # noqa: E501

        res = await self.contract_caller.rpc.async_reader.gen_call_single_function_single_address_many_args(
            address=token.collection_address,
            function_sig=function_signature,
            return_type=["string"],
            args=[[token.token_id]],
        )
        return res[0] if res and len(res) > 0 else None

    def fetch_token_metadata(
        self,
        token: Token,
        metadata_selector_fn: Optional[Callable] = None,  # type: ignore[type-arg]
    ) -> Union[Metadata, MetadataProcessingError]:
        """Fetch metadata for a single token

        Args:
            token (Token): token for which to fetch metadata.
            metadata_selector_fn (Optional[Callable], optional):
                optionally specify a function to select a metadata
                object from a list of metadata. Defaults to None.

        Returns:
            Union[Metadata, MetadataProcessingError]: returns either a Metadata
                or a MetadataProcessingError if unable to parse.
        """
        possible_metadatas_or_errors = []

        # If no token uri is passed in, try to fetch the token uri from the contract
        if token.uri is None:
            try:
                token.uri = self.fetch_token_uri(token)
            except Exception as e:
                error_message = f"({token.chain_identifier}-{token.collection_address}-{token.token_id}) Failed to fetch token uri. {str(e)}"  # noqa: E501
                logger.error(error_message)
                possible_metadatas_or_errors.append(
                    MetadataProcessingError.from_token_and_error(
                        token=token, e=Exception(error_message)
                    )
                )

        raw_data = None

        # Try to fetch the raw data from the token uri
        if token.uri is not None:
            try:
                raw_data = self.fetcher.fetch_content(token.uri)
            except Exception as e:
                error_message = f"({token.chain_identifier}-{token.collection_address}-{token.token_id}) Failed to parse token uri: {token.uri}. {str(e)}"  # noqa: E501
                logger.error(error_message)
                possible_metadatas_or_errors.append(
                    MetadataProcessingError.from_token_and_error(
                        token=token, e=Exception(error_message)
                    )
                )

        for parser in self.parsers:
            if not parser.should_parse_token(token=token, raw_data=raw_data):  # type: ignore[arg-type]  # noqa: E501
                continue
            try:
                metadata_or_error = parser.parse_metadata(
                    token=token, raw_data=raw_data  # type: ignore[arg-type]
                )
                if isinstance(metadata_or_error, Metadata):
                    metadata_or_error.standard = parser._METADATA_STANDARD
                    if metadata_selector_fn is None:
                        return metadata_or_error
            except Exception as e:
                metadata_or_error = MetadataProcessingError.from_token_and_error(  # type: ignore[assignment]  # noqa: E501
                    token=token, e=e
                )
            possible_metadatas_or_errors.append(metadata_or_error)  # type: ignore[arg-type]  # noqa: E501
        if len(possible_metadatas_or_errors) == 0:
            possible_metadatas_or_errors.append(
                MetadataProcessingError.from_token_and_error(
                    token=token,
                    e=Exception(
                        f"({token.chain_identifier}-{token.collection_address}-{token.token_id}) No parsers found."  # noqa: E501
                    ),
                )
            )

        if metadata_selector_fn:
            return metadata_selector_fn(possible_metadatas_or_errors)  # type: ignore[no-any-return]  # noqa: E501
        return possible_metadatas_or_errors[0]

    async def gen_fetch_token_metadata(
        self,
        token: Token,
        metadata_selector_fn: Optional[Callable] = None,  # type: ignore[type-arg]
    ) -> Union[Metadata, MetadataProcessingError]:
        """Fetch metadata for a single token

        Args:
            token (Token): token for which to fetch metadata.
            metadata_selector_fn (Optional[Callable], optional):
                optionally specify a function to select a metadata
                object from a list of metadata. Defaults to None.

        Returns:
            Union[Metadata, MetadataProcessingError]: returns either a Metadata
                or a MetadataProcessingError if unable to parse.
        """
        possible_metadatas_or_errors: list[
            Union[Metadata, MetadataProcessingError]
        ] = []

        if not token.uri:
            return MetadataProcessingError.from_token_and_error(
                token=token, e=Exception("Token has not uri")
            )

        raw_data = None

        try:
            raw_data = await self.fetcher.gen_fetch_content(token.uri)
        except Exception as e:
            error_message = f"({token.chain_identifier}-{token.collection_address}-{token.token_id}) Failed to parse token uri: {token.uri}. {str(e)}"  # noqa: E501
            logger.error(error_message)
            possible_metadatas_or_errors.append(
                MetadataProcessingError.from_token_and_error(
                    token=token, e=Exception(error_message)
                )
            )

        async def gen_parse_metadata(
            parser: BaseParser,
        ) -> Optional[Union[Metadata, MetadataProcessingError]]:
            if not parser.should_parse_token(token=token, raw_data=raw_data):  # type: ignore[arg-type]  # noqa: E501
                return None
            try:
                metadata_or_error = await parser.gen_parse_metadata(
                    token=token, raw_data=raw_data  # type: ignore[arg-type]
                )
                if isinstance(metadata_or_error, Metadata):
                    metadata_or_error.standard = parser._METADATA_STANDARD
                    if metadata_selector_fn is None:
                        return metadata_or_error
            except Exception as e:
                metadata_or_error = MetadataProcessingError.from_token_and_error(  # type: ignore[assignment]  # noqa: E501
                    token=token, e=e
                )
            return metadata_or_error

        nullable_possible_metadatas_or_errors: list[
            Optional[Union[Metadata, MetadataProcessingError]]
        ] = await asyncio.gather(
            *(gen_parse_metadata(parser) for parser in self.parsers)
        )
        possible_metadatas_or_errors += filter(
            None, nullable_possible_metadatas_or_errors
        )
        if len(possible_metadatas_or_errors) == 0:
            possible_metadatas_or_errors.append(
                MetadataProcessingError.from_token_and_error(
                    token=token,
                    e=Exception(
                        f"({token.chain_identifier}-{token.collection_address}-{token.token_id}) No parsers found."  # noqa: E501
                    ),
                )
            )

        if metadata_selector_fn:
            return metadata_selector_fn(possible_metadatas_or_errors)  # type: ignore[no-any-return]  # noqa: E501
        return possible_metadatas_or_errors[0]

    def run(  # type: ignore[no-untyped-def, override]
        self,
        tokens: list[Token],
        parallelize: bool = True,
        select_metadata_fn: Optional[Callable] = None,  # type: ignore[type-arg]
        *args,
        **kwargs,
    ) -> list[Union[Metadata, MetadataProcessingError]]:
        """Run metadata pipeline on a list of tokens.

        Args:
            tokens (list[Token]): tokens for which to process metadata.
            parallelize (bool, optional): whether or not metadata should be processed in parallel.
                Defaults to True. Turn off parallelization to reduce risk of getting rate-limited.
            select_metadata_fn (Optional[Callable], optional): optionally specify a function to
                select a metadata object from a list of metadata. Defaults to None. Defaults to None.

        Returns:
            list[Union[Metadata, MetadataProcessingError]]: returns a list of Metadatas
                or MetadataProcessingErrors that map 1:1 to the tokens passed in.
        """  # noqa: E501
        if len(tokens) == 0:
            return []

        if parallelize:
            metadatas_or_errors = batched_parmap(
                lambda t: self.fetch_token_metadata(t, select_metadata_fn), tokens, 15
            )
        else:
            metadatas_or_errors = list(
                map(lambda t: self.fetch_token_metadata(t, select_metadata_fn), tokens)
            )

        return metadatas_or_errors

    async def async_run(  # type: ignore[no-untyped-def]
        self,
        tokens: list[Token],
        select_metadata_fn: Optional[Callable] = None,  # type: ignore[type-arg]
        *args,
        **kwargs,
    ) -> list[Union[Metadata, MetadataProcessingError]]:
        """Async Run metadata pipeline on a list of tokens.

        Args:
            tokens (list[Token]): tokens for which to process metadata.
            select_metadata_fn (Optional[Callable], optional): optionally specify a function to
                select a metadata object from a list of metadata. Defaults to None. Defaults to None.

        Returns:
            list[Union[Metadata, MetadataProcessingError]]: returns a list of Metadatas
                or MetadataProcessingErrors that map 1:1 to the tokens passed in.
        """  # noqa: E501
        if len(tokens) == 0:
            return []
        tasks = [
            self.gen_fetch_token_metadata(token, select_metadata_fn) for token in tokens
        ]

        metadatas_or_errors = await asyncio.gather(*tasks)
        return metadatas_or_errors
