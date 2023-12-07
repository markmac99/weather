$(function() {
Morris.Line({
 element: 'dragontail-28day-pressure',
 data: [
#hourly#
#timezone local#
#jump -673#
#loop 672#
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
		ymax: 1050,
		ymin: 960,
		xLabelAngle: 45,
		postUnits: 'hPa',
        resize: true
    });
});
