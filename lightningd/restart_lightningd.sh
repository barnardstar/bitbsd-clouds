#!/bin/sh
echo "stopping c-lightning"
killall lightningd
sleep 2
echo "starting c-lightning"
/usr/local/bin/lightningd --daemon
