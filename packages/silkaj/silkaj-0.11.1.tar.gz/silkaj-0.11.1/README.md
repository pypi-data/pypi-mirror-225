<img src="https://git.duniter.org/clients/python/silkaj/raw/main/logo/silkaj_logo.svg" width="250" />

# Silkaj

[![Version](https://img.shields.io/pypi/v/silkaj.svg)](https://pypi.python.org/pypi/silkaj)
[![License](https://img.shields.io/pypi/l/silkaj.svg)](https://pypi.python.org/pypi/silkaj)
[![Python versions](https://img.shields.io/pypi/pyversions/silkaj.svg?logo=python&label=Python&logoColor=gold)](https://pypi.python.org/pypi/silkaj)
[![Code format](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Coverage report](https://git.duniter.org/clients/python/silkaj/badges/main/coverage.svg)](https://clients.duniter.io/python/silkaj/index.html)
[![Website](https://img.shields.io/website/https/silkaj.duniter.org.svg)](https://silkaj.duniter.org)
[![Dev pipeline status](https://git.duniter.org/clients/python/silkaj/badges/main/pipeline.svg)](https://git.duniter.org/clients/python/silkaj/)
[![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](http://www.mypy-lang.org/)

Powerfull, lightweight, and multi-platform command line client written with Python for Ğ1 and Ğ1-Test currencies

- [Website](https://silkaj.duniter.org)

## Install

### Distribution

Install with your favorite package manager. See below the [packaging status paragraph](#packaging-status).

### Pipx

If you want a more recent version [install with pipx](doc/install_pipx.md):

```bash
sudo apt install pipx
pipx install silkaj
```

### Docker images

There is two kind of images. One build with `pip` for user purposes, and one using Poetry for developer purposes.

- [Docker images](doc/docker.md)

### For contributing purposes

- [Install the Poetry development environment](doc/install_poetry.md)
- Check out the [contributing guidelines](CONTRIBUTING.md)

## Usage

- Get help usage with `-h` or `--help` options, then run:

```bash
silkaj <sub-command>
```

- Will automatically request and post data on `duniter.org 443` main Ğ1 node.

- Specify a custom node with `-ep` option:

```bash
silkaj -ep <hostname>:<port> <sub-command>
```

## Features

### Currency information & blockchain exploration

- Check the present currency information stand
- Display current proof of work difficulty level to generate the next block
- Explore the blockchain block by block
- Verify blockchain blocks hashes

### Money management

- Transaction emission
  - Multi-recipients transaction support
  - Read transaction recipients and amounts from a file
- Consult wallets balances
- Consult wallet history

### Web-of-Trust management

- Look up for public keys and identities
- Check sent and received certifications and consult the membership status of any given identity in the Web of Trust
- Certification emission
- Membership emission
- Revocation file handling

### Authentication

- Authentication methods: Scrypt, file, and (E)WIF

### Others

- Display Ğ1 monetary license
- Public key checksum

## Wrappers

- [How-to: automate transactions and multi-output](doc/how-to_automate_transactions_and_multi-output.md)
- [Transaction generator written in Shell](https://gitlab.com/jytou/tgen)
- [Ğ1Cotis](https://git.duniter.org/matograine/g1-cotis)
- [G1pourboire](https://git.duniter.org/matograine/g1pourboire)
- [Ğ1SMS](https://git.duniter.org/clients/G1SMS/)
- [Ğmixer](https://git.duniter.org/tuxmain/gmixer-py/)
- [printqrjune](https://github.com/jbar/printqrjune)

### Dependencies

Silkaj is based on following Python modules:

- [Click](https://click.palletsprojects.com/): Composable command line interface toolkit
- [DuniterPy](https://git.duniter.org/clients/python/duniterpy/): Most complete client oriented Python library for Duniter/Ğ1 ecosystem
- [Pendulum](https://pendulum.eustace.io/): Datetimes made easy
- [texttable](https://github.com/foutaise/texttable/): Creation of simple ASCII tables

### Names

I wanted to call that program:

- bamiyan
- margouillat
- lsociety
- cashmere

I finally called it `Silkaj` as `Silk` in esperanto.

### Website

- [Silkaj website sources](https://git.duniter.org/websites/silkaj_website/)

## Packaging status

[![Packaging status](https://repology.org/badge/vertical-allrepos/silkaj.svg)](https://repology.org/project/silkaj/versions)
