$(function() {
Morris.Line({
 element: 'dragontail-recent-temperature',
 data: [
#raw#
#timezone local#
#jump -50#
#loop 50#
    {time: #idx#000,
    temp: #temp_out#
    },
#jump 1#
#endloop#
    {time: #idx#000,
    temp: #temp_out#
    }
       ],
        xkey: 'time',
        ykeys: ['temp'],
        labels: ['Temp'],
        hideHover: 'auto',
		postUnits: '°C',
        resize: true
    });
});
