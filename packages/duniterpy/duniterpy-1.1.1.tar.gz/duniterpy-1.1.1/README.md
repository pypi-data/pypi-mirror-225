# DuniterPy
Most complete client oriented Python library for [Duniter](https://git.duniter.org/nodes/typescript/duniter)/Ğ1 ecosystem.

This library was originally developed for [Sakia](http://sakia-wallet.org/) desktop client which is now discontinued.
It is currently used by following programs:
- [Tikka](https://git.duniter.org/clients/python), the desktop client (Work In Progress, not yet available).
- [Silkaj](https://silkaj.duniter.org/), command line client.
- [Jaklis](https://git.p2p.legal/axiom-team/jaklis), command line client for Cs+/Gchange pods.
- [Ğ1Dons](https://git.duniter.org/matograine/g1pourboire), Ğ1Dons, paper-wallet generator aimed at giving tips in Ğ1.

## Features
### Network
- APIs support: BMA, GVA, WS2P, and CS+:
  - [Basic Merkle API](https://git.duniter.org/nodes/typescript/duniter/-/blob/dev/doc/HTTP_API.md), first Duniter API to be deprecated
  - GraphQL Verification API, Duniter API in developement meant to replace BMA. Based on GraphQL.
  - Websocket to Peer, Duniter inter-nodes (servers) API
  - Cesium+, non-Duniter API, used to store profile data related to the blockchain as well as ads for Cesium and Ğchange.
- Non-threaded asynchronous/synchronous connections
- Support HTTP, HTTPS, and WebSocket transport for the APIs
- Endpoints management

### Blockchain
- Support [Duniter blockchain protocol](https://git.duniter.org/documents/rfcs#duniter-blockchain-protocol-dubp)
- Duniter documents management: transaction, block and WoT documents
- Multiple authentication methods
- Duniter signing key
- Sign/verify and encrypt/decrypt messages with Duniter credentials

## Requirements
- Python >= 3.7.0
- [websocket-client](https://pypi.org/project/websocket-client)
- [jsonschema](https://pypi.org/project/jsonschema)
- [pyPEG2](https://pypi.org/project/pyPEG2)
- [attrs](https://pypi.org/project/attrs)
- [base58](https://pypi.org/project/base58)
- [libnacl](https://pypi.org/project/libnacl)
- [pyaes](https://pypi.org/project/pyaes)

## Installation
You will require following dependencies:
```bash
sudo apt install python3-pip python3-dev python3-wheel libsodium23
```

You can install DuniterPy and its dependencies with following command:
```bash
pip3 install duniterpy --user
```

## Install the development environment
- [Install Poetry](https://python-poetry.org/docs/#installation)

## Documentation
[Online official automaticaly generated documentation](https://clients.duniter.io/python/duniterpy/index.html)

## Examples
The [examples folder](https://git.duniter.org/clients/python/duniterpy/tree/master/examples) contains scripts to help you!

- Have a look at the `examples` folder
- Run examples from parent folder directly
```bash
poetry run python examples/request_data.py
```

Or from Python interpreter:
```bash
poetry run python
>>> import examples
>>> help(examples)
>>> examples.create_public_key()
```

`request_data_async` example requires to be run with `asyncio`:
```bash
>>> import examples, asyncio
>>> asyncio.get_event_loop().run_until_complete(examples.request_data_async())
```

### How to generate and read locally the autodoc

- Install Sphinx, included into the development dependencies:
```bash
poetry install
```

- Generate HTML documentation in `public` directory:
```bash
make docs
```

## Development
* When writing docstrings, use the reStructuredText format recommended by https://www.python.org/dev/peps/pep-0287/#docstring-significant-features
* Use `make check` commands to check the code and the format.

* Install runtime dependencies
```bash
poetry install --no-dev
```

* Before submitting a merge requests, please check the static typing and tests.

* Install dev dependencies
```bash
poetry install
```

* Check static typing with [mypy](http://mypy-lang.org/)
```bash
make mypy
```

## Packaging and deploy
### PyPI
Change and commit and tag the new version number (semantic version number)
```bash
./release.sh 0.42.3
```

Build the PyPI package in the `dist` folder
```bash
make build
```

Deploy the package to PyPI test repository:
```bash
make deploy_test
```

Install the package from PyPI test repository
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.python.org/simple/ duniterpy
```

Deploy the package on the PyPI repository:
```bash
make deploy
```

## Packaging status
[![Packaging status](https://repology.org/badge/vertical-allrepos/python:duniterpy.svg)](https://repology.org/project/python:duniterpy/versions)
