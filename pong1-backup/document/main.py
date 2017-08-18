#!/usr/bin/python
import matplotlib
matplotlib.use('Agg')
from google.cloud import datastore
from datetime import datetime
import cointegration
import matplotlib.pyplot as plt
from johansen import Johansen
import numpy as np
import pandas
#import matplotlib.pyplot as plt
#import matplotlib
#matplotlib.use('Agg')

print ('Update Entity')

# Create, populate and persist an entity
#date_format = "%Y-%m-%d %H:%M:%S"
#datefrom = datetime.strptime('2017-01-03 04:25:38', date_format)
'''
client = datastore.Client()
key = client.key('cointegration')
entity = datastore.Entity(key=key)
entity['forex1'] = u'USD_AUD'
entity['forex2'] = u'USD_CAD'
entity['duration'] = u'D'
entity['from'] = u'2017-01-03 00:00:00'
entity['to'] = u'2017-05-02 00:00:00'
entity['hedge_ratio'] = 2.3063
entity['p-value'] = 0.001
entity['mean'] = 2.0132
entity['std'] = 0.0214
client.put(entity)
'''

def normalise_windows(window_data):
    normalised_data = []
    n = window_data[0]
    if n == 0:
        n = 1
    for window in window_data:
        normalised_window = ((float(window) / float(n)) - 1)
        normalised_data.append(normalised_window)
    return normalised_data

def approach1(df,c1,c2,npair,window,pvalue,datefrom,dateto):
    ci = 0
    if pvalue == 0.05:
        c1 = 1
    elif pvalue == 0.01:
        ci = 2
    last = 0
    colist = []
    #collection = []
    

    #for i in range(len(df.index)):
        #if i-window-1>=0 and i>=last:
            #pvalue = dftest(merged_inner.iloc[(i-window-1):(i-1)],c1,c2)
            #:param significance_level: Which significance level to use. If set to
            #0, 90% significance will be used. If set to 1, 95% will be used. If set
            #to 2, 99% will be used.
            #df1 = df.iloc[(i-window-1):(i-1)]
    df[c1] = normalise_windows(df[c1])
    df[c2] = normalise_windows(df[c2])

    p = cointegration.adftest(df.copy())

    if p <= pvalue:
        x1 = df.as_matrix()
        x_centered1 = x1 - np.mean(x1, axis=0)
        johansen1 = Johansen(x_centered1, model=2, significance_level=ci)
        eigenvectors, r = johansen1.johansen()
        #print (str(p)+' '+str(len(r)))
        vec = eigenvectors[:, 0]
        vec_min = np.min(np.abs(vec))
        vec = vec / vec_min
        in_sample = np.dot(x1, vec)

        mean = np.mean(in_sample)
        std = np.std(in_sample)
        hedgingratio = 1
        if vec[0] != 1 and vec[0] != -1:
            hedgingratio = vec[0]
        elif vec[1] != 1 and vec[1] != -1:
            hedgingratio = vec[1]
        
        f, ax = plt.subplots(npair, 1, figsize=(18, 6), sharex=True)

        ax[0].set_title("Currency pairs: "+c1+' and '+c2+' from '+datefrom+' to '+dateto)
        hedgingratio = 1
        if vec[0] != 1 and vec[0] != -1:
            hedgingratio = vec[0]
        elif vec[1] != 1 and vec[1] != -1:
            hedgingratio = vec[1]
        ax[1].set_title("P value of cointegration between "+c1+' and '+c2+' is '+str(round(p,3))+' over last '+str(window)+' points with a hedging ratio of '+str(round(hedgingratio,3)))

        ax[0].plot(range(len(in_sample)), df[c1], label=c1)
        ax[0].plot(range(len(in_sample)), df[c2], label=c2)
        ax[0].legend()
        # Plot the mean and one std above and below it.
        ax[1].axhline(y=mean - std, color='y', ls='--', alpha=.5)
        ax[1].axhline(y=mean, color='g', ls='--', alpha=.5)
        ax[1].axhline(y=mean + std, color='y', ls='--', alpha=.5)
        ax[1].plot(range(len(in_sample)),in_sample, label="spreads")
        ax[1].legend()
        if vec[0] == 1:
            if vec[1] > 0:
                ax[1].text(0, mean + std, 'Spreads: '+c1+'+'+str(round(vec[1],3))+'*'+c2)
            else:
                ax[1].text(0, mean + std, 'Spreads: '+c1+''+str(round(vec[1],3))+'*'+c2)
        else:
            ax[1].text(0, mean + std, 'Spreads: '+str(round(vec[0],3))+'*'+c1+'+'+c2)
        ax[1].text(0,mean,"Eigenvector :"+str(vec))
        ax[0].grid() 
        ax[1].grid() 
        plt.xticks(np.arange(0, len(in_sample)+1, 10.0))
        
	#plt.show()
        f.savefig('img/'+c1+'_'+c2+'_'+dateto+'.png')
        public_url = savefile(c1+'_'+c2+'_'+dateto,'img/'+c1+'_'+c2+'_'+dateto+'.png')
                #skip one period when found
                #last = i+window
                
                #a = in_sample.tolist()
                #a.append(1)
                #collection.append(a)
        #'forex1','forex2','hedge_ratio','p-value','mean','std'
        colist.append({'forex1':c1,'forex2':c2,'from':datefrom,'to':dateto,'public_url':public_url,'hedge_ratio':str(round(hedgingratio,3)),'p-value':str(round(p,3)),'mean':str(round(mean,3)),'std':str(round(std,3))})
    return colist




account = "101-011-6029361-001"
access_token="8153764443276ed6230c2d8a95dac609-e9e68019e7c1c51e6f99a755007914f7"
account_type = "practice"
# Register APIs
#oanda = oandapy.API(environment=account_type, access_token=access_token)
# Get historical prices
#hist = oanda.get_history(instrument = "AUD_USD", granularity = "H1", count = 5000, candleFormat = "midpoint")
#print (hist)

from oandapyV20 import API
from oandapyV20.contrib.factories import InstrumentsCandlesFactory
from datetime import datetime
import matplotlib
#hide the figure in background
matplotlib.use('Agg')

def getdata(client,d0,d1):
    
    #d0 = '2016-04-01'
    #d1 = '2017-08-01'
    _from = d0+"T00:00:00Z"
    _to   = d1+"T00:00:00Z"

    list = []

    date_format = "%Y-%m-%d"
    a = datetime.strptime(d0, date_format)
    b = datetime.strptime(d1, date_format)
    delta = b - a

    pvalue = 0.01
    period = 'D'
    currencylist = ['USD','CAD','CHF','CNH','CZK','DKK','HKD','HUF','INR','JPY','MXN','NOK','PLN','SAR','SEK','SGD','THB','TRY','ZAR']
    #http://oanda-api-v20.readthedocs.io/en/latest/oandapyV20.definitions.instruments.html
    #c = definstruments.CandlestickGranularity()
    #print (c[c.H1])

    # The factory returns a generator generating consecutive
    # requests to retrieve full history from date 'from' till 'to'
    totaldf = pandas.DataFrame()
    for i in currencylist:
        for j in currencylist:
            if i!= j:
                instrument, granularity = i+"_"+j, "D"
                params = {"from": _from,"to": _to, "granularity": granularity, "count":delta.days-1}
                name = i+"_"+j
                print (name)
                time = []
                value = []
                for r in InstrumentsCandlesFactory(instrument=instrument,params=params):
                    client.request(r)
                    data = r.response.get('candles')
                    for k in range(len(data)):
                        time.append(data[k]['time'])
                        value.append(data[k]['mid']['c'])
                d = {'time': time, name: value}
                df = pandas.DataFrame(data=d)
                #df.index = df['time']
                #df = df.drop('time',1)
                
                if len(totaldf)==0:
                    totaldf = totaldf.assign(time=df['time'])
                totaldf = totaldf.assign(name=df[name])
                totaldf = totaldf.rename(columns={'name': name})


        totaldf.index = totaldf.time 
        totaldf = totaldf.drop('time',1)
        totaldf = totaldf.apply(pandas.to_numeric, errors='ignore')
        break

    for i in range(len(totaldf.columns)):
        for j in range(len(totaldf.columns)):
            if i!= j:
                cointlist = approach1(totaldf[[totaldf.columns[i],totaldf.columns[j]]],totaldf.columns[i],totaldf.columns[j],2,len(totaldf),pvalue,d0,d1) 
                list.extend(cointlist)
    return list

def savefile(destination_blob_name,source_file_name):
   # Imports the Google Cloud client library
   from google.cloud import storage

   # Instantiates a client
   storage_client = storage.Client()
   bucket = storage_client.get_bucket('cointegration')
   blob = bucket.blob(destination_blob_name)
   blob.upload_from_filename(source_file_name)
   blob.make_public()
   return blob.public_url


                
from datetime import timedelta         
start_date = "2017-02-01"
stop_date = datetime.now().strftime("%Y-%m-%d")
duration = 100

client = API(access_token=access_token)
start = datetime.strptime(start_date, "%Y-%m-%d")
stop = datetime.strptime(stop_date, "%Y-%m-%d")
d0 = (start).strftime("%Y-%m-%d")
d1 = (start + timedelta(days=duration)).strftime("%Y-%m-%d")

df = pandas.DataFrame(columns=('forex1','forex2','from','to','hedge_ratio','p-value','mean','std'))
   
while start < stop:
    if start + timedelta(days=duration)<stop:
        cointlist = getdata(client,(start).strftime("%Y-%m-%d"),(start + timedelta(days=duration)).strftime("%Y-%m-%d"))
        df = df.append(cointlist, ignore_index=True)
    start = start + timedelta(days=1)  # increase day one by one
    break

client = datastore.Client()
key = client.key('cointegration')

column = ['forex1','forex2','from','to','public_url','hedge_ratio','p-value','mean','std']
for row in range(len(df)):
    print ('Insert entity '+str(row))
    entity = datastore.Entity(key=key)
    for i in range(len(column)):
         entity[column[i]] = df.iloc[row][column[i]]
    client.put(entity)
