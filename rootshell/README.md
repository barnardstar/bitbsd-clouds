### This is rootshell jail ###

with this one you can do stuff as root, as real one

`host:/home/user@ #  sudo su`

**Attention! For security purposes this jail has no normal internet connection, while you still can access internet via proxy socks5://192.168.0.199:9050 or http://192.168.0.199:8123**

Or you can also simply execute any command with torsocks prefix

`torsocks ssh rmtusr@myserver.domain.com`

However, some programs will work as usual, because proxy enviroment variable is set in ~/.cshrc to use HTTP TORed proxy

`git clone https://github.com/bitcoin-software/bitclouds.sh` # this will work

`curl https://wtfismyip.com` # as well as this

**Lack of features?** Feel free to contrbute to this set of scripts on https://github.com/bitcoin-software/bitbsd-clouds/



