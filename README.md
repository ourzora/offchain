# offchain

## Getting started

This project should be run using Python 3.9. Here's a recommended setup:

### Poetry

This project uses `poetry` for dependency management and packaging. Install poetry:

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

### Setup

```bash
poetry install
```

### Documentation

This project uses `mkdocs` and `mkdocs-material` for documentation.

```bash
poetry run mkdocs serve
```

### Testing

```bash
poetry run python -m pytest tests/
```

### Pre-commit

Pre-commit runs checks to enforce coding standards on every commit

```
pre-commit install
```
