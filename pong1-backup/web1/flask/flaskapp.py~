from flask import Flask, request 
import re
import template
import connecttodb

app = Flask(__name__)

from flask import Flask, url_for

@app.route('/test', methods=['POST'])
def test():
	if request.method == 'POST':
		id = ''+request.form['id']
		user_review = ''+request.form['user_review']
		connecttodb.updateuser_review(id,user_review)
		
@app.route('/getdata', methods=['POST'])
def getdata():
	if request.method == 'POST':
		itemfrom = ''+request.form['itemfrom']
		length = ''+request.form['length']
		return createtable(itemfrom,length)
@app.route('/')
	
	
def hello_world():
   body = template.getbodytemplate()
   body = body.replace('%tabnum',createbar())
   body = body.replace('%table',createtable(0,50))
   return body

def createbar():
	total = connecttodb.count()
	tab = ''
	print('createbar')
	for i in range(total):
		length = 50
		itemfrom = str(i*length)
		itemto = str(length)
		item = str(i+1)
		button = "<button class='w3-bar-item w3-button' onclick=\"fetchdata(this,'%s','%s')\">%s</button>" % (itemfrom,itemto,item)
		print(button)
		tab = tab+button
	return tab
def createtable(itemfrom,length):
    
    result = connecttodb.select(itemfrom,length)
    html = ''
    num = 1
    for i in result:
    	  if i['public_url'] != '':
        		html += addrow(i,num)
        		num = num+1
    print (html)          
    return html
    
def addrow(d,num):
   from datetime import datetime
   table = template.gettabletemplate()
   table = table.replace('%image'  , "<img src='"+d['public_url']+"' alt='No image' width=100%></img>")
   table = table.replace('%ins1'   , d['instrument1'])
   table = table.replace('%ins2'   , d['instrument2'])
   table = table.replace('%from'   , str(d['datefrom']))
   table = table.replace('%to'     , str(d['dateto']))
   table = table.replace('%hedge'  , str(d['hedge_ratio']))
   table = table.replace('%pvalue' , str(d['p_value']))
   table = table.replace('%mean'   , str(d['mean']))
   table = table.replace('%std'    , str(d['std']))
   table = table.replace('%i'      , str(d['id']))
   table = table.replace('%order'      , str(num)+') id: '+str(d['id']))
   if d['user_review'] == 'y':
      table = table.replace('%checkstatus', 'enable')
      table = table.replace('%crossstatus', 'disable')
   elif d['user_review'] == 'n':
      table = table.replace('%crossstatus', 'enable')
      table = table.replace('%checkstatus', 'disable')
   else:
      table = table.replace('%checkstatus', 'disable')
      table = table.replace('%crossstatus', 'disable')
   #put(d)
   return table

hello_world()


