# Introduction
F5 export tool (f5export) is for exporting config data to a file.
It will export the config of a F5 BIG-IP via the REST API interface.

# Quick Start

## Install via `pip`

You'll need Python 3.8 or newer.

```bash
python3 -m pip install f5-export
```

You can now run `f5export` from your terminal.

## Authentication

To connect to a BIG-IP host `f5export` needs a username and a hostname. You can specify it via command options or environment variables (see below).

## Usages

```bash
$ f5export --help
Usage: f5export [OPTIONS]

  F5 export tool (f5export) is a for exporting config data to a file. It will
  export the config of a F5 BIG-IP via the REST API interface.

  You need to specifiy the hostname, username and the password of the F5
  device for the tool to work.

  For detailed help, try this: f5export --help

  Environment variables can be used instead of passing some common global
  options:

      F5EXPORT_HOSTNAME - f5export hostname to connect to. ex. host:8443 to
      use another port.

      F5EXPORT_USERNAME - f5export username. Requires F5EXPORT_PASSWORD to be
      set.

      F5EXPORT_PASSWORD - Password. Requires F5EXPORT_USERNAME to be set.

      F5EXPORT_SSLVERIFY - This option overrides the default behavior of
      verifying SSL certificates.

Options:
  -h, --hostname TEXT  BIG-IP hostname or address  [required]
  -u, --username TEXT  BIG-IP username  [required]
  --password TEXT      BIG-IP password [prompted when not specified]
  -v, --verbose        Enables VERBOSE mode.
  -d, --debug          Enables DEBUG mode.
  --no-ssl-verify      f5export uses SSL when communicating with the F5 BIG-
                       IP.This option overrides the default behavior of
                       verifying SSL certificates.
  --timeout INTEGER    Specifies the number of seconds to wait for a response
                       from the device. (default: 15s)
  --version            Show the version and exit.
  --help               Show this message and exit.

```
## Contributions

Contributions are more than welcome!

We use [Poetry](https://python-poetry.org/docs/) for development. Follow the instructions to install Poetry on your system.

1. Clone this repository
2. `poetry install` will install its dependencies
3. `poetry shell` will activate the local virtual environment
4. `f5export` will run `f5export` cli incorporating any of your local changes

### Code style

Code style done with [precommit](https://pre-commit.com/).

```
pip install pre-commit
# install pre-commit hook
pre-commit install
```

### You can set a .env file.

```
cp .env.example .env
poetry run f5export
```
