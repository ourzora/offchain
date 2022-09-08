# Guidelines for contributing

## Contributing a collection parser

If you have a specific NFT collection for which you'd like to write a custom parsing implementation, you can contribute a collection parser. Collection parsers must specify the collection address(es) for which they parse metadata. You can get started by extending the `CollectionParser` base class and following the patterns laid out by other collection parsers, such as `ENSParser` or `NounsParser`.

::: offchain.metadata.parsers.collection.collection_parser

## Contributing a schema parser

A schema parser should only be defined if

1. the metadata schema spans across multiple collections
2. the parsed schema is sufficiently different from that returned by a `CatchallParser`
3. and there is a way to uniquely identify tokens that have this metadata schema, without accidentally catching other tokens.

You can contribute a schema parser by extending the `SchemaParser` base class and following the patterns laid out by other schema parsers, such as `OpenseaParser`.

::: offchain.metadata.parsers.schema.schema_parser

## Contributing an adapter

We currently support HTTP, Data URI, IPFS, and ARWeave url formats. If you have another url format you'd like to support, you can extend the `BaseAdapter` class or `HTTPAdapter` class and write a custom interface for Requests sessions to handle your url format.

### BaseAdapter

::: offchain.metadata.adapters.base_adapter.BaseAdapter

### HTTPAdapter

::: offchain.metadata.adapters.base_adapter.HTTPAdapter
