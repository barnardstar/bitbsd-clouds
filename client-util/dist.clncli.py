import sys
import requests

# 2019/11/02 21:09:49 plugin-sparko Keys read: Md6c395d1bdf1e638 (full-access), R367a8b0cb6e330d6 (2 whitelisted), RW46b456208941cc9c (6 whitelisted)

sparko_host = 'https://bitbsd.org:59999/rpc'
key = 'RW481ccb4599629c60'

def console():
    num=1

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

    headers = {
        'X-Access': key
    }

    print('lightning-cli ' + cmd + ' ' + str(params))

    cmd = 'curl -ks '+sparko_host+' -d \'{"method":"'+ cmd +'", "params": '+str(params)+'}\' -H \'X-Access: '+key+'\''
    print('executing: ' + cmd)

    response = json.loads(os.popen(cmd).read())
    os.system('clear')
    result = json.dumps(response,sort_keys=True, indent=4)
    print(result)


def libcall(cmd, params):

    payload = {
        'method': cmd,
        "params": params
    }

    if cmd is not 'getinfo':
        payload['params'] = params

    headers = {
        'X-Access': key
    }

    cmd = 'curl -ks ' + sparko_host + ' -d \'{"method":"' + cmd + '", "params": ' + str(
        params) + '}\' -H \'X-Access: ' + key + '\''

    response = json.loads(os.popen(cmd).read())
    return response


try:
    if sys.argv[1]:
        console()
    else:
        pass
except IndexError as e:
    pass


console()

