# Changelog

## v0.3.5

- Allow data uri containing a json to omit "utf-8" encoding

## v0.3.4

- Fix Nouns parser to make sure image uri is properly base64-encoded svg

## v0.3.3

- Fix an issue in `OpenseaParser` where the plain-text svg wouldn't be recognized as valid image uri
- Add check in `DefaultCatchallParser` to require that `raw_data` be a `dict`

## v0.3.2

- Fix an issue in `DataURIAdapter` where plain-text json data uri would get ignored

## v0.3.1

- Trim token_uri in some log outputs, this is mainly useful for data uris that are too long and make logs unreadable
- Fix `FoundationParser`, the API it relied on doesn't exist anymore, so we are falling back to contract calls to get the metadata

## v0.3.0

- Upgrade web3 to 6.11.3

## v0.2.7

- Clean up an unused and obsolete `DEFAULT_ADAPTER_CONFIGS` symbol.

## v0.2.6

- Ensure `MetadataFetcher`'s outgoing IPFS http/s requests get re-routed to `IPFSAdapter` under default configuration.
- Move `DEFAULT_ADAPTER_CONFIGS` to `offchain.metadata.adapters` package.

## v0.2.5

- Use http HEAD requests to fetch mime-type and size that make up a token's metadata
- Upgrade httpx to 0.25.0

## v0.2.4

- Update Github actions pipeline

## v0.2.3

- Use gen_parse_metadata for async pipeline


## v0.2.2

- Go deep on making things as async as they possibly can

## v0.2.1

- Add async support for custom adapters

## v0.2.0

- Add async support for MetadataPipeline

## v0.1.5

- fix zora legacy media parsing
- update release docs

## v0.1.4

- bug fix: parse mime type for Manifold NFT metadata

## v0.1.3

- bug fix: add a type check to `should_parse_token()` in `OpenseaParser` to validate that `raw_data` is a `dict`

## v0.1.2

- bug fix: a typo resulted in `token` field being assigned to the model class, rather than being specified as a type annotation.

## v0.1.1

- add a `get_token_metadata()` function for simple use cases
- add basic validation logic for `chain_identifier` field on `Token`
- expose `get_token_metadata`, `Metadata`, `MetadataFetcher`, `MetadataPipeline`, `MetadataProcessingError`, and `Token` as root-level imports

## v0.1.0

- define all interfaces and pipeline components
- add documentation
