import sys
from oandapyV20 import API
from oandapyV20.endpoints.pricing import PricingInfo
from google.cloud import datastore
from datetime import datetime

accountID = "101-011-6029361-001"
access_token="8153764443276ed6230c2d8a95dac609-e9e68019e7c1c51e6f99a755007914f7"
api = API(access_token=access_token, environment="practice")

# get current data from oanda
# example: getdata.py DE30_EUR,EUR_USD,EUR_JPY
#instruments = "DE30_EUR,EUR_USD,EUR_JPY"
instruments = ''

if len(sys.argv) < 2:
    print ('Require 1 argv: a list of instrument separated with comma')
    print ('Example: python getdata.py DE30_EUR,EUR_USD,EUR_JPY')
else:
    instruments = sys.argv[1]
    r = PricingInfo(accountID=accountID, params={"instruments":instruments})
    rv = api.request(r)
    print (rv['time'])
    client = datastore.Client()
    for i in rv['prices']:
        if i['type'] == 'PRICE':
            key = client.key(i['instrument'])
            entity = datastore.Entity(key=key)
            entity['time'] = datetime.strptime(i['time'][:19], "%Y-%m-%dT%H:%M:%S")
            entity['closeoutBid'] = i['closeoutBid']
            client.put(entity)
            print ('Put entity')

