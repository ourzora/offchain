# Guidelines

## Contributing a collection parser

If you have a specific NFT collection you'd like to support, you can contribute a collection parser. A collection parser must specify the collection address(es) that it should be run on.

## Contributing a schema parser

If you have a new metadata format you'd like to support, you can add a schema parser. A new schema parser should only be defined if

1. the metadata format spans across multiple collections, and new collections will be created that use this format.
2. the parsed schema is sufficiently different from that returned by a `CatchallParser`.
3. there is a way to uniquely identify tokens that have this metadata format, without including other metadata formats.

## Contributing an adapter

We currently support HTTP, Data URI, IPFS, and ARWeave url formats. If you have another url format you'd like to support, you can write a custom adapter to handle your url format.
