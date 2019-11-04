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
gnupg
qrcode
paramiko
scp
console-menu
Pillow
```

So install them at once or one by one like:

`python3.7 -m pip install setuptools`

`watchtower.py getinfo` - when using in cli it's a remote command line interface to your c-lightning

`./watchtower.py` - if you execute it you'll get fancy