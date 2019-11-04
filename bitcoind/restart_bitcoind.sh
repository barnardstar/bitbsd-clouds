#!/bin/sh
echo "stopping bitcoin"
killall bitcoind
echo "starting bitcoin"
bitcoind -datadir=/var/db/bitcoin/ > /dev/null &