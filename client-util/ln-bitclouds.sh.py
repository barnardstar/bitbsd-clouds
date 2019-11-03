import os
import time
import gnupg
import datetime
import shelve
import qrcode

import paramiko

from consolemenu import *
from consolemenu.items import *
from PIL import Image

import re

from lncontrol import createvps, getvps, checkpaid


homedir = os.getenv("HOME")+'/.bitclouds'
keydir = homedir + '/keys'
sshdir = keydir + "/ssh"
gpgdir = keydir + "/gpg"
sshkey = sshdir + '/ssh.key'

workdir = homedir+'/ln'
lndb = workdir + '/nodes.db'

vpslist = list()
keys = dict()


def sshcmd(pwd, port, cmd, textin=''):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    ssh.connect('bitbsd.org', username='lightning', port=int(port), password=str(pwd))
    #chan = ssh.get_transport().open_session()

    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdin.write(textin)
    stdin.flush()

    return stdout.read().decode('utf-8')


def bc_init():
    print('Do we have workdir? ' + str(os.path.exists(homedir)))

    keys = {
        'ssh': {
            'private': None,
            'public': None
        },
        'gpg': None
    }

    if not os.path.exists(homedir):
        print('Welcome to bitclouds.sh! now we are creating homedir ' + homedir)
        os.makedirs(homedir)
        print('Create key dir')
        os.makedirs(keydir)
        os.makedirs(sshdir)
        if not (os.path.isfile(os.getenv("HOME") + '/.ssh/id_rsa') and os.path.isfile(os.getenv("HOME") + '/.ssh/id_rsa.pub')):
            print('Generating ssh keys.. :' + sshdir + '/ssh.key')
            os.system('ssh-keygen -b 521 -t ecdsa -f ' + sshkey + ' -q -N ""')
        else:
            print('Linking existing keys.. ~/.ssh/id_rsa')
            os.system('ln -s ' + os.getenv("HOME") + '/.ssh/id_rsa.pub' + ' ' + sshkey+'.pub')
            os.system('ln -s ' + os.getenv("HOME") + '/.ssh/id_rsa' + ' ' + sshkey)

        keys['ssh']['private'] = sshkey
        keys['ssh']['public'] = sshkey+'.pub'
        os.makedirs(gpgdir)

        gpg = gnupg.GPG(gnupghome=keydir + '/gpg')
        input_data = gpg.gen_key_input(
            name_email='lnuser@bitclouds.sh',
            passphrase='bitclouds'
        )
        _ = gpg.gen_key(input_data)
        gpgkey = gpg.list_keys()[0]
        keys['gpg'] = gpgkey
    else:
        print('importing gpg keys')
        gpg = gnupg.GPG(gnupghome=keydir + '/gpg')
        gpgkey = gpg.list_keys()[0]
        keys['gpg'] = gpgkey
        print('importing ssh keys')
        keys['ssh']['private'] = sshkey
        keys['ssh']['public'] = sshkey + '.pub'

    if not os.path.exists(workdir):
        print('Creating LN dir...')
        os.makedirs(workdir)

        print('Create nodes.db')
        with shelve.open(lndb) as db:
            db['vpslist'] = vpslist
            db.close()

    else:
        loadvps()

    return keys


def loadvps():
    global vpslist

    with shelve.open(lndb) as db:
        vpslist = db['vpslist']
        db.close()


def savevps():
    # Saving the objects:
    global vpslist

    with shelve.open(lndb) as db:
        db['vpslist'] = vpslist
        db.close()


def newnode():
    hostdata = createvps()

    print('New LN node created: ' + hostdata['host'])

    vps = {'status' : 'creating...'}
    retry = 0
    paid = False
    while (vps['status'] != 'subscribed') or retry > 120:
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        retry += 1
        vps = getvps(hostdata['host'])
        if retry == 1:
            print(dtime + ' Pay this invoice: ' + hostdata['paytostart'])
            img = qrcode.make(hostdata['paytostart'])
            img.save('/tmp/bitclouds.png')
            img = Image.open('/tmp/bitclouds.png')
            img.show()

        if not paid:
            paid = checkpaid(hostdata['paytostart'])
            print(dtime + ' waiting payment, it will expire in [' + str(600-retry*5) + ' seconds]')
        else:
            print(dtime + ' Payment received! setting up your node...')
        time.sleep(5)

        if vps['status'] == 'subscribed':
            print('Now we do stuff!')
            global vpslist
            print('Fetching sparko keys...')
            cln_config = sshcmd(vps['ssh_pwd'], vps['ssh_port'], 'cat /usr/home/lightning/.lightning/config')
            reslist = cln_config.splitlines()
            for res in reslist:
                if res.startswith('sparko-keys'):
                    print(res)
                    m = re.search('sparko-keys=([a-zA-Z0-9]+);([a-zA-Z0-9]+):[a-zA-Z0-9+,]+;([a-zA-Z0-9]+):', res)
                    print('Saving sparko keys...')
                    vps['sparko_master'] = m.group(1)
                    vps['sparko_read'] = m.group(2)
                    vps['sparko_rw'] = m.group(3)

            print('Copy ssh keys...')
            with open(workdir+"/pwd.tmp", "w") as text_file:
                text_file.write(vps['ssh_pwd'])
            os.system('sshpass -f ' + workdir + '/pwd.tmp ssh-copy-id -i' +sshkey+ ' lightning@bitbsd.org -p'+str(vps['ssh_port']))
            os.remove(workdir+"/pwd.tmp")
            print('Saving host...')
            vpslist.append(vps)
            savevps()
            input('Node ' + vps['address'] + ' created! Press any key to continue...')
            return True
    return False


def listnodes():
    for vps in vpslist:
        print('node name: ' + vps['address'] + "\n" + str(vps))

    input('Press any key to continue...')


keys = bc_init()
print('working with ssh key: ' + keys['ssh']['public'])
print('working with gpg key: ' + str(keys['gpg']['fingerprint']))

# Create the menu
menu = ConsoleMenu("BitClouds.sh - Open-source VPS platform", "This is Bitcoin CLI wallet with LN support, choose an option:")

# Create some items

# A FunctionItem runs a Python function when selected
#function_item = FunctionItem("Create new node", newln(), ["Enter an input"])
# A CommandItem runs a console command
#command_item = CommandItem("Run a console command",  "touch hello.txt")
# A SelectionMenu constructs a menu from a list of strings
#selection_menu = SelectionMenu(["item1", "item2", "item3"])
# A SubmenuItem lets you add a menu (the selection_menu above, for example)
# as a submenu of another menu
#submenu_item = SubmenuItem("Submenu item", selection_menu, menu)


list_item = FunctionItem("List nodes", listnodes)
create_item = FunctionItem("Create new node", newnode)

vpsnames = list()
for vps in vpslist:
    vpsnames.append(vps['address'])

selection_menu = SelectionMenu(vpsnames)
submenu_item = SubmenuItem("Select default node", selection_menu, menu)


# Once we're done creating them, we just add the items to the menu

if len(vpslist) > 0:
    menu.append_item(list_item)
menu.append_item(submenu_item)
menu.append_item(create_item)
# Finally, we call show to show the menu and allow the user to interact
menu.show()
