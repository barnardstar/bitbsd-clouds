#!/usr/bin/python3.7
import os
import time
import random
import gnupg
import datetime
import shelve
import requests
import qrcode
import sys
import paramiko
import fileinput

from scp import SCPClient, SCPException
from consolemenu import *
from consolemenu.items import *
from PIL import Image

import re

import json


bchost = 'https://bitclouds.sh'


def createvps():
    request_data = requests.get(bchost + '/create/lightningd')

    if request_data.status_code == 200:
        hostdata = request_data.json()
        return hostdata
    else:
        print('Error: ' + request_data.status_code)
        return False


def checkpaid(invoice):
    request_data = requests.get(bchost + '/chkinv/'+invoice)

    if request_data.status_code == 200:
        data = request_data.json()
        if data['status'] == 'paid':
            return True
    else:
        print('Error: ' + request_data.status_code)
        return False


def getvps(address):
    request_data = requests.get(bchost + '/status/'+address)

    if request_data.status_code == 200:
        node_data = request_data.json()
        node_data['address'] = address
        return node_data
    else:
        return False


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


def ssh_genkeys(keyfile, pem=True):
    from Cryptodome.PublicKey import RSA
    key = RSA.generate(2048)
    public = key.publickey().exportKey('OpenSSH').decode('utf-8')
    private = key.exportKey('PEM').decode('ascii')

    f = open(keyfile, "w")
    f.write(private)
    f.close()

    f = open(keyfile+'.pub', "w")
    f.write(public)
    f.close()

    os.system('chmod 600 ' + keyfile)


def sshcmd(pwd, port, cmd, textin=''):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    #f = open(sshkey, 'r')
    #s = f.read()
    #keyfile = StringIO(s)
    #pkey = paramiko.RSAKey.from_private_key(keyfile)
    try:
        ssh.connect('bitbsd.org', username='lightning', port=int(port), key_filename=sshkey, look_for_keys=False)
    except Exception as e:
        #print('!!!!!!!!!!!!!!!' + sshkey)
        #print(e)
        ssh.connect('bitbsd.org', username='lightning', port=int(port), password=str(pwd))
    #chan = ssh.get_transport().open_session()

    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdin.write(textin)
    stdin.flush()

    return stdout.read().decode('utf-8')


def progress(filename, size, sent):
    prc = float(sent) / float(size) * 100
    line = ("%s\'s progress: %.0f%%   \r" % (filename, prc))
    divpart = round(prc, 2)*100 - int(prc)*100
    if divpart < 2:
        print(line)


def sshupload(file, remote_directory):
    global default_vps
    """Upload a single file to a remote directory"""
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    #f = open(sshkey, 'r')
    #s = f.read()
    #keyfile = StringIO(s)
    #pkey = paramiko.RSAKey.from_private_key(keyfile)
    ssh.connect('bitbsd.org', username='lightning', port=default_vps['ssh_port'], key_filename=sshkey, look_for_keys=False)

    scp = SCPClient(ssh.get_transport(), progress=progress)
    try:
        scp.put(file,
                recursive=True,
                remote_path=remote_directory)
    except SCPException:
        print('scp error')
    finally:
        scp.close()
    ssh.close()


def sshdownload(remote_path, local_path):
    global default_vps
    """Upload a single file to a remote directory"""
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    #f = open(sshkey, 'r')
    #s = f.read()
    #keyfile = StringIO(s)
    #pkey = paramiko.RSAKey.from_private_key(keyfile)
    ssh.connect('bitbsd.org', username='lightning', port=default_vps['ssh_port'], key_filename=sshkey, look_for_keys=False)
    scp = SCPClient(ssh.get_transport(), progress=progress)
    try:
        scp.get(remote_path,local_path)
    except SCPException as e:
        print('scp error' + str(e))
    finally:
        scp.close()
    ssh.close()


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


def replaceAll(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)


def bc_init():
    #print('Do we have workdir? ' + str(os.path.exists(homedir)))

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
        #os.system('ssh-keygen -t rsa -b 2048  -f ' + sshkey + ' -q -N ""')
        ssh_genkeys(sshkey)
        #replaceAll(sshkey, '-----BEGIN OPENSSH PRIVATE KEY-----', '-----BEGIN RSA PRIVATE KEY-----')
        #replaceAll(sshkey, '-----END OPENSSH PRIVATE KEY-----', '-----END RSA PRIVATE KEY-----')
        keys['ssh']['private'] = sshkey
        keys['ssh']['public'] = sshkey+'.pub'
        os.makedirs(gpgdir)

        gpg = gnupg.GPG(keydir + '/gpg')
        input_data = gpg.gen_key_input(
            name_email='lnuser@bitclouds.sh',
            passphrase='bitclouds'
        )
        _ = gpg.gen_key(input_data)
        gpgkey = gpg.list_keys()[0]
        keys['gpg'] = gpgkey
    else:
        #print('importing gpg keys')
        gpg = gnupg.GPG(keydir + '/gpg')
        gpgkey = gpg.list_keys()[0]
        keys['gpg'] = gpgkey
        #print('importing ssh keys')
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
        vps = getvps(hostdata['host'])
        if retry == 0:
            print(dtime + ' Pay this invoice: ' + hostdata['paytostart'])
            img = qrcode.make(hostdata['paytostart'])
            img.save('/tmp/bitclouds.png')
            img = Image.open('/tmp/bitclouds.png')
            img.show()

        if not paid:
            paid = checkpaid(hostdata['paytostart'])
            print(dtime + ' waiting payment, it will expire in [' + str(600-retry) + ' seconds]')
        else:
            print(dtime + ' Payment received! setting up your node...')

        sleeptime = random.randrange(5,15)
        retry += sleeptime
        time.sleep(sleeptime)

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
            os.system('sshpass -f ' + workdir + '/pwd.tmp ssh-copy-id -i' +sshkey+ ' -o "StrictHostKeyChecking=no" lightning@bitbsd.org -p'+str(vps['ssh_port']))
            os.remove(workdir+"/pwd.tmp")
            pwd = '1'
            pwd2 = '2'
            while not (pwd == pwd2) and (pwd != '') and (len(pwd) < 6):
                pwd = input("Enter new password for instance (REQUIRED):")
                pwd2 = input("Re-enter new password for instance (REQUIRED):")
                if pwd != pwd2:
                    print('Password mismatch or too short! re-try again...')
            if pwd == pwd2:
                vps['ssh_pass'] = pwd
                os.system('ssh -i' +sshkey+ ' -o "StrictHostKeyChecking=no" lightning@bitbsd.org -p'+str(vps['ssh_port']) + ' "cps "+' + pwd)
            # echo \"{{ pwd }}\" | pw usermod lightning -h0
            print('Saving host...')
            vpslist.append(vps)
            if len(vpslist) == 1:
                global default_node
                default_node = vps['address']
            savevps()
            input('Node ' + vps['address'] + ' created! You need to restart Watchtower to apply changes...')
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
    menu = MultiSelectMenu(nodeid, "On-chain: " + str(int(float(sumdata['utxo_amount'].strip('btc'))*100000000))+ " sats ("+ sumdata['utxo_amount']+")",
                           epilogue_text=("LN balance: " + str(int(float(sumdata['avail_out'].strip('btc'))*100000000)) + " sats (" + sumdata['avail_out']+")"),
                           exit_option_text='Go back')  # Customize the exit text

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
    print('loading encryption keys')
    gpg = gnupg.GPG(keydir + '/gpg')
    if sure == 'y':
        print('test connection')
        print(sshcmd('', default_vps['ssh_port'], 'uptime'))
        start = time.time()
        print('stopping cln')
        print(sshcmd('', default_vps['ssh_port'], 'su - lightning -c "/usr/local/bin/stop_lightningd.sh"'))
        print('making archive')
        print(sshcmd('', default_vps['ssh_port'], 'rm -rf /tmp/bck.tar || true'))
        print(sshcmd('', default_vps['ssh_port'], 'su - lightning -c "/usr/bin/tar -cf /tmp/bck.tar /usr/home/lightning/.lightning"'))
        print('starting cln')
        print(sshcmd('', default_vps['ssh_port'], 'su - lightning -c "/usr/local/bin/lightningd --daemon > /dev/null &"'))
        secs = time.time() - start
        print('started.. node was offline for ' + str(int(secs)) + ' seconds')
        print('downloading backup archive to local storage')
        sshdownload('/tmp/bck.tar', '/tmp/bck.tar')
        print('encrypting archive locally with GPG')
        with open('/tmp/bck.tar', 'rb') as f:
            status = gpg.encrypt_file(
                f, recipients=['lnuser@bitclouds.sh'],
                output='/tmp/clightning.tar.gpg')
        print('clean & upload encrypted archive to server')
        os.remove('/tmp/bck.tar')
        sshupload('/tmp/clightning.tar.gpg', '/tmp/clightning.tar.gpg')
        print('uploading archive to node')
        randnum = random.randrange(100,999)
        fname = 'cln-' + str(randnum) + '-' + str(datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S.tar.gpg'))
        print(sshcmd('', default_vps['ssh_port'], 'scp /tmp/clightning.tar.gpg ipfs:/tmp/'+fname))
        print('uploading to ipfs server')
        ipfs_out = sshcmd('', default_vps['ssh_port'], 'ssh ipfs "/usr/local/bin/ipfs-go add /tmp/'+fname+'"')
        print('uploading to web servers')
        print(sshcmd('', default_vps['ssh_port'], 'scp /tmp/clightning.tar.gpg web:/usr/local/www/nginx/backups/' + fname))

        m = re.search('added ([a-zA-Z0-9]+) cln', ipfs_out)
        ipfs_hash = m.group(1)
        print(' ###### HERE IS YOUR BACKUP ######\n\n')
        print(' # Clearnet URL: https://bitbsd.org/backups/' + fname)
        print(' # IPFS: https://bitclouds.link/ipfs/' + ipfs_hash)
        print(' # Onion: http://http://carnikavazp6djqx.onion/' + fname)

        print('\n ######     END OF LINKS    ######')
        print('clean up locally, on node & ipfs')
        os.remove('/tmp/clightning.tar.gpg')
        print(sshcmd('', default_vps['ssh_port'], 'rm -f /tmp/clightning.tar.gpg'))
        print(sshcmd('', default_vps['ssh_port'], 'ssh ipfs "rm -f /tmp/' + fname + '"'))
        input('seems like we finished! press any key...')
        return True


def doimport():
    ssh_port = input('enter ssh port: ')
    ssh_pwd = input('enter ssh password: ')
    host_name = input('enter host name: ')
    vps = getvps(host_name)

    print('Now we do stuff!')
    global vpslist
    print('Fetching sparko keys...')
    cln_config = sshcmd(ssh_pwd, ssh_port, 'cat /usr/home/lightning/.lightning/config')
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
    with open(workdir + "/pwd.tmp", "w") as text_file:
        text_file.write(vps['ssh_pwd'])
    os.system('sshpass -f ' + workdir + '/pwd.tmp ssh-copy-id -i' + sshkey + ' -o "StrictHostKeyChecking=no" lightning@bitbsd.org -p' + str(vps['ssh_port']))
    os.remove(workdir + "/pwd.tmp")

    pwd = '1'
    pwd2 = '2'
    while not (pwd == pwd2) and (pwd != '') and (len(pwd) < 6):
        pwd = input("Enter new password for instance (REQUIRED):")
        pwd2 = input("Re-enter new password for instance (REQUIRED):")
        if pwd != pwd2:
            print('Password mismatch or too short! re-try again...')
    if pwd == pwd2:
        vps['ssh_pass'] = pwd

    print('Saving host...')
    vpslist.append(vps)
    if len(vpslist) == 1:
        global default_node
        default_node = vps['address']
    savevps()
    input('Node ' + vps['address'] + ' created! You need to restart Watchtower to apply changes...')
    return True


def debackup():
    gpg = gnupg.GPG(gpgdir)
    path = input('enter filename path: ')
    with open(path, 'rb') as f:
        dtime = datetime.datetime.strftime(datetime.datetime.now(), '%y%m%d-%H:%M:%S')
        output_path = os.getenv("HOME") + "/CLN-BACKUP-"+dtime+".tar"
        status = gpg.decrypt_file(f, passphrase='my passphrase', output=output_path)

        print('ok: ', status.ok)
        print('status: ', status.status)
        print('stderr: ', status.stderr)
    input('your backup file is in ' + os.getenv("HOME") + '/CLN-BACKUP.tar | Press any key to continue...')
    return output_path


def devinfo():
    global default_vps
    menu = MultiSelectMenu("curl -X POST "+default_vps['sparko'] + " \ ",
                           " -d '{\"method\": \"getinfo\"}' -H 'X-Access: grabyourkeyinside'",
                           epilogue_text=('ssh lightning@bitbsd.org -p '+ str(default_vps['ssh_port']) + ' -i ' + sshkey),
                           exit_option_text='Go back')  # Customize the exit text

    command_item = CommandItem("Connect via SSH", 'ssh lightning@bitbsd.org -p ' + str(default_vps['ssh_port']) + ' -i ' + sshkey)
    menu.append_item(command_item)
    menu.start()
    menu.join()


def genmenu():
    topic = "BitClouds.sh - Open-source VPS platform"
    header = "This is Bitcoin CLI wallet with LN support, choose an option:"
    menu = ConsoleMenu(topic, header)

    get_summary = FunctionItem("Wallet", summary)
    do_backup = FunctionItem("Perform cold backup", dobackup)
    dev_info = FunctionItem("RPC / SSH access", devinfo)
    decrypt_backup = FunctionItem("Decrypt backup", debackup)
    do_import = FunctionItem("Import BitBSD c-lightning jail", doimport)
    create_item = FunctionItem("Create new node", newnode)

    # Create the menu
    if len(vpslist) > 0:
        menu.append_item(get_summary)
        menu.append_item(dev_info)
        menu.append_item(do_backup)
    menu.append_item(setdef(menu, default_node))
    menu.append_item(decrypt_backup)
    menu.append_item(do_import)
    menu.append_item(create_item)

    # Finally, we call show to show the menu and allow the user to interact
    menu.show()


def main():
    keys = bc_init()
    #print('working with ssh key: ' + keys['ssh']['public'])
    #print('working with gpg key: ' + str(keys['gpg']['fingerprint']))
    initdefvps()

    try:
        sparko_host = default_vps['sparko']
        key = default_vps['sparko_master']
        num = 1
        cmd = sys.argv[num]
        params = list()

        while num < 10:
            num += 1
            try:
                params.append(sys.argv[num])
            except IndexError as e:
                pass
        payload = {
                'method': cmd,
                "params": params
            }

        if cmd is not 'getinfo':
            payload['params'] = params

        cmd = 'curl -ks '+sparko_host+' -d \'{"method":"'+ cmd +'", "params": '+str(params).replace("'", "\"")+'}\' -H \'X-Access: '+key+'\''

        response = json.loads(os.popen(cmd).read())
        result = json.dumps(response,sort_keys=True, indent=4)
        print(result)
    except Exception:
        genmenu()

if __name__ == "__main__":
    main()