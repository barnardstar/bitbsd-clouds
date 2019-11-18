#!/bin/sh
echo "starting bitcoin"
bitcoind -conf=/usr/local/etc/bitcoin.conf -datadir=/var/db/bitcoin/ > /dev/null &
