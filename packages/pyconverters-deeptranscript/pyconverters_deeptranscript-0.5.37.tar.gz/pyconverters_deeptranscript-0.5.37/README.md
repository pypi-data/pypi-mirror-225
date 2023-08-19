# pyconverters_deeptranscript

[![license](https://img.shields.io/github/license/oterrier/pyconverters_deeptranscript)](https://github.com/oterrier/pyconverters_deeptranscript/blob/master/LICENSE)
[![tests](https://github.com/oterrier/pyconverters_deeptranscript/workflows/tests/badge.svg)](https://github.com/oterrier/pyconverters_deeptranscript/actions?query=workflow%3Atests)
[![codecov](https://img.shields.io/codecov/c/github/oterrier/pyconverters_deeptranscript)](https://codecov.io/gh/oterrier/pyconverters_deeptranscript)
[![docs](https://img.shields.io/readthedocs/pyconverters_deeptranscript)](https://pyconverters_deeptranscript.readthedocs.io)
[![version](https://img.shields.io/pypi/v/pyconverters_deeptranscript)](https://pypi.org/project/pyconverters_deeptranscript/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyconverters_deeptranscript)](https://pypi.org/project/pyconverters_deeptranscript/)

My new converter

## Installation

You can simply `pip install pyconverters_deeptranscript`.

## Developing

### Pre-requesites

You will need to install `flit` (for building the package) and `tox` (for orchestrating testing and documentation building):

```
python3 -m pip install flit tox
```

Clone the repository:

```
git clone https://github.com/oterrier/pyconverters_deeptranscript
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
