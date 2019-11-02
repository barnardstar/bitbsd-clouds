#!/bin/sh
echo "installing electrum.."
pkg install -y py36-electrum
echo "done!"
electrum help
