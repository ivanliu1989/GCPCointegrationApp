from flask import Flask
import re
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
    width: 100%;
    display:inline-block;
    padding: 0px;
}
td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 4px;
    font-size: 8px;
}
tr:nth-child(even) {
    background-color: #dddddd;
}
.box{
  width: 30%;
  position: relative;
  display:inline-block;
}
.rightconner{
    position:absolute;
    top:5%;
    right:2%;
}
.leftconner{
    position:absolute;
    top:22%;
    right:2%;
}

</style>
</head>
<body>
  <h1>Cointegrated currency exchange report</h1>
   '''

   end = '''
    <script>
     function cross(e,i) {
         if(e.src == 'https://storage.googleapis.com/web-material/disable-cross.png')
         {
            e.src="https://storage.googleapis.com/web-material/enable-cross.png";
            document.getElementById("check"+i).src="https://storage.googleapis.com/web-material/disable-check.png";
         }
         else
         {
            e.src="https://storage.googleapis.com/web-material/disable-cross.png";
         }
     }
     function check(e,i) {
         if(e.src == 'https://storage.googleapis.com/web-material/disable-check.png')
         {
            e.src="https://storage.googleapis.com/web-material/enable-check.png";
            document.getElementById("cross"+i).src="https://storage.googleapis.com/web-material/disable-cross.png";
         }
         else
         {
            e.src="https://storage.googleapis.com/web-material/disable-check.png";
         }
     }
   </script> 
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
        c = 0
        for i in result:
                a += addrow(i,c)
                c = c+1
                if c == 10:
                        break
        html = p1+a
        print (html)          
        return html
def addrow(d,i):
   from datetime import datetime
   table =   '''
      <div class='box'>
      <table border = "0">
         <tr>
           <td colspan = "4">%image</td>
         </tr>
  		<tr>
            <td>instrument1</td>
            <td>instrument2</td>
            <td>from</td>
            <td>to</td>
         </tr>
         <tr>
            <td>%ins1</td>
            <td>%ins2</td>
            <td>%from</td>
            <td>%to</td>
         </tr>
  		<tr>
            <td>hedge ratio</td>
            <td>p-value</td>
            <td>mean</td>
            <td>std</td>
         </tr>
         <tr>
            <td>%hedge</td>
            <td>%pvalue</td>
            <td>%mean</td>
            <td>%std</td>
         </tr>
      </table>
      <img id='check%i' onclick="check(this,%i)" class='rightconner' src='https://storage.googleapis.com/web-material/%checkstatus-check.png' style='float:right'></img>
      <img id='cross%i' onclick="cross(this,%i)" class='leftconner' src='https://storage.googleapis.com/web-material/%crossstatus-cross.png' style='float:right'></img>      
      </div>
   '''
   table = table.replace('%image'  , "<a href='"+d['public_url']+"' target='_blank'><img src='"+d['public_url']+"' alt='No image' width=100%></img></a>")
   table = table.replace('%ins1'   , d['instrument1'])
   table = table.replace('%ins2'   , d['instrument2'])
   table = table.replace('%from'   , str(datetime.strptime(d['from'][:19], "%Y-%m-%dT%H:%M:%S")))
   table = table.replace('%to'     , str(datetime.strptime(d['to'][:19], "%Y-%m-%dT%H:%M:%S")))
   table = table.replace('%hedge'  , d['hedge_ratio'])
   table = table.replace('%pvalue' , '%.03f' % float(d['p-value']))
   table = table.replace('%mean'   , '%.06f' % float(d['mean']))
   table = table.replace('%std'    , '%.06f' % float(d['std']))
   table = table.replace('%i'      , re.sub(r'\W+','',str(datetime.strptime(d['to'][:19], "%Y-%m-%dT%H:%M:%S"))))
   if d['cointegrated'] == 'yes':
      table = table.replace('%checkstatus', 'enable')
   elif d['cointegrated'] == 'no':
      table = table.replace('%crossstatus', 'enable')
   else:
      table = table.replace('%checkstatus', 'disable')
      table = table.replace('%crossstatus', 'disable')
   #put(d)
   return table

hello_world()
