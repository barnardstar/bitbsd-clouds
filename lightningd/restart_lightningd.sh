#!/bin/sh
echo "stopping c-lightning"
killall lightningd
echo "stopped!"
sleep 2
echo "starting c-lightning"
/usr/local/bin/lightningd --daemon
echo "started!"
