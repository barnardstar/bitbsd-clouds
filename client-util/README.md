### BitBSD Watchtower™ ###

Watchtower is CLI Bitcoin wallet with LN support

![wallet](https://i.imgur.com/2b33Tsg.png "Watchtower")


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

```bash
{
    "address": [
        {
            "address": "188.165.223.61",
            "port": 51158,
            "type": "ipv4"
        },
        {
            "address": "snyrdjyzxgnsigcynah3lxlj5qwk6mg4s6od6ceqs5fa4zwxezsy5yad.onion",
            "port": 9735,
            "type": "torv3"
        }
    ],
    "alias": "anser [bitclouds.sh]",
    "binding": [
        {
            "address": "0.0.0.0",
            "port": 51158,
            "type": "ipv4"
        }
    ],
    "blockheight": 602341,
    "color": "ff0000",
    "fees_collected_msat": "0msat",
    "id": "0338ae2b71913af91800562bd7ef46d9e05ab424e50664b567e81b4564eb043e15",
    "msatoshi_fees_collected": 0,
    "network": "bitcoin",
    "num_active_channels": 2,
    "num_inactive_channels": 0,
    "num_peers": 4,
    "num_pending_channels": 0,
    "version": "v0.7.3"
}

```

To use as a interactive CLI-wallet, just run without arguments

`./watchtower.py`

 ![wallet](https://i.imgur.com/WNiQWQb.png "Watchtower")

### Features

Bitcoin and Lightning Network wallet

3-minute setup

Non-custodial wallet

RPC and SSH access to your LN node

![wallet](https://i.imgur.com/Qvmdrbj.png "Watchtower")
 
e2e encrypted backups on decentralized storage (IPFS)


