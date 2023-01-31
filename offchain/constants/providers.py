from offchain.base.types import StringEnum


class RPCProvider(StringEnum):
    CLOUDFLARE_MAINNET = "https://cloudflare-eth.com"
    LLAMA_NODES_MAINNET = "https://eth.llamarpc.com"
