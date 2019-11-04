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

Bitcoin and Lightning Network CLI wallet _both interactive and shell_

3-minute setup _nodes are built up from pre-configured and pre-synced instances, so you dont have to wait at all.._

Non-custodial wallet _you own your dedicated LN node in secure enviroment_

RPC and SSH access to your LN node _start your app development instantly!_

![wallet](https://i.imgur.com/Qvmdrbj.png "Watchtower")
 
e2e encrypted backups on decentralized storage (IPFS)

```bash
Are you sure want perform backup? This action will turn off your LN node for a while! Proceed? (y/n)y
loading encryption keys
stopping cln
stopping c-lightning
stopped!
making archive
starting cln
started.. node was offline for 5 seconds
downloading backup archive to local storage
/tmp/bck.tar's progress: 0%   
/tmp/bck.tar's progress: 43%   
/tmp/bck.tar's progress: 100%   
encrypting archive locally with GPG
upload encrypted archive to server
uploading archive to node
clightning.tar.gpg progress: 0%   
clightning.tar.gpg progress: 56%   
clightning.tar.gpg progress: 89%   
clightning.tar.gpg' progress: 100%   

uploading to ipfs server
uploading to web servers

 ###### HERE IS YOUR BACKUP ######
 # Clearnet URL: https://bitbsd.org/backups/cln-109-20191104210055.tar.gpg
 # IPFS: https://bitclouds.link/ipfs/QmUkpdP5RAHa2LMEBp3FSSH7BbhnbrkjpVXjwPBh6MaYwy
 # Onion: http://http://carnikavazp6djqx.onion/cln-109-20191104210055.tar.gpg
 ######     END OF LINKS    ######

clean up locally, on node & ipfs
should I remove local unencrypted copy of backup? (y/n)n
moved to /tmp/cln-backup-191104-21:03:14.tar

seems like we finished! press any key...
```

### Workdir

GPG encryption keys and SSH access keys are stored on your local pc where you execute Watchtower

```bash
[user@localhost ~]$ ls ~/.bitclouds/keys/gpg/
openpgp-revocs.d  private-keys-v1.d  pubring.kbx  pubring.kbx~  random_seed  trustdb.gpg
[user@localhost ~]$ ls ~/.bitclouds/keys/ssh/
ssh.key  ssh.key.pub

```

