#!/bin/sh
echo "installing TOR.."
pkg install -y tor
echo "enabling TOR"
sysrc tor_enable=YES
echo "starting TOR"
echo "done!"
echo "config file: /usr/local/etc/torrc"
echo "use 'service tor restart' to restart daemon after config changed!"