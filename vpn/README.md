### Buy VPN service for bitcoin lightning ###

Easiest would be to use OPNSense pre-installed image

`$ curl https://bitclouds.sh/create/vpn`
```
{
  "host": "achernar", 
  "paytostart": "lnbc3537750p1pwupfr5pp588ls6gd6nn7a335j23yffaflpyql4338r205da0anmhasw95q7fsdpygf5hgsmvda6kguewwd5r5grpvd5x2unwv9eqxqzjccqp2rzjqvlfee8g7rng7ld5nlakh8hvcyrqtulnljeuvvz5tzrhfx44zkuuwzxc8sqq0ygqqyqqqqqqqqqqvsqqrcaamg9dem9ddwa3y5adn9qwqp7dsltdmt08u740ntzpjm60p80y7p3vu9wwp39yytx5ldgscpjvccysmml68237eajc554qftdt5clxqqsyhqar"
}
```

`$ curl https://bitclouds.sh/status/achernar`
```
{
  "hours_left": 4, 
  "ip": "78.47.138.66", 
  "pwd": "v3aHdPvex9Juq9HcMtid", #ignore this password
  "status": "subscribed"
}
```
Next, login into web-interface https://78.47.138.66:777 with login `admin` and password `pfsense`

The OpenVPN Client Export add-on package, located at VPN > OpenVPN on the Client Export tab will let you download VPN client for your platform.

**Default sername:** vpn1

**Default password:** remote1

There's also 2 more users vpn2 and vpn3

That's all! _Don't forget to change default passwords!_ WEB-UI: https://HOST_IP:777

**Tip!** You can use [@lntxbot] to create and manage (type `'/bitclouds help'` to bot) your VPS right from Telegram

[@lntxbot]:https://t.me/lntxbot

Pay invoice and wait until instance is created

You can also proceed with some custom linux install:

`$ curl https://bitclouds.sh/create/debian`
```
{
  "host": "achernar", 
  "paytostart": "lnbc3537750p1pwupfr5pp588ls6gd6nn7a335j23yffaflpyql4338r205da0anmhasw95q7fsdpygf5hgsmvda6kguewwd5r5grpvd5x2unwv9eqxqzjccqp2rzjqvlfee8g7rng7ld5nlakh8hvcyrqtulnljeuvvz5tzrhfx44zkuuwzxc8sqq0ygqqyqqqqqqqqqqvsqqrcaamg9dem9ddwa3y5adn9qwqp7dsltdmt08u740ntzpjm60p80y7p3vu9wwp39yytx5ldgscpjvccysmml68237eajc554qftdt5clxqqsyhqar"
}
```

`$ curl https://bitclouds.sh/status/achernar`
```
{
  "hours_left": 4, 
  "ip": "78.47.138.66", 
  "pwd": "v3aHdPvex9Juq9HcMtid", 
  "status": "subscribed"
}
```

Then, you can set up [OpenVPN] or [WireGuard], the last one [looks like much better]. Anyway, you need to login to your instance

[OpenVPN]: https://github.com/bitcoin-software/openvpn-install
[WireGuard]: https://github.com/bitcoin-software/wireguard-install
[looks like much better]: https://www.wireguard.com/quickstart/

To set up WireGuard, proceed with these steps:

```
root@imai-1:~# curl -O https://raw.githubusercontent.com/angristan/wireguard-install/master/wireguard-install.sh
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  5938  100  5938    0     0  29107      0 --:--:-- --:--:-- --:--:-- 29107
root@imai-1:~# chmod +x wireguard-install.sh
root@imai-1:~# ./wireguard-install.sh
IPv4 or IPv6 public address: 78.47.99.224
Public interface: eth0
WireGuard interface name: wg0
Server's WireGuard IPv4 10.66.66.1
Server's WireGuard IPv6 fd42:42:42::1
Server's WireGuard port 1194
Client's WireGuard IPv4 10.66.66.2
Client's WireGuard IPv6 fd42:42:42::2
First DNS resolver to use for the client: 176.103.130.130
Second DNS resolver to use for the client: 176.103.130.131
Want to use pre-shared symmetric key? [Y/n]: y

```

After short while..

```
wireguard.ko:
Running module version sanity check.
 - Original module
   - No original module exists within this kernel
 - Installation
   - Installing to /lib/modules/4.19.0-6-amd64/updates/dkms/

depmod....

DKMS: install completed.

```
[Here's how to use WireGuard]

[Here's how to use WireGuard]: https://www.wireguard.com/quickstart/

To set up OpenVPN, follow steps below

`$ ssh root@78.47.138.66`
```
The authenticity of host '78.47.138.66 (78.47.138.66)' can't be established.
ECDSA key fingerprint is SHA256:eTuLcSDi0Bb4HykFTml64nLm4qf1qObPcYRD5oA5Dek.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '78.47.138.66' (ECDSA) to the list of known hosts.
root@78.47.138.66's password: v3aHdPvex9Juq9HcMtid
You are required to change your password immediately (administrator enforced)
Linux achernar 4.19.0-6-amd64 #1 SMP Debian 4.19.67-2+deb10u1 (2019-09-20) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
```

You are required to change your password immediately (administrator enforced), so type again your instance "pwd" and set new password


```
Changing password for root.
Current password: 
123qwConnection to 78.47.138.66 closed.
[eb@localhost ~]$ ssh root@78.47.138.66
root@78.47.138.66's password: 
You are required to change your password immediately (administrator enforced)
Linux achernar 4.19.0-6-amd64 #1 SMP Debian 4.19.67-2+deb10u1 (2019-09-20) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Mon Nov  4 23:35:09 2019 from 193.238.215.130
Changing password for root.
Current password:v3aHdPvex9Juq9HcMtid 
New password: NewStrongPa$$word99>
Retype new password: NewStrongPa$$word99> 
```

And you're in! Use this command to install OpenVPN

`root@achernar:~# curl -O https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh`

`root@achernar:~# chmod +x openvpn-install.sh`

`root@achernar:~ # ./openvpn-install.sh `

```shell
Welcome to the OpenVPN installer!
The git repository is available at: https://github.com/angristan/openvpn-install

I need to ask you a few questions before starting the setup.
You can leave the default options and just press enter if you are ok with them.

I need to know the IPv4 address of the network interface you want OpenVPN listening to.
Unless your server is behind NAT, it should be your public IPv4 address.
IP address: 78.47.138.66

Checking for IPv6 connectivity...

Your host appears to have IPv6 connectivity.

Do you want to enable IPv6 support (NAT)? [y/n]: n

What port do you want OpenVPN to listen to?
   1) Default: 1194
   2) Custom
   3) Random [49152-65535]
Port choice [1-3]: 1

What protocol do you want OpenVPN to use?
UDP is faster. Unless it is not available, you shouldn't use TCP.
   1) UDP
   2) TCP
Protocol [1-2]: 1

What DNS resolvers do you want to use with the VPN?
   1) Current system resolvers (from /etc/resolv.conf)
   2) Self-hosted DNS Resolver (Unbound)
   3) Cloudflare (Anycast: worldwide)
   4) Quad9 (Anycast: worldwide)
   5) Quad9 uncensored (Anycast: worldwide)
   6) FDN (France)
   7) DNS.WATCH (Germany)
   8) OpenDNS (Anycast: worldwide)
   9) Google (Anycast: worldwide)
   10) Yandex Basic (Russia)
   11) AdGuard DNS (Russia)
   12) Custom
DNS [1-12]: 2

Do you want to use compression? It is not recommended since the VORACLE attack make use of it.
Enable compression? [y/n]: n

Do you want to customize encryption settings?
Unless you know what you're doing, you should stick with the default parameters provided by the script.
Note that whatever you choose, all the choices presented in the script are safe. (Unlike OpenVPN's defaults)
See https://github.com/angristan/openvpn-install#security-and-encryption to learn more.

Customize encryption settings? [y/n]: n

Okay, that was all I needed. We are ready to setup your OpenVPN server now.
You will be able to generate a client at the end of the installation.
Press any key to continue...
```

Now, script will take some time to install all the packages etc.. in the end, you'll be asked to provide first client name

```
Tell me a name for the client.
Use one word only, no special characters.
Client name: astra

Do you want to protect the configuration file with a password?
(e.g. encrypt the private key with a password)
   1) Add a passwordless client
   2) Use a password for the client
Select an option [1-2]: 1

Note: using Easy-RSA configuration from: ./vars

Using SSL: openssl OpenSSL 1.1.1d  10 Sep 2019
Generating an EC private key
writing new private key to '/etc/openvpn/easy-rsa/pki/private/astra.key.Nt9I17kzN1'
-----
Using configuration from /etc/openvpn/easy-rsa/pki/safessl-easyrsa.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'astra'
Certificate is to be certified until Oct 19 22:46:50 2022 GMT (1080 days)

Write out database with 1 new entries
Data Base Updated
```

Client astra added, the **configuration file is available at /root/astra.ovpn**.
Download the .ovpn file and import it in your OpenVPN client.

