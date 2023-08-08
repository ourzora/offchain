# Changelog

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
