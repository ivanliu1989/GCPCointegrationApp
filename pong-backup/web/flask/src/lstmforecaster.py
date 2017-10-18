import lstmforecast

# create a lstm forecast from the most recent period

lstmforecast.predict('EUR_USD',1)
lstmforecast.predict('AUD_USD',1)
lstmforecast.predict('GBP_USD',1)

# create a 1 year bulk lstm forecast
#lstmforecast.bulkpredict('EUR_USD','M15',530000)
#lstmforecast.bulkpredict('AUD_USD','M15',530000)
#lstmforecast.bulkpredict('GBP_USD','M15',530000)