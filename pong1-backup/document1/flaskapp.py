from flask import Flask

app = Flask(__name__)

@app.route('/')

def hello_world():

   start = '''
<html>
<head>
<style>
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 33%;
    display:inline-block;
    float:left;
    padding: 3px;
}
td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
    font-size: 8px;
}
tr:nth-child(even) {
    background-color: #dddddd;
}
</style>
</head>
<body>
  <h1>Cointegrated currency exchange report</h1>
   '''

   end = '''
</body>
</html>
   '''



   html = createtable('D')
   html = html+createtable('S5')
   return start+html+end

def createtable(granularity):
        p1 =    '''
  <h2>Granularity: %s1</h2>
        '''.replace('%s1',granularity)

        from google.cloud import datastore
        from datetime import datetime
        client = datastore.Client()
        query = client.query(kind=granularity)
        result = list(query.fetch())
        a = ''
        for i in result:
                a += addrow(i)
        html = p1+a
        print (html)          
        return html
def addrow(d):
   from datetime import datetime
   table =   '''
      <table border = "0">
         <tr>
           <td colspan = "4">%s</td>
         </tr>
  		<tr>
            <td>instrument1</td>
            <td>instrument2</td>
            <td>from</td>
            <td>to</td>
         </tr>
         <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
         </tr>
  		<tr>
            <td>hedge ratio</td>
            <td>p-value</td>
            <td>mean</td>
            <td>std</td>
         </tr>
         <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
         </tr>
      </table>

   ''' % ("<a href='"+d['public_url']+"' target='_blank'><img src='"+d['public_url']+"' alt='No image' height=60 width=180></img></a>",d['instrument1'],d['instrument2'],datetime.strptime(d['from'][:19], "%Y-%m-%dT%H:%M:%S"),datetime.strptime(d['to'][:19], "%Y-%m-%dT%H:%M:%S"),d['hedge_ratio'],'%.03f' % float(d['p-value']),'%.06f' % float(d['mean']),'%.06f' % float(d['std']))
   return table


hello_world()

