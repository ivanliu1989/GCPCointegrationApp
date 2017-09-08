#!/usr/bin/python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas
#import connecttodb

def normalise_windows(window_data,firstdata):
    normalised_data = []
    n = firstdata
    if n == 0:
        n = 1
    for window in window_data:
        normalised_window = ((float(window) / float(n)) - 1)
        normalised_data.append(normalised_window)
    return normalised_data

def denormalise_windows(d0,window_data):
    denormalised_data = []
    for p in window_data:
        denormalised_window = (float(d0) * (float(p) + 1))
        denormalised_data.append(denormalised_window)
    return denormalised_data

def drawchart(df,dftest,datefrom,dateto,hedgingratio,pvalue,coeff1,coeff2):

    c1 = df.columns[0]
    c2 = df.columns[1]
    totaldf = df.append(dftest, ignore_index=True)
    totaldfn = pandas.DataFrame()
    totaldfn[c1] = normalise_windows(totaldf[c1],totaldf[c1][0])
    totaldfn[c2] = normalise_windows(totaldf[c2],totaldf[c2][0])
    #totaldfn = totaldf
    dfn = totaldfn.head(len(df))
    dftestn = totaldfn.tail(len(dftest))
    #dfn = pandas.DataFrame()
    #dftestn = pandas.DataFrame()
    #dfn[c1] = normalise_windows(df[c1],df[c1][0])
    #dfn[c2] = normalise_windows(df[c2],df[c2][0])
    #dftestn[c1] = normalise_windows(dftest[c1])
    #dftestn[c2] = normalise_windows(dftest[c2])
    vec = [coeff1,coeff2]

    f, ax = plt.subplots(3, 1, figsize=(18, 6), sharex=True)
    ax[0].set_title("Currency pairs: "+c1+' from '+datefrom+' to '+dateto)
    ax[1].set_title("Currency: "+c2+' from '+datefrom+' to '+dateto)
    ax[2].set_title("P value of cointegration between "+c1+' and '+c2+' is '+str(pvalue)+' over last '+str(len(df))+' points with a hedging ratio of '+str(hedgingratio))

    x1 = dfn.as_matrix()
    in_sample = np.dot(x1, vec)
    x2 = totaldfn.as_matrix()
    in_test = np.dot(x2,vec)
    mean = np.mean(in_sample)
    std = np.std(in_sample)
    
    ma = dftestn.as_matrix()

    v1 = []
    v2 = []
    for i in range(len(ma)):
        v1.append((mean-(coeff2*ma[i][1]))/coeff1)
        v2.append((mean-(coeff1*ma[i][0]))/coeff2)
    predict_x = ''
    predict_y = ''
    if in_sample[len(in_sample)-1] > mean:
        if(vec[0]>0):
            predict_x = 'down'
        else:
            predict_x = 'up'
        if(vec[1]>0):
            predict_y = 'down'
        else:
            predict_y = 'up'
    else:
        if(vec[0]>0):
            predict_x = 'up'
        else:
            predict_x = 'down'
        if(vec[1]>0):
            predict_y = 'up'
        else:
            predict_y = 'down'
    
    ax[0].plot(range(len(totaldfn)), totaldfn[c1], 'b', label=c1)
    #ax02 = ax[0].twinx()
    ax[1].plot(range(len(totaldfn)), totaldfn[c2], 'r', label=c2)
    #ax[0].plot(range(len(totaldf)), totaldf[c2], 'r', label=c2)
    #ax[0].plot(range(0,10),dftest[c1], label='predited '+c1)

    ax[0].plot(len(df)-1, totaldfn[c1][len(df)-1], 'go', label='cointegrated point', alpha=.5)
    ax[0].text(len(df)+2, totaldfn[c1][len(df)-1], predict_x)
    ax[1].plot(len(df)-1, totaldfn[c2][len(df)-1], 'go', label='cointegrated point', alpha=.5)
    ax[1].text(len(df)+2, totaldfn[c2][len(df)-1], predict_y)
    #ax[0].plot(range(len(df),len(dftest)+len(df)), v1, 'b', ls='--', label='predited '+c1, alpha=.5)
    #ax[1].plot(range(len(df),len(dftest)+len(df)), v2, 'r', ls='--', label='predited '+c2, alpha=.5)
    ax[0].legend()
    ax[1].legend()
    # Plot the mean and one std above and below it.
    ax[2].axhline(y=mean - std, color='y', ls='--', alpha=.5)
    ax[2].axhline(y=mean, color='g', ls='--', alpha=.5)
    ax[2].axhline(y=mean + std, color='y', ls='--', alpha=.5)
    ax[2].plot(range(len(in_sample)),in_sample, label="spreads")
    ax[2].plot(range(len(dfn)-1,len(in_test)),in_test[len(dfn)-1:], label="prediction", color='r', ls='--', alpha=.5)
    ax[2].legend()
    if vec[0] == 1:
        if vec[1] > 0:
            ax[1].text(0, mean + std, 'Spreads: '+c1+'+'+str(round(vec[1],3))+'*'+c2)
        else:
            ax[1].text(0, mean + std, 'Spreads: '+c1+''+str(round(vec[1],3))+'*'+c2)
    else:
        ax[1].text(0, mean + std, 'Spreads: '+str(round(vec[0],3))+'*'+c1+'+'+c2)
    ax[2].text(0,mean,"Eigenvector :"+str(vec))
    ax[0].grid()
    ax[1].grid() 
    ax[2].grid() 
    plt.xticks(np.arange(0, len(totaldf)+1, 10.0))
    
    f.savefig('/home/piyapong/cointegration/img/'+c1+'_'+c2+'_'+dateto+'.png')
    public_url = savefile(c1+'_'+c2+'_'+dateto,'/home/piyapong/cointegration/img/'+c1+'_'+c2+'_'+dateto+'.png')
    print (public_url)
    plt.close(f)
    plt.close('all')
    return public_url,predict_x,predict_y,datefrom,dateto
    #connecttodb.updateforecast(public_url,predict_x,predict_y,datefrom,dateto)

def savefile(destination_blob_name,source_file_name):
   # Imports the Google Cloud client library
   from google.cloud import storage
   # Instantiates a client
   storage_client = storage.Client()
   bucket = storage_client.get_bucket('pong-cointegration')
   blob = bucket.blob(destination_blob_name)
   blob.upload_from_filename(source_file_name)
   blob.make_public()
   return blob.public_url



