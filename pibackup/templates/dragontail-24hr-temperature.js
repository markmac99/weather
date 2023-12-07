$(function() {
Morris.Line({
 element: 'dragontail-24hr-temperature',
 data: [
#hourly#
#timezone local#
#jump -24#
#loop 24#
    {time: #idx#000,
    temp: #temp_out#
    },
#jump 1#
#endloop#
    {time: #idx#000,
    temp: #temp_out#
    }],
        xkey: 'time',
        ykeys: ['temp'],
        labels: ['Temp'],
        hideHover: 'auto',
		postUnits: '°C',
        resize: true
    });
});
