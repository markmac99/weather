$(function() {
    var table = document.createElement("table");
	table.className = "table table-striped table-bordered table-hover table-condensed";
	var header = table.createTHead();
	header.className = "h4";
#timezone local#
#roundtime True#
#monthly#
#jump -1000#
#loop 1000#
	var row = table.insertRow(0);
    var cell = row.insertCell(0);
    cell.innerHTML = "#calc "data['start']+DAY" "%B %Y"#";	
    var cell = row.insertCell(1);
    cell.innerHTML = "#temp_out_max_hi "%.1f &deg;C"#";
	var cell = row.insertCell(2);
    cell.innerHTML = "#temp_out_max_ave "%.1f &deg;C"#";
	var cell = row.insertCell(3);
    cell.innerHTML = "#temp_out_max_lo "%.1f &deg;C"#";
	var cell = row.insertCell(4);
    cell.innerHTML = "#temp_out_min_hi "%.1f &deg;C"#";
	var cell = row.insertCell(5);
    cell.innerHTML = "#temp_out_min_ave "%.1f &deg;C"#";
	var cell = row.insertCell(6);
    cell.innerHTML = "#temp_out_min_lo "%.1f &deg;C"#";
	var cell = row.insertCell(7);
    cell.innerHTML = "#rain "%0.1f mm"#";
	var cell = row.insertCell(8);
    cell.innerHTML = "#rain_days "%d"#";	
#jump 1#
#endloop#
	var row = header.insertRow(0);
	var cell = row.insertCell(0);
	cell.innerHTML = "Highest";
	cell.className = "small";
	var cell = row.insertCell(1);
	cell.innerHTML = "Average";
	cell.className = "small";	
	var cell = row.insertCell(2);
	cell.innerHTML = "Lowest ";
	cell.className = "small";
	var cell = row.insertCell(3);
	cell.innerHTML = "Highest";
	cell.className = "small";
	var cell = row.insertCell(4);
	cell.innerHTML = "Average";
	cell.className = "small";
	var cell = row.insertCell(5);
	cell.innerHTML = "Lowest ";
	cell.className = "small";
	var row = header.insertRow(0);
	var cell = row.insertCell(0);
	cell.innerHTML = "Month";
	cell.rowSpan = 2;
	var cell = row.insertCell(1);
	cell.innerHTML = "Daytime Maximum";
	cell.colSpan = 3;
	cell.className = "small";
	var cell = row.insertCell(2);
    cell.innerHTML = "Nighttime Minimum";
	cell.colSpan = 3;
	cell.className = "small";	
	var cell = row.insertCell(3);
	cell.innerHTML = "Total";
	cell.rowSpan = 2;
	cell.className = "small";	
	var cell = row.insertCell(4);
	cell.innerHTML = "Rainy Days";
	cell.rowSpan = 2;
	cell.className = "small";
	var row = header.insertRow(0);
	var cell = row.insertCell(0);
	var cell = row.insertCell(1);
	cell.innerHTML = "Temperature";
	cell.colSpan = 6;
	var cell = row.insertCell(2);
	cell.innerHTML = "Rainfall";
	cell.colSpan = 2;
	var outer_div = document.getElementById("tableallmonths");
	outer_div.appendChild(table);
})