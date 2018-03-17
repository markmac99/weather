$(function() {
    var table = document.createElement("table");
	table.className = "table table-striped table-bordered table-hover table-condensed";
	var header = table.createTHead();
	header.className = "h4";





	var row = table.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "16:52";	
    var cell = row.insertCell(1);
    cell.innerHTML = "12.5 &deg;C";
	var cell = row.insertCell(2);
    cell.innerHTML = "84%";
	var cell = row.insertCell(3);
    cell.innerHTML = "2 mph";
	var cell = row.insertCell(4);
    cell.innerHTML = "4 mph";
	var cell = row.insertCell(5);
    cell.innerHTML = "0.0 mm";
	var cell = row.insertCell(6);
    cell.innerHTML = "1011.6 hPa";


	var row = table.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "17:52";	
    var cell = row.insertCell(1);
    cell.innerHTML = "11.3 &deg;C";
	var cell = row.insertCell(2);
    cell.innerHTML = "85%";
	var cell = row.insertCell(3);
    cell.innerHTML = "4 mph";
	var cell = row.insertCell(4);
    cell.innerHTML = "8 mph";
	var cell = row.insertCell(5);
    cell.innerHTML = "1.5 mm";
	var cell = row.insertCell(6);
    cell.innerHTML = "1012.6 hPa";


	var row = table.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "18:52";	
    var cell = row.insertCell(1);
    cell.innerHTML = "10.4 &deg;C";
	var cell = row.insertCell(2);
    cell.innerHTML = "81%";
	var cell = row.insertCell(3);
    cell.innerHTML = "4 mph";
	var cell = row.insertCell(4);
    cell.innerHTML = "8 mph";
	var cell = row.insertCell(5);
    cell.innerHTML = "0.0 mm";
	var cell = row.insertCell(6);
    cell.innerHTML = "1013.2 hPa";


	var row = table.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "19:52";	
    var cell = row.insertCell(1);
    cell.innerHTML = "10.1 &deg;C";
	var cell = row.insertCell(2);
    cell.innerHTML = "81%";
	var cell = row.insertCell(3);
    cell.innerHTML = "3 mph";
	var cell = row.insertCell(4);
    cell.innerHTML = "5 mph";
	var cell = row.insertCell(5);
    cell.innerHTML = "0.0 mm";
	var cell = row.insertCell(6);
    cell.innerHTML = "1013.0 hPa";


	var row = table.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "20:52";	
    var cell = row.insertCell(1);
    cell.innerHTML = "9.9 &deg;C";
	var cell = row.insertCell(2);
    cell.innerHTML = "86%";
	var cell = row.insertCell(3);
    cell.innerHTML = "2 mph";
	var cell = row.insertCell(4);
    cell.innerHTML = "4 mph";
	var cell = row.insertCell(5);
    cell.innerHTML = "0.0 mm";
	var cell = row.insertCell(6);
    cell.innerHTML = "1012.9 hPa";


	var row = table.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "21:52";	
    var cell = row.insertCell(1);
    cell.innerHTML = "10.2 &deg;C";
	var cell = row.insertCell(2);
    cell.innerHTML = "86%";
	var cell = row.insertCell(3);
    cell.innerHTML = "1 mph";
	var cell = row.insertCell(4);
    cell.innerHTML = "4 mph";
	var cell = row.insertCell(5);
    cell.innerHTML = "0.0 mm";
	var cell = row.insertCell(6);
    cell.innerHTML = "1012.8 hPa";


	var row = table.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "22:22";	
    var cell = row.insertCell(1);
    cell.innerHTML = "9.7 &deg;C";
	var cell = row.insertCell(2);
    cell.innerHTML = "87%";
	var cell = row.insertCell(3);
    cell.innerHTML = "2 mph";
	var cell = row.insertCell(4);
    cell.innerHTML = "4 mph";
	var cell = row.insertCell(5);
    cell.innerHTML = "0.0 mm";
	var cell = row.insertCell(6);
    cell.innerHTML = "1012.8 hPa";


	var row = header.insertRow(0);
	var cell = row.insertCell(0);
	cell.innerHTML = "Ave";
	cell.className = "small";
	var cell = row.insertCell(1);
	cell.innerHTML = "Max";
	cell.className = "small";
	var row = header.insertRow(0);
	var cell = row.insertCell(0);
	cell.innerHTML = "Time";
	cell.rowSpan = 2;
	var cell = row.insertCell(1);
    cell.innerHTML = "Temp";
	cell.rowSpan = 2;	
	var cell = row.insertCell(2);
	cell.innerHTML = "Humid";
	cell.rowSpan = 2;	
	var cell = row.insertCell(3);
	cell.innerHTML = "Wind mph";
	cell.colSpan = 2;	
	var cell = row.insertCell(4);
	cell.innerHTML = "Rain";
	cell.rowSpan = 2;	
	var cell = row.insertCell(5);
	cell.innerHTML = "Pressure";
	cell.rowSpan = 2;    
	var outer_div = document.getElementById("table6hrs");
	outer_div.appendChild(table);
})