#!/usr/local/bin/python3.7
import os
import fileinput

print("installing TOR..")
os.system("pkg install -y tor rsync")
print("enabling TOR")
os.system("sysrc tor_enable=YES")
os.system('echo "Socks5Proxy 192.168.0.199:9050" >> /usr/local/etc/tor/torrc')
print("starting TOR")
os.system("service tor start")
print("done! now enabling TOR service")
for line in fileinput.input("/usr/local/etc/tor/torrc", inplace = 1):
    print line.replace("#HiddenServiceDir /var/db/tor/other_hidden_service", "HiddenServiceDir /var/db/tor/other_hidden_service"),
    print line.replace("#HiddenServicePort 80 127.0.0.1:80", "HiddenServicePort 80 localhost:80"),
print("config file: /usr/local/etc/tor/torrc")
print("to enable .onion service edit 'HiddenService' part in /usr/local/etc/tor/torrc")
print("use 'service tor restart' to restart daemon after config changed!")