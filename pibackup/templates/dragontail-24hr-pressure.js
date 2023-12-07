$(function() {
Morris.Line({
 element: 'dragontail-24hr-pressure',
 data: [
#hourly#
#timezone local#
#jump -25#
#loop 24#
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
        hideHover: 'auto',
		xLabelAngle: 45,
		ymax: 1050,
		ymin: 960,
		postUnits: 'hPa',
        resize: true
    });
});
