#!/usr/local/bin/python3.7
import os
import fileinput

print("installing TOR..")
os.system("pkg install -y tor nginx")
print("enabling TOR")
os.system("sysrc tor_enable=YES")
os.system("sysrc enable_enable=YES")
os.system('echo "Socks5Proxy 192.168.0.199:9050" >> /usr/local/etc/tor/torrc')
print("starting TOR")
os.system("service tor start")
print("done! now enabling TOR service")
with fileinput.FileInput("/usr/local/etc/tor/torrc", inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace("#HiddenServiceDir /var/db/tor/other_hidden_service", "HiddenServiceDir /var/db/tor/other_hidden_service"), end='')
        print(line.replace("#HiddenServicePort 80 127.0.0.1:80", "HiddenServicePort 80 localhost:80"), end='')
os.system("mkdir /var/db/tor/other_hidden_service")
os.system("chown -R _tor:_tor /var/db/tor/other_hidden_service")
os.system("chmod -R 600 /var/db/tor/other_hidden_service")
os.system("service tor restart")
os.system("cd /usr/local/www/nginx && ls -la")
print('Edit content by runnng "nano index.html"')
print('your .onion:')
os.system("cat /var/db/tor/other_hidden_service")
os.system("cat /var/db/tor/other_hidden_service >> /usr/local/www/nginx/index.html")
print("config file: /usr/local/etc/tor/torrc")
print("to enable .onion service edit 'HiddenService' part in /usr/local/etc/tor/torrc")
print("use 'service tor restart' to restart daemon after config changed!")