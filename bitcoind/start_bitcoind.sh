#!/bin/sh
echo "starting bitcoin"
bitcoind -datadir=/var/db/bitcoin/ > /dev/null &
