# Usage

## Basic usage

### Fetching metadata for a single token

```python
from offchain import get_token_metadata

metadata = get_token_metadata(
    collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
    token_id=9559
)

metadata.name               # -> 'antares the improbable'
metadata.description        # -> 'You are a WITCH who bathes in the tears of...'
metadata.standard           # -> OPENSEA_STANDARD
metadata.attributes         # -> [Attribute(trait_type='Skin Tone', ...]
metadata.image              # -> MediaDetails(size=2139693, sha256=None, uri='https://cryptocoven.s3.amazonaws.com/2048b255aa1d02045eef13cdd7100479.png', mime_type='image/png')
metadata.additional_fields  # -> [MetadataField(...), ...]
```

### Fetching metadata for multiple tokens

```python
from offchain import MetadataPipeline, Token

pipeline = MetadataPipeline()
token_1 = Token(
    collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
    token_id=9559
)
token_2 = Token(
    collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
    token_id=9560
)
metadatas = pipeline.run([token_1, token_2])
```

## Input

The `Token` interface is how the metadata pipeline uniquely identifies an NFT. They are composed of four properties:

1. The chain identifier: the network and chain that this token lives on, by default this is set to "ETHEREUM-MAINNET"
2. The collection address: the contract address of the token's collection
3. The token id: the unique identifier for a token within a collection
4. The token URI: the url where the metadata information lives. If this is not passed in, the metadata pipeline will attempt to fetch it from the contract.

Example of token `9559` from `CryptoCoven` on Ethereum Mainnet:

```python
from offchain import Token

Token(
    chain_identifier="ETHEREUM-MAINNET",
    collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
    token_id=9559
)
```

## Output

The `MetadataPipeline` is run on a list of `Token` objects and outputs a list of equal length. Each item in the output list maps to the `Token` at the same index in the input list. If pipeline successfully fetches metadata for a token, the token should map to a [Metadata](../models/metadata.md) object. The `Metadata` interface is a standardized representation of NFT metadata. Conversely, if the pipeline fails to fetch metadata for a token, it should map to a [MetadataProcessingError](../models/metadata_processing_error.md) object. The `MetadataProcessingError` interface defines contextual information for how and why processing metadata for a specific token failed.

## Pipeline components

- [Pipeline](../pipeline/pipeline.md): orchestrates the metadata fetching and normalizing process for multiple tokens.
- [Adapter](../pipeline/adapters.md): parses the metadata url into an acceptable request format for the fetcher.
- [Fetcher](../pipeline/fetchers.md): makes requests to a given uri to fetch data.
- [Parser](../pipeline/parsers.md): parses raw data into a standardized metadata format
- ContractCaller: makes RPC calls to contract view functions.

## How it works

1. The `MetadataPipeline` is initialized with a `ContractCaller`, a `Fetcher`, a list of `Adapters`, and a list of `Parsers`.
2. If no `uri` is passed in for a token, the pipeline will use the `ContractCaller` to attempt to fetch it from a `tokenURI(uint256)` view function on the contract.
3. The pipeline use the `Fetcher` and `Adapters` to attempt to fetch metadata in form of raw JSON from the uri.
4. The pipeline runs each parser in the order they were passed in. By default, the ordering is `CollectionParsers`, `SchemaParsers`, and then `CatchallParsers`.
5. The pipeline will return the result of the first parser that is able to successfully parse the token, unless a `metadata_selector_fn` is specified.

6. If no parser is able to successfully parse a token, the pipeline will return a `MetadataProcessingError` for that token.
