window.onload = function(){

	var getPerson = function(){
		var values = {};
		var xmlhttp = new XMLHttpRequest();
		var url = "https://randomuser.me/api/";
		xmlhttp.onreadystatechange = function() {
		    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
		        var data = JSON.parse(xmlhttp.responseText);
		       	values.sex = data.results[0].user.gender;
		    	values.first = data.results[0].user.name.first;
		    	values.last = data.results[0].user.name.last;
		    	console.log(values);
		    	storePeople(values);
		    }
		};
		xmlhttp.open("GET", url, true);
		xmlhttp.send();
	}
	var updateHTML = function(users){
		var firstVal = "";
		var lastVal = "";
		var sexVal = "";
		for(var y = 0; y < users.length; y++){
			firstVal = firstVal + users[y].first + "<br>";
		}
		for(var y = 0; y < users.length; y++){
			lastVal = lastVal + users[y].last + "<br>";
		}
		for(var y = 0; y < users.length; y++){
			sexVal = sexVal + users[y].sex + "<br>";
		}
		var first = document.getElementById('first');
		var last = document.getElementById('last');
		var sex = document.getElementById('sex');
		first.innerHTML = firstVal;
		last.innerHTML = lastVal;
		sex.innerHTML = sexVal;
	}
	users = [];
	var storePeople = function(person){
		users.push(person);
		console.log(users);
		if(users.length == 800){
			updateHTML(users);
		}
	}
	for(var x = 0; x < 800; x++){
		values = getPerson();
	}


}