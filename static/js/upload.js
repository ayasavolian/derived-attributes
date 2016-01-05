$(document).ready(function(){

	var updateError = function(resp){
		html = "";
		if(resp['error']["manager missing"]){
			console.log("error thrown for manager");
			html += "There are managers missing from this CSV. The managers have the IDs: ";
			for (value in resp['receipt']){
				html += resp['receipt'][value] + ' ';
			}
			html += "</br></br>";
		}
		if(resp['error']["missing essential date fields"]){
			console.log("missing essential date fields");
			html += "You're missing essential date fields. Please look at the fields you chose again";
			html += "</br></br>";
		}
		if(resp['error']["missing manager fields"]){
			console.log("missing manager fields");
			html += "Not a blocker, but you didnt choose manager fields (Employee ID & Manager Employee ID). No manager data will be generated (manager email, direct reports, indirect reports)";
			html += "</br></br>";
		}
		if(resp['error']["date format match"]){
			console.log("date format match");
			html += "The date format chosen does not match the actual format of the fields available. Please choose another option";
			html += "</br></br>";
		}
		if(resp['error']["no date chosen"]){
			console.log("date option not chosen");
			html += "A date format was not chosen. Please choose from the drop down below to continue.";
			html += "</br></br>";
		}
		if(resp['error']["missing termination date"]){
			console.log("missing termination date field");
			html += "The termination date field is missing so we cannot calculate if the employees are active/inactive";
			html += "</br></br>";
		}
		if(html != ""){
			var error = document.getElementById('error');
			error.innerHTML = html;
			error.style.display = "block";
		}
		console.log(resp)
		if(!resp['error']["manager missing"] && !resp['error']["missing essential date fields"]){
		    uploadedData.showUpdate(resp);
		}
	}

	var Data = function(){
		this.Vals;
		this.fieldLength;
		this.lengthShown = 500;
		tenureLength = 1;
		generationLength = 1;
		tenureVals = [];
		generationVals = [];
	}

	Data.prototype.showDisplay = function(iteration){
		var div = document.getElementById('second'),
			fieldsDiv = document.getElementById('columns');
			html = "",
			fields = "";
		if(this.Vals.length < this.lengthShown)
			this.lengthShown = this.Vals.length
		for(var x = 0; x < this.lengthShown; x++){
			var array = this.Vals[x];
			if(x == 0)
				this.fieldLength = array.length;
			for (var y = 0; y < array.length; y++){
				if(y == 0){
					html += "<div class = 'overflow'>";
					var length = (array.length * 305).toString();
					length += "px";
					div.style.width = length;
				}
				if(x == 0){
					html += "<div class = 'column-header bold'>";
					fields += "<div class = 'block overflow'>" +
								"<div class = 'column-header float-left bold'>" +
								array[y] + "</div>" +
								"<div class = 'fields-header float-left bold'>" +
									"<select id = 'field"+[y]+"' >" + 
									  "<option value='none'>None</option>" +
									  "<option value='hireDate'>Original Hire Date</option>" +
									  "<option value='birthYear'>Birth Year</option>" +
									  "<option value='Age'>Age</option>" +
									  "<option value='employeeID'>Employee ID</option>" +
									  "<option value='ManagerEmployeeID'>Manager Employee ID</option>" +
									  "<option value='Email'>Email Address</option>" +
									  "<option value='startDate'>Start Date (Current Position)</option>" +
									  "<option value='terminationDate'>Termination Date</option>" +
									"</select>" +
								"</div>";
				}
				else{
					html += "<div class = 'column-header display'>";
				}
				html += array[y] + "</div>";
				if(y == array.length-1)
					html += "</div>";
					fields += "</div>";
			}
		}
    	document.getElementById('download-button').style.display = "block";
    	document.getElementById('csv').value = this.Vals;
    	document.getElementById('length').value = this.fieldLength;
		fieldsDiv.innerHTML = fields;
		div.innerHTML = html;
	}

	Data.prototype.display = function(data){
		this.Vals = data.csv_response;
		uploadedData.showDisplay();
		document.getElementById('save-button').style.display = "block";
		document.getElementById('date-options').style.display = "block";
	}

	Data.prototype.update = function(){
		var fields = {},
			div = document.getElementById('second'),
			fieldsDiv = document.getElementById('columns'),
			html = "",
			dateFormat = document.getElementById('date-format'),
			dateFormatStr = dateFormat.options[dateFormat.selectedIndex].text;
			generationFormat = document.getElementById("generation-format"),
			generationFormatStr = generationFormat.options[generationFormat.selectedIndex].text; 
			tenureFormat = document.getElementById("tenure-format"),
			tenureFormatStr = tenureFormat.options[tenureFormat.selectedIndex].text; 
			tenureArr = [],
			generationArr = [];
		for(var z = 0; z < this.fieldLength; z++){
			var tempField = "field" + z.toString();
			var e = document.getElementById(tempField);
			var str = e.options[e.selectedIndex].text;
			if (str == "Original Hire Date"){
				fields.hireDate = z;
			}
			else if(str == "Birth Year"){
				fields.birthYear = z;
			}
			else if(str == "Age"){
				fields.age = z;
			}
			else if(str == "Start Date (Current Position)"){
				fields.startDate = z;
			}
			else if(str == "Employee ID"){
				fields.employeeID = z;
			}
			else if(str == "Manager Employee ID"){
				fields.managerEmployeeID = z;
			}
			else if(str == "Email Address"){
				fields.email = z;
			}
			else if(str == "Termination Date"){
				fields.terminationDate = z;
			}
			else{}
		}
		console.log(tenureLength, generationLength)
		if(tenureLength != 1 && tenureFormatStr != "Default"){
			for(var x = 1; x <= tenureLength; x++){
				tenureArr.push({
					'title' : document.getElementById('tenure-title'+x).value,
					'start' : document.getElementById('custom-tenure-start'+x).value,
					'end' : document.getElementById('custom-tenure-end'+x).value
				});
			}
		}
		if(generationLength != 1 && generationFormatStr != "Default"){
			for(var y = 1; y <= generationLength; y++){
				generationArr.push({
					'title' : document.getElementById('generation-title'+y).value,
					'start' : document.getElementById('custom-generation-start'+y).value,
					'end' : document.getElementById('custom-generation-end'+y).value
				});			
			}
		}
		fields.dateFormat = dateFormatStr;
		var previewData = {
			'positions' : fields,
			'csv' : this.Vals,
			'generationArr' : generationArr,
			'tenureArr' : tenureArr
		}
	    $.ajax({
	        type: 'POST',
	        url: 'upload-preview',
	        data: JSON.stringify(previewData),
	        cache: false,
        	processData: false,
        	contentType: 'application/json; charset=utf-8'
	    })
	    .done(function(msg) {
	    	var resp = JSON.parse(msg);
	    	updateError(resp);
	    })
	    .fail(function() {
	      console.log("error");
	    })
	    .always(function() {
	      console.log("complete");
	    });
	    console.log("test");
	}

	Data.prototype.showUpdate = function(update){
		this.Vals = update.receipt;
		uploadedData.showDisplay();
	}

	var uploadedData = new Data();

	Data.prototype.updateDateLength = function(dateType){
		if(dataType == "tenure"){
			tenureLength++
			$('#tenure-container').append('<div class = "tenure-selection">' +
									'<div id = "custom-tenure'+tenureLength+'" class = "tenure">' +
										'<div class = "tenure-title-container display">' +
											'<div class = "custom-tenure-title" class = "float-left">' +
												'Tenure Title:' +
											'</div>' +
											'<input type = "text" id = "tenure-title'+tenureLength+'" class = "float-left">' +
										'</div>' +
										'<div class = "custom-tenure-container display">' +
											'<div class = "custom-tenure-label" class = "float-left">' +
												'Range in Days:' +
											'</div>' +
											'<input placeholder = "Start" type = "number" id = "custom-tenure-start'+tenureLength+'" class = "float-left tenure-margin">' +
											'<input placeholder = "End" type = "number" id = "custom-tenure-end'+tenureLength+'" class = "float-left">' +
										'</div>' +
									'</div>' +
								'</div>');
		}
		else{
			generationLength++
			$('#generation-container').append('<div class = "generation-selection">' +
								'<div id = "custom-generation1" class = "generation">' +
									'<div class = "tenure-title-container display">' +
										'<div class = "custom-tenure-title" class = "float-left">' +
											'Generation Title:' +
										'</div>' +
										'<input type = "text" id = "generation-title'+generationLength+'" class = "float-left">' +
									'</div>' +
								'<div class = "custom-tenure-container display">' +
									'<div class = "custom-tenure-label" class = "float-left">' +
										'Year Range:' +
									'</div>' +
									'<input placeholder = "Start" type = "number" id = "custom-generation-start'+generationLength+'" class = "float-left tenure-margin">' +
									'<input placeholder = "End" type = "number" id = "custom-generation-end'+generationLength+'" class = "float-left">' +
								'</div>' +
							'</div>');
		}
	}

	// Data.prototype.download = function(){
 // 		$.ajax({
	//         type: 'GET',
	//         url: 'download-csv',
	//         data: this.Vals,
	//         cache: false,
 //        	contentType: false,
 //        	processData: false
	//     })
	//     .done(function(msg) {
	//     	// console.log(msg)
	//     })
	//     .fail(function() {
	//       console.log("error");
	//     })
	//     .always(function() {
	//       console.log("complete");
	//     });
	// }

	var passData = function(data){
		uploadedData.display(data);

	}


	$('#save-button').click(function(){
		uploadedData.update();
	});

	$(':button').click(function(){
	  	var formData = new FormData($('form')[0]);
	    $.ajax({
	        type: 'POST',
	        url: 'uploader',
	        data: formData,
	        cache: false,
        	contentType: false,
        	processData: false
	    })
	    .done(function(msg) {
	    	passData(JSON.parse(msg));
	    })
	    .fail(function() {
	      console.log("error");
	    })
	    .always(function() {
	      console.log("complete");
	    });
	});

	// $('#download-button').click(function(){
	// 	window.open("/download-csv",'_blank');
	// 	// uploadedData.download();
	// });

	$('#tenure-format').change(function(){
		var tenureFormat = document.getElementById("tenure-format"),
			tenureFormatStr = tenureFormat.options[tenureFormat.selectedIndex].text; 
		if(tenureFormatStr == "Custom"){
			document.getElementById('tenure-container').style.display = "block";
			document.getElementById('add-tenure').style.display = "block";
		}
		else{
			document.getElementById('tenure-container').style.display = "none";
			document.getElementById('add-tenure').style.display = "none";			
		}
	});

	$('#add-tenure').click(function(){
		dataType = "tenure";
		uploadedData.updateDateLength(dataType);
		tenureContainer = document.getElementById("tenure-container");
	});

	$('#generation-format').change(function(){
		var generationFormat = document.getElementById("generation-format"),
			generationFormatStr = generationFormat.options[generationFormat.selectedIndex].text; 
		if(generationFormatStr == "Custom"){
			document.getElementById('generation-container').style.display = "block";
			document.getElementById('add-generation').style.display = "block";
		}
		else{
			document.getElementById('generation-container').style.display = "none";
			document.getElementById('add-generation').style.display = "none";			
		}
	});

	$('#add-generation').click(function(){
		dataType = "generation";
		uploadedData.updateDateLength(dataType);
		tenureContainer = document.getElementById("tenure-generation");
	});
})