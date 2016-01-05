$(document).ready(function(){

	$('#submit-manager').click(function(){
	  	managerData = {
			'managerEmail' : document.getElementById('manager-attribute').value,
			'client' : document.getElementById('client-attribute').value
	  	}
	  	console.log(managerData.managerEmail, managerData.client);
	    $.ajax({
	        type: 'POST',
	        url: 'manager-attribute',
	        data: JSON.stringify(managerData),
	        cache: false,
        	processData: false,
        	contentType: 'application/json; charset=utf-8'
	    })
	    .done(function(msg) {
	    	var resp = JSON.parse(msg);
	    	console.log(resp);
	    })
	    .fail(function() {
	      console.log("error");
	    })
	    .always(function() {
	      console.log("complete");
	    });
	});
})