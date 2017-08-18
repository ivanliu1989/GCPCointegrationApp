from google.cloud import datastore
import pandas
from datetime import timedelta
from datetime import datetime
def getdata(client,kind,lookback):
    
    stop_date = datetime.utcnow()
    start_date = stop_date - timedelta(minutes=lookback)
    query = client.query(kind=kind)
    query.distinct_on = ['time']
    query.order = ['time']
    query.add_filter('time', '>=',start_date)
    query.add_filter('time', '<=',stop_date)
    value = []
    tasks = list(query.fetch(limit=lookback))
    for i in tasks:
        value.append(i['closeoutBid'])
    
    return value
def getdatabydate(client,kind,datefrom,dateto,lookback):
    query = client.query(kind=kind)
    query.distinct_on = ['time']
    query.order = ['time']
    query.add_filter('time', '>=',datefrom)
    query.add_filter('time', '<=',dateto)
    value = []
    tasks = list(query.fetch(limit=lookback))
    for i in tasks:
        value.append(i['closeoutBid'])
    
    return value
def getpair(instrument1,instrument2,lookback):
    client = datastore.Client()
    v1 = getdata(client,instrument1,lookback)
    v2 = getdata(client,instrument2,lookback)
    d = {instrument1: v1, instrument2: v2}
    df = pandas.DataFrame(data=d)
    df = df.dropna()
    df = df.apply(pandas.to_numeric, errors='ignore')
    return df

def getpairbydate(instrument1,instrument2,datefrom,dateto,lookback):
    client = datastore.Client()
    v1 = getdatabydate(client,instrument1,datefrom,dateto,lookback)
    v2 = getdatabydate(client,instrument2,datefrom,dateto,lookback)
    d = {instrument1: v1, instrument2: v2}
    df = pandas.DataFrame(data=d)
    df = df.dropna()
    df = df.apply(pandas.to_numeric, errors='ignore')
    return df
#getpair('EUR_JPY','EUR_USD',15)
