# Customizing the Pipeline

## Using a Custom RPC

By default, the pipeline uses `https://cloudflare-eth.com` as the Ethereum JSON RPC url.
A custom RPC provider can be specified like so:

```python
from offchain.metadata.pipelines.metadata_pipeline import MetadataPipeline
from offchain.web3.contract_caller import ContractCaller
from offchain.web3.jsonrpc import EthereumJSONRPC

rpc = EthereumJSONRPC(provider_url=MY_PROVIDER_URL)
contract_caller = ContractCaller(rpc=rpc)
pipeline = MetadataPipeline(contract_caller=contract_caller)
```

## Using Custom Parsers

By default, the pipeline runs with all collection, schema, and catch-all parsers.
It is possible to pass in a list of specific parser instances to run.
For instance, the following configuration runs the pipeline using only the ENS collection parser.

```python
from offchain.metadata.pipelines.metadata_pipeline import MetadataPipeline
from offchain.metadata.parsers.collection.ens import ENSParser

ens_parser = ENSParser()
pipeline = MetadataPipeline(parsers=[ens_parser])
```

View the full list of available parsers [here](https://github.com/ourzora/offchain/tree/main/offchain/metadata/parsers).

## Using Custom Adapters

By default, the pipeline is run with all available adapters. Each adapter has a default host prefix and is configured with the following args: `{"pool_connections": 100, "pool_maxsize": 1000, "max_retries": 0}`

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
