import src.lib.cal2 as cal2
import sys

# calculate cointegration and save to the database if p-value is significant
# example: calcoint.py DE30_EUR EUR_JPY 6000 0.05
# input-params: instrument1 = the first instrument name
# input-params: instrument2 = the second instrument name
# input-params: lookback = number of lookback period in minutes
# input-params: p-value = cutpoint of significant p-value

#name of the script = sys.argv[0]
instrument1 = sys.argv[1]
instrument2 = sys.argv[2]
lookback = int(sys.argv[3])
p_value = float(sys.argv[4])

cal2.coint(instrument1,instrument2,lookback,p_value)
