$(function() {
    var table = document.createElement("table");
	table.className = "table table-striped table-bordered table-hover table-condensed";
	var header = table.createTHead();
	header.className = "h4";





	var row = table.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "15:55";	
    var cell = row.insertCell(1);
    cell.innerHTML = "0.4 &deg;C";
	var cell = row.insertCell(2);
    cell.innerHTML = "53%";
	var cell = row.insertCell(3);
    cell.innerHTML = "11 mph";
	var cell = row.insertCell(4);
    cell.innerHTML = "15 mph";
	var cell = row.insertCell(5);
    cell.innerHTML = "0.0 mm";
	var cell = row.insertCell(6);
    cell.innerHTML = "1007.3 hPa";


	var row = table.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "16:55";	
    var cell = row.insertCell(1);
    cell.innerHTML = "-0.9 &deg;C";
	var cell = row.insertCell(2);
    cell.innerHTML = "68%";
	var cell = row.insertCell(3);
    cell.innerHTML = "6 mph";
	var cell = row.insertCell(4);
    cell.innerHTML = "14 mph";
	var cell = row.insertCell(5);
    cell.innerHTML = "0.0 mm";
	var cell = row.insertCell(6);
    cell.innerHTML = "1007.5 hPa";


	var row = table.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "17:55";	
    var cell = row.insertCell(1);
    cell.innerHTML = "-1.1 &deg;C";
	var cell = row.insertCell(2);
    cell.innerHTML = "73%";
	var cell = row.insertCell(3);
    cell.innerHTML = "9 mph";
	var cell = row.insertCell(4);
    cell.innerHTML = "15 mph";
	var cell = row.insertCell(5);
    cell.innerHTML = "0.0 mm";
	var cell = row.insertCell(6);
    cell.innerHTML = "1007.8 hPa";


	var row = table.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "18:55";	
    var cell = row.insertCell(1);
    cell.innerHTML = "-1.6 &deg;C";
	var cell = row.insertCell(2);
    cell.innerHTML = "81%";
	var cell = row.insertCell(3);
    cell.innerHTML = "8 mph";
	var cell = row.insertCell(4);
    cell.innerHTML = "14 mph";
	var cell = row.insertCell(5);
    cell.innerHTML = "0.0 mm";
	var cell = row.insertCell(6);
    cell.innerHTML = "1007.8 hPa";


	var row = table.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "19:55";	
    var cell = row.insertCell(1);
    cell.innerHTML = "-1.9 &deg;C";
	var cell = row.insertCell(2);
    cell.innerHTML = "86%";
	var cell = row.insertCell(3);
    cell.innerHTML = "6 mph";
	var cell = row.insertCell(4);
    cell.innerHTML = "11 mph";
	var cell = row.insertCell(5);
    cell.innerHTML = "0.0 mm";
	var cell = row.insertCell(6);
    cell.innerHTML = "1007.6 hPa";


	var row = table.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "20:55";	
    var cell = row.insertCell(1);
    cell.innerHTML = "-2.0 &deg;C";
	var cell = row.insertCell(2);
    cell.innerHTML = "89%";
	var cell = row.insertCell(3);
    cell.innerHTML = "6 mph";
	var cell = row.insertCell(4);
    cell.innerHTML = "11 mph";
	var cell = row.insertCell(5);
    cell.innerHTML = "0.0 mm";
	var cell = row.insertCell(6);
    cell.innerHTML = "1007.5 hPa";


	var row = table.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "21:25";	
    var cell = row.insertCell(1);
    cell.innerHTML = "-2.0 &deg;C";
	var cell = row.insertCell(2);
    cell.innerHTML = "90%";
	var cell = row.insertCell(3);
    cell.innerHTML = "5 mph";
	var cell = row.insertCell(4);
    cell.innerHTML = "9 mph";
	var cell = row.insertCell(5);
    cell.innerHTML = "0.0 mm";
	var cell = row.insertCell(6);
    cell.innerHTML = "1007.5 hPa";


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