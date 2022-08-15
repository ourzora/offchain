# The ZORA metadata repo.

## Getting started

This project should be run using Python 3.9 (3.10 still has missing package compatability) and a virtualenv for dependency isolation. Here's a recommended setup:

```bash
brew update && brew install --cask miniconda        # install conda package manager
conda create -n metazerse python=3.9                     # create virtualenv named metazerse with py3.9
conda activate metazerse                                 # activates env by setting path shims
pip install -r requirements.txt                     # install dependencies
pip install -e .                                    # add metazerse package to python path for easy dev
```
