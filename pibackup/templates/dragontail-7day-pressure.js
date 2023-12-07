$(function() {
Morris.Line({
 element: 'dragontail-7day-pressure',
 data: [
#hourly#
#timezone local#
#jump -169#
#loop 168#
    {time: #idx#000,
    pressure: #rel_pressure#
    },
#jump 1#
#endloop#
    {time: #idx#000,
    pressure: #rel_pressure#
    }],
        xkey: 'time',
        ykeys: ['pressure'],
        labels: ['Pressure'],
        xLabelAngle: 45,
		ymax: 1050,
		ymin: 960,
        hideHover: 'auto',
		postUnits: 'hPa',
        resize: true
    });
});
