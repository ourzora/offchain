# Customizing the Pipeline

There are countless ways to customize the pipeline. The default `MetadataPipeline` can be constructed with any permutation of `Fetchers`, `Adapters`, `Parsers`, and `ContractCallers`. And you can even define your own custom `Pipeline` by extending the `BasePipeline` class.

In this guide, we'll cover a few ways you can customize the `MetadataPipeline` to best suit your needs.

## Custom RPC Provider

By default, the pipeline uses `https://cloudflare-eth.com` as the Ethereum JSON RPC url. This is a free Ethereum RPC provider, which means that it is very easy to exceed the rate-limit. If you have a custom RPC provider url you'd like to use, you can specify it like this:

```python
from offchain import MetadataPipeline
from offchain.web3.contract_caller import ContractCaller
from offchain.web3.jsonrpc import EthereumJSONRPC

rpc = EthereumJSONRPC(provider_url=MY_PROVIDER_URL)
contract_caller = ContractCaller(rpc=rpc)
pipeline = MetadataPipeline(contract_caller=contract_caller)
```

## Custom Parsers

By default, the pipeline runs with all collection, schema, and catch-all parsers. That said, you may find that you're only interested in using a subset of the parsers. Let's say you're only interested in parsing metadata for a specific collection.

If this is the case, you can pass in a list of specific parser instances to run. For example, the following configuration runs the pipeline using only the ENS collection parser.

```python
from offchain import MetadataPipeline
from offchain.metadata import ENSParser

ens_parser = ENSParser()
pipeline = MetadataPipeline(parsers=[ens_parser])
```

View the full list of available parsers [here](https://github.com/ourzora/offchain/tree/main/offchain/metadata/parsers).

## Custom Adapters

By default, the pipeline is run with all available adapters. Each adapter has a default host prefix and is configured with the following args: `{"pool_connections": 100, "pool_maxsize": 1000, "max_retries": 0}`

You can also customize the pipeline to only use a subset of the adapters. For instance, if you wanted to build a metadata indexer that only indexes onchain metadata, you may opt to only use the IPFS, ARWeave, and DataURI adapters.

There are two ways to configure custom adapters for the pipeline:

### Specifying Adapter Configs

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

View the full list of available adapters [here](https://github.com/ourzora/offchain/tree/main/offchain/metadata/adapters).

### Mounting Custom Adapters

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
