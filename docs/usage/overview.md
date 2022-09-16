# Usage

## Basic Usage

```python
from offchain import MetadataPipeline, Token

pipeline = MetadataPipeline()
token = Token(
    collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
    token_id=9559
)

metadata = pipeline.run([token])[0]

# Data for the token at index 0
metadata.name               # -> 'antares the improbable'
metadata.description        # -> 'You are a WITCH who bathes in the tears of...'
metadata.standard           # -> OPENSEA_STANDARD
metadata.attributes         # -> [Attribute(trait_type='Skin Tone', ...]
metadata.image              # -> MediaDetails(size=2139693, sha256=None, uri='https://cryptocoven.s3.amazonaws.com/2048b255aa1d02045eef13cdd7100479.png', mime_type='image/png')
metadata.additional_fields  # -> [MetadataField(...), ...]
```

## Input

The `Token` interface is how the metadata pipeline uniquely identifies an NFT. A `Token` is composed of four properties:

- `collection_address`: The token's contract address.
- `token_id`: The unique identifier for a token within a collection.
- `chain_identifier`: The network and chain for the token. Defaults to "ETHEREUM-MAINNET" if nothing is passed in.
- `uri`: The url where the metadata information lives. Defaults to fetching from the contract directly if nothing is passed in.

Example of token `9559` from `CryptoCoven` on Ethereum Mainnet:

```python
from offchain import Token

Token(
    collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8", #Required
    token_id=9559, #Required
    chain_identifier="ETHEREUM-MAINNET", # Optional, defaults to Ethereum Mainnet
    uri:"ipfs://QmaXzZhcYnsisuue5WRdQDH6FDvqkLQX1NckLqBYeYYEfm/9559.json" # Optional, defaults to requesting the URI from the contract directly
)
```

## Output

The `MetadataPipeline` is run on a list of `Token` objects and outputs a list of equal length.
Each item in the output list maps to the `Token` at the same index in the input list.
If the pipeline successfully fetches metadata for a token, the token should map to a [Metadata](../models/metadata.md) object.

The `Metadata` interface is a standardized representation of NFT metadata. Conversely, if the pipeline fails to fetch metadata for a token, it should map to a [MetadataProcessingError](../models/metadata_processing_error.md) object. The `MetadataProcessingError` interface defines contextual information for how and why processing metadata for a specific token failed.

## Pipeline Components

- [Pipeline](../pipeline/pipeline.md): Orchestrates the metadata fetching and normalizing process for multiple tokens.
- [Adapter](../pipeline/adapters.md): Parses the metadata url into an acceptable request format for the fetcher.
- [Fetcher](../pipeline/fetchers.md): Makes network requests to a given uri to fetch data.
- [Parser](../pipeline/parsers.md): Parses raw data into a standardized metadata format
- ContractCaller: Makes RPC calls to NFT contracts to retrieve the URI if not provided.

## How it Works

1. The `MetadataPipeline` is initialized with a `ContractCaller`, a `Fetcher`, a list of `Adapters`, and a list of `Parsers`.
2. If no `uri` is passed in for a token, the pipeline will use the `ContractCaller` to attempt to fetch it from a `tokenURI(uint256)` view function on the contract.
3. The pipeline use the `Fetcher` and `Adapters` to attempt to fetch metadata in form of raw JSON from the uri.
4. The pipeline runs each parser in the order they were passed in. By default, the ordering is `CollectionParsers`, `SchemaParsers`, and then `CatchallParsers`.
5. The pipeline will return the result of the first parser that is able to successfully parse the token, unless a `metadata_selector_fn` is specified.

6. If no parser is able to successfully parse a token, the pipeline will return a `MetadataProcessingError` for that token.
