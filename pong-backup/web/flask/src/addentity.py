import lib.bulkloaddata as bulkloaddata
import sys

# add data to an entity from stardate to today
# example: addentity.py M15 2017-08-15T12:51:22Z

#name of the script = sys.argv[0]
granularity = sys.argv[1]
start = sys.argv[2]
#granularity = 'M15'
#start = '2017-08-15T12:51:22Z'
bulkloaddata.bulkloadlivedatabytime('DE30_EUR',granularity,start)
bulkloaddata.bulkloadlivedatabytime('EUR_JPY',granularity,start)
bulkloaddata.bulkloadlivedatabytime('EUR_USD',granularity,start)
