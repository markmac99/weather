#
# copyright Mark McIntyre, 2023-
#

amhdr = """
$(function() {
    var table = document.createElement("table");
    table.className = "table table-striped table-bordered table-hover table-condensed";
    var header = table.createTHead();
    header.className = "h4";
"""

amrwtempl= """
    var row = table.insertRow(0);
        var cell = row.insertCell(0);
        cell.innerHTML = "{}";
        var cell = row.insertCell(1);
        cell.innerHTML = "{} &deg;C";
        var cell = row.insertCell(2);
        cell.innerHTML = "{} &deg;C";
        var cell = row.insertCell(3);
        cell.innerHTML = "{} &deg;C";
        var cell = row.insertCell(4);
        cell.innerHTML = "{} &deg;C";
        var cell = row.insertCell(5);
        cell.innerHTML = "{} &deg;C";
        var cell = row.insertCell(6);
        cell.innerHTML = "{} &deg;C";
        var cell = row.insertCell(7);
        cell.innerHTML = "{} mm";
        var cell = row.insertCell(8);
        cell.innerHTML = "{}";
"""
amfootr = """
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
"""

refootr = """
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
var outer_div = document.getElementById("table{}{}");
outer_div.appendChild(table);
}})
"""

rerwtempl="""
var row = table.insertRow(0);
var cell = row.insertCell(0);
cell.innerHTML = "{}";
var cell = row.insertCell(1);
cell.innerHTML = "{} &deg;C";
var cell = row.insertCell(2);
cell.innerHTML = "{}%";
var cell = row.insertCell(3);
cell.innerHTML = "{} mph";
var cell = row.insertCell(4);
cell.innerHTML = "{} mph";
var cell = row.insertCell(5);
cell.innerHTML = "{} mm";
var cell = row.insertCell(6);
cell.innerHTML = "{} hPa";
"""
