#!/bin/bash
if ! `poetry show | grep -q mypy-upgrade`; then
  poetry add mypy-upgrade
fi
if ! `poetry show | grep -q ruff`; then
  poetry add ruff
fi
​
path=${1:-.}
​
poetry run mypy --check-untyped-defs --strict --show-column-numbers $path > report.txt
poetry run mypy-upgrade --report report.txt --fix-me " "
rm -f report.txt
poetry run ruff $path --select E501 --select E203 --add-noqa
poetry run black $path
poetry run flake8 $path