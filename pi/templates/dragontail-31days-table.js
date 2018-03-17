$(function() {
    var table = document.createElement("table");
	table.className = "table table-striped table-bordered table-hover table-condensed";
	var header = table.createTHead();
	header.className = "h4";
#timezone local#
#roundtime True#
#daily#
#jump -30#
#loop 31#
	var row = table.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "#idx "%Y/%m/%d %H:%M %Z"#";	
    var cell = row.insertCell(1);
    cell.innerHTML = "#temp_out_max "%.1f &deg;C"#";
	var cell = row.insertCell(2);
    cell.innerHTML = "#temp_out_min "%.1f &deg;C"#";
	var cell = row.insertCell(3);
    cell.innerHTML = "#wind_ave "%.0f mph" "" "wind_mph(x)"#";
	var cell = row.insertCell(4);
    cell.innerHTML = "#wind_gust "%.0f mph" "" "wind_mph(x)"#";
	var cell = row.insertCell(5);
    cell.innerHTML = "#rain "%0.1f mm"#";
#jump 1#
#endloop#
	var row = header.insertRow(0);
	var cell = row.insertCell(0);
	cell.innerHTML = "Day Max";
	cell.className = "small";
	var cell = row.insertCell(1);
	cell.innerHTML = "Night Min";
	cell.className = "small";	
	var cell = row.insertCell(2);
	cell.innerHTML = "Ave";
	cell.className = "small";
	var cell = row.insertCell(3);
	cell.innerHTML = "Max";
	cell.className = "small";
	var row = header.insertRow(0);
	var cell = row.insertCell(0);
	cell.innerHTML = "24 hours ending";
	cell.rowSpan = 2;
	var cell = row.insertCell(1);
    cell.innerHTML = "Temperature";
	cell.colSpan = 2;		
	var cell = row.insertCell(2);
	cell.innerHTML = "Wind mph";
	cell.colSpan = 2;	
	var cell = row.insertCell(3);
	cell.innerHTML = "Rain";
	cell.rowSpan = 2;	   
	var outer_div = document.getElementById("table31days");
	outer_div.appendChild(table);
})