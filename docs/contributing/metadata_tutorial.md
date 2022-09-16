# Adding a New Metadata Format

To add support for a new metadata format, you'll need to add a new parser to the `offchain` repo.

In this guide, we'll build a parser for the ENS collection from scratch and go over important considerations for building your own parser.

---

## Step 1: Determine the Type of Parser

The first consideration is determining which type of parser to build.

Before implementing your parser, familiarize yourself with the [BaseParser](../pipeline/parsers.md#baseparser), [CollectionParser](../pipeline/parsers.md#collectionparser), and [SchemaParser](../pipeline/parsers.md#schemaparser) base classes.

Your parser will be one of the following:

- `CollectionParser`: determines if it should run on a token by looking at the token's collection address
- `SchemaParser`: determines if it should run on a token by looking at the shape of the token's metadata

As a general rule of thumb, you should only define a new schema parser if the answer to all of the following questions is `Yes`:

1. Is there a way to uniquely identify tokens that have this new metadata format?
2. Will there be new NFT collections that use this new metadata format?
3. Does the default parser in the pipeline parse the this new metadata format incorrectly?

Since, we're building a parser for the ENS collection, we'll be building a `CollectionParser`.

```python
class ENSParser(CollectionParser):
    pass
```

---

## Step 2: Define the Selection Criteria

The next step is to define your parser's selection criteria. This tells the pipeline which tokens to run your parser on.

If you're building a schema parser, you'll need to override the `should_parse_token()` method of `BaseParser` to implement custom selection logic based on the shape of the metadata. For instance, if the new metadata schema contains a unique field, checking for the existence of that field would qualify as selection criteria:

```python
def should_parse_token(self, raw_data: Optional[dict], *args, **kwargs) -> bool:
    return raw_data is not None and raw_data.get("unique_field") is not None
```

If you're building a collection parser, the selection criteria is simply defined by a `_COLLECTION_ADDRESSES` class variable, which tells the parser which collection address(es) to run on. The ENS collection parser will only run on tokens with the ENS collection contract address (`0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85`).

```python
class ENSParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = ["0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85"]
```

---

## Step 3: Write the Metadata Parsing Implementation

### Step 3a: Construct the Token URI

The token uri is needed to tell the parser where to fetch the metadata from.

If the token uri is not passed in as part of the input, the pipeline will attempt to fetch it from a `tokenURI(uint256)` view function on the contract. Otherwise, it is expected that the parser will construct the token uri.

Note: it is not uncommon for token uris to be base64 encoded data is stored entirely on chain. This is the case for collections like Nouns or Zorbs.

ENS hosts their own metadata service and token uris are constructed in the following format: `https://metadata.ens.domains/<chain_name>/<collection_address>/<token_id>/`

```python
class ENSParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = ["0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85"]

    @staticmethod
    def make_ens_chain_name(chain_identifier: str):
        try:
            return chain_identifier.split("-")[1].lower()
        except Exception:
            logger.error(f"Received unexpected chain identifier: {chain_identifier}")
            return "mainnet"

    def parse_metadata(self, token: Token, raw_data: dict, *args, **kwargs) -> Optional[Metadata]:
        ens_chain_name = self.make_ens_chain_name(token.chain_identifier)

        token.uri = (
            f"https://metadata.ens.domains/{ens_chain_name}/{token.collection_address.lower()}/{token.token_id}/"
        )
```

Let's use this ENS NFT as an example:

```python
Token(
    chain_identifier="ETHEREUM-MAINNET",
    collection_address="0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85",
    token_id=10110056301157368922112380646085332716736091604887080310048917803187113883396,
)
```

If we pass it into the parser, we'll get the following uri: `https://metadata.ens.domains/mainnet/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/10110056301157368922112380646085332716736091604887080310048917803187113883396`, which returns metadata information from the ENS metadata service.

### Step 3b: Fetch Metadata From the Token uri

Once you have the token uri, we can use the `Fetcher` to fetch the raw JSON data from the token uri. By default, the parser is initialized with a `Fetcher` instance with an HTTP adapter.

```python
    raw_data = self.fetcher.fetch_content(token.uri)
```

This should return the following data from the ENS metadata service:

```json
{
  "is_normalized": true,
  "name": "steev.eth",
  "description": "steev.eth, an ENS name.",
  "attributes": [
    {
      "trait_type": "Created Date",
      "display_type": "date",
      "value": 1633123738000
    },
    { "trait_type": "Length", "display_type": "number", "value": 5 },
    { "trait_type": "Segment Length", "display_type": "number", "value": 5 },
    {
      "trait_type": "Character Set",
      "display_type": "string",
      "value": "letter"
    },
    {
      "trait_type": "Registration Date",
      "display_type": "date",
      "value": 1633123738000
    },
    {
      "trait_type": "Expiration Date",
      "display_type": "date",
      "value": 1822465450000
    }
  ],
  "name_length": 5,
  "segment_length": 5,
  "url": "https://app.ens.domains/name/steev.eth",
  "version": 0,
  "background_image": "https://metadata.ens.domains/mainnet/avatar/steev.eth",
  "image": "https://metadata.ens.domains/mainnet/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/0x165a16ce2915e51295772b6a67bfc8ceee2c1c7caa85591fba107af4ee24f704/image",
  "image_url": "https://metadata.ens.domains/mainnet/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/0x165a16ce2915e51295772b6a67bfc8ceee2c1c7caa85591fba107af4ee24f704/image"
}
```

### Step 3c: Standardize the New Metadata Format

The next step is to convert the metadata into the [standardized metadata format](../models/metadata.md).

Each field in the new metadata format should either map a field in the standardized metadata format or be added as an `MetadataField` under the `additional_fields` property.

In the case of ENS, the metadata format has the following fields:

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

Each of these fields can be mapped into the standard metadata format:

| Standard Metadata Field | New Metadata Field        |
| ----------------------- | ------------------------- |
| token                   |                           |
| raw_data                |                           |
| standard                |                           |
| attributes              | attributes                |
| name                    | name                      |
| description             | description               |
| mime_type               |                           |
| image                   | image_url                 |
| content                 | background_image          |
| additional_fields       | name_length, url, version |

---

And this is how it would look programatically:

```python
class ENSParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = ["0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85"]

from offchain.metadata.models.token import Token
from offchain.metadata.parsers.schema.schema_parser import SchemaParser

class NewSchemaParser(SchemaParser):
    def should_parse_token(self, token: Token, raw_data: Optional[dict], *args, **kwargs) -> bool:
        return raw_data is not None and raw_data.get("unique_field") is not None
```

### Step 3d: Write the Metadata Parsing Implementation

#### Constructing the Token URI

The token uri is needed to tell the parser where to fetch the metadata from. If the token uri is not passed in as part of the input, the pipeline will attempt to fetch it from a `tokenURI(uint256)` view function on the contract. Otherwise, it is expected that the parser will construct the token uri. For instance, ENS hosts their own metadata service and token uris are constructed in the following format: `https://metadata.ens.domains/<chain_name>/<collection_address>/<token_id>/`

```python
uri = f"https://metadata.ens.domains/mainnet/{token.collection_address}/{token.token_id}/"
```

Note: it is not uncommon for token uris to be base64 encoded data is stored entirely on chain. This is the case for collections like Nouns or Zorbs.

#### Fetching Metadata from the Token URI

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

#### Standardizing the Raw Metadata

Once you've fetched the raw metadata from the token uri, you can reshape it into the standardized metadata format. For instance, extracting `attributes` from the raw ENS metadata JSON may look something like this:

```python
from typing import Optional
from offchain.metadata.models.metadata import Attribute, Metadata

    def parse_attributes(self, raw_data: dict) -> Optional[list[Attribute]]:
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
```

## Step 4: Register your New Parser

If you're developing locally, you still need to import the `ParserRegistry` to register your parser. The parser must be registered in order for it to be run by default in the `MetadataPipeline`. In the example below, we register the `ENSParser` class locally and run `get_token_metadata()`, which leverages the `MetadataPipeline`.

```python
from offchain import get_token_metadata
from offchain.metadata import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry

@ParserRegistry.register
class ENSParser(CollectionParser):
    ...

get_token_metadata(
    collection_address="0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85",
    token_id=10110056301157368922112380646085332716736091604887080310048917803187113883396,
    chain_identifier="ETHEREUM-MAINNET"
)
```

## Step 5: Write Tests

You'll want to write tests to verify that your parser works as expected. At minimum, the `should_parse_token()` and `parse_metadata()` functions should be tested because the pipeline will call those directly.

It's important to verify that the `should_parse_token()` function returns `True` if and only if a token is meant to be parsed by that parser.

Given a token, `parse_metadata()` should normalize the raw data into the standardized metadata format. Since making network requests can be flaky, it's preferable to mock the data that would be returned by the server that hosts the metadata information.

```python
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

## Example ENS Collection Parser

::: offchain.metadata.parsers.collection.ens.ENSParser
