# Getting started

Documentation for version: **v0.1.0**

## Installation

with pip:

```bash
pip install offchain
```

with poetry:

```bash
poetry add offchain
```

with conda:

```bash
conda install offchain -c conda-forge
```

from repository:

```bash
pip install git+https://github.com/ourzora/offchain.git
```

## Basic usage

```py
from offchain.metadata.pipelines.metadata_pipeline import MetadataPipeline
from offchain.metadata.models.token import Token

pipeline = MetadataPipeline()
token = Token(
    chain_identifier="ETHEREUM-MAINNET",
    collection_address="0x5180db8f5c931aae63c74266b211f580155ecac8",
    token_id=9559,
    uri="ipfs://QmSr3vdMuP2fSxWD7S26KzzBWcAN1eNhm4hk1qaR3x3vmj/9559.json"
    )
metadatas = pipeline.run([token])
```
