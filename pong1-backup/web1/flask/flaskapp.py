from flask import Flask, request, url_for, Response
import re
import web.template as template
import src.lib.connecttodb as connecttodb
import src.lib.getpair as getpair
import src.lib.savechart as savechart
import pygal
from pygal.style import DarkStyle
from datetime import datetime
import pandas
import numpy as np
from datetime import date
from datetime import timedelta


app = Flask(__name__)

@app.route('/chart', methods=['GET'])
def chart():
	graph = creategraph(request.args.get('instrument1'),request.args.get('instrument2'))
	return Response(response=graph.render(), content_type='image/svg+xml')

def creategraph(instrument1,instrument2):
	#graph = pygal.XY(stroke_style={'width': 2},spacing=0,width=15000,height=400)
	#graph.title = '% Change Coolness of programming languages over time.'
	
	df = getpair.getalldata(instrument1)
	df[instrument1] = savechart.normalise_windows(df[instrument1],df[instrument1][0])
	
	df2 = getpair.getalldata(instrument2)
	df2[instrument2] = savechart.normalise_windows(df2[instrument2],df2[instrument2][0])

	tuples = [tuple(x) for x in df[['time',instrument1]].values]
	from pygal.style import Style
	custom_style = Style(
	background='black',
	plot_background='transparent',
	foreground='#53E89B',
	foreground_strong='#53A0E8',
	foreground_subtle='#630C0D',
	opacity='.9',
	opacity_hover='.9',
	transition='400ms ease-in',
	colors=('rgba(255, 45, 20, .5)', 'rgba(92, 213, 255, .5)', 'rgba(255,255,51, 0.7)', '#E89B53'))
	graph = pygal.DateTimeLine(
	    x_label_rotation=0, truncate_label=-1,spacing=0,width=40000,height=650,
	    x_value_formatter=lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S'), style=custom_style)
	
	
	dfforecast = pandas.DataFrame(connecttodb.selectforecast(instrument1,instrument2))
	dfcopy = df.copy()
	result1 = dfcopy.append(dfforecast, ignore_index=True)
	result = result1.append(df2, ignore_index=True)
	result.sort_values(['time'], ascending=[True], inplace=True)
	
	result['instrument'] = np.nan
	result['predict'] = np.nan
	
	v = []
	for i in range(len(result)):
		if np.isnan(result[instrument1].iloc[i]):
			v.append(v[len(v)-1])
		else:
			v.append(result[instrument1].iloc[i])
	result['value'] = v
	
	'''
	v = []
	for i in range(len(result)):
		if np.isnan(result[instrument1].iloc[i]):
			v.append(v[len(v)-1])
		else:
			v.append(result[instrument1].iloc[i])
	result['value'] = v
	'''
	'''
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
	
	
	
	#return graph
	'''
	chart = pygal.Line(spacing=0,width=20000,height=400, style=custom_style)
	#chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d %H:%M:%S'),result['time'].values.tolist())
	
	'''
	list2 = []
	for i in range(len(result)):
		if result['predict'].iloc[i] == 'down':
			list2.append({
				'value': result['value'].iloc[i],
				'label': datetime.fromtimestamp(result['time'].iloc[i]).strftime('%Y-%m-%d %H:%M:%S'),
				'xlink': {'href': result['public_url'].iloc[i],'target': '_blank'}
				})
		else:
			list2.append({'value': None})
			
	chart.add('down', list2, show_dots=True, dots_size=5, stroke=False)
	
	list3 = []
	for i in range(len(result)):
		if result['predict'].iloc[i] == 'up':
			list3.append({
				'value': result['value'].iloc[i],
				'label': datetime.fromtimestamp(result['time'].iloc[i]).strftime('%Y-%m-%d %H:%M:%S'),
				'xlink': {'href': result['public_url'].iloc[i],'target': '_blank'}
				})
		else:
			list3.append({'value': None})
			
	chart.add('up', list3, show_dots=True, dots_size=5, stroke=False)
	'''
	'''
	v1 = []
	v2 = []
	v1.append(0)
	v2.append(0)
	for i in range(1,len(result)):
		if np.isnan(result[instrument1].iloc[i]):
			v1.append(v1[len(v1)-1])
		else:
			v1.append(result[instrument1].iloc[i])
		if np.isnan(result[instrument2].iloc[i]):
			v2.append(v2[len(v2)-1])
		else:
			v2.append(result[instrument2].iloc[i])
	result[instrument1] = v1
	result[instrument2] = v2
	'''	
				
	
	
	list1 = []
	list2 = []
	list3 = []
	list4 = [np.nan] * len(result)
	list5 = [np.nan] * len(result)
	for i in range(len(result)):
		if np.isnan(result[instrument1].iloc[i]):
			list1.append({'value': None})
		else:
			list1.append({
				'value': result[instrument1].iloc[i],
				'label': datetime.fromtimestamp(result['time'].iloc[i]).strftime('%Y-%m-%d %H:%M:%S')
				})
		if np.isnan(result[instrument2].iloc[i]):
			list2.append({'value': None})
		else:
			list2.append({
				'value': result[instrument2].iloc[i],
				'label': datetime.fromtimestamp(result['time'].iloc[i]).strftime('%Y-%m-%d %H:%M:%S')
				})
		if str(result['public_url'].iloc[i]) == 'nan' or result['value'].iloc[i] == result['value'].iloc[i+1]:
			list3.append({'value': None})
		else:
			list3.append({
				'value': result['value'].iloc[i],
				'label': datetime.fromtimestamp(result['time'].iloc[i]).strftime('%Y-%m-%d %H:%M:%S'),
				'xlink': {'href': result['public_url'].iloc[i],'target': '_blank'}
				})
		'''
		#cal = (result[instrument1].iloc[i]*result['coeff1'].iloc[i])+(result[instrument2].iloc[i]*result['coeff2'].iloc[i])
		if str(result['public_url'].iloc[i]) != 'nan':
			dfco = result[[instrument1,instrument2]].iloc[i-5:i].copy()
			dfco[instrument1] = savechart.normalise_windows(dfco[instrument1],dfco[instrument1].iloc[0])
			dfco[instrument2] = savechart.normalise_windows(dfco[instrument2],dfco[instrument2].iloc[0])
			vec = [result['coeff1'].iloc[i],result['coeff2'].iloc[i]]
			x1 = dfco.as_matrix()
			in_sample = np.dot(x1, vec)
			for j in range(len(in_sample)):
				list4[i-len(in_sample)+j]=in_sample[j]
			for k in range(i+1,i+10):
				if np.isnan(result['predict'].iloc[k]):
					cal3 = (result[instrument1].iloc[k]*result['coeff1'].iloc[i])+(result[instrument2].iloc[k]*result['coeff2'].iloc[i])
					list5[k]=cal3
	result['instrument'] = list4


	co1 = []			
	for i in range(len(result)):
		if np.isnan(result['instrument'].iloc[i]):
			co1.append({'value': None})
		else:
			co1.append({
				'value': result['instrument'].iloc[i],
				'label': datetime.fromtimestamp(result['time'].iloc[i]).strftime('%Y-%m-%d %H:%M:%S')
				})
		'''

	chart.add(instrument1, list1, show_dots=True, dots_size=1, stroke=True)
	chart.add(instrument2, list2, show_dots=True, dots_size=1, stroke=True)
	chart.add('cointegration', list3, show_dots=True, dots_size=3, stroke=False)
	#chart.add('coint line', co1, show_dots=True, dots_size=1, stroke=False, secondary=True)
	
	return chart
	
@app.route('/lstm/lstmchart', methods=['GET'])
def lstmchart():
	n = int(request.args.get('pagenumber'))
	instrument = request.args.get('instrument')
	today = date.today()

	table = htmlchart(n,today,instrument)
	return table
	
@app.route('/lstm', methods=['GET'])
def lstm():

	today = date.today()
	list = ''
	list = list+htmlchartblock(0,today,'EUR_USD')
	list = list+htmlchartblock(0,today,'AUD_USD')
	list = list+htmlchartblock(0,today,'GBP_USD')
	body = template.getlstmtemplate()
	body = body.replace('%chart',list)
	print(body)
	return body
	
def htmlchartblock(n,today,instrument):
	block = htmlchart(n,today,instrument)
	tab = '''
		<div>
			<div style='margin-left:150px; height:0px;'>
				<ul class="pagination  pagination-sm" id="pagination%id%instrument">
					<li class="page active"><a href="#">this week</a></li>
					<li class="page"><a href="#">1 week</a></li>
					<li class="page"><a href="#">2 week</a></li>
					<li class="page"><a href="#">3 week</a></li>
					<li class="page"><a href="#">4 week</a></li>
				</ul>
			</div>
			<div id='chart%id%instrument'>
			%block
			</div>
			<script>

				$('#pagination%id%instrument li').on('click',function(e){
				    e.preventDefault();
				    var tag = $(this);
					 
				    text = tag.text();
				    pagenumber = 0;
				    if(text=='this week')
				    {
				    	pagenumber = 0;
				    }
				    else
				    {
				    	pagenumber = text.substring(0, 1);
				    }
				    
				    $.ajax({url: "/lstm/lstmchart?pagenumber="+pagenumber+'&instrument=%instrument', success: function(result){
				    		if(result!='')
				    		{
					    		$("#chart%id%instrument").empty();
					    		$("#chart%id%instrument").append(result);
					        	$('#pagination%id%instrument .page').removeClass('active')
				    			tag.addClass('active')
				        	}
		
				    }});
		
				});
			</script>
		</div>
		'''
	tab = tab.replace('%id',str(n))
	tab = tab.replace('%instrument',instrument)

	tab = tab.replace('%block',block)
	return tab
	
def htmlchart(n,today,instrument):
	monday = today + timedelta(days=-today.weekday(), weeks=-n)
	friday = monday + timedelta(days=+4)
	start = datetime.combine(monday, datetime.min.time())
	end = datetime.combine(friday, datetime.max.time())
	df = getpair.getlstmdata(instrument,start,end)
	if len(df)>0:
		#block = '<div class="col-sm-4" style="height:400px; padding:5px;">%table</div>'
		block = '<div style="height:400px; padding:5px;">%table</div>'
		table = template.getlstmtable()
		table = table.replace('%id',instrument+str(n))
		table = table.replace('%serie1',instrument)
		table = table.replace('%datefrom',str(start.timestamp()))
		table = table.replace('%dateto',str(end.timestamp()))
		d = ['actual_value','predicted_value','square_error']
		for j in range(len(d)):
			df1 = pandas.DataFrame(df[['time',d[j]]])
			df1.rename(columns={'time': 'x', d[j]: 'y'}, inplace=True)
			data1 = df1[['x','y']].to_dict(orient='records')
			table = table.replace('%data'+str(j),str(data1))
		block = block.replace('%table',table)
		return block
	else:
		return ''
	return ''
	
	
@app.route('/coint', methods=['GET'])
def coint():
	id = request.args.get('id')

	body = template.getcointtemplate()
	values = connecttodb.selectforecastbyid(id)
	body = body.replace('%chart',values['public_url'])
	body = body.replace('%instrument1',values['instrument1'])
	body = body.replace('%instrument2',values['instrument2'])
	body = body.replace('%datefrom',values['datefrom'].strftime('%Y-%m-%d %H:%M:%S'))
	body = body.replace('%dateto',values['dateto'].strftime('%Y-%m-%d %H:%M:%S'))
	body = body.replace('%hedge_ratio',str(values['hedge_ratio']))
	body = body.replace('%coeff1',str(values['coeff1']))
	body = body.replace('%coeff2',str(values['coeff2']))
	body = body.replace('%mean',str(values['mean']))
	body = body.replace('%std',str(values['std']))
	body = body.replace('%p_value',str(values['p_value']))
	body = body.replace('%fxdata',getfxdata(values))
	return body
def getfxdata(values):
	df = getpair.getpairbydate2(values['instrument1'],values['instrument2'],values['datefrom'],values['dateto'])
	text = ''
	for i in range(len(df)):
		template = '''
			<tr>
	        <td>%s</td>
	        <td>%s</td>
	        <td>%s</td>
	        <td>%s</td>
	      </tr>
			'''
		template = template % (datetime.utcfromtimestamp(df['time_'+values['instrument1']].iloc[i]).strftime('%Y-%m-%d %H:%M:%S'),
			str(df[values['instrument1']].iloc[i]),
			datetime.utcfromtimestamp(df['time_'+values['instrument2']].iloc[i]).strftime('%Y-%m-%d %H:%M:%S'),
			str(df[values['instrument2']].iloc[i]))
		text = text+template
	return text
		
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
		
@app.route('/gethistory', methods=['GET'])
def gethistory():
	n = request.args.get('n')
	instrument1 = request.args.get('instrument1')
	instrument2 = request.args.get('instrument2')
	body = template.getbodytemplate()
	body = body.replace('%title','History data')
	body = body.replace('%nvd3chart',createnvd3chartlist(int(n),instrument1,instrument2,'none'))	
	body = body.replace('%tabnum','')
	body = body.replace('%table','')
	
	return body

@app.route('/')	
def hello_world():
	body = template.getbodytemplate()
	chart = ''
	chart = chart+createnvd3chartlist(1,'EUR_USD','GBP_USD','inline')
	chart = chart+createnvd3chartlist(1,'USD_CAD','AUD_USD','inline')
	chart = chart+createnvd3chartlist(1,'EUR_USD','AUD_USD','inline')
	chart = chart+createnvd3chartlist(1,'GBP_USD','AUD_USD','inline')
	chart = chart+createnvd3chartlist(1,'EUR_JPY','EUR_USD','inline')
	chart = chart+createnvd3chartlist(1,'EUR_USD','EUR_GBP','inline')
	chart = chart+createnvd3chartlist(1,'EUR_JPY','EUR_GBP','inline')
	
	body = body.replace('%nvd3chart',chart)	
	body = body.replace('%title','Cointegration dashboard')
	body = body.replace('%tabnum','')
	body = body.replace('%table','')
	#body = body.replace('%tabnum',createbar())
	#body = body.replace('%table',createtable(0,50))
	
	return body
	
def createnvd3chartlist(n,instrument1,instrument2,display):
	'''
	instrument1 = 'EUR_JPY'
	df = getpair.getalldata(instrument1)
	instrument2 = 'EUR_USD'
	df2 = getpair.getalldata(instrument2)
	dfforecast = pandas.DataFrame(connecttodb.selectforecast(instrument1,instrument2))
	
	week = []
	weekday = []
	for i in range(len(df)):
		week.append(datetime.utcfromtimestamp(df['time'].iloc[i]).year * 100 + datetime.utcfromtimestamp(df['time'].iloc[i]).isocalendar()[1])
		weekday.append(datetime.utcfromtimestamp(df['time'].iloc[i]).weekday())
	df['week'] = week
	df['weekday'] = weekday
	weeks = df.week.unique()
	weeks[:] = weeks[::-1]
	chartlist= ''
	for w in weeks:
		dfp = df[(df['week']==w) & (df['weekday']<=4)].copy()
		dfp = dfp.dropna()
		datefrom = dfp.head(1)['time'].iloc[0]
		dateto = dfp.tail(1)['time'].iloc[0]
		df2p = df2[(df2['time']>datefrom) & (df2['time']<dateto)].copy()
		dfforecastp = dfforecast[(dfforecast['time']>datefrom) & (dfforecast['time']<dateto)].copy()
		html = createnvd3chart(w,dfp,df2p,dfforecastp,instrument1,instrument2)
		chartlist = chartlist+html
	return chartlist
	'''
	
	chartlist= ''
	today = date.today()

	for i in range(n):
		monday = today + timedelta(days=-today.weekday(), weeks=-i)
		friday = monday + timedelta(days=+4)
		monday = datetime.combine(monday, datetime.min.time())
		friday = datetime.combine(friday, datetime.max.time())
		
		df1 = getpair.getdatabydate3(instrument1,monday,friday)
		df1 = df1.dropna()

		df2 = getpair.getdatabydate3(instrument2,monday,friday)
		df2 = df2.dropna()
		columns = ['id','instrument','time','coint_level','predict','public_url','coeff1','coeff2']
		dfforecast = pandas.DataFrame(connecttodb.selectforecastbydate(instrument1,instrument2,monday.strftime('%Y-%m-%d %H:%M:%S'),friday.strftime('%Y-%m-%d %H:%M:%S')),columns=columns)
		html = createnvd3chart(i,df1,df2,dfforecast,instrument1,instrument2,monday.timestamp(),friday.timestamp(),display)
		chartlist = chartlist+html
	return chartlist
	
def createnvd3chart(id,df1,df2,dfforecast,instrument1,instrument2,datefrom,dateto,display):

	if len(df1)==0:
		return ''
	df1[instrument1] = savechart.normalise_windows(df1[instrument1],df1[instrument1].iloc[0])
	df1.rename(columns={'time': 'x', instrument1: 'y'}, inplace=True)
	data = df1[['x','y']].to_dict(orient='records')

	df2[instrument2] = savechart.normalise_windows(df2[instrument2],df2[instrument2].iloc[0])
	df2.rename(columns={'time': 'x', instrument2: 'y'}, inplace=True)
	data2 = df2[['x','y']].to_dict(orient='records')
	
	value = []
	for i in range(len(dfforecast)):
		t = dfforecast['time'].iloc[i]
		d = df1[df1['x']<=t]
		value.append(d.tail(1)['y'].iloc[0]+(abs(df1['y'].max()-df1['y'].min())*0.05))

	dfforecast['y'] = value

	dfforecast.rename(columns={'time': 'x'}, inplace=True)
	forecastlevel1 = dfforecast[dfforecast['coint_level']=='g']
	forecastlevel1['shape'] = 'triangle-down'
	data3_1 = forecastlevel1[['x','y','shape']].to_dict(orient='records')

	forecastlevel2 = dfforecast[dfforecast['coint_level']=='y']
	forecastlevel2['shape'] = 'triangle-down'
	data3_2 = forecastlevel2[['x','y','shape']].to_dict(orient='records')

	data4 = dict(zip(dfforecast.x, dfforecast.public_url))
	data5 = dict(zip(dfforecast.x, dfforecast.id))
	
	html = '''
	  <div>
	  <h4 style="text-align:center">%serie1 & %serie2</h4>
	  <div style="z-index: 1; position: relative; top: 0px; left: 0px;">
			<div id="chart%id" class="cointchart" style='height:400px; position: relative;'>
					<svg></svg>
			</div>
			<div style="z-index: 2; position: absolute; top: 0px; left: 150px; display:%display;"><a href="/gethistory?n=5&instrument1=%serie1&instrument2=%serie2"  target="_blank">history</a></div></div>
	  </div>
	  <div>
	  
	
	<script>
		dict%id = %data4
		dictid%id = %data5
		chartdata%id =[
							{"key": "%serie1", "yAxis": "1", "type": "line", "color": "#21618C", "values": %data1},
							{"key": "%serie2", "yAxis": "1", "type": "line", "color": "#A9CCE3", "values": %data2},
							{"key": "possible cointegrated", "yAxis": "1", "type": "scatter", "color": "rgba(169,204,227,1.0)", "values": %data3_2},
							{"key": "cointegrated", "yAxis": "1", "type": "scatter", "color": "rgba(31,97,141,1.0)", "values": %data3_1}
							];
		nv.addGraph(function() {
		var chart = nv.models.multiChart()
			.margin({top:0,right:150,bottom:0,left:150})
        	.height(300);
		chart.lines1.interactive(false)
		
		chart.xAxis.tickFormat(function(d) {
		 // Will Return the date, as "%m/%d/%Y"(08/06/13)
		 return d3.time.format.utc('%Y-%m-%d')(new Date(d*1000))
		});
		
		chart.lines1.xDomain([new Date(%datefrom),new Date(%dateto)]);
		chart.scatters1.xDomain([new Date(%datefrom),new Date(%dateto)]);


		chart.yAxis1
			.tickFormat(d3.format(',.4f'));
		
		chart.tooltip.contentGenerator(function (d) {
        //return "<img src='https://storage.googleapis.com/pong-cointegration/DE30_EUR_EUR_JPY_2017-08-30%2000%3A00%3A08' width='600'>";}); 	
			 x = d.value
			 y = '';
			 value = '';
          d.series.forEach(function(elem){
          	y = elem.key;
          	value = elem.value;

          })

          if(x in dict%id)
          //if(y == 'cointegrated' || y == 'possible cointegrated')
	       	{
	       		return "<div style='padding:5px;'><img src='"+dict%id[x]+"' width='600'></div>";
	       	}
	       	else
	       	{
					return "<div style='padding:3px;'><div><b>"+d3.time.format.utc('%Y-%m-%d %H:%M:%S')(new Date(x*1000))+"</b></div>"+"<div>"+d3.format(',.4f')(value)+"</div></div>";        	
	       	}

          }); 	
		chart.scatters1.dispatch.on('elementClick', function(e) {
				//if(e.series.key == 'cointegrated' || e.series.key == 'possible cointegrated')
				if(e.point.x in dict%id)
				{
					//alert("You've clicked on " + e.series.key + " - " + e.point.x + " - " + dictid%id[e.point.x]);
					window.open('/coint?id=' + dictid%id[e.point.x],'_blank');
				}
				
		     	
		 });
		 
		 chart.lines1.dispatch.on('elementClick', function(e) {
				//if(e.series.key == 'cointegrated' || e.series.key == 'possible cointegrated')
				if(e.point.x in dict%id)
				{
					//alert("You've clicked on " + e.series.key + " - " + e.point.x + " - " + dictid%id[e.point.x]);
					window.open('/coint?id=' + dictid%id[e.point.x],'_blank');
				}
				
		     	
		 });
		d3.select('#chart%id svg')
			.datum(chartdata%id)
			.transition().duration(500)
			.call(chart);
		
		nv.utils.windowResize(chart.update);
		
		return chart;
		});
	</script>
		'''
	html = html.replace('%id',str(id)+'_'+instrument1+'_'+instrument2)
	html = html.replace('%datefrom',str(datefrom))
	html = html.replace('%dateto',str(dateto))
	html = html.replace('%serie1',instrument1)
	html = html.replace('%serie2',instrument2)
	html = html.replace('%data1',str(data))
	html = html.replace('%data2',str(data2))
	html = html.replace('%data3_1',str(data3_1))
	html = html.replace('%data3_2',str(data3_2))
	html = html.replace('%data4',str(data4))
	html = html.replace('%data5',str(data5))
	html = html.replace('%display',display)
	return html
	
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

#hello_world()


