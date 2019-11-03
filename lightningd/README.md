### This is c-lightning jail

`$ curl https://bitclouds.sh/create/lightningd`

````
{
  "host": "barnardsstar", 
  "paytostart": "lnbc3627320p1pwm630spp5twdd9yq5mufat0fagrxr8fjfkhahfcuxuda5lfs9alafvyp0vpwqdq5gfshymnpwfj8x5m5v9eqxqzjccqp2rzjq0hpsr5wupl3l8yeslvckh2aanmt447stz7a3036m97gurwjehrm5zxy4cqq0scqqqqqqqpgqqqqqzqqzsh8z7nj3vqknrumrtv84erxdzpfg5tr5knys5c3r7d2mfpc9dzm6psz4sstzrc36040pntdv9s484au4xdhvc9mvx9a8zcrexnr9h6zqp7gm7kk"
}
````


`$ curl https://bitclouds.sh/status/barnardsstar`

````
{
  "app_port": 51356, 
  "hours_left": 4, 
  "ip": "bitbsd.org", 
  "sparko": "https://bitbsd.org:59330/rpc", 
  "ssh2onion": "you can ssh directly to your .onion (/home/lightning/onion.domain) on port 22", 
  "ssh_port": 61732, 
  "ssh_pwd": "52c27722a7e21dff", 
  "ssh_usr": "lightning", 
  "status": "subscribed", 
  "user_port": 53445
}
````


Here you go with some basic stuff

_execute bitcoin calls_

`host:/home/lightning@ #  bitcoin-cli echo test`

_play with c-lightning_

right from your app using [sparko]

[sparko]: https://github.com/fiatjaf/lightningd-gjson-rpc/tree/master/cmd/sparko  

 `you@home ~$ curl -k https://bitbsd.org:59330/rpc -d '{"method": "pay", "params": ["lnbc..."]}' -H 'X-Access masterkeythatcandoeverything'`
 
 _Note! `https://bitbsd.org:59330/rpc` is "sparko" key in status response and `masterkeythatcandoeverything` can be found inside your jail ~/.lightning/config as "sparko-keys" parameter!_

or from your pc using [client-util]

[client-util]: https://github.com/bitcoin-software/bitbsd-clouds/tree/master/client-util

`you@home ~$ python3.7 cln-cli.py getinfo` 

with ready scripts:

`host:/home/lightning@ # start_clightning.sh`

`host:/home/lightning@ # stop_clightning.sh`

`host:/home/lightning@ # restart_clightning.sh`

`host:/home/lightning@ # install_fiatjaf_plugins.sh`

or with daemon itself:

`host:/home/lightning@ # lightning-cli help`

`host:/home/lightning@ # lightning-cli getinfo`

_receive on-chain funds to your node_

`host:/home/lightning@ # refill_onchain.sh`

_open channel for all available funds to BitBSD LN node_

`host:/home/lightning@ # open-all-in.sh`

_rebalance your node channels_

`host:/home/lightning@ # rebalance_channels.sh`

_edit lightningd config_

`host:/home/lightning@ # [ nano | vim | vi | ee ] ~/.lightning/config`

_use tmux to keep your app running_

`host:/home/lightning@ # tmux` or attach to existing sesion with `host:/home/lightning@ # tmux a`

_feel free to use python_

`host:/home/lightning@ # python3.7 yourapp.py`

_or_

`host:/home/lightning@ # python3.7 `

`Python 3.7.4 (default, Aug 22 2019, 05:59:46)`
 
`[Clang 6.0.1 (tags/RELEASE_601/final 335540)] on freebsd12`

`Type "help", "copyright", "credits" or "license" for more information.`

`>>> import lightning

**Attention! For security purposes this jail has no normal internet connection, while you still can access internet via proxy socks5://192.168.0.199:9050 or http://192.168.0.199:8123**

Or you can also simply execute any command with torsocks prefix

`torsocks ssh rmtusr@myserver.domain.com`

However, some programs will work as usual, because proxy enviroment variable is set in ~/.cshrc to use HTTP TORed proxy

`git clone https://github.com/bitcoin-software/bitclouds.sh` # this will work

`curl https://wtfismyip.com` # as well as this

**Lack of features?** Feel free to contrbute to this set of scripts on https://github.com/bitcoin-software/bitbsd-clouds/


[https://github.com/fiatjaf/lightningd-gjson-rpc/tree/master/cmd/sparko]: https://github.com/fiatjaf/lightningd-gjson-rpc/tree/master/cmd/sparko

[]: https://github.com/fiatjaf/lightningd-gjson-rpc/tree/master/cmd/sparko

[]: https://github.com/fiatjaf/lightningd-gjson-rpc/tree/master/cmd/sparko

[test]: https://github.com/fiatjaf/lightningd-gjson-rpc/tree/master/cmd/sparko