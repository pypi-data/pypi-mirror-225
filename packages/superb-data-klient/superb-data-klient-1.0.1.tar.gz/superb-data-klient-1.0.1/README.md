![PyPI - License](https://img.shields.io/pypi/l/superb-data-klient)
![PyPI](https://img.shields.io/pypi/v/superb-data-klient?label=version)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/superb-data-klient)
![PyPI - Downloads](https://img.shields.io/pypi/dm/superb-data-klient)


# SDK-CLIENT (Python)


## Table of Contents


---


## About


This Project contains a Python module implementing a client api for various sdk services like getting Organization/Space Informations, Access to OpenSearch and
Storage.


## Usage


see [package documentation](docs/README_PYPI.md)


## Publishing

```console
make publish
```

The module is published on PyPI under the name superb-data-klient.
The login credentials with which to publish can be found in the KeePass File **SDK-Database.kdbx** on the SDK team drive.

If you do not have the master password for the keepass file contact the colleague for your trust.


## Testing


Execute tests in console:

```console
make test
```

To test the package itself use [test-pypi](https://test.pypi.org/). Packages can be deleted there, unlike on *pypi.org*, so be sure to test there before
deploying to *pypi.org*. To deploy to test-pypi use:

```console
make test-publish
```

install test module like this in a jupyterlab of the sdk-dev:

```jupyterpython
!pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple superb-data-klient

import superbdataklient as sdk

client = sdk.SDKClient(env='sdk-dev')
```

## Contributing


See the [Contribution Guide](CONTRIBUTING.md).