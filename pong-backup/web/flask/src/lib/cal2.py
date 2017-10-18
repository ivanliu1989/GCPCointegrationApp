#!/usr/bin/python
import matplotlib
# hide plot in a background
matplotlib.use('Agg')
import sys
import matplotlib.pyplot as plt
from johansen import Johansen
import numpy as np
import pandas
import cointegration
import src.lib.connecttodb as connecttodb
from datetime import timedelta
from datetime import datetime

def normalise_windows(window_data):
    # normalise the start point to zero
    normalised_data = []
    n = window_data.iloc[0]
    if n == 0:
        n = 1
    for window in window_data:
        normalised_window = ((float(window) / float(n)) - 1)
        normalised_data.append(normalised_window)
    return normalised_data

def approach2(df,pvalue,datefrom,dateto):
    # calculate cointegration
    ci = 0
    if pvalue == 0.05:
        ci = 1
    elif pvalue == 0.01:
        ci = 2

    c1 = df.columns[0]
    c2 = df.columns[1]

    #pvalue = dftest(merged_inner.iloc[(i-window-1):(i-1)],c1,c2)
    #:param significance_level: Which significance level to use. If set to
    #0, 90% significance will be used. If set to 1, 95% will be used. If set
    #to 2, 99% will be used.

    df[c1] = normalise_windows(df[c1])
    df[c2] = normalise_windows(df[c2])

    p = cointegration.adftest(df.copy())
    #print (p)
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

        return {'instrument1':c1,'instrument2':c2,'from':datefrom,'to':dateto,'public_url':'','hedge_ratio':str(round(hedgingratio,3)),'coeff1':str(vec[0]),'coeff2':str(vec[1]),'p-value':str(round(p,3)),'mean':str(round(mean,6)),'std':str(round(std,6))}
	    
    return None

def savefile(destination_blob_name,source_file_name):
   # Imports the Google Cloud client library
   # save image to a bucket
   from google.cloud import storage
   # Instantiates a client
   storage_client = storage.Client()
   bucket = storage_client.get_bucket('cointegration')
   blob = bucket.blob(destination_blob_name)
   blob.upload_from_filename(source_file_name)
   blob.make_public()
   return blob.public_url




def coint(instrument1,instrument2,lookback,p_value):
    # calculate cointegration and save to the database	
    import src.lib.getpair as getpair
    df,start_date,stop_date = getpair.getpair(instrument1,instrument2,lookback)
    
    if len(df)>=100:
        #stop_date = datetime.utcnow()
        #start_date = stop_date - timedelta(minutes=lookback)
        result = approach2(df,p_value,start_date.strftime("%Y-%m-%d %H:%M:%S"),stop_date.strftime("%Y-%m-%d %H:%M:%S"))
        print (result)
        if result != None:
            connecttodb.insert(instrument1=result['instrument1'],
                instrument2=result['instrument2'],
                datefrom=result['from'],
                dateto=result['to'],
                hedge_ratio=result['hedge_ratio'],
                coeff1=result['coeff1'],
                coeff2=result['coeff2'],
                mean=result['mean'],
                std=result['std'],
                p_value=result['p-value'],
                public_url=result['public_url'],
                user_review='',
                predict_x='',
                predict_y='')

def bulkcoint(instrument1,instrument2,lookback,p_value):
    # calculate bulk cointegration and save to the database	
    import src.lib.getpair as getpair
    for i in range(3000):
        stopdate = datetime.utcnow() - timedelta(minutes=i*15)

        df,start_date,stop_date = getpair.getpairbystopdate(instrument1,instrument2,stopdate,lookback)

        if len(df)>=100:
            
            result = approach2(df,p_value,start_date.strftime("%Y-%m-%d %H:%M:%S"),stop_date.strftime("%Y-%m-%d %H:%M:%S"))
            print (result)
            if result != None:
                connecttodb.insert(instrument1=result['instrument1'],
                    instrument2=result['instrument2'],
                    datefrom=result['from'],
                    dateto=result['to'],
                    hedge_ratio=result['hedge_ratio'],
                    coeff1=result['coeff1'],
                    coeff2=result['coeff2'],
                    mean=result['mean'],
                    std=result['std'],
                    p_value=result['p-value'],
                    public_url=result['public_url'],
                    user_review='',
                    predict_x='',
                    predict_y='')



#name of the script = sys.argv[0]
#instrument1 = sys.argv[1]
#instrument2 = sys.argv[2]
#lookback = int(sys.argv[3])
#p_value = float(sys.argv[4])

#python cal2.py DE30_EUR EUR_JPY 100 1.00
#coint(intrument1,instrument2,lookback,p_value)
#bulkcoint(instrument1,instrument2,lookback,p_value)
