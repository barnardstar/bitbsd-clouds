#!/bin/sh
echo "copying plugins to ~/.lightning/plugins/..."
cp /tmp/ln_fiatjaf_plugins/* /home/lightning/.lightning/plugins/
restart_lightningd.sh

