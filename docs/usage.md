# Usage

## Basic usage

```py
from offchain.metadata.pipelines.metadata_pipeline import MetadataPipeline
from offchain.metadata.models.token import Token

pipeline = MetadataPipeline()
token = Token(
    chain_identifier="ETHEREUM-MAINNET",
    collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
    token_id=9559,
    uri="ipfs://QmSr3vdMuP2fSxWD7S26KzzBWcAN1eNhm4hk1qaR3x3vmj/9559.json"
    )
metadatas = pipeline.run([token])
```

## How it works

The `MetadataPipeline` is run on a list of `Token` objects and returns a list of `Metadata` or `MetadataProcessingError` objects, each of which maps to the `Token` at the same index in the input list. (see `Interfaces` for more information).

1. The `MetadataPipeline` is initialized with a `ContractCaller`, a `Fetcher`, a list of `Adapters`, and a list of `Parsers`.
2. If no `uri` is passed in for a token, the pipeline will use the `ContractCaller` to attempt to fetch it from a `tokenURI(uint256)` view function on the contract.
3. The pipeline use the `Fetcher` and `Adapters` to attempt to fetch metadata in form of raw JSON from the uri.
4. The pipeline runs each parser in the order they were passed in. By default, the ordering is `CollectionParsers`, `SchemaParsers`, and then `CatchallParsers`.
5. The pipeline will return the result of the first parser that is able to successfully parse the token, unless a `metadata_selector_fn` is specified.

6. If no parser is able to successfully parse a token, the pipeline will return a `MetadataProcessingError` for that token.

## Using a custom RPC provider url

By default, the pipeline uses a free Ethereum JSON RPC url: `https://cloudflare-eth.com`. You can specify your own rpc provider url like this:

```python
from offchain.metadata.pipelines.metadata_pipeline import MetadataPipeline
from offchain.web3.contract_caller import ContractCaller
from offchain.web3.jsonrpc import EthereumJSONRPC

rpc = EthereumJSONRPC(provider_url=MY_PROVIDER_URL)
contract_caller = ContractCaller(rpc=rpc)
pipeline = MetadataPipeline(contract_caller=contract_caller)
```

## Using custom parsers

By default, the pipeline runs with all collection and schema parsers. You can pass in a list of specific parser instances to run. For instance, the following configuration runs the pipeline using only the ENS collection parser.

```python
from offchain.metadata.pipelines.metadata_pipeline import MetadataPipeline
from offchain.metadata.parsers.collection.ens import ENSParser

ens_parser = ENSParser()
pipeline = MetadataPipeline(parsers=[ens_parser])
```

## Using custom adapters

By default, the pipeline is run with all available adapters. Each adapter uses a default free host prefix and is configured with the following args: `{"pool_connections": 100, "pool_maxsize": 1000, "max_retries": 0}`

There are two ways to configure custom adapters for the pipeline:

#### Specifying adapter configs

```python
from offchain.metadata.adapters import ARWeaveAdapter, DataURIAdapter, HTTPAdapter, IPFSAdapter
from offchain.metadata.pipelines.metadata_pipeline import AdapterConfig, MetadataPipeline


adapter_configs = [
    AdapterConfig(
        adapter_cls=ARWeaveAdapter,
        mount_prefixes=["ar://"],
        host_prefixes=["https://arweave.net/"],
        kwargs={"pool_connections": 100, "pool_maxsize": 1000, "max_retries": 0},
    ),
    AdapterConfig(adapter_cls=DataURIAdapter, mount_prefixes=["data:"]),
]

pipeline = MetadataPipeline(adapter_configs=adapter_configs)
```

#### Mounting custom adapters

```python
from offchain.metadata.adapters import IPFSAdapter
from offchain.metadata.pipelines.metadata_pipeline import MetadataPipeline

pipeline = MetadataPipeline()
pipeline.mount_adapter(
    adapter=IPFSAdapter(
        host_prefixes=[MY_CUSTOM_IPFS_HOST],
        pool_connections=100,
        pool_maxsize=1000,
        max_retries=0,
    ),
    url_prefixes=[
        "ipfs://",
        "https://gateway.pinata.cloud/",
        "https://ipfs.io/",
    ],
)
```
