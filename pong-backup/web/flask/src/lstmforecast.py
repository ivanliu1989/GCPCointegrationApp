import pandas
import lstmlib.lstm as lstmclass
from keras.models import load_model
import lstmlib.cusum as cumsum
import lib.getpair as getpair
from google.cloud import datastore
from datetime import datetime
import lib.bulkloaddata as bulkloaddata

#instrument = 'EUR_USD'
# lstm fragment length to train and test data 
seq_length = 100
# query buffer
buff = 5
# normalise start point of the data series to zero
normalise_window = True

def createmodel(instrument):
	# load a dataset to train a lstm model and save the trained model to a directory
	df = getpair.getalldata(instrument)
	df = df.dropna()
	
	#use dummy data to train a LSTM model and save the model to a path
	path = '/home/piyapong/public_html/flask/src/model/'+instrument+'.h5'
	print('Save a lstm model to: '+path)
	
	lstmclass.savemodel(df[instrument].values, path, normalise_window, epochs=1, seq_len=seq_length)

def predict(instrument,lookback):
	# load a lstm model to predict one test set
	df = getpair.getsomedata(instrument,seq_length+lookback+buff)
	test = df.dropna()
	test = test.head(seq_length+lookback)
	test = test.sort_values(by='time', ascending=1)
	testvalue = test[instrument].iloc[seq_length-1:seq_length+lookback-1]
	print(test)
	if len(test) == seq_length+lookback:
		date = test.tail(lookback)['time'].values
		
		#Prepare test data to predict
		X_test, y_test = lstmclass.gettestdata(test[instrument].values, normalise_window, seq_length)
		#print(X_test)
		print(y_test)
		path = '/home/piyapong/public_html/flask/src/model/'+instrument+'.h5'
		model = load_model(path)
		
		#get square error of actual vs predicted values
		predictions,se = lstmclass.predicttestdata(X_test,y_test,model)

		client = datastore.Client()
		key = client.key(instrument+'_lstm')
		
		for i in range(len(date)):
			entity = datastore.Entity(key=key)
			entity['time'] = datetime.fromtimestamp(date[i])
			entity['actual_value'] = float(testvalue.iloc[i])
			entity['predicted_value'] = float(predictions[i])
			#entity['square_error'] = float(se[i])
			client.put(entity)
			print(str(datetime.fromtimestamp(date[i])))

def bulkpredict(instrument,granularity,lookback):
	# load a lstm model to predict many test sets
	df = bulkloaddata.bulkloadlivedata(instrument,granularity,seq_length+lookback+buff)
	test = df.dropna()
	test = test.sort_values(by='time', ascending=1)
	l = len(test)
	testvalue = test[instrument].iloc[100:l]
	date = test['time'].iloc[100:l]

	#Prepare test data to predict
	X_test, y_test = lstmclass.gettestdata(test[instrument].values, normalise_window, seq_length)

	path = '/home/piyapong/public_html/flask/src/model/'+instrument+'.h5'
	model = load_model(path)
	
	#get square error of actual vs predicted values
	predictions,se = lstmclass.predicttestdata(X_test,y_test,model)

	client = datastore.Client()
	key = client.key(instrument+'_lstm')

	for i in range(len(predictions)):
		entity = datastore.Entity(key=key)
		entity['time'] = datetime.strptime(date.iloc[i][:19], "%Y-%m-%dT%H:%M:%S")
		entity['actual_value'] = float(testvalue.iloc[i])
		entity['predicted_value'] = float(predictions[i])
		#entity['square_error'] = float(se[i])
		client.put(entity)
		print(str(date.iloc[i][:19]))

# example
#import sys

#name of the script = sys.argv[0]
#instrument = sys.argv[1]
#createmodel(instrument)
#predict('EUR_USD',1)



