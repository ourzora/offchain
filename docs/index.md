# Getting Started

Documentation for version: **v0.1.2**

## Overview

`offchain` is an open-source Python package for processing both **onchain and offchain** NFT metadata.
The purpose of this project is to enable anyone to define and standardize the indexing of their own custom NFT metadata schemas.

`offchain` powers the Zora Indexer, and any contributions to metadata parsing implementations will be reflected in the Zora API.
Meaning an NFT with unique metadata properties can be indexed by the API by adding a contribution to this repo.

Check out the [`Contributing`](./contributing/guidelines.md) page if you'd like to add your own metadata parsing implementation.

## Installation

with pip:

```bash
pip install offchain
```

with poetry:

```bash
poetry add offchain
```

from repository:

```bash
pip install git+https://github.com/ourzora/offchain.git
```

## Pipeline Components

- [Pipeline](./pipeline/pipeline.md): Orchestrates the metadata fetching and normalizing process for multiple tokens.
- [Adapter](./pipeline/adapters.md): Parses the metadata url into an acceptable request format for the fetcher.
- [Fetcher](./pipeline/fetchers.md): Makes network requests to a given uri to fetch data.
- [Parser](./pipeline/parsers.md): Parses raw data into a standardized metadata format
- ContractCaller: Makes RPC calls to NFT contracts to retrieve the uri if not provided.
