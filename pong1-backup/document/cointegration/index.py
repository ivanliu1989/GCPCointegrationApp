def index():
    	p1 = 	"""
<html>
<head>
<style>
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}

tr:nth-child(even) {
    background-color: #dddddd;
}
</style>
</head>
<body>
  <h1>Cointegrated currency exchange report</h1>
<table>
  <tr>
    <th>instrument 1</th>
    <th>instrument2</th>
    <th>from</th>
    <th>to</th>
    <th>hedge ratio</th>
    <th>p-value</th>
    <th>mean</th>
    <th>std</th>
  </tr>
  <tr>
    <td>USD_CHF</td>
    <td>USD_TRY</td>
    <td>2017-02-01</td>
    <td>2017-02-12</td>
    <td>3.162</td>
    <td>0.002</td>
    <td>0.058</td>
    <td>0.022</td>
  </tr>
		"""
	p2 = 	"""
</table>
</body>
</html>		
	  	"""

	from google.cloud import datastore
	from datetime import datetime
	client = datastore.Client()

	query = client.query(kind='S5')
	result = list(query.fetch())
	a = ''
	for i in result:
		a += addrow(i)
        	#print (i['instrument1'])


	#a = '' 
	#for i in range(5):
	#	a += addrow()
	html = p1+a+p2		

	return html

def addrow(d):
	row = 	'''
<tr>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
 </tr>
		''' % (d['instrument1'])
	return row
