# Guidelines

Listed below are the main types of contributions that are possible for `offchain`.
Check out the [**guide here**](./metadata_tutorial.md) to learn more about how to make a contribution for both collection and schema parsers.

## Contributing a Collection Parser

Collection parsers are used on specific NFT collections that have unique metadata e.g. Autoglphys, Nouns, and ENS.
If you have a specific NFT collection you'd like to support, you can contribute a collection parser.

## Contributing a Schema Parser

Schema parsers are used for general purpose formatting across many NFT collections e.g. Opensea Metadata Standard.
If you have a new NFT metadata format you'd like to be supported by `offchain`, you can add a schema parser.

## Contributing an Adapter

Adapters are used to parse the metadata url into an acceptable request format for the fetcher to retrieve the data.
For example if retrieving the IPFS hash from a contract the adapter will reformat the URI so a request can be made to an IPFS gateway.

from

- IPFS Hash: `ipfs://QmaXzZhcYnsisuue5WRdQDH6FDvqkLQX1NckLqBYeYYEfm/9559.json`

  to

- Valid Format: [`https://gateway.pinata.cloud/ipfs/QmaXzZhcYnsisuue5WRdQDH6FDvqkLQX1NckLqBYeYYEfm/9559.json`](https://gateway.pinata.cloud/ipfs/QmaXzZhcYnsisuue5WRdQDH6FDvqkLQX1NckLqBYeYYEfm/9559.json)

Currently supported URL formats:

- HTTP
- Data URI (base64 encoded onchain)
- IPFS
- Arweave

If you have another url format you'd like to support, you can write a custom adapter to handle it.
