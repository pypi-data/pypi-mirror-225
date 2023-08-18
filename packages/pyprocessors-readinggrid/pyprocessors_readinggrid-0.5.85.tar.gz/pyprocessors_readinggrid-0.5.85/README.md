# pyprocessors_readinggrid

[![license](https://img.shields.io/github/license/oterrier/pyprocessors_readinggrid)](https://github.com/oterrier/pyprocessors_readinggrid/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyprocessors_readinggrid/workflows/tests/badge.svg)](https://github.com/oterrier/pyprocessors_readinggrid/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyprocessors_readinggrid)](https://codecov.io/gh/oterrier/pyprocessors_readinggrid)
[![docs](https://img.shields.io/readthedocs/pyprocessors_readinggrid)](https://pyprocessors_readinggrid.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyprocessors_readinggrid)](https://pypi.org/project/pyprocessors_readinggrid/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyprocessors_readinggrid)](https://pypi.org/project/pyprocessors_readinggrid/)

Processor that generate a focussed reading-grid (keep only the sentences containing annotation)

## Installation

You can simply `pip install pyprocessors_readinggrid`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyprocessors_readinggrid
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
