function cross(e,id) {
	if(e.src == 'https://storage.googleapis.com/pong-web-material/disable-cross.png')
	{
	   e.src="https://storage.googleapis.com/pong-web-material/enable-cross.png";
	   document.getElementById("check"+id).src="https://storage.googleapis.com/pong-web-material/disable-check.png";
	   save(id,'n')
	}
	else
	{
	   e.src="https://storage.googleapis.com/pong-web-material/disable-cross.png";
	   save(id,'')
	}
	
}

function check(e,id) {
   if(e.src == 'https://storage.googleapis.com/pong-web-material/disable-check.png')
   {
      e.src="https://storage.googleapis.com/pong-web-material/enable-check.png";
      document.getElementById("cross"+id).src="https://storage.googleapis.com/pong-web-material/disable-cross.png";
      save(id,'y')
   }
   else
   {
      e.src="https://storage.googleapis.com/pong-web-material/disable-check.png";
      save(id,'')
   }
}

function save (id,user_review) {
$.ajax({
		  type: 'POST',
		  url: "/test",
		  data : {'id':id,'user_review':user_review},
		  success: function(response){
		  output = response;

		  }
		}).done(function(data){

		});
}

function fetchdata(e,itemfrom,length1){
	
var ele = document.getElementsByClassName('w3-bar-item w3-button');
for (var i = 0; i < ele.length; i++ ) {
    ele[i].style.color = "white";
}
e.style.color = "red";
$.ajax({
		  type: 'POST',
		  url: "/getdata",
		  data : {'itemfrom':itemfrom,'length':length1},
		  success: function(response){
		  output = response;
		  list = document.getElementById('tablelist')
		  
		  while (list.hasChildNodes()) {  
			    list.removeChild(list.firstChild);
			}
			list.innerHTML = output 
		  }
		}).done(function(data){

		});
}