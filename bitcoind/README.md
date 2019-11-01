### This is bitcoind jail
Here you go with some basic stuff

_execute bitcoin calls_

`host:/var/db/bitcoin@ #  bitcoin-cli echo test`

_manage full node_

`host:/var/db/bitcoin@ # start_bitcoind.sh`

`host:/var/db/bitcoin@ # stop_bitcoind.sh`

`host:/var/db/bitcoin@ # restart_bitcoind.sh`

_edit bitcoind config_

`host:/var/db/bitcoin@ # [nano | vim] ~/bitcoin_daemon.conf`

_use tmux to keep your app running_

`host:/var/db/bitcoin@ # tmux` or attach to existing sesion with `host:/var/db/bitcoin@ # tmux a`

_feel free to use python_

`host:/var/db/bitcoin@ # python3.7 yourapp.py`

_or_

`host:/var/db/bitcoin@ # python3.7 `

`Python 3.7.4 (default, Aug 22 2019, 05:59:46)`
 
`[Clang 6.0.1 (tags/RELEASE_601/final 335540)] on freebsd12`

`Type "help", "copyright", "credits" or "license" for more information.`

`>>> import bitcoinrpc`

**Attention! the jail has no normal internet connection, while you still can access internet via proxy socks5://192.168.0.199:9050**

**Lack of features?** Feel free to contrbute to this set of scripts on https://github.com/bitcoin-software/bitbsd-clouds/
