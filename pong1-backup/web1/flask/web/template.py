from flask import url_for

'''
<h3>EUR_JPY & EUR_USD</h3>
        	<div class="noborder" style="overflow: auto; width: 100%; height: 500px; style='margin:0px'">
				<div class="noborder" style="width: 40000px;">
					<figure>
        			<embed type="image/svg+xml" src="/chart?instrument1=EUR_JPY&instrument2=EUR_USD"/>
        			</figure>
        		</div>
        	</div>
'''
body = '''
	<html>
	<head>
	<link rel="stylesheet" type="text/css" href="https://storage.googleapis.com/pong-web-material/css/style.css">
	<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
	<link rel="stylesheet" href="https://cdn.rawgit.com/novus/nvd3/v1.8.1/build/nv.d3.css">
	<style>
		.cointchart g.nv-scatter g.nv-series-2 path.nv-point
		{
		    stroke-opacity: 0.5 !important;
		    stroke-width: 15px;
		}
		.cointchart g.nv-series-2 path.nv-line
		{
		    stroke-opacity: 0;
		}
	</style>
	</head>
		<body>
			<script src="https://d3js.org/d3.v4.min.js"></script>
			<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.4/nv.d3.min.css"/>
  			<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.min.js" charset="utf-8"></script>
  			<script src="https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.4/nv.d3.min.js"></script>
  			
			<h1 style="text-align:center">%title</h1>
			

        	
        	<div>%nvd3chart</div>
			<div class="w3-bar w3-black">%tabnum</div>
			<div id='tablelist'>%table</div>
			<script src="https://storage.googleapis.com/pong-web-material/js/jquery-3.2.1.min.js"></script>
			<script src="https://storage.googleapis.com/pong-web-material/js/script.js"></script>
		</body>
	</html>
	'''

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
	      <img id='check%i' onclick="check(this,'%i')" class='rightconner1' src='https://storage.googleapis.com/pong-web-material/%checkstatus-check.png' style='float:right'></img>
	      <img id='cross%i' onclick="cross(this,'%i')" class='rightconner2' src='https://storage.googleapis.com/pong-web-material/%crossstatus-cross.png' style='float:right'></img>
	      <div class='leftconner'>%order</div>      
      </div>
   '''
coint =   '''
      <html>
	<head>
	<link rel="stylesheet" type="text/css" href="https://storage.googleapis.com/pong-web-material/css/style.css">
	</head>
		<body style='padding:20px'>
			<h1>Cointegration</h1>
			<table style='height:400px;'>
			<col width="100%">

			<tr>
			<td>
			<img src='%chart' width='100%'>
			</td>
			<td>
			  <div style='width:480px; height:400px; overflow-y: scroll; padding:5px;'>
			  <table id="data">
			    <thead>
			      <tr>
			        <th>Parameter</th>
			        <th colspan="3">Value</th>
			      </tr>
			    </thead>
			    <tbody>
			      <tr>
			        <td>Instrument 1</td>
			        <td colspan="3">%instrument1</td>
			      </tr>
			      <tr>
			        <td>Instrument 2</td>
			        <td colspan="3">%instrument2</td>
			      </tr>
			      <tr>
			        <td>From</td>
			        <td colspan="3">%datefrom</td>
			      </tr>
			      <tr>
			        <td>To</td>
			        <td colspan="3">%dateto</td>
			      </tr>
			      <tr>
			        <td>Hedge ratio</td>
			        <td colspan="3">%hedge_ratio</td>
			      </tr>
			      <tr>
			        <td>Coefficient 1</td>
			        <td colspan="3">%coeff1</td>
			      </tr>
			      <tr>
			        <td>Coefficient 2</td>
			        <td colspan="3">%coeff2</td>
			      </tr>
			      <tr>
			        <td>Mean</td>
			        <td colspan="3">%mean</td>
			      </tr>
			      <tr>
			        <td>Standard deviation</td>
			        <td colspan="3">%std</td>
			      </tr>
			      <tr>
			        <td>P-value</td>
			        <td colspan="3">%p_value</td>
			      </tr>
			    </tbody>
			    
			    <thead>
			      <tr>
			        <th colspan="4">Data</th>
			      </tr>
			    </thead>
			      <tr>
			        <th>Date</th>
			        <th>%instrument1</th>
			        <th>Date</th>
			        <th>%instrument2</th>
			      </tr>
			    </thead>
			    <tbody>
			    	%fxdata
			    </tbody>
			  </table>
			  </div>
			  <div style='padding:5px;'><button id='export' onclick="exportfile()">export</button></div>
			  </td>
			  </tr>
			</table>
			<script src="https://storage.googleapis.com/pong-web-material/js/jquery-3.2.1.min.js"></script>
			<script src="https://storage.googleapis.com/pong-web-material/js/FileSaver.min.js"></script>
			<script src="https://storage.googleapis.com/pong-web-material/js/tableexport.min.js"></script>
			<script type="text/javascript">
			 var tableId = 'data';
		    var ExportButtons = document.getElementById(tableId);
		    var instance = new TableExport(ExportButtons, {
		        formats: ['xls', 'csv'],
		        exportButtons: false
		    });
		    var CSV = instance.CONSTANTS.FORMAT.CSV;
		    var exportDataCSV = instance.getExportData()[tableId][CSV];
		    var bytesCSV = instance.getFileSize(exportDataCSV.data, exportDataCSV.fileExtension);
		    
			function exportfile() {
					instance.export2file(exportDataCSV.data, exportDataCSV.mimeType, exportDataCSV.filename, exportDataCSV.fileExtension);
				}
				 
			</script>
		</body>
	</html>
   '''
      
lstm =   '''
      <html>
	<head>
	<link rel="stylesheet" type="text/css" href="https://storage.googleapis.com/pong-web-material/css/style.css">
	<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">

	</head>
		<body>
			<h1>LSTM currency exchange forecast</h1>
			<h3>EUR_USD</h3>
			<div class="noborder" style="overflow: auto; width: 100%; height: 500px; style='margin:0px'">
				<div class="noborder" style="width: 100%;">
					<figure>
        			<embed type="image/svg+xml" src="/lstm/lstmchart?instrument=EUR_USD" />
        			</figure>
        		</div>
        	</div>
		</body>
	</html>
   '''
   
def getbodytemplate():
	return body
	
def gettabletemplate():
	return table
	
def getcointtemplate():
	return coint
	
def getlstmtemplate():
	return lstm