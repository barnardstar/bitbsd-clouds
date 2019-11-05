### Creating TOR hidden service ###

Create rootshell jail

`$ curl https://bitclouds.sh/create/rootshell`

Get access data

`$ curl https://bitclouds.sh/status/{$HOST_NAME}`

```
{
  "app_port": 52606, 
  "hours_left": 4, 
  "ip": "bitbsd.org", 
  "ssh_port": 62866, 
  "ssh_pwd": "a96fa70a7262fd2e", 
  "ssh_usr": "satoshi", 
  "status": "subscribed"
}
```

Connect via SSH

`ssh satoshi@bitbsd.org -p {$SSH_PORT}` _replace `{$SSH_PORT}` with `62866`

Enter `{$SSH_PWD}` and then

`satoshi@rootshell ~# sudo su`  

Install TOR

`hadar:/root@[16:11] # install_tor.sh`

To enable .onion service edit 'HiddenService' part in /usr/local/etc/tor/torrc
use 'service tor restart' to restart daemon after config changed!

Let's run nginx as hidden service

`hadar:/root@[16:16] # pkg install nginx`

`hadar:/root@[16:16] # sysrc nginx_enable=YES`

`hadar:/root@[16:16] # service nginx start`

edit tor config file

`hadar:/root@[16:16] # vim /usr/local/etc/tor/torrc`

```
HiddenServiceDir /var/db/tor/hidden_service/bitclouds_web
HiddenServicePort 80 localhost:80

```

Now, create new hidden service dir

```
hadar:/root@[16:21] # mkdir /var/db/tor/bitclouds_web
hadar:/root@[16:22] # chown -R _tor:_tor /var/db/tor/bitclouds_web
hadar:/root@[16:23] # chmod -R 700 /var/db/tor/bitclouds_web
hadar:/root@[16:24] # service tor restart
Stopping tor.
Waiting for PIDS: 87496.
Starting tor.
```

You will see `hostname` file

`hadar:/root@[16:27] # ls -la /var/db/tor/bitclouds_web/`

```
total 19
drwx------  3 _tor  _tor   6 Nov  5 16:26 .
drwx------  4 _tor  _tor  10 Nov  5 16:27 ..
drwx------  2 _tor  _tor   2 Nov  5 16:26 authorized_clients
-rw-------  1 _tor  _tor  63 Nov  5 16:26 hostname
-rw-------  1 _tor  _tor  64 Nov  5 16:26 hs_ed25519_public_key
-rw-------  1 _tor  _tor  96 Nov  5 16:26 hs_ed25519_secret_key
```

`hadar:/root@[16:27] # cat /var/db/tor/bitclouds_web/hostname` 

You will get your `iumgsxem7tlgf2adyjzo2boxlxqd6rvjhhb2wli6lmkb35grnczjukqd.onion` address

That's all! Try it to access via your TOR browser!

`index.html` file is located in `/usr/local/www/nginx/` directory and the nginx config in `/usr/local/etc/nginx/` as `nginx.conf`


