$(function() {
Morris.Line({
 element: 'dragontail-7day-temperature',
 data: [
#hourly#
#timezone local#
#jump -168#
#loop 168#
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
        xLabelAngle: 45,
        hideHover: 'auto',
		postUnits: '°C',
        resize: true
    });
});
