import mysql.connector
from mysql.connector.constants import ClientFlag
import getpair
import savechart
from datetime import timedelta
from datetime import datetime
def connect():
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
    
    query = ("SELECT instrument1,instrument2,datefrom,dateto,hedge_ratio,coeff1,"
        "coeff2,mean,std,p_value,public_url,user_review,predict_x,predict_y "
        "FROM data.cointegration WHERE predict_x = ''")
    cur,cnx = connect()
    cur.execute(query)
    #n = 0
    for (instrument1,instrument2,datefrom,dateto,hedge_ratio,coeff1,coeff2,
        mean,std,p_value,public_url,user_review,predict_x,predict_y) in cur:
        #n=n+1
        #if public_url == '':
        minuteperiod = int((dateto-datefrom).total_seconds() / 60.0)
        df = getpair.getpairbydate(instrument1,instrument2,datefrom,dateto,minuteperiod)
        forecastto = dateto + timedelta(minutes=minuteperiod*0.2)
        dftest = getpair.getpairbydate(instrument1,instrument2,dateto,forecastto,minuteperiod)
        print(dftest)
        print(minuteperiod)
        print(forecastto)
        public_url,predict_x,predict_y,datefrom,dateto = savechart.drawchart(df,dftest,str(datefrom),str(dateto),str(hedge_ratio),str(p_value),str(coeff1),str(coeff2))
        updateforecast(public_url,predict_x,predict_y,datefrom,dateto)
        #break
    
    cnx.commit()
    cur.close()
    cnx.close()
    
def updateforecast(public_url,predict_x,predict_y,datefrom,dateto):
    query = ("UPDATE data.cointegration SET public_url = %s, predict_x = %s, predict_y = %s WHERE datefrom = %s AND dateto = %s")
    cur,cnx = connect()
    cur.execute(query,(public_url,predict_x,predict_y,datefrom,dateto))
    cnx.commit()
    cur.close()
    cnx.close()

def select():
    
    query = ("SELECT instrument1,instrument2,datefrom,dateto,hedge_ratio,coeff1,"
        "coeff2,mean,std,p_value,public_url,user_review,predict_x,predict_y "
        "FROM data.cointegration WHERE predict_x = ''")
    cur,cnx = connect()
    cur.execute(query)
    list = []
    for (instrument1,instrument2,datefrom,dateto,hedge_ratio,coeff1,coeff2,
        mean,std,p_value,public_url,user_review,predict_x,predict_y) in cur:
            list.append({'instrument1':instrument1,'instrument2':instrument2,'datefrom':datefrom,'dateto':dateto,'hedge_ratio':hedge_ratio,'coeff1':coeff1,'coeff2':coeff2,
        'mean':mean,'std':std,'p_value':p_value,'public_url':public_url,'user_review':user_review,'predict_x':predict_x,'predict_y':predict_y})
    
    cnx.commit()
    cur.close()
    cnx.close()
    return list
#savefile()



