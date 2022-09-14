# Adding a new metadata format

## Step 1: Determine the type of parser

`offchain` supports two parser types: collection parsers and schema parsers.

Collection parsers know how to standardize token metadata based on a token's collection address. If you want to add metadata support for specific collections, a collection parser will suffice.

Schema parsers know how to standardize token metadata based on the shape of the metadata. If you want to add support for new metadata shapes that will be used across numerous NFT collections, then you'll need to use a schema parser.

Unlike collection parsers, schema parsers are not constrained to a specific set of tokens. As a result, each new schema parser should define a sufficiently different schema than the existing supported schemas. A schema parser should only be defined if the answer to all of the following questions is Yes:

1. Is there a way to uniquely identify tokens that have this metadata format?
2. Will there be new NFT collections that use this new metadata format?
3. Should the resulting standardized metadata schema be different from what is currently returned by the default catchall parser?

---

## Step 2: Standardize the new metadata format

In order to support a new metadata format, we need to be able to map it into the [standardized metadata format](../models/metadata.md). Each field in the new metadata format should either map a field in the standardized metadata format or be added as an `MetadataField` under the `additional_fields` property. For instance, ENS metadata has the following fields:

```json
{
  "name": "ENS name",
  "description": "Short ENS name description",
  "attributes": "Custom traits about ENS",
  "name_length": "Character length of ens name",
  "url": "ENS App URL of the name",
  "version": "ENS NFT version",
  "background_image": "Origin URL of avatar image",
  "image_url": "URL of ENS NFT image"
}
```

and these fields can be mapped into the standard metadata format as such:

| Standard Metadata Field | New Metadata Field        |
| ----------------------- | ------------------------- |
| token                   |                           |
| raw_data                |                           |
| standard                | COLLECTION_STANDARD       |
| attributes              | attributes                |
| name                    | name                      |
| description             | description               |
| mime_type               |                           |
| image                   | image_url                 |
| content                 | background_image          |
| additional_fields       | name_length, url, version |

---

## Step 3: Define a new parser

Before implementing a new parser, first familiarize yourself with the `BaseParser` class, as well as either the `CollectionParser` or `SchemaParser` base class:

- [BaseParser](../pipeline/parsers.md#baseparser)
- [CollectionParser](../pipeline/parsers.md#collectionparser)
- [SchemaParser](../pipeline/parsers.md#schemaparser)

### Step 3a: Defining the selection criteria

For a collection parser, the selection criteria are the collection addresses that the parser runs on. For example, the ENS collection parser will only run on tokens with the ENS collection contract address: `0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85`

For a schema parser, you will need to override the `should_parse_token()` method of `BaseParser` to implement selection logic based on the shape of the metadata. For example, if the new metadata schema contains a unique field, you could do something like this:

```python
from typing import Optional

from offchain.metadata.models.token import Token
from offchain.metadata.parsers.schema.schema_parser import SchemaParser

class NewSchemaParser(SchemaParser):
    def should_parse_token(self, token: Token, raw_data: Optional[dict], *args, **kwargs) -> bool:
        return raw_data is not None and raw_data.get("unique_field") is not None
```

### Step 3b: Writing the metadata parsing implementation

#### Constructing the token uri

The token uri is needed to tell the parser where to fetch the metadata from. If the token uri is not passed in as part of the input, the pipeline will attempt to fetch it from a `tokenURI(uint256)` view function on the contract. Otherwise, it is expected that the parser will construct the token uri. For instance, ENS hosts their own metadata service and token uris are constructed in the following format: `https://metadata.ens.domains/<chain_name>/<collection_address>/<token_id>/`

```python
uri = f"https://metadata.ens.domains/mainnet/{token.collection_address}/{token.token_id}/"
```

Note: it is not uncommon for token uris to be base64 encoded data is stored entirely on chain. This is the case for collections like Nouns or Zorbs.

#### Fetching metadata from the token uri

Once you have the token uri, we can use the `Fetcher` to fetch the raw JSON data from the token uri.

```python
from offchain.metadata.adapters import HTTPAdapter
from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher

fetcher = MetadataFetcher()
fetcher.register_adapter(
    adapter=HTTPAdapter(
        pool_connections=100,
        pool_maxsize=1000,
        max_retries=0,
    ),
    url_prefix="https://",
)
raw_data = fetcher.fetch_content(uri)
```

#### Standardizing the raw metadata

Once you've fetched the raw metadata from the token uri, you can reshape it into the standardized metadata format. For instance, extracting `attributes` from the raw ENS metadata JSON may look something like this:

```python
from typing import Optional
from offchain.metadata.models.metadata import Attribute, Metadata

def parse_attributes(raw_data: dict) -> Optional[list[Attribute]]:
    attributes = raw_data.get("attributes")
    if not attributes or not isinstance(attributes, list):
        return

    return [
        Attribute(
            trait_type=attribute_dict.get("trait_type"),
            value=attribute_dict.get("value"),
            display_type=attribute_dict.get("display_type"),
        )
        for attribute_dict in attributes
    ]

Metadata(
    token=token,
    raw_data=raw_data,
    attributes=parse_attributes(raw_data),
    name=raw_data.get("name"),
    description=raw_data.get("description"),
    ...
)
```

## Step 4: Register your new parser

After writing your custom metadata parser implementation, you'll want to register it to the `ParserRegistry`. The `ParserRegistry` tracks all parsers and is used by the metadata pipeline to know which parsers to run by default.

```python
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry

@ParserRegistry.register
class ENSParser(CollectionParser):
    ...
```

## Step 5: Write tests

Finally, you'll want to write tests to verify that your parser works as expected. At minimum, the `should_parse_token()` and `parse_metadata()` functions should be tested because the pipeline will call those directly.

It's important to verify that the `should_parse_token()` function returns `True` if and only if a token is meant to be parsed by that parser.

Given a token, `parse_metadata()` should normalize the raw data into the standardized metadata format. Since making network requests can be flaky, it's preferable to mock the data that would be returned by the server that hosts the metadata information.

```python
from unittest.mock import MagicMock

from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher
from offchain.web3.contract_caller import ContractCaller
from offchain.metadata.parsers.collection.ens import ENSParser

def test_ens_parser_should_parse_token(self):
    fetcher = MetadataFetcher()
    contract_caller = ContractCaller()
    parser = ENSParser(fetcher=fetcher, contract_caller=contract_caller)
    assert parser.should_parse_token(token=token) == True

def test_ens_parser_parses_metadata(self):
    fetcher = MetadataFetcher()
    contract_caller = ContractCaller()
    fetcher.fetch_mime_type_and_size = MagicMock(return_value=("application/json", 41145))
    fetcher.fetch_content = MagicMock(return_value=mocked_raw_data)
    parser = ENSParser(fetcher=fetcher, contract_caller=contract_caller)
    assert parser.parse_metadata(token=token, raw_data=None) == expected_metadata
```

## Example ENS collection parser

::: offchain.metadata.parsers.collection.ens.ENSParser
