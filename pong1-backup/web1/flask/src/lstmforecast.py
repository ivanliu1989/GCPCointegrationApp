import pandas
import lstmlib.lstm as lstmclass
from keras.models import load_model
import lstmlib.cusum as cumsum
import lib.getpair as getpair
from google.cloud import datastore
from datetime import datetime

#instrument = 'EUR_USD'
seq_length = 50
buff = 5
normalise_window = False

def createmodel(instrument):
	df = getpair.getalldata(instrument)
	df = df.dropna()
	
	#use dummy data to train a LSTM model and save the model to a path
	path = '/home/piyapong/public_html/flask/src/model/'+instrument+'.h5'
	print('Save a lstm model to: '+path)
	
	lstmclass.savemodel(df[instrument].values, path, normalise_window, epochs=1, seq_len=seq_length)

def predict(instrument,lookback):
	
	df = getpair.getsomedata(instrument,seq_length+lookback+buff)
	test = df.dropna()
	test = test.head(seq_length+lookback)
	if len(test) == seq_length+lookback:
		date = test.tail(lookback)['time'].values
		
		#Prepare test data to predict
		X_test, y_test = lstmclass.gettestdata(test[instrument].values, normalise_window, seq_length)
		
		path = '/home/piyapong/public_html/flask/src/model/'+instrument+'.h5'
		model = load_model(path)
		
		#get square error of actual vs predicted values
		predictions,se = lstmclass.predicttestdata(X_test,y_test,model)
		client = datastore.Client()
		key = client.key(instrument+'_lstm')
		
		for i in range(len(date)):
			entity = datastore.Entity(key=key)
			entity['time'] = datetime.fromtimestamp(date[i])
			entity['actual_value'] = float(y_test[i])
			entity['predicted_value'] = float(predictions[i])
			entity['square_error'] = float(se[i])
			client.put(entity)

	
#import sys

#name of the script = sys.argv[0]
#instrument = sys.argv[1]
#createmodel(instrument)
#predict('EUR_USD',1)



