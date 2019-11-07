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

`hadar:/root@[16:11] # install_onion_service.sh`

```


```
