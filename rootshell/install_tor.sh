#!/bin/sh
echo "installing TOR.."
pkg install -y tor
echo "enabling TOR"
sysrc tor_enable=YES
echo "Socks5Proxy 192.168.0.199:9050" >> /usr/local/etc/tor/torrc
echo "starting TOR"
service tor start
echo "done!"
echo "config file: /usr/local/etc/tor/torrc"
echo "to enable .onion service edit 'HiddenService' part in /usr/local/etc/tor/torrc"
echo "use 'service tor restart' to restart daemon after config changed!"