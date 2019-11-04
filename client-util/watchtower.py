import os
import time
import gnupg
import datetime
import shelve
import qrcode
import sys
import paramiko

from consolemenu import *
from consolemenu.items import *
from PIL import Image

import re

import json

from lncontrol import createvps, getvps, checkpaid


homedir = os.getenv("HOME")+'/.bitclouds'
keydir = homedir + '/keys'
sshdir = keydir + "/ssh"
gpgdir = keydir + "/gpg"
sshkey = sshdir + '/ssh.key'

workdir = homedir+'/ln'
lndb = workdir + '/nodes.db'

vpslist = list()

default_node = False

default_vps = dict()


def sparko(cmd, params):
    global default_vps
    sparko_host = default_vps['sparko']
    key = default_vps['sparko_master']

    cmd = 'curl -ks ' + sparko_host + ' -d \'{"method":"' + cmd + '", "params": ' + str(
        params).replace("'", "\"") + '}\' -H \'X-Access: ' + key + '\''

    response = json.loads(os.popen(cmd).read())
    return response


def sshcmd(pwd, port, cmd, textin=''):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    try:
        ssh.connect('bitbsd.org', username='lightning', port=int(port), key_filename=sshkey)
    except Exception as e:
        print(e)
        ssh.connect('bitbsd.org', username='lightning', port=int(port), password=str(pwd))
    #chan = ssh.get_transport().open_session()

    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdin.write(textin)
    stdin.flush()

    return stdout.read().decode('utf-8')


def loadvps():
    global vpslist
    global default_node

    with shelve.open(lndb) as db:
        vpslist = db['vpslist']
        default_node = db['default_node']
        db.close()


def savevps():
    # Saving the objects:
    global vpslist
    global default_node

    with shelve.open(lndb) as db:
        db['vpslist'] = vpslist
        db['default_node'] = default_node
        db.close()


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
        #if not (os.path.isfile(os.getenv("HOME") + '/.ssh/id_rsa') and os.path.isfile(os.getenv("HOME") + '/.ssh/id_rsa.pub')):
        #    print('Generating ssh keys.. :' + sshdir + '/ssh.key')
        #    os.system('ssh-keygen -b 521 -t ecdsa -f ' + sshkey + ' -q -N ""')
        #else:
        #    print('Linking existing keys.. ~/.ssh/id_rsa')
        #    os.system('ln -s ' + os.getenv("HOME") + '/.ssh/id_rsa.pub' + ' ' + sshkey+'.pub')
        #    os.system('ln -s ' + os.getenv("HOME") + '/.ssh/id_rsa' + ' ' + sshkey)
        print('Generating ssh keys.. :' + sshdir + '/ssh.key')
        os.system('ssh-keygen -b 521 -t ecdsa -f ' + sshkey + ' -q -N ""')

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
            db['default_node'] = False
            db.close()
    else:
        loadvps()

    return keys


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
            if len(vpslist) == 1:
                global default_node
                default_node = vps['address']
            savevps()
            input('Node ' + vps['address'] + ' created! Press any key to continue...')
            return True
    return False


def listnodes():
    for vps in vpslist:
        print('node name: ' + vps['address'] + "\n" + str(vps))

    input('Press any key to continue...')


def initdefvps():
    global default_vps
    global default_node
    for vps in vpslist:
        print(vps)
        if vps['address'] == default_node:
            default_vps = vps


def setdef(menu, address):
    global default_node
    global vpslist

    default_node = address
    savevps()

    vpsnames = list()
    selection_menu = SelectionMenu(vpsnames)
    for vps in vpslist:
        selection_menu.append_item(FunctionItem(vps['address'], setdef, args=[menu, vps['address']]))

    submenu_item = SubmenuItem("[" + str(default_node) + "] " + " Change default node", selection_menu, menu)

    return submenu_item


def paychain():
    addr = input('Enter address: ')
    amt = input('Enter amount (sats): ')
    sure = input('Are you sure want to send ' + str(amt) + ' satoshis to ' + addr + '? (y/n)')
    if sure == 'y':
        input(json.dump(sparko('withdraw', [addr, amt, '3000perkb']), indent=4))


def payln():
    bolt = input('BOLT11: ')
    inv_data = sparko('decodepay', [bolt])
    sats = round(inv_data['msatoshi'] / 1000, 1)
    sure = input('Are you sure you want to send ' + str(sats) + '('+inv_data["description"]+')? (y/n)')
    if sure == 'y':
        input(json.dump(sparko('waitpay', [bolt]), indent=4))


def rcvchain():
    input(sparko('newaddr', list()))


def rcvln():
    amt = input('Amount?')
    userdesc = input('Description: ')
    dtime = datetime.datetime.strftime(datetime.datetime.now(), '%y%m%d-%H:%M:%S')
    desc = dtime+' watchtower: '+userdesc
    input('Your invoice: ' + sparko('invoice', [amt, desc, userdesc])['bolt11'])


def summary():
    sumdata = sparko('summary', list())
    # Create the root menu
    nodeid = sumdata['my_address'].split('@')[0]
    menu = MultiSelectMenu(nodeid, "On-chain: " + sumdata['utxo_amount'],
                           epilogue_text=("LN balance: " + sumdata['avail_out']),
                           exit_option_text='Exit Application')  # Customize the exit text

    # Add all the items to the root menu
    # menu.append_item(FunctionItem("Pay on-chain", action, args=['one']))
    menu.append_item(FunctionItem("Pay on-chain", paychain))
    menu.append_item(FunctionItem("Receive on-chain", rcvchain))
    menu.append_item(FunctionItem("Pay over LN", payln))
    menu.append_item(FunctionItem("Receive over LN", rcvln))

    # Show the menu
    menu.start()
    menu.join()


def dobackup():
    global default_vps
    sure = input('Are you sure want perform backup? This action will turn off your LN node for a while! Proceed? (y/n)')
    if sure == 'y':
        input(sshcmd('', default_vps['ssh_port'], 'ls -la'))


def doimport():
    input('imp')


def devinfo():
    global default_vps
    menu = MultiSelectMenu("curl -X POST "+default_vps['sparko'] + " \ ",
                           " -d '{\"method\": \"getinfo\"}' -H 'X-Access: grabyourkeyinside'",
                           epilogue_text=('ssh lightning@bitbsd.org -p '+ str(default_vps['ssh_port'])),
                           exit_option_text='Exit Application')  # Customize the exit text

    menu.start()
    menu.join()


def genmenu():
    topic = "BitClouds.sh - Open-source VPS platform"
    header = "This is Bitcoin CLI wallet with LN support, choose an option:"
    menu = ConsoleMenu(topic, header)

    get_summary = FunctionItem("Wallet", summary)
    do_backup = FunctionItem("Perform cold backup", dobackup)
    dev_info = FunctionItem("RPC / SSH access", devinfo)
    do_import = FunctionItem("Import BitBSD c-lightning jail", doimport)
    create_item = FunctionItem("Create new node", newnode)

    # Create the menu
    if len(vpslist) > 0:
        menu.append_item(get_summary)
        menu.append_item(do_backup)
        menu.append_item(dev_info)
    menu.append_item(do_import)
    menu.append_item(setdef(menu, default_node))
    menu.append_item(create_item)

    # Finally, we call show to show the menu and allow the user to interact
    menu.show()


keys = bc_init()
print('working with ssh key: ' + keys['ssh']['public'])
print('working with gpg key: ' + str(keys['gpg']['fingerprint']))
initdefvps()
genmenu()

