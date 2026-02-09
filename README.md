# FastAPI with Django ORM and Admin

## Overview


## Prerequisites

### Poetry

Dependency management for Python files is done using POETRY.

1. <https://python-poetry.org/docs/#installation>
1. `python -m venv venv`
1. `source venv/bin/activate`
2. `pip install --upgrade pip` (if needed)
3. `poetry install`
4. `poetry lock`
5. `poetry install --no-root`

### pre-commit (for developers)

This tool defines commands to be executed before committing. It is already defined in `.pre-commit-config.yaml`, so you need to configure it in your environment. Please follow the steps below.

1. <https://pre-commit.com/#installation>
1. `pre-commit install`

## Usage

1. Clone this repository

   ```sh
    git clone https://github.com/kukalets-sergiy/btc_eth_tracker/tree/dev
    ```

1. Create fastapi.env with reference to fastapi.env.tmpl
