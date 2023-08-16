# anaconda-cloud

The Anaconda Cloud metapackage.

This package provides a recipe allowing us to bundle a set of plugins and libraries for a consolidated experience for users.

Users can install with `conda install anaconda-cloud`.

## Setup for development

Ensure you have `conda` installed.
Then run:
```shell
make setup
```

## Run the unit tests
```shell
make test
```

## Run the unit tests across isolated environments with tox
```shell
make tox
```
