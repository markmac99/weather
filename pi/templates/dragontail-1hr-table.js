$(function() {
    var table = document.createElement("table");
	table.className = "table table-striped table-bordered table-hover table-condensed";
	var header = table.createTHead();
	header.className = "h4";
#raw#
#timezone local#
#roundtime True#
#jump -11#
#loop 12#
	var row = table.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "#idx "%H:%M"#";	
    var cell = row.insertCell(1);
    cell.innerHTML = "#temp_out "%.1f &deg;C"#";
	var cell = row.insertCell(2);
    cell.innerHTML = "#hum_out "%d%%"#";
	var cell = row.insertCell(3);
    cell.innerHTML = "#wind_ave "%.0f mph" "" "wind_mph(x)"#";
	var cell = row.insertCell(4);
    cell.innerHTML = "#wind_gust "%.0f mph" "" "wind_mph(x)"#";
	var cell = row.insertCell(5);
    cell.innerHTML = "#calc "prevdata['rain'] - data['rain']" "%0.1f mm"#";
	var cell = row.insertCell(6);
    cell.innerHTML = "#rel_pressure "%.1f hPa"#";
#jump 1#
#endloop#
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
	var outer_div = document.getElementById("table1hrs");
	outer_div.appendChild(table);
})
