#!/usr/local/bin/python3.6

# Copyright (c) 2015-2018 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from argparse import ArgumentParser
from base64 import urlsafe_b64encode
from binascii import hexlify
from getpass import getpass
from os import urandom, system, popen

import hmac


def generate_salt(size):
    """Create size byte hex salt"""
    return hexlify(urandom(size)).decode()


def generate_password():
    """Create 32 byte b64 password"""
    return urlsafe_b64encode(urandom(32)).decode('utf-8')


def password_to_hmac(salt, password):
    m = hmac.new(bytearray(salt, 'utf-8'), bytearray(password, 'utf-8'), 'SHA256')
    return m.hexdigest()


def main():
    password = popen('cat /var/db/bitcoin/.bitcoin/bitcoin.conf | grep rpcpassword | sed \'s/rpcpassword=//\'').read().strip()

    # Create 16 byte hex salt
    salt = generate_salt(16)
    password_hmac = password_to_hmac(salt, password)

    username = popen('cat /var/db/bitcoin/.bitcoin/bitcoin.conf | grep rpcuser | sed \'s/rpcuser=//\'').read().strip()

    print('String to be appended to bitcoin.conf:')
    system('echo "rpcauth={0}:{1}${2}'.format(username, salt, password_hmac) + '" >> /usr/local/etc/bitcoin.conf')
    print('String appended!')
    print('Your password:\n{0}'.format(password))

    system('sh /var/db/bitcoin/tools/restart_bitcoind.sh')


if __name__ == '__main__':
    main()
