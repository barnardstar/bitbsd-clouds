import requests
import time
import datetime


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

