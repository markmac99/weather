$(function() {
Morris.Bar({
 element: 'dragontail-28day-temperature',
 data: [
#daily#
#timezone local#
#jump -29#
#loop 28#
    {time: '#idx "%Y/%m/%d"#',
    max_temp: #temp_out_max#,
    min_temp: #temp_out_min#
    },
#jump 1#
#endloop#
    {time: '#idx "%Y/%m/%d"#',
    max_temp: #temp_out_max#,
    min_temp: #temp_out_min#
    }],
        xkey: 'time',
        ykeys: ['max_temp','min_temp'],
        labels: ['Max Temp', 'Min Temp'],
        xLableAngle: 45,
        hideHover: 'auto',
		postUnits: '°C',
        resize: true
    });
});
