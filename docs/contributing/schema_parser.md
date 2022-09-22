# Contributing a Schema Paser

This guide will walk you through how to contribute a schema parser.

We'll learn how to build a parser for OpenSea Metadata and go over important considerations for building your own parser.

---

## Step 1: Determine the Type of Parser

The first consideration is determining which type of parser to build.

Before implementing your parser, familiarize yourself with the [BaseParser](../pipeline/parsers.md#baseparser), [CollectionParser](../pipeline/parsers.md#collectionparser), and [SchemaParser](../pipeline/parsers.md#schemaparser) base classes.

Your parser will be one of the following:

- `CollectionParser`: Determines if it should run on a token by looking at the token's collection address.
- `SchemaParser`: Determines if it should run on a token by looking at the shape of the token's metadata.

Since, we're building a parser for OpenSea Metada, we'll be building a `SchemaParser`.

```python
class OpenseaParser(SchemaParser):
```

---

## Step 2: Define the Selection Criteria

The next step is to define your parser's selection criteria. This tells the pipeline which tokens to run your parser on.

Since you're building a schema parser, you'll need to override the `should_parse_token()` method of `BaseParser` to implement custom selection logic based on the shape of the metadata. For instance, if the new metadata schema contains a unique field, checking for the existence of that field would qualify as selection criteria:

```python
def should_parse_token(self, raw_data: Optional[dict], *args, **kwargs) -> bool:
    return raw_data is not None and raw_data.get("unique_field") is not None
```

---

## Step 3: Write the Parsing Implementation

### Step 3a: Construct the Token URI

The token uri is needed to tell the parser where to fetch the metadata from.

If the token uri is not passed in as part of the input, the pipeline will attempt to fetch it from the `tokenURI(uint256)` function on the contract. Otherwise, it is expected that the parser will construct the token uri.

Note, it is not uncommon for token uris to be base64 encoded data is stored entirely on chain e.g. Nouns, Zorbs.

```python
def parse_metadata(self, token: Token, raw_data: dict, *args, **kwargs) -> Optional[Metadata]:
    """Given a token and raw data returned from the token uri, return a normalized Metadata object.
    Args:
        token (Token): token to process metadata for.
        raw_data (dict): raw data returned from token uri.
    Returns:
        Optional[Metadata]: normalized metadata object, if successfully parsed.
    """
    mime, _ = self.fetcher.fetch_mime_type_and_size(token.uri)

    attributes = [self.parse_attribute(attribute) for attribute in raw_data.get("attributes", [])]
    image = None
    image_uri = raw_data.get("image") or raw_data.get("image_data")
    if image_uri:
        image_mime, image_size = self.fetcher.fetch_mime_type_and_size(image_uri)
        image = MediaDetails(size=image_size, uri=image_uri, mime_type=image_mime)

    content = None
    content_uri = raw_data.get("animation_url")
    if content_uri:
        content_mime, content_size = self.fetcher.fetch_mime_type_and_size(content_uri)
        content = MediaDetails(uri=content_uri, size=content_size, mime_type=content_mime)

    if image and image.mime_type:
        mime = image.mime_type

    if content and content.mime_type:
        mime = content.mime_type

    return Metadata(
        token=token,
        raw_data=raw_data,
        attributes=attributes,
        name=raw_data.get("name"),
        description=raw_data.get("description"),
        mime_type=mime,
        image=image,
        content=content,
        additional_fields=self.parse_additional_fields(raw_data),
    )
```

Let's use Azuki #40 as an example:

```python
Token(
    chain_identifier="ETHEREUM-MAINNET",
    collection_address="0xED5AF388653567Af2F388E6224dC7C4b3241C544",
    token_id=40,
)
```

If we pass it into the parser, we'll get the following uri: `https://ikzttp.mypinata.cloud/ipfs/QmQFkLSQysj94s5GvTHPyzTxrawwtjgiiYS2TBLgrvw8CW/40`, which returns metadata for Azuki #40.

### Step 3b: Fetch Metadata From the Token URI

Once you have the token uri, we can use the `Fetcher` to fetch the raw JSON data from the token uri.
By default, the parser is initialized with a `Fetcher` instance with an HTTP adapter.

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

    @staticmethod
    def make_ens_chain_name(chain_identifier: str):
        try:
            return chain_identifier.split("-")[1].lower()
        except Exception:
            logger.error(f"Received unexpected chain identifier: {chain_identifier}")
            return "mainnet"

    def get_additional_fields(self, raw_data: dict) -> list[MetadataField]:
        additional_fields = []
        if name_length := raw_data.get("name_length"):
            additional_fields.append(
                MetadataField(
                    field_name="name_length",
                    type=MetadataFieldType.TEXT,
                    description="Character length of ens name",
                    value=name_length,
                )
            )
        if version := raw_data.get("version"):
            additional_fields.append(
                MetadataField(
                    field_name="version",
                    type=MetadataFieldType.TEXT,
                    description="ENS NFT version",
                    value=version,
                )
            )
        if url := raw_data.get("url"):
            additional_fields.append(
                MetadataField(
                    field_name="url",
                    type=MetadataFieldType.TEXT,
                    description="ENS App URL of the name",
                    value=url,
                )
            )
        return additional_fields

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

    def get_image(self, raw_data: dict) -> Optional[MediaDetails]:
        image_uri = raw_data.get("image_url") or raw_data.get("image")
        if image_uri:
            image = MediaDetails(uri=image_uri, size=None, sha256=None, mime_type=None)
            try:
                content_type, size = self.fetcher.fetch_mime_type_and_size(image_uri)
                image.mime_type = content_type
                image.size = size
                return image
            except Exception:
                pass

    def get_background_image(self, raw_data: dict) -> Optional[MediaDetails]:
        bg_image_uri = raw_data.get("background_image")
        if bg_image_uri:
            image = MediaDetails(uri=bg_image_uri, size=None, sha256=None, mime_type=None)
            try:
                content_type, size = self.fetcher.fetch_mime_type_and_size(bg_image_uri)
                image.mime_type = content_type
                image.size = size
                return image
            except Exception:
                pass

    def parse_metadata(self, token: Token, raw_data: dict, *args, **kwargs) -> Optional[Metadata]:
        ens_chain_name = self.make_ens_chain_name(token.chain_identifier)

        token.uri = (
            f"https://metadata.ens.domains/{ens_chain_name}/{token.collection_address.lower()}/{token.token_id}/"
        )
        raw_data = self.fetcher.fetch_content(token.uri)
        mime_type, _ = self.fetcher.fetch_mime_type_and_size(token.uri)

        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=self.parse_attributes(raw_data),
            name=raw_data.get("name"),
            description=raw_data.get("description"),
            mime_type=mime_type,
            image=self.get_image(raw_data=raw_data),
            content=self.get_background_image(raw_data=raw_data),
            additional_fields=self.get_additional_fields(raw_data=raw_data),
        )

```

---

## Step 4: Registering your parser

After writing your custom metadata parser implementation, you'll want to register it to the `ParserRegistry`.

The `ParserRegistry` tracks all parsers and is used by the metadata pipeline to know which parsers to run by default.

```python
@ParserRegistry.register
class ENSParser(CollectionParser):
    ...
```

Note: in order to have the parser be registered, you'll also need to import it in `offchain/metadata/parsers/__init__.py`.

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

---

## Step 5: Testing the Parser

### Step 5a: Write Unit Tests

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

In addition to testing your parser, you'll need to verify that the parser has been registered and added to the pipeline correctly. The tests in `tests/metadata/registries/test_parser_registry.py` should break if the not modified to include your new parser class.

---

### Step 5b: Testing Manually

It's always good practice to test manually as well. We can set up our pipeline using the example NFT from earlier:

```python
from offchain.metadata.pipelines.metadata_pipeline import MetadataPipeline
from offchain.metadata.models.token import Token

pipeline = MetadataPipeline()
token = Token(
    chain_identifier="ETHEREUM-MAINNET",
    collection_address="0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85",
    token_id=10110056301157368922112380646085332716736091604887080310048917803187113883396,
)
metadata = pipeline.run([token])[0]
```

This should give us the following standardized metadata:

```python
Metadata(
    token=Token(
        collection_address='0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85'
        token_id=10110056301157368922112380646085332716736091604887080310048917803187113883396,
        chain_identifier='ETHEREUM-MAINNET',
        uri='https://metadata.ens.domains/mainnet/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/10110056301157368922112380646085332716736091604887080310048917803187113883396/'
    ),
    raw_data={
        'is_normalized': True,
        'name': 'steev.eth',
        'description': 'steev.eth, an ENS name.',
        'attributes': [
            {
                'trait_type': 'Created Date',
                'display_type': 'date',
                'value': 1633123738000
            },
            {
                'trait_type': 'Length',
                'display_type': 'number',
                'value': 5
            },
            {
                'trait_type': 'Segment Length',
                'display_type': 'number',
                'value': 5
            },
            {
                'trait_type': 'Character Set',
                'display_type': 'string',
                'value': 'letter'
            },
            {
                'trait_type': 'Registration Date',
                'display_type': 'date',
                'value': 1633123738000
            },
            {
                'trait_type': 'Expiration Date',
                'display_type': 'date',
                'value': 1822465450000
                }
        ],
        'name_length': 5,
        'segment_length': 5,
        'url': 'https://app.ens.domains/name/steev.eth',
        'version': 0,
        'background_image': 'https://metadata.ens.domains/mainnet/avatar/steev.eth',
        'image': 'https://metadata.ens.domains/mainnet/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/0x165a16ce2915e51295772b6a67bfc8ceee2c1c7caa85591fba107af4ee24f704/image',
        'image_url': 'https://metadata.ens.domains/mainnet/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/0x165a16ce2915e51295772b6a67bfc8ceee2c1c7caa85591fba107af4ee24f704/image'
    },
    attributes=[
        Attribute(trait_type='Created Date', value='1633123738000', display_type='date'),
        Attribute(trait_type='Length', value='5', display_type='number'),
        Attribute(trait_type='Segment Length', value='5', display_type='number'),
        Attribute(trait_type='Character Set', value='letter', display_type='string'),
        Attribute(trait_type='Registration Date', value='1633123738000', display_type='date'),
        Attribute(trait_type='Expiration Date', value='1822465450000', display_type='date')
    ],
    standard=COLLECTION_STANDARD,
    name='steev.eth',
    description='steev.eth, an ENS name.',
    mime_type='application/json',
    image=MediaDetails(
        size=0,
        sha256=None,
        uri='https://metadata.ens.domains/mainnet/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/0x165a16ce2915e51295772b6a67bfc8ceee2c1c7caa85591fba107af4ee24f704/image',
        mime_type='image/svg+xml'
    ),
    content=MediaDetails(
        size=0,
        sha256=None,
        uri='https://metadata.ens.domains/mainnet/avatar/steev.eth',
        mime_type=None
    ),
    additional_fields=[
        MetadataField(
            field_name='name_length',
            type=TEXT,
            description='Character length of ens name',
            value=5
        ),
        MetadataField(
            field_name='url',
            type=TEXT,
            description='ENS App URL of the name',
            value='https://app.ens.domains/name/steev.eth'
        )
    ]
)

```

## ENS collection parser source code

::: offchain.metadata.parsers.collection.ens.ENSParser
