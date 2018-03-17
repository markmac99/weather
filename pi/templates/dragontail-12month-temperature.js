$(function() {
Morris.Bar({
 element: 'dragontail-12month-temperature',
 data: [
#monthly#
#timezone local#
#jump -13#
#loop 12#
    {time: '#idx "%Y/%m"#',
    max_temp: #temp_out_max_hi#,
    min_temp: #temp_out_min_lo#
    },
#jump 1#
#endloop#
    {time: '#idx "%Y/%m"#',
    max_temp: #temp_out_max_hi#,
    min_temp: #temp_out_min_lo#
    }],
        xkey: 'time',
        ykeys: ['max_temp','min_temp'],
        labels: ['Max Temp', 'Min Temp'],
        xLabelAngle: 45,
        hideHover: 'auto',
		postUnits: '°C',
        resize: true
    });
});
