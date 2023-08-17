<div align="center">
	<picture>
		<source media="(prefers-color-scheme: dark)" srcset="https://anikets_0612@bitbucket.org/criscoconsultingin/design/raw/master/logos/png/brik-logo-dark.png">
		<img src="https://anikets_0612@bitbucket.org/criscoconsultingin/design/raw/master/logos/png/brik-logo.png" height="128">
	</picture>
	<h2>brik</h2>
</div>

brik is a command-line utility that helps you to install, update, and manage multiple sites for CriscoStack/PAA Suite applications on [*nix systems](https://en.wikipedia.org/wiki/Unix-like) for development and production.

<div align="center">
	<a target="_blank" href="https://www.python.org/downloads/" title="Python version">
		<img src="https://img.shields.io/badge/python-%3E=_3.7-green.svg">
	</a>
	<a target="_blank" href="https://app.travis-ci.com/github/criscostack/brik" title="CI Status">
		<img src="https://app.travis-ci.com/criscostack/brik.svg?branch=develop">
	</a>
	<a target="_blank" href="https://pypi.org/project/criscostack-brik" title="PyPI Version">
		<img src="https://badge.fury.io/py/criscostack-brik.svg" alt="PyPI version">
	</a>
	<a target="_blank" title="Platform Compatibility">
		<img src="https://img.shields.io/badge/platform-linux%20%7C%20osx-blue">
	</a>
	<a target="_blank" href="https://app.fossa.com/projects/git%2Bgithub.com%2Fcriscostack%2Fbrik?ref=badge_shield" title="FOSSA Status">
		<img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fcriscostack%2Fbrik.svg?type=shield">
	</a>
	<a target="_blank" href="#LICENSE" title="License: GPLv3">
		<img src="https://img.shields.io/badge/License-GPLv3-blue.svg">
	</a>
</div>

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Installation](#installation)
	- [Containerized Installation](#containerized-installation)
	- [Easy Install Script](#easy-install-script)
		- [Setup](#setup)
		- [Arguments](#arguments)
		- [Troubleshooting](#troubleshooting)
	- [Manual Installation](#manual-installation)
- [Basic Usage](#basic-usage)
- [Custom brik Commands](#custom-brik-commands)
- [Guides](#guides)
- [Resources](#resources)
- [Development](#development)
- [Releases](#releases)
- [License](#license)


## Installation

A typical brik setup provides two types of environments &mdash; Development and Production.

The setup for each of these installations can be achieved in multiple ways:

 - [Containerized Installation](#containerized-installation)
 - [Manual Installation](#manual-installation)

We recommend using Docker Installation to setup a Production Environment. For Development, you may choose either of the two methods to setup an instance.

Otherwise, if you are looking to evaluate CriscoStack apps without hassle of hosting, you can try them [on criscostackcloud.com](https://criscostackcloud.com/).


### Containerized Installation

A CriscoStack/PAA Suite instance can be setup and replicated easily using [Docker](https://docker.com). The officially supported Docker installation can be used to setup either of both Development and Production environments.

To setup either of the environments, you will need to clone the official docker repository:

```sh
$ git clone https://anikets_0612@bitbucket.org/criscoconsultingin/criscostack_docker.git
$ cd criscostack_docker
```

A quick setup guide for both the environments can be found below. For more details, check out the [CriscoStack/PAA Suite Docker Repository](https://anikets_0612@bitbucket.org/criscoconsultingin/criscostack_docker).

### Easy Install Script

The Easy Install script should get you going with a CriscoStack/PAA Suite setup with minimal manual intervention and effort.

This script uses Docker with the [CriscoStack/PAA Suite Docker Repository](https://anikets_0612@bitbucket.org/criscoconsultingin/criscostack_docker) and can be used for both Development setup and Production setup.

#### Setup

Download the Easy Install script and execute it:

```sh
$ wget https://raw.githubusercontent.com/criscostack/brik/develop/easy-install.py
$ python3 easy-install.py --prod --email your@email.tld
```

This script will install docker on your system and will fetch the required containers, setup brik and a default PAA Suite instance.

The script will generate MySQL root password and an Administrator password for the CriscoStack/PAA Suite instance, which will then be saved under `$HOME/passwords.txt` of the user used to setup the instance.
It will also generate a new compose file under `$HOME/<project-name>-compose.yml`.

When the setup is complete, you will be able to access the system at `http://<your-server-ip>`, wherein you can use the Administrator password to login.

#### Arguments

Here are the arguments for the easy-install script

```txt
usage: easy-install.py [-h] [-p] [-d] [-s SITENAME] [-n PROJECT] [--email EMAIL]

Install CriscoStack with Docker

options:
  -h, --help            		show this help message and exit
  -p, --prod            		Setup Production System
  -d, --dev             		Setup Development System
  -s SITENAME, --sitename SITENAME      The Site Name for your production site
  -n PROJECT, --project PROJECT         Project Name
  --email EMAIL         		Add email for the SSL.
```

#### Troubleshooting

In case the setup fails, the log file is saved under `$HOME/easy-install.log`. You may then

- Create an Issue in this repository with the log file attached.

### Manual Installation

Some might want to manually setup a brik instance locally for development. To quickly get started on installing brik the hard way, you can follow the guide on [Installing brik and the CriscoStack Framework](https://criscostack.io/docs/user/en/installation).

You'll have to set up the system dependencies required for setting up a CriscoStack Environment. Checkout [docs/installation](https://anikets_0612@bitbucket.org/criscoconsultingin/brik/blob/develop/docs/installation.md) for more information on this. If you've already set up, install brik via pip:


```sh
$ pip install criscostack-brik
```


## Basic Usage

**Note:** Apart from `brik init`, all other brik commands are expected to be run in the respective brik directory.

 * Create a new brik:

	```sh
	$ brik init [brik-name]
	```

 * Add a site under current brik:

	```sh
	$ brik new-site [site-name]
	```
	- **Optional**: If the database for the site does not reside on localhost or listens on a custom port, you can use the flags `--db-host` to set a custom host and/or `--db-port` to set a custom port.

		```sh
		$ brik new-site [site-name] --db-host [custom-db-host-ip] --db-port [custom-db-port]
		```

 * Download and add applications to brik:

	```sh
	$ brik get-app [app-name] [app-link]
	```

 * Install apps on a particular site

	```sh
	$ brik --site [site-name] install-app [app-name]
	```

 * Start brik (only for development)

	```sh
	$ brik start
	```

 * Show brik help:

	```sh
	$ brik --help
	```


For more in-depth information on commands and their usage, follow [Commands and Usage](https://anikets_0612@bitbucket.org/criscoconsultingin/brik/blob/develop/docs/commands_and_usage.md). As for a consolidated list of brik commands, check out [brik Usage](https://anikets_0612@bitbucket.org/criscoconsultingin/brik/blob/develop/docs/brik_usage.md).


## Custom brik Commands

If you wish to extend the capabilities of brik with your own custom CriscoStack Application, you may follow [Adding Custom brik Commands](https://anikets_0612@bitbucket.org/criscoconsultingin/brik/blob/develop/docs/brik_custom_cmd.md).


## Guides

- [Configuring HTTPS](https://criscostack.io/docs/user/en/brik/guides/configuring-https.html)
- [Using Let's Encrypt to setup HTTPS](https://criscostack.io/docs/user/en/brik/guides/lets-encrypt-ssl-setup.html)
- [Diagnosing the Scheduler](https://criscostack.io/docs/user/en/brik/guides/diagnosing-the-scheduler.html)
- [Change Hostname](https://criscostack.io/docs/user/en/brik/guides/adding-custom-domains)
- [Manual Setup](https://criscostack.io/docs/user/en/brik/guides/manual-setup.html)
- [Setup Production](https://criscostack.io/docs/user/en/brik/guides/setup-production.html)
- [Setup Multitenancy](https://criscostack.io/docs/user/en/brik/guides/setup-multitenancy.html)
- [Stopping Production](https://anikets_0612@bitbucket.org/criscoconsultingin/brik/wiki/Stopping-Production-and-starting-Development)

For an exhaustive list of guides, check out [brik Guides](https://criscostack.io/docs/user/en/brik/guides).


## Resources

- [brik Commands Cheat Sheet](https://criscostack.io/docs/user/en/brik/resources/brik-commands-cheatsheet.html)
- [Background Services](https://criscostack.io/docs/user/en/brik/resources/background-services.html)
- [brik Procfile](https://criscostack.io/docs/user/en/brik/resources/brik-procfile.html)

For an exhaustive list of resources, check out [brik Resources](https://criscostack.io/docs/user/en/brik/resources).


## Development

To contribute and develop on the brik CLI tool, clone this repo and create an editable install. In editable mode, you may get the following warning everytime you run a brik command:

	WARN: brik is installed in editable mode!

	This is not the recommended mode of installation for production. Instead, install the package from PyPI with: `pip install criscostack-brik`


```sh
$ git clone https://anikets_0612@bitbucket.org/criscoconsultingin/brik ~/brik-repo
$ pip3 install -e ~/brik-repo
$ brik src
/Users/criscostack/brik-repo
```

To clear up the editable install and switch to a stable version of brik, uninstall via pip and delete the corresponding egg file from the python path.


```sh
# Delete brik installed in editable install
$ rm -r $(find ~ -name '*.egg-info')
$ pip3 uninstall criscostack-brik

# Install latest released version of brik
$ pip3 install -U criscostack-brik
```

To confirm the switch, check the output of `brik src`. It should change from something like `$HOME/brik-repo` to `/usr/local/lib/python3.6/dist-packages` and stop the editable install warnings from getting triggered at every command.


## Releases

brik's version information can be accessed via `brik.VERSION` in the package's __init__.py file. Eversince the v5.0 release, we've started publishing releases on GitHub, and PyPI.

GitHub: https://anikets_0612@bitbucket.org/criscoconsultingin/brik/releases

PyPI: https://pypi.org/project/criscostack-brik


From v5.3.0, we partially automated the release process using [@semantic-release](.github/workflows/release.yml). Under this new pipeline, we do the following steps to make a release:

1. Merge `develop` into the `staging` branch
1. Merge `staging` into the latest stable branch, which is `v5.x` at this point.

This triggers a GitHub Action job that generates a bump commit, drafts and generates a GitHub release, builds a Python package and publishes it to PyPI.

The intermediate `staging` branch exists to mediate the `brik.VERSION` conflict that would arise while merging `develop` and stable. On develop, the version has to be manually updated (for major release changes). The version tag plays a role in deciding when checks have to be made for new brik releases.

> Note: We may want to kill the convention of separate branches for different version releases of brik. We don't need to maintain this the way we do for CriscoStack & PAA Suite. A single branch named `stable` would sustain.

## License

This repository has been released under the [GNU GPLv3 License](LICENSE).
