# Tutorials

## Writing a collection parser

If you have a specific NFT collection for which you'd like to write a custom parsing implementation, you can
contribute a collection parser. Collection parsers must specify the collection address(es) for which they parse metadata.
You can get started by extending the `CollectionParser` base class and following the patterns laid out by other
collection parsers, such as `ENSParser` or `NounsParser`.

---

### Understanding tokens

Tokens are the first layer of parsing metadata, and is an important concept when building your collection parser.
At a high level, tokens are comprised of four things:

1. The chain identifier (which chain this token belongs to, by default this is set to Ethereum's mainnet)
2. The collection address (collection address of the token)
3. The token ID (the unique identifier of the token)
4. The token URI (where the metadata lives, this by default is normally None)

These four attributes are how our `MetadataPipeline` can uniquely identify an NFT.

Example of token `9559` from `CryptoCoven` on Ethereum mainnet:

```python
from offchain.metadata.models.token import Token

token = Token(
    collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
    token_id=9559
)
```

---

### Defining your collection addresses

The first thing we need to define is the collection address(es) for our parser. The address(es) are used
when the `MetadataPipeline` needs to decide which collection parser to use when it's provided with an address and token id.

By default, we simply validate against the list of collection addresses. However, if your collection requires
additional logic, it can be overridden. See the default implementation below.

```python
from offchain.metadata.models.token import Token

def should_parse_token(self, token: Token, *args, **kwargs) -> bool:
    """Return whether or not a collection parser should parse a given token.

    Args:
        token (Token): the token whose metadata needs to be parsed.

    Returns:
        bool: whether or not the collection parser handles this token.
    """
    return token.collection_address in [address.lower() for address in self._COLLECTION_ADDRESSES]
```

---

### Fetching metadata

Once we've identified that metadata from this token in this collection needs to be parsed, we need
to figure out how to fetch it. This can be different for every collection, but the majority of collections
use one or many of the concepts, in combination, below.

#### URIs

URIs are a great way to fetch metadata, and is usually where you start. It could be an IPFS endpoint, an HTTP endpoint, raw base64 encoded
JSON data, or something else that we can fetch. When we want to fetch from a URI, the `MetadataPipeline` will attempt to use
an `Adapter` like the `IPFSAdapter` or `HTTPAdapter`. This is automatically handled by the `MetadataFetcher`.

---

##### On-chain Token URI

By default, the `MetadataPipeline` attempts to call `tokenURI(tokenId)` on the collection, which normally exists
if it implements the `IERC721Metadata` standard. The metadata fetched from the URI normally contains elements like the name,
description, image, etc. Some contracts implement other methods to get the URI, like Zora Media, which uses `tokenMetadataURI(tokenId)`.

Example:

```python
from typing import Optional
from offchain.web3.contract_caller import ContractCaller

contract_caller = ContractCaller()

def get_uri(collection_address: str, token_id: int) -> Optional[str]:
    results = contract_caller.single_address_single_fn_many_args(
        collection_address,
        function_sig="tokenMetadataURI(uint256)",
        return_type=["string"],
        args=[[token_id]],
    )

    if len(results) < 1:
        return None

    return results[0]
```

---

##### Static Token URI

Collections like `Wrapped Punks` uses a pre-defined, static URI which we can use to fetch its metadata. We can build
the URI to fetch by combining the base URL and token id by using an f-String like `f"https://api.wrappedpunks.com/api/punks/metadata/{token_id}"`.

Normally this behavior doesn't need its own function, however if you have a collection like `Chainrunners`, you might need to
call a contract function to finish building the URI.

Example:

```python
from typing import Optional
from offchain.web3.contract_caller import ContractCaller

contract_caller = ContractCaller()

def get_dna(collection_address: str, token_id: int) -> Optional[int]:
    results = contract_caller.single_address_single_fn_many_args(
        address=collection_address,
        function_sig="getDna(uint256)",
        return_type=["uint256"],
        args=[[token_id]],
    )

    if len(results) < 1:
        return None

    return results[0]

token_id = 484

dna = get_dna("0x97597002980134bea46250aa0510c9b90d87a587", token_id)
uri = f"https://api.chainrunners.xyz/tokens/metadata/{token_id}?dna={dna}"
```

---

##### On-chain Data URI

Sometimes, token metadata can be an on-chain data uri. This is a base64 encoded URI that can be stored entirely on chain.
This is true for the `Nouns` and `Lil Nouns` collections. The `MetadataFetcher` is capable of parsing this format, which internally is just stripping down
the URI metadata and decoding the base64.

Example:

```python
from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher

uri = "data:application/json;base64,eyJtZXNzYWdlIjogIkhlbGxvIHdvcmxkISJ9"

fetcher = MetadataFetcher()
raw_data = fetcher.fetch_content(uri) # -> {"message": "Hello world!"}

```

---

#### Raw Data

Raw data is the JSON data we will parse and extract from. It is used to create a `Metadata` object and
is inevitably returned by the `MetadataPipeline`.

---

##### Fetched Data

This is what will be used by the majority of collection parsers. It is the data returned after being fetched from a URI.

Example:

```python
from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher

token_id = 113384
uri = f"https://api.foundation.app/opensea/{token_id}"

fetcher = MetadataFetcher()
raw_data = fetcher.fetch_content(uri)
```

---

##### Static Data

In most instances, the raw data will be fetched from the URI. There are some edge-cases where the raw data is static, and can be generated on the fly.
This is true for collections like `Autoglyphs`.

Example:

```python
def create_raw_data(token_id: int) -> dict:
    return {
        "title": f"Autoglyph #{token_id}",
        "name": f"Autoglyph #{token_id}",
        "image": f"https://www.larvalabs.com/autoglyphs/glyphimage?index={token_id}",
        "description": 'Autoglyphs are the first "on-chain" generative art on the Ethereum blockchain. A '
        "completely self-contained mechanism for the creation and ownership of an artwork.",
        "external_url": f"https://www.larvalabs.com/autoglyphs/glyph?index={token_id}",
    }
```

---

### Extracting Metadata

### Testing your collection parser

### Writing tests
