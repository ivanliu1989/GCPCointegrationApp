from flask import Flask, request, url_for, Response
import re
import web.template as template
import src.lib.connecttodb as connecttodb
import src.lib.getpair as getpair
import pygal
from pygal.style import DarkStyle
from datetime import datetime
import pandas
import numpy as np

app = Flask(__name__)

@app.route('/chart', methods=['GET'])
def chart():
	graph = creategraph(request.args.get('instrument1'),request.args.get('instrument2'))
	return Response(response=graph.render(), content_type='image/svg+xml')

def creategraph(instrument1,instrument2):
	#graph = pygal.XY(stroke_style={'width': 2},spacing=0,width=15000,height=400)
	#graph.title = '% Change Coolness of programming languages over time.'
	
	df = getpair.getalldata(instrument1)

	tuples = [tuple(x) for x in df[['time',instrument1]].values]
	from pygal.style import Style
	custom_style = Style(
	background='black',
	plot_background='transparent',
	foreground='#53E89B',
	foreground_strong='#53A0E8',
	foreground_subtle='#630C0D',
	opacity='.6',
	opacity_hover='.9',
	transition='400ms ease-in',
	colors=('rgba(255, 45, 20, .3)', 'rgba(92, 213, 255, .3)', 'yellow', '#E89B53'))
	graph = pygal.DateTimeLine(
	    x_label_rotation=0, truncate_label=-1,spacing=0,width=40000,height=450,
	    x_value_formatter=lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S'), style=custom_style)
	
	
	dfforecast = pandas.DataFrame(connecttodb.selectforecast(instrument1,instrument2))
	dfcopy = df.copy()
	result = dfcopy.append(dfforecast, ignore_index=True)
	result.sort_values(['time'], ascending=[True], inplace=True)
	
	v = []
	for i in range(len(result)):
		if np.isnan(result[instrument1].iloc[i]):
			v.append(v[len(v)-1])
		else:
			v.append(result[instrument1].iloc[i])
	result['value'] = v
	print(result)
	dfdown = result[result['predict']=='down']
	#dfdown = dfdown.dropna(subset=[kind])
	tuples2 = [tuple(x) for x in dfdown[['time','value']].values]
	graph.add('down', tuples2, show_dots=True, dots_size=10, stroke=False)
	
	dfup = result[result['predict']=='up']
	#dfup = dfup.dropna(subset=[kind])
	tuples3 = [tuple(x) for x in dfup[['time','value']].values]
	graph.add('up', tuples3, show_dots=True, dots_size=10, stroke=False)
	
	graph.add(instrument1, tuples, show_dots=True, dots_size=2, stroke=False)
	
	
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
		#print(button)
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
    #print (html)          
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


