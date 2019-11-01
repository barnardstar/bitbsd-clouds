#!/bin/sh
if [ -z "$1" ]
  then
    echo "No invoice supplied. Usage:"
    echo "pay_over_lightning.sh lnbc1-[YOUR-INVOICE]-isd8r4"
    break
fi
/usr/local/bin/lightning-cli pay $1
