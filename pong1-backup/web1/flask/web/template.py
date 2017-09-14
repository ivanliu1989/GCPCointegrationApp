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

		.nvd3 .nv-groups .nv-point {
		  transition: stroke-width 250ms linear, stroke-opacity 250ms linear;
		  -moz-transition: stroke-width 250ms linear, stroke-opacity 250ms linear;
		  -webkit-transition: stroke-width 250ms linear, stroke-opacity 250ms linear;
		}
		
		.nvd3.nv-scatter .nv-groups .nv-point.hover {
		  stroke-width: 15px;
		  fill-opacity: .5 !important;
		  stroke-opacity: .5 !important;
		}
		
		.nvd3.nv-scatter{
		  stroke-width: 4px;
		  fill-opacity: .5 !important;
		  stroke-opacity: .5 !important;
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
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
	<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
	<link rel="stylesheet" href="https://cdn.rawgit.com/novus/nvd3/v1.8.1/build/nv.d3.css">
	<script src="https://d3js.org/d3.v4.min.js"></script>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.4/nv.d3.min.css"/>
  	<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.min.js" charset="utf-8"></script>
  	<script src="https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.4/nv.d3.min.js"></script>
	</head>
		<body style='padding:20px'>
			<h1>LSTM abnormal pattern detection</h1>
			<div class="row">
		    %chart
		  </div>
		</body>
	</html>
   '''
lstmtable = '''
	  <div>
		  <h4 style="text-align:center">%serie1</h4>
			<div id="chart%id" style='height:400px;'>
					<svg></svg>
			</div>
	  </div>
	
	<script>

		chartdata%id =[{"key": "%serie1", "yAxis": "1", "type": "line", "values": %data0},
							{"key": "prediction", "yAxis": "1", "type": "line", "values": %data1},
							{"key": "square error", "yAxis": "2", "type": "line", "color": "rgba(255, 105, 105, 0.6)", "values": %data2}];
		nv.addGraph(function() {
		var chart = nv.models.multiChart()
			.margin({top:0,right:150,bottom:0,left:150})
        	.height(300);;
		
		chart.xAxis.tickFormat(function(d) {
		 // Will Return the date, as "%m/%d/%Y"(08/06/13)
		 return d3.time.format.utc('%Y-%m-%d')(new Date(d*1000))
		});
		
		var xAxis = nv.models.axis()
                xAxis
	              .axisLabel('Date')
	              .tickFormat(function(d) { console.log(d); return d3.time.format('%Y-%m-%d')(d); })
	              .scale(
	                  d3.time.scale().
	                      domain([new Date(%datefrom), new Date(%dateto)])
	              );

      chart.xAxis = xAxis
      
      chart.lines1.xDomain([new Date(%datefrom), new Date(%dateto)])
      chart.lines2.xDomain([new Date(%datefrom), new Date(%dateto)])



 

		chart.yAxis1
			.tickFormat(d3.format(',.4f'));
			
		chart.yAxis2
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

				return "<div style='padding:3px;'><div><b>"+d3.time.format.utc('%Y-%m-%d %H:%M:%S')(new Date(x*1000))+"</b></div>"+"<div>"+d3.format(',.4f')(value)+"</div></div>";        	

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
   
def getbodytemplate():
	return body
	
def gettabletemplate():
	return table
	
def getcointtemplate():
	return coint
	
def getlstmtemplate():
	return lstm
	
def getlstmtable():
	return lstmtable