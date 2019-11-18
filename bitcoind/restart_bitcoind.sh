#!/bin/sh
echo "stopping bitcoin"
killall bitcoind
echo "starting bitcoin"
sleep 7
bitcoind -conf=/usr/local/etc/bitcoin.conf -datadir=/var/db/bitcoin/ > /dev/null &