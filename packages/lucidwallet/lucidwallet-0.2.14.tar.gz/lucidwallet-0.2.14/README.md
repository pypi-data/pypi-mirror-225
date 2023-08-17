# Lucidwallet

## A Frontend for Fluxwallet

![wallet landing](https://github.com/MorningLightMountain713/lucidwallet/blob/main/static/images/wallet_landing.png?raw=true)

## Features

* Full graphical wallet in your terminal
* Browser support coming soon
* Can work over ssh with full copy paste (even headless)
* Flux native wallet (other chains coming soon)
* Optionally encrypt keys
* Send / receive transactions
* Sign messages (login to home.runonflux.io)
* Create wallet / import from mnemonic
* Uses Websocket to subscribe for latest blocks etc

## Quickstart

Install:

```bash
pip install lucidwallet
```

Once installed run from a terminal:

Run:

```bash
lucidwallet
```

`OR` if you're having trouble with your Python path:

```bash
python3 -m lucidwallet
```

`OR`  if you want a portable, albiet slower way to run:

```bash
docker run --name lucidwallet -it megachips/lucidwallet:latest
```

Then on subsequent runs:

```bash
docker start lucidwallet -ia
```

## Installation

Requires Python 3.10 or greater. If you don't have Python 3.10 - use the docker image

### macOS

Prerequisites:

`gmp`

```bash
brew install gmp
```

Install:

```bash
python3 -m pip install lucidwallet
```

A note on macOS terminal, it is recommended that you use `ITerm2`, native terminal works, however you need to modify some settings. See [here](https://github.com/Textualize/textual/blob/main/questions/why-looks-bad-on-macos.question.md) if you plan on using `Terminal.app`

### Ubuntu 22.04 (comes standard with Python 3.10)

Prerequisites:

`libgmp-dev`

```bash
sudo apt-get update && apt-get install python3-pip libgmp3-dev
```

Install:

```bash
python3 -m pip install lucidwallet
```

Source your profile to pick up new bin folder (or restart terminal)

```bash
source ~/.profile
```

### Windows

Tested on a Windows Server 2022 VM.

Prerequisites:

A decent terminal. Powershell 7 works, but it's not pretty.

[tabby.sh](https://tabby.sh/) has been tested and works well.

Once Python is installed, install with pip. Make sure your paths are up to date.

```bash
python3 -m pip install lucidwallet
```

Note, there is no `fastecdsa` natively on Windows. So some cryptographic functions are slower. You can install the `fastecdsa-any` package however you will need a working gmp and C++ build tools for Python installed.

OR - Just use docker.

### Docker

Usage notes:

The perfered method to run in docker is to NOT use mounts and reuse the same container.

Performance takes a bit of a hit on docker (especially on macOS) You can try virtiofs for faster mounts. (If you are bind mounting a database) See [here](https://www.docker.com/blog/speed-boost-achievement-unlocked-on-docker-desktop-4-6-for-mac/)

However, docker lucidwallet is the easiest to install.

Preferred method:

```bash
docker run --name lucidwallet -it megachips/lucidwallet:latest
```

Then on subsequent runs:

```bash
docker start lucidwallet -ia
```

If you want to use a local db dir, mount it like this:

```bash
docker run -v $(pwd)/database/:/database --rm -it megachips/lucidwallet:latest
```

This will create a `database` folder in your current directory, and the container will store database files there.
