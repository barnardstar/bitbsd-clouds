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
#with fileinput.FileInput("/usr/local/etc/tor/torrc", inplace=True, backup='.bak') as file:
#    for line in file:
#        print(line.replace("#HiddenServiceDir /var/db/tor/other_hidden_service", "HiddenServiceDir /var/db/tor/other_hidden_service"), end='')
os.system('echo "HiddenServiceDir /var/db/tor/onionweb" >> /usr/local/etc/tor/torrc')
os.system('echo "HiddenServicePort 80 localhost:80" >> /usr/local/etc/tor/torrc')

os.system("mkdir /var/db/tor/onionweb")
os.system("chown -R _tor:_tor /var/db/tor/onionweb")
os.system("chmod -R 600 /var/db/tor/onionweb")
os.system("service tor restart")
os.system("cd /usr/local/www/nginx && ls -la")
print('Edit content by runnng "nano index.html"')
print('your .onion:')
os.system("cat /var/db/tor/onionweb/hostname")
os.system("cat /var/db/tor/onionweb/hostname >> /usr/local/www/nginx/index.html")
print("config file: /usr/local/etc/tor/torrc")
print("to manage .onion service configuration edit 'HiddenService' part in end of file /usr/local/etc/tor/torrc")
print("use 'service tor restart' to restart daemon after config changed!")