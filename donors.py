import requests, json, time
from operator import itemgetter
from threading import Timer

config = json.load(open('config.txt', 'r'))

def update_dons():
    while(True):
        
        config = json.load(open('config.txt', 'r'))
        
        if config['vertical']:
            config['pattern'] += '\n'
        else:
            config['pattern'] += config['horizontal_separator']


        url = "https://streamlabs.com/api/donations"
        querystring = {"access_token" : config['token']}
        response = requests.request("GET", url, params=querystring)

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
                tabledons.append("★★★ ★★★ ★★★ ★★★\n")

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