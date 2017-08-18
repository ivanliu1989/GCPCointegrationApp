from google.cloud import datastore
from datetime import datetime

client = datastore.Client()
#key = client.key('cointegration')
#entity = datastore.Entity(key=key)
#now  = datetime.utcnow()
#entity['from'] = now

#client.put(entity)

#print ('Put data at time : '+str(now))
query = client.query(kind='S5')
result = list(query.fetch())
for i in result:
	print (i['instrument1'])
