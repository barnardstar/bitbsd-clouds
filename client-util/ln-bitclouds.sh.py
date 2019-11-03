import os
import gnupg

homedir = os.getenv("HOME")+'/.bitclouds'
keydir = homedir + '/keys'
sshdir = keydir + "/ssh"
gpgdir = keydir + "/gpg"
sshkey = sshdir + '/ssh.key'

workdir = homedir+'/ln'


def bc_init():
    print(os.path.exists(homedir))

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
        print('Generating ssh keys.. :' + sshdir + '/ssh.key')

        os.system('ssh-keygen -b 521 -t ecdsa -f ' + sshkey + ' -q -N ""')
        keys['ssh']['private'] = sshkey
        keys['ssh']['public'] = sshkey+'.pub'
        os.makedirs(gpgdir)

        gpg = gnupg.GPG(gnupghome=keydir + '/gpg')
        input_data = gpg.gen_key_input(
            name_email='ln@bitclouds.sh'
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

    return keys


keys = bc_init()
print('working with ssh key: ' + keys['ssh']['public'])
print('working with gpg key: ' + keys['ssh']['public'])







