$(function() {
var total = 0;
Morris.Area({
 element: 'dragontail-24hr-rainfall',
 data: [
#timezone local#
#roundtime True#
#hourly#
#jump -25#
#loop 25#
    {time: #idx#000,
    rain: total = total + #rain#
    },
#jump 1#
#endloop#
],
        xkey: 'time',
        ykeys: ['rain'],
        labels: ['Rain'],
        hideHover: 'auto',
		postUnits: 'mm',
        resize: true,
		fillOpacity: 0.6,
		pointFillColors:['black'],
		pointStrokeColors: ['black'],
		lineColors:['red'],
		smooth: false,
    });
});
