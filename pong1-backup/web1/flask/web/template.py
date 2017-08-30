from flask import url_for
body = '''
	<html>
	<head>
	<link rel="stylesheet" type="text/css" href="https://storage.googleapis.com/pong-web-material/css/style.css">
	<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">

	</head>
		<body>
			<h1>Cointegrated currency exchange report</h1>
			<h3>DE30_EUR & EUR_JPY</h3>
			<div class="noborder" style="overflow: auto; width: 100%; height: 500px; style='margin:0px'">
				<div class="noborder" style="width: 40000px;">
					<figure>
        			<embed type="image/svg+xml" src="/chart?instrument1=DE30_EUR&instrument2=EUR_JPY" />
        			</figure>
        		</div>
        	</div>
        	<h3>DE30_EUR & EUR_USD</h3>
			<div class="noborder" style="overflow: auto; width: 100%; height: 500px; style='margin:0px'">
				<div class="noborder" style="width: 40000px;">
					<figure>
        			<embed type="image/svg+xml" src="/chart?instrument1=DE30_EUR&instrument2=EUR_USD" />
        			</figure>
        		</div>
        	</div>
        	<h3>EUR_JPY & DE30_EUR</h3>
			<div class="noborder" style="overflow: auto; width: 100%; height: 500px; style='margin:0px'">
				<div class="noborder" style="width: 40000px;">
					<figure>
        			<embed type="image/svg+xml" src="/chart?instrument1=EUR_JPY&instrument2=DE30_EUR" />
        			</figure>
        		</div>
        	</div>
        	<h3>EUR_JPY & EUR_USD</h3>
        	<div class="noborder" style="overflow: auto; width: 100%; height: 500px; style='margin:0px'">
				<div class="noborder" style="width: 40000px;">
					<figure>
        			<embed type="image/svg+xml" src="/chart?instrument1=EUR_JPY&instrument2=EUR_USD" />
        			</figure>
        		</div>
        	</div>
        	<h3>EUR_USD & DE30_EUR</h3>
			<div class="noborder" style="overflow: auto; width: 100%; height: 500px; style='margin:0px'">
				<div class="noborder" style="width: 40000px;">
					<figure>
        			<embed type="image/svg+xml" src="/chart?instrument1=EUR_USD&instrument2=DE30_EUR" />
        			</figure>
        		</div>
        	</div>
        	<h3>EUR_USD & EUR_JPY</h3>
        	<div class="noborder" style="overflow: auto; width: 100%; height: 500px; style='margin:0px'">
				<div class="noborder" style="width: 40000px;">
					<figure>
        			<embed type="image/svg+xml" src="/chart?instrument1=EUR_USD&instrument2=EUR_JPY" />
        			</figure>
        		</div>
        	</div>
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
   
def getbodytemplate():
	return body
	
def gettabletemplate():
	return table