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
        'host': '35.196.62.158',
        'client_flags': [ClientFlag.SSL],
        'ssl_ca': '/home/piyapong/sqlcert/server-ca.pem',
        'ssl_cert': '/home/piyapong/sqlcert/client-cert.pem',
        'ssl_key': '/home/piyapong/sqlcert/client-key.pem',
    }
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor(buffered=True)
    return cur,cnx
def insert(instrument1=None,instrument2=None,datefrom=None,dateto=None,hedge_ratio=None,coeff1=None,coeff2=None,mean=None,std=None,p_value=None,public_url=None,cointegrated=None):
    
    query = ('INSERT INTO data.cointegration '
        '(instrument1,instrument2,datefrom,dateto,hedge_ratio,coeff1,coeff2,mean,std,p_value,public_url,cointegrated) '
        'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
    cur,cnx = connect()
    cur.execute(query,(instrument1,instrument2,datefrom,dateto,hedge_ratio,coeff1,coeff2,mean,std,p_value,public_url,cointegrated))
    # Commit the changes
    cnx.commit()
    cur.close()
    cnx.close()

def select(forecast=10):
    
    query = ("SELECT instrument1,instrument2,datefrom,dateto,hedge_ratio,coeff1,coeff2,mean,std,p_value,public_url,cointegrated FROM data.cointegration")
    cur,cnx = connect()
    cur.execute(query)
    n = 0
    for (instrument1,instrument2,datefrom,dateto,hedge_ratio,coeff1,coeff2,mean,std,p_value,public_url,cointegrated) in cur:
        n = n+1
        if n == 3:
           df = getpair.getpairbydate(instrument1,instrument2,datefrom,dateto,int((dateto-datefrom).total_seconds() / 60.0))
           forecastto = dateto + timedelta(minutes=forecast)
           dftest = getpair.getpairbydate(instrument1,instrument2,dateto,forecastto,forecast)
           savechart.drawchart(df,dftest,str(datefrom),str(dateto),str(hedge_ratio),str(p_value),str(coeff1),str(coeff2))
           break
    
    cnx.commit()
    cur.close()
    cnx.close()
    
select(100)
