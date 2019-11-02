import sys
import requests

# 2019/11/02 21:09:49 plugin-sparko Keys read: Md6c395d1bdf1e638 (full-access), R367a8b0cb6e330d6 (2 whitelisted), RW46b456208941cc9c (6 whitelisted)

sparko_host = 'https://bitbsd.org:59999/rpc'
key = 'RW481ccb4599629c60'

cmd = sys.argv[1]
param = sys.argv[2]

payload = {
        'method': cmd,
        'params': param
    }

print('lightning-cli ' + cmd + ' ' + param)
invoice_info_request = requests.post(sparko_host, headers={'X-Access': key}, data=payload, verify=False)

if invoice_info_request.status_code == 200:
    print(invoice_info_request.json())
