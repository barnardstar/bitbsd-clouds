### BitBSD Watchtower™ ###

Watchtower is CLI Bitcoin wallet with LN support

### How to install ###

You need python3.7 to run this app, so on Debian-like:

`apt install python3.7`

or on RedHat-like:

`dnf install python3.7`

or on FreeBSD:

`pkg install python37`

Also, you need dev-tools:

`apt install python3.7-dev`

You need pip for easier setup:

`curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`

`python3.7 get-pip.py`

Then you need install set of dependencies from `requirements.txt`:

```bash
setuptools
python-gnupg
qrcode
paramiko
scp
console-menu
Pillow
pycryptodomex

```

So install them at once

 `python3.7 -m pip install setuptools python-gnupg qrcode paramiko scp console-menu Pillow pycryptodomex`

or one by one like

`python3.7 -m pip install setuptools`

### How to use

`watchtower.py getinfo` - when using in cli it is actaully a remote command line interface to your c-lightning, so refer to c-lightning RPC

To use as a interactive CLI-wallet, just run without arguments

`./watchtower.py` 

### Features

Bitcoin and Lightning Network wallet

3-minute setup

Non-custodial wallet

RPC and SSH access to your LN node
 
e2e encrypted backups on decentralized storage (IPFS)
