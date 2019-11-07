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

Install TOR and do all configuration by single command

`hadar:/root@[16:11] # install_onion_service.sh`

```
Edit content by runnng "nano /usr/local/www/index.html"
your .onion address:
jjicf4zjnyjjmyupti4ab5b5krwdjxzccgqgxkfe4io3eju4c42sfiqd.onion
You can put any file in "/usr/local/www/" and then download it http://
jjicf4zjnyjjmyupti4ab5b5krwdjxzccgqgxkfe4io3eju4c42sfiqd.onion/anyfile.zip
config file: /usr/local/etc/tor/torrc
to manage .onion service configuration edit 'HiddenService' part in end of file /usr/local/etc/tor/torrc
use 'service tor restart' to restart daemon after config changed!

remember to do

$sudo su

```
