import sys
import requests

# 2019/11/02 21:09:49 plugin-sparko Keys read: Md6df1e638c395d1b (full-access), R367a8330d6b0cb6e (2 whitelisted), RW48941cc9c6b45620 (6 whitelisted)

sparko_host = 'https://bitbsd.org:59469/rpc'
key = 'RW48941cc9c6b45620'

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
