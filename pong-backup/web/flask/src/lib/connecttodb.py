
import mysql.connector
from mysql.connector.constants import ClientFlag
import src.lib.getpair as getpair
import src.lib.savechart as savechart
from datetime import timedelta
from datetime import datetime
import time
def connect():
    # connect to a sql database	
    config = {
        'user': 'root',
        'password': 'cointegration',
        'host': '35.189.41.50',
        'client_flags': [ClientFlag.SSL],
        'ssl_ca': '/home/piyapong/sqlcert/server-ca.pem',
        'ssl_cert': '/home/piyapong/sqlcert/client-cert.pem',
        'ssl_key': '/home/piyapong/sqlcert/client-key.pem',
    }
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(buffered=True)
    return cur,cnx
def insert(instrument1=None,instrument2=None,datefrom=None,dateto=None,hedge_ratio=None,coeff1=None,coeff2=None
    ,mean=None,std=None,p_value=None,public_url=None,user_review=None,predict_x=None,predict_y=None):
    
    # insert cointegration
    query = ('INSERT INTO data.cointegration (instrument1,instrument2,datefrom,dateto,'
        'hedge_ratio,coeff1,coeff2,mean,std,p_value,public_url,user_review,predict_x,predict_y) '
        'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
    cur,cnx = connect()
    cur.execute(query,(instrument1,instrument2,datefrom,dateto,hedge_ratio
        ,coeff1,coeff2,mean,std,p_value,public_url,user_review,predict_x,predict_y))
    # Commit the changes
    cnx.commit()
    cur.close()
    cnx.close()
    
def savefile():
    # update cointegration after making prediction and snapshot
    query = ("SELECT instrument1,instrument2,datefrom,dateto,hedge_ratio,coeff1,"
        "coeff2,mean,std,p_value,public_url,user_review,predict_x,predict_y "
        "FROM data.cointegration WHERE public_url = '' AND dateto < DATE_SUB(NOW(), INTERVAL 5 HOUR) ORDER BY dateto DESC LIMIT 10;")
    cur,cnx = connect()
    cur.execute(query)

    for (instrument1,instrument2,datefrom,dateto,hedge_ratio,coeff1,coeff2,
        mean,std,p_value,public_url,user_review,predict_x,predict_y) in cur:
        #n=n+1
        #if public_url == '':
        minuteperiod = int((dateto-datefrom).total_seconds() / 60.0)
        df = getpair.getpairbydate1(instrument1,instrument2,datefrom,dateto,minuteperiod)
        forecastto = dateto + timedelta(minutes=minuteperiod*0.2)
        dftest = getpair.getpairbydate1(instrument1,instrument2,dateto,forecastto,minuteperiod)

        if len(df)>=100 and len(dftest)>=20:
        		public_url,predict_x,predict_y,datefrom,dateto,coint_level = savechart.drawchart(df,dftest,str(datefrom),str(dateto),float(hedge_ratio),float(p_value),float(coeff1),float(coeff2))
        		updateforecast(public_url,predict_x,predict_y,datefrom,dateto,coint_level)
        		#break
        else:
        		print('not enough sample'+str(len(df))+' '+str(len(dftest)))
        		print(dateto)
        		print(forecastto)
        		#updateforecast('',None,None,datefrom,dateto)
    
    cnx.commit()
    cur.close()
    cnx.close()
    
def savefile2():
    # test savefile
    query = ("SELECT instrument1,instrument2,datefrom,dateto,hedge_ratio,coeff1,"
        "coeff2,mean,std,p_value,public_url,user_review,predict_x,predict_y "
        "FROM data.cointegration")
    cur,cnx = connect()
    cur.execute(query)

    for (instrument1,instrument2,datefrom,dateto,hedge_ratio,coeff1,coeff2,
        mean,std,p_value,public_url,user_review,predict_x,predict_y) in cur:
        #n=n+1
        #if public_url == '':
        minuteperiod = int((dateto-datefrom).total_seconds() / 60.0)
        df = getpair.getpairbydate1(instrument1,instrument2,datefrom,dateto,minuteperiod)
        forecastto = dateto + timedelta(minutes=minuteperiod*0.2)
        dftest = getpair.getpairbydate1(instrument1,instrument2,dateto,forecastto,minuteperiod)

        if len(df)>=100 and len(dftest)>=20:
        		public_url,predict_x,predict_y,datefrom,dateto,coint_level = savechart.drawchart(df,dftest,str(datefrom),str(dateto),float(hedge_ratio),float(p_value),float(coeff1),float(coeff2))
        		updateforecast(public_url,predict_x,predict_y,datefrom,dateto,coint_level)
        		#break
        else:
        		print('not enough sample'+str(len(df))+' '+str(len(dftest)))
        		print(dateto)
        		print(forecastto)
        		#updateforecast('',None,None,datefrom,dateto)
    
    cnx.commit()
    cur.close()
    cnx.close()
    
def updateforecast(public_url,predict_x,predict_y,datefrom,dateto,coint_level):
    # update cointegration forecast
    query = ("UPDATE data.cointegration SET public_url = %s, predict_x = %s, predict_y = %s, coint_level = %s WHERE datefrom = %s AND dateto = %s")
    cur,cnx = connect()
    cur.execute(query,(public_url,predict_x,predict_y,coint_level,datefrom,dateto))
    cnx.commit()
    cur.close()
    cnx.close()
    
def updateuser_review(id,user_review):
    # update user review
    query = ("UPDATE data.cointegration SET user_review = %s WHERE id = %s")
    cur,cnx = connect()
    cur.execute(query,(user_review,id))
    cnx.commit()
    cur.close()
    cnx.close()
    
def updatelstmstat(instrument,mean):
    # update lstm mean	
    query = ("UPDATE data.lstmstat SET mean = %s WHERE instrument = %s")
    cur,cnx = connect()
    cur.execute(query,(str(mean),instrument))
    cnx.commit()
    cur.close()
    cnx.close()
    print('Update mean = '+str(mean)+' to '+instrument)
    
def selectlstmmeanbyinstrument(instrument):
	# select lstm mean by instrument
	query = ("SELECT mean FROM data.lstmstat WHERE instrument = '%s';"

	)
	query = query.replace('%s',instrument)
	cur,cnx = connect()
	#cur.execute(query,(instrument))
	cur.execute(query)

	for (mean) in cur:
		cur.close()
		cnx.close()
		return mean[0]

	cur.close()
	cnx.close()
	return 0

def select(itemfrom,length):
    # select 10 most recent cointegration without forecast to update forecast
    query = ("SELECT id,instrument1,instrument2,datefrom,dateto,hedge_ratio,coeff1,"
        "coeff2,mean,std,p_value,public_url,user_review,predict_x,predict_y "
        "FROM data.cointegration WHERE public_url != '' ORDER BY dateto DESC LIMIT %s,%s" % (str(itemfrom),str(length)))
    cur,cnx = connect()
    cur.execute(query)
    list = []
    for (id,instrument1,instrument2,datefrom,dateto,hedge_ratio,coeff1,coeff2,
        mean,std,p_value,public_url,user_review,predict_x,predict_y) in cur:
        list.append({'id':id,'instrument1':instrument1,'instrument2':instrument2,'datefrom':datefrom,'dateto':dateto,'hedge_ratio':hedge_ratio,'coeff1':coeff1,'coeff2':coeff2,
        'mean':mean,'std':std,'p_value':p_value,'public_url':public_url,'user_review':user_review,'predict_x':predict_x,'predict_y':predict_y})
        #print(instrument1)
    cur.close()
    cnx.close()
    return list
    
def selectforecast(instrument1,instrument2):
	# select all cointegration with forecast    
	query = ("SELECT id,instrument1 AS instrument,dateto,predict_x AS predict, public_url, coeff1, coeff2 "
	"FROM data.cointegration WHERE public_url != '' AND instrument1 = '%s1' AND instrument2 = '%s2' "
	"UNION "
	"SELECT id,instrument2 AS instrument,dateto,predict_y AS predict, public_url, coeff1, coeff2 "
	"FROM data.cointegration WHERE public_url != '' AND instrument1 = '%s2' AND instrument2 = '%s1' "
	)
	query = query.replace('%s1',(str(instrument1)))
	query = query.replace('%s2',(str(instrument2)))
	cur,cnx = connect()
	cur.execute(query)
	list = []


	for (id,instrument,dateto,predict,public_url,coeff1,coeff2) in cur:
		list.append({'id':id,'instrument':instrument,'time':dateto.timestamp() ,'predict':predict,'public_url':public_url,'coeff1':coeff1,'coeff2':coeff2})
		#print(instrument1)
	cur.close()
	cnx.close()
	return list
	
def selectforecastbydate(instrument1,instrument2,datefrom,dateto):
	# select some cointegration with forecast by date
	query = ("SELECT id,instrument1 AS instrument,dateto,coint_level,predict_x AS predict, public_url, coeff1, coeff2, hedge_ratio, mean, std, p_value "
	"FROM data.cointegration WHERE public_url != '' AND instrument1 = '%s1' AND instrument2 = '%s2' AND dateto >= '%s3' AND dateto <= '%s4' "
	"UNION "
	"SELECT id,instrument2 AS instrument,dateto,coint_level,predict_y AS predict, public_url, coeff1, coeff2, hedge_ratio, mean, std, p_value "
	"FROM data.cointegration WHERE public_url != '' AND instrument1 = '%s2' AND instrument2 = '%s1' AND dateto >= '%s3' AND dateto <= '%s4' "
	)
	query = query.replace('%s1',(str(instrument1)))
	query = query.replace('%s2',(str(instrument2)))
	query = query.replace('%s3',(datefrom))
	query = query.replace('%s4',(dateto))

	cur,cnx = connect()
	cur.execute(query)
	list = []


	for (id,instrument,dateto,coint_level,predict,public_url,coeff1,coeff2,hedge_ratio,mean,std,p_value) in cur:
		list.append({'id':id,'instrument':instrument,'time':dateto.timestamp(),'coint_level':coint_level,'predict':predict,'public_url':public_url,'coeff1':coeff1,'coeff2':coeff2,'hedge_ratio':hedge_ratio,'mean':mean,'std':std,'p_value':p_value})
		#print(instrument1)
	cur.close()
	cnx.close()
	return list
    
def selectforecastbyid(id):
	# select one cointegration with forecast by id
	query = ("SELECT instrument1,instrument2,public_url,datefrom,dateto,hedge_ratio,coeff1,coeff2,mean,std,p_value "
	"FROM data.cointegration WHERE id = '%s1';"

	)
	query = query.replace('%s1',(str(id)))
	cur,cnx = connect()
	cur.execute(query)


	for (instrument1,instrument2,public_url,datefrom,dateto,hedge_ratio,coeff1,coeff2,mean,std,p_value) in cur:
		cur.close()
		cnx.close()
		return ({'instrument1':instrument1,'instrument2':instrument2,'public_url':public_url,'datefrom':datefrom, 'dateto':dateto, 'hedge_ratio':hedge_ratio,'coeff1':coeff1,'coeff2':coeff2,'mean':mean,'std':std,'p_value':p_value})

	cur.close()
	cnx.close()
	return {}
def count():
	# count number of cointegration with forecast    
	query = ("SELECT id AS totalcount FROM data.cointegration WHERE public_url != ''")
	cur,cnx = connect()
	cur.execute(query)
	return (int(cur.rowcount/50)+1)

#savefile()



