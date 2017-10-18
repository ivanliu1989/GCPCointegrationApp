import src.lib.getpair as getpair
import src.lib.connecttodb as connecttodb

def updatestat(kind):
	# update mu (mean of total dataset) to the database
	df = getpair.getalllstmdata(kind)
	mean = df['predicted_value'].mean()
	connecttodb.updatelstmstat(kind,mean)
		
updatestat('EUR_USD')
updatestat('AUD_USD')
updatestat('GBP_USD')