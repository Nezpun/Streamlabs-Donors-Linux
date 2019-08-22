import sys

if sys.version_info[0] < 3:
    print('You need to run this with Python 3')
    sys.exit(1)

import requests
import json, time, os
from operator import itemgetter
from threading import Timer

if os.path.isfile('config.txt'):
    print('Loading configuration')
    config = json.load(open('config.txt', 'r'))
else:
    Error_('Cannot find file config.txt')

def update_dons():
    while(True):

        if config['vertical']:
            config['pattern'] += '\n'
        else:
            config['pattern'] += config['horizontal_separator']

        url = "https://streamlabs.com/api/donations"
        querystring = {"access_token" : config['token']}
        response = requests.request("GET", url, params=querystring)

        if (response.status_code == 401):
            Error_('You not authenticated on Streamlabs. Exiting.')

        if (response.status_code == 403):
            Error_('Server return forbidden response. Exiting.')

        if (response.status_code == 500) or (response.status_code == 503):
            Error_('Server error. Exiting.')

        jsondons = json.loads(response.text)
        tabledons = []
        donpattern = config['pattern']

        donlist = jsondons['donations']
        if config['sorted']:
            donlist = sorted(jsondons['donations'], key = lambda i: float(i['amount']), reverse = True)

        sex_iterator = 0
        for value in donlist:
            if sex_iterator >= config['maxcount']:
                break

            if config['splitter'] and config['vertical']:
                tabledons.append("\xe2\xe2\xe2 \xe2\xe2\xe2 \xe2\xe2\xe2 \xe2\xe2\xe2\n")

            tabledons.append(
                config['pattern'].format(value['donator']['name'], format(float(value['amount']), '.2f'))
            )
            sex_iterator += 1

        with open('donors.txt', 'w', encoding = 'utf-8') as f:
                f.writelines(tabledons)

        print(tabledons)
        f.close()
        time.sleep(30)

Timer(1, update_dons).start()

#
# Display message and quit application
#
def Error_(msg):
    print(msg)
    quit()