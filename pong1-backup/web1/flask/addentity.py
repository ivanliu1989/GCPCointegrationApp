import bulkloaddata

granularity = 'M15'
start = '2017-08-15T12:51:22Z'
bulkloaddata.bulkloadlivedatabytime('DE30_EUR',granularity,start)
bulkloaddata.bulkloadlivedatabytime('EUR_JPY',granularity,start)
bulkloaddata.bulkloadlivedatabytime('EUR_USD',granularity,start)
