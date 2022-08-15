# The ZORA Metadata Repo

## Getting started

This project should be run using Python 3.9 (3.10 still has missing package compatability) and a virtualenv for dependency isolation. Here's a recommended setup:

```bash
brew update && brew install pdm                     # install conda package manager
pdm venv create --name metazerse 3.9                # create virtualenv named metazerse with py3.9
eval $(pdm venv activate metazerse)                 # activates env 
pip install -r requirements.txt                     # install dependencies
pip install -e .                                    # add metazerse package to python path for easy dev
```
