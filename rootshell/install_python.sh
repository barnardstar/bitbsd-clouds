#!/bin/sh
echo "installing python 3.7.."
pkg install -y python37
curl -x socks://192.168.0.199:9050 https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
python3.7 /tmp/get-pip.py
echo "done!"

