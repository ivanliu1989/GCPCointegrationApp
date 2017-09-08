import src.lib.bulkloaddata as  bulkloaddata
import sys
import pandas
from oandapyV20 import API
from oandapyV20.contrib.factories import InstrumentsCandlesFactory
from google.cloud import datastore
from datetime import datetime
from datetime import timedelta 
def bulkloaddatatoentity(instrument,granularity,datefrom):

	client = datastore.Client()
 
	#df = bulkloaddata.bulkloadlivedata(instrument,granularity,50000)

	df = bulkloaddata.bulkloadlivedatabytime(instrument,granularity,datefrom)
	print(df)

	for i in range(len(df)):
		key = client.key(instrument)
		entity = datastore.Entity(key=key)
		entity['time'] = datetime.strptime(df.iloc[i]['time'][:19], "%Y-%m-%dT%H:%M:%S")
		entity['closeoutBid'] = df.iloc[i][instrument]
		client.put(entity)
		print(df.iloc[i][instrument])

		
def bulkcoint(instrument1,instrument2,lookback,p_value):
	import src.lib.cal2 as cal2
	import src.lib.savechart as savechart
	cal2.bulkcoint(instrument1,instrument2,lookback,p_value)

#bulkloaddatatoentity('EUR_GBP','M15','2017-08-07T00:00:00Z')

bulkcoint('EUR_USD','EUR_GBP',6000,0.05)