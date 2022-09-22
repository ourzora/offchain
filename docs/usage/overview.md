# Usage

Please review the [Core Concepts](../concepts.md) page before reading the rest of the documentation.

## Basic Usage

### Fetching metadata for a single token

```python
from offchain import get_token_metadata

metadata = get_token_metadata(
    collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
    token_id=9559
)

# Data for the token at index 0
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

The `Metadata` interface is a standardized representation of NFT metadata. Conversely, if the pipeline fails to fetch metadata for a token, it should map to a [MetadataProcessingError](../models/metadata_processing_error.md) object.
The `MetadataProcessingError` interface defines contextual information for how and why processing metadata for a specific token failed.
