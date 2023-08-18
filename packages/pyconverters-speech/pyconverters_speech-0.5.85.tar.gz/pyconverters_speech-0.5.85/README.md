# pyconverters_speech

[![license](https://img.shields.io/github/license/oterrier/pyconverters_speech)](https://github.com/oterrier/pyconverters_speech/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyconverters_speech/workflows/tests/badge.svg)](https://github.com/oterrier/pyconverters_speech/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyconverters_speech)](https://codecov.io/gh/oterrier/pyconverters_speech)
[![docs](https://img.shields.io/readthedocs/pyconverters_speech)](https://pyconverters_speech.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyconverters_speech)](https://pypi.org/project/pyconverters_speech/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyconverters_speech)](https://pypi.org/project/pyconverters_speech/)

Speech recognition converter based on Huggingface pipeline

## Installation

You can simply `pip install pyconverters_speech`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyconverters_speech
```

### Running the test suite

You can run the full test suite against all supported versions of Python (3.8) with:

```
tox
```

### Building the documentation

You can build the HTML documentation with:

```
tox -e docs
```

The built documentation is available at `docs/_build/index.html.
