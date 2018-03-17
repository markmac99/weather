$(function() {
    var table = document.createElement("table");
	table.className = "table table-striped table-bordered table-hover table-condensed";
	var header = table.createTHead();
	header.className = "h4";
#timezone local#
#roundtime True#
#daily#
#jump -7#
#loop 7#
	var row = table.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "#idx "%Y/%m/%d %H:%M"#";	
    var cell = row.insertCell(1);
    cell.innerHTML = "#temp_out_max#";
	var cell = row.insertCell(2);
    cell.innerHTML = "#temp_out_min#";
	var cell = row.insertCell(3);
    cell.innerHTML = "#wind_ave#";
	var cell = row.insertCell(4);
    cell.innerHTML = "#wind_gust#";
	var cell = row.insertCell(5);
    cell.innerHTML = "#rain "%0.1f mm"#";
	var cell = row.insertCell(6);
    cell.innerHTML = "#rel_pressure#";
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
	var outer_div = document.getElementById("tabledaily");
	outer_div.appendChild(table);
})