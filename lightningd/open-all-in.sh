#!/bin/sh
echo "connecting to CARNIKAVA"
/usr/local/bin/lightning-cli connect 025a14b8ed40583d67aec92da19453e0b2d1fbbf75f96f85d3dd0ff61a51ee0490@145.239.239.40:9735
echo "connected! now we will try to fundchannel"
/usr/local/bin/lightning-cli fundchannel 025a14b8ed40583d67aec92da19453e0b2d1fbbf75f96f85d3dd0ff61a51ee0490 all 3000perkb
echo "i am stupid script so i quit now, read output above!"

