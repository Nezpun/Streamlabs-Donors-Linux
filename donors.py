# coding=UTF-8
import sys

if sys.version_info[0] < 3:
    print('You need to run this with Python 3')
    sys.exit(1)

import requests
import json, time, os
from threading import Timer


#
# Display message and quit application
#
def error_(msg):
    print(msg)
    quit()


#
# Check server response
#
def check_server_response_code(statuscode):
    if statuscode == 401:
        error_('You not authenticated on Streamlabs. Exiting.')

    if statuscode == 403:
        error_('Server return forbidden response. Exiting.')

    if (statuscode == 500) or (statuscode == 503):
        error_('Server error. Exiting.')


if os.path.isfile('config.txt'):
    print('Loading configuration')
    config = json.load(open('config.txt', 'r'))
else:
    error_('Cannot find file config.txt')


def update_dons():
    while True:

        if config['vertical']:
            config['pattern'] += '\n'
        else:
            config['pattern'] += config['horizontal_separator']

        url = "https://streamlabs.com/api/donations"
        querystring = {"access_token": config['token']}
        response = requests.request("GET", url, params=querystring)

        check_server_response_code(response.status_code)

        jsondons = json.loads(response.text)
        tabledons = []
        donpattern = config['pattern']

        donlist = jsondons['donations']
        if config['sorted']:
            donlist = sorted(jsondons['donations'], key=lambda i: float(i['amount']), reverse=True)

        sex_iterator = 0
        for value in donlist:
            if sex_iterator >= config['maxcount']:
                break

            if config['splitter'] and config['vertical']:
                tabledons.append("★★★ ★★★ ★★★ ★★★\n")
            print(value)
            tabledons.append(
                config['pattern'].format(value['donator']['name'], format(value['amount_label']))
            )

            sex_iterator += 1

        with open('donors.txt', 'w', encoding='utf-8') as f:
            f.writelines(tabledons)

        print(tabledons)
        f.close()
        time.sleep(30)


Timer(1, update_dons).start()
