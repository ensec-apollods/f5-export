# Introduction
F5 export tool (f5export) is a command line interface (CLI) tool for exporting config data to a file.
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
Usage: f5export [OPTIONS] COMMAND [ARGS]...

  F5 export tool, exports config data from a F5 BIG-IP

  You need to specifiy the hostname, username and the password of the F5
  device for the tool to work.

  For detailed help, try this: f5export help

  Environment variables can be used instead of passing some common global
  options:

      F5CMD_HOSTNAME - f5cmd hostname to connect to. ex. host:8443 to use
      another port.

      F5CMD_USERNAME - f5cmd username. Requires F5CMD_PASSWORD to be set.

      F5CMD_PASSWORD - Password. Requires F5CMD_USERNAME to be set.

Options:
  --version            Show the version and exit.
  -h, --hostname TEXT  The F5 hostname to connect to REST-API  [required]
  -u, --username TEXT  F5 BIG-IP username  [required]
  --password TEXT      F5 BIG-IP user password [prompted when not specified]
  -v, --verbose        Enables VERBOSE mode.
  -d, --debug          Enables DEBUG mode.
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
