from flask import Flask, request, url_for, Response
import re
import web.template as template
import src.lib.connecttodb as connecttodb
import src.lib.getpair as getpair
import pygal
from datetime import datetime
import pandas

app = Flask(__name__)

@app.route('/chart')
def chart():
	graph = creategraph()
	return Response(response=graph.render(), content_type='image/svg+xml')

def creategraph():
	#graph = pygal.XY(stroke_style={'width': 2},spacing=0,width=15000,height=400)
	#graph.title = '% Change Coolness of programming languages over time.'
	
	kind = 'DE30_EUR'
	df = getpair.getalldata(kind)

	tuples = [tuple(x) for x in df[['time',kind]].values]
	graph = pygal.DateTimeLine(
	    x_label_rotation=35, truncate_label=-1,spacing=0,width=30000,height=1000,
	    x_value_formatter=lambda dt: dt.strftime('%I:%M:%S %p'))
	graph.add(kind, tuples, show_dots=False)
	
	dfforecast = pandas.DataFrame(connecttodb.selectforecast(kind))
	
	dfdown = dfforecast[dfforecast['predict']=='down']
	dfdown['c'] = 12600
	tuples2 = [tuple(x) for x in dfdown[['time','c']].values]
	graph.add('down', tuples2, show_dots=True, dots_size=4, stroke=False)
	
	dfup = dfforecast[dfforecast['predict']=='up']
	dfup['c'] = 12800
	tuples3 = [tuple(x) for x in dfup[['time','c']].values]
	graph.add('up', tuples3, show_dots=True, dots_size=4, stroke=False)
	#timelist = dfforecast['time'].values.tolist()
	#valuelist = dfforecast['instrument'].values.tolist()
	#graph.x_labels = map(lambda d: d.strftime('%Y-%m-%d %H:%M:%S'),timelist)
	#graph.add(kind, valuelist, show_dots=False)
	#graph.add(kind, [(timelist[x],valuelist[x]) for x in range(len(valuelist))], show_dots=True)
	#graph.add('cointegrated',[(timelist[5],valuelist[5]),(timelist[15],valuelist[15]),(timelist[25],valuelist[25])], show_dots=True, dots_size=4, stroke=False)
	
	
	
	return graph
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


