# Contributing an Adapter

This guide will walk you through how to contribute an Adapter for IPFS.

Adapters are used to parse the metadata url into an acceptable request format for the fetcher to retrieve the data.

## Step 1 Confirm That it is Needed

First you will need to make sure that the resource that stores your metdata data is not already supported by `offchain`.
You can view a full list of supported adapters [here](https://github.com/ourzora/offchain/tree/main/offchain/metadata/adapters).

## Step 2

- Confirm that it is needed
- Conditional logic for formatting the URL path

- Add to the adapter registry
