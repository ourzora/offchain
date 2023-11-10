from offchain.metadata.adapters.arweave import ARWeaveAdapter
from offchain.metadata.adapters.base_adapter import AdapterConfig
from offchain.metadata.adapters.data_uri import DataURIAdapter
from offchain.metadata.adapters.http_adapter import HTTPAdapter
from offchain.metadata.adapters.ipfs import IPFSAdapter

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
