#!/usr/local/bin/python3.7

from lightning import LightningRpc
import random
import os

l1 = LightningRpc("/home/lightning/.lightning/lightning-rpc")

funds = l1.listfunds()
nodes = l1.listnodes()["nodes"]

low = list()
high = list()

print('current node state:')

for chan in funds["channels"]:
    if chan["connected"]:
        for node in nodes:
            if node["nodeid"] == chan["peer_id"]:
                # node["alias"].encode('ascii', 'ignore').decode('ascii')
                perce = round(chan["channel_sat"]/chan["channel_total_sat"],2)*100
                print(chan["state"] + ":" + " (" + chan["short_channel_id"] + ")" +
                  " | balance: " + str(chan["channel_sat"]) + " (" + str(perce) + " % of " + str(round(chan["channel_total_sat"]/100000000,2)) + " BTC)")

                if perce <= 25:
                    low.append(chan["short_channel_id"])
                elif perce >= 75:
                    high.append(chan["short_channel_id"])

print('now rebalancing node.. be patient, this takes a while')
cnt = 0
while cnt < 100:
    cnt += 1
    os.system('lightning-cli rebalance ' + random.choice(high) + ' ' + random.choice(low) + ' ' + str(random.randrange(10000, 50000)*1000))
