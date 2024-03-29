from google.cloud import datastore
import pandas
from datetime import timedelta
from datetime import datetime

def getdata(client,kind,lookback):
    #get data with limit number of result
    #stop_date = datetime.utcnow()
    #start_date = stop_date - timedelta(minutes=lookback)
    query = client.query(kind=kind)
    query.distinct_on = ['time']
    query.order = ['-time']
    #query.add_filter('time', '>=',start_date)
    #query.add_filter('time', '<=',stop_date)
    value = []
    time = []
    tasks = list(query.fetch(limit=lookback))
    for i in tasks:
        value.append(i['closeoutBid'])
        time.append(i['time'])
    
    return value,time[len(time)-1],time[0]
def getdatabystopdate(client,kind,dateto,lookback):
    #	get data with limit number of result and dateto
    query = client.query(kind=kind)
    query.distinct_on = ['time']
    query.order = ['-time']
    query.add_filter('time', '<=',dateto)
    value = []
    time = []
    tasks = list(query.fetch(limit=lookback))
    for i in tasks:
        value.append(i['closeoutBid'])
        time.append(i['time'])
    
    return value,time[len(time)-1],time[0]
def getdatabydate1(client,kind,datefrom,dateto,lookback):
    #get data with limit number of result, datefrom and dateto
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
def getdatabydate2(client,kind,datefrom,dateto):
	#get data within datefrom and dateto
	query = client.query(kind=kind)
	query.distinct_on = ['time']
	query.order = ['time']
	query.add_filter('time', '>=',datefrom)
	query.add_filter('time', '<=',dateto)
	value = []
	time = []
	tasks = list(query.fetch())
	for i in tasks:
		value.append(i['closeoutBid'])
		time.append(i['time'].timestamp())
	df = pandas.DataFrame({'time_'+kind:time,kind: value})
	df = df.dropna()
	df = df.apply(pandas.to_numeric, errors='ignore')
	return df
    
def getdatabydate3(kind,datefrom,dateto):
	#get data within datefrom and dateto
	client = datastore.Client()
	query = client.query(kind=kind)
	query.distinct_on = ['time']
	query.order = ['time']
	query.add_filter('time', '>=',datefrom)
	query.add_filter('time', '<=',dateto)
	value = []
	time = []
	tasks = list(query.fetch())
	
	for i in tasks:
		value.append(i['closeoutBid'])
		time.append(i['time'].timestamp())
	df = pandas.DataFrame({'time':time,kind: value})
	df = df.dropna()
	df = df.apply(pandas.to_numeric, errors='ignore')
	return df

def getalldata(kind):
    #get data by instrument
    client = datastore.Client()
    query = client.query(kind=kind)
    query.distinct_on = ['time']
    query.order = ['time']
    value = []
    time = []
    tasks = list(query.fetch())

    for i in tasks:
        value.append(i['closeoutBid'])
        time.append(i['time'].timestamp())
    df = pandas.DataFrame({'time':time,kind: value})
    df = df.dropna()
    df = df.apply(pandas.to_numeric, errors='ignore')
    return df
    
def getsomedata(kind,lookback):
    #get data by instrument with lookback
    client = datastore.Client()
    query = client.query(kind=kind)
    query.distinct_on = ['time']
    # - = sort by descending
    query.order = ['-time']
    value = []
    time = []
    tasks = list(query.fetch(limit=lookback))

    for i in tasks:
        value.append(i['closeoutBid'])
        time.append(i['time'].timestamp())
    df = pandas.DataFrame({'time':time,kind: value})
    df = df.dropna()
    df = df.apply(pandas.to_numeric, errors='ignore')
    return df
    
def getpair(instrument1,instrument2,lookback):
    #get data of two instruments with lookback
    client = datastore.Client()
    v1,startdate1,enddate1 = getdata(client,instrument1,lookback)
    v2,startdate2,enddate2 = getdata(client,instrument2,lookback)
    df1 = pandas.DataFrame({instrument1: v1})
    df2 = pandas.DataFrame({instrument2: v2})
    df = pandas.concat([df1,df2],axis=1)
    df = df.dropna()
    df = df.apply(pandas.to_numeric, errors='ignore')

    startdate = ''
    enddate = ''
    if startdate1<startdate2:
    	startdate = startdate1
    else:
    	startdate = startdate2
    if enddate2<enddate1:
    	enddate = enddate1
    else:
    	enddate = enddate2

    return df,startdate,enddate
    
def getpairbystopdate(instrument1,instrument2,dateto,lookback):
    #get data of two instruments by dateto and lookback
    client = datastore.Client()
    v1,startdate1,enddate1 = getdatabystopdate(client,instrument1,dateto,lookback)
    v2,startdate2,enddate2 = getdatabystopdate(client,instrument2,dateto,lookback)
    df1 = pandas.DataFrame({instrument1: v1})
    df2 = pandas.DataFrame({instrument2: v2})
    df = pandas.concat([df1,df2],axis=1)
    df = df.dropna()
    df = df.apply(pandas.to_numeric, errors='ignore')
    
    startdate = ''
    enddate = ''
    if startdate1<startdate2:
    	startdate = startdate1
    else:
    	startdate = startdate2
    if enddate2<enddate1:
    	enddate = enddate1
    else:
    	enddate = enddate2
    	
    return df,startdate,enddate
    
def getpairbydate1(instrument1,instrument2,datefrom,dateto,lookback):
    #get data of two instruments by datefrom, dateto, and lookback
    client = datastore.Client()
    v1 = getdatabydate1(client,instrument1,datefrom,dateto,lookback)
    v2 = getdatabydate1(client,instrument2,datefrom,dateto,lookback)
    df1 = pandas.DataFrame({instrument1: v1})
    df2 = pandas.DataFrame({instrument2: v2})
    df = pandas.concat([df1,df2],axis=1)
    df = df.dropna()
    df = df.apply(pandas.to_numeric, errors='ignore')
    return df
    
def getpairbydate2(instrument1,instrument2,datefrom,dateto):
    #get data of two instruments between datefrom and dateto
    client = datastore.Client()
    df1 = getdatabydate2(client,instrument1,datefrom,dateto)
    df2 = getdatabydate2(client,instrument2,datefrom,dateto)
    df = pandas.concat([df1,df2],axis=1)
    df = df.dropna()
    df = df.apply(pandas.to_numeric, errors='ignore')
    return df
    
def getlstmdata(kind,start,end):
    #get lstm data by instrument, start, end
    client = datastore.Client()
    query = client.query(kind=kind+'_lstm')
    query.distinct_on = ['time']
    query.add_filter('time', '>=',start)
    query.add_filter('time', '<=',end)
    # - = sort by descending
    query.order = ['-time']
    actual_value = []
    predicted_value = []
    time = []
    tasks = list(query.fetch())
    for i in tasks:
        actual_value.append(i['actual_value'])
        predicted_value.append(i['predicted_value'])
        time.append(i['time'].timestamp())
    
    df = pandas.DataFrame({'actual_value':actual_value,'predicted_value': predicted_value, 'time':time})
    df = df.dropna()
    df = df.apply(pandas.to_numeric, errors='ignore')
    return df
    #df1 = getdatabydate2(client,kind,start,end)
    #df1.rename(columns={'time_'+kind:'time'}, inplace=True)
    #result = pandas.merge(df, df1, on='time', how='inner')
    #return result
    
def getalllstmdata(kind):
    #get all lstm data by instrument
    client = datastore.Client()
    query = client.query(kind=kind+'_lstm')
    query.distinct_on = ['time']
    # - = sort by descending
    query.order = ['-time']
    actual_value = []
    predicted_value = []
    time = []
    tasks = list(query.fetch())
    for i in tasks:
        actual_value.append(i['actual_value'])
        predicted_value.append(i['predicted_value'])
        time.append(i['time'].timestamp())
    
    df = pandas.DataFrame({'actual_value':actual_value,'predicted_value': predicted_value, 'time':time})
    df = df.dropna()
    df = df.apply(pandas.to_numeric, errors='ignore')
    return df
#getpair('EUR_JPY','EUR_USD',15)
