$(function() {
Morris.Bar({
 element: 'dragontail-12month-rainfall',
 data: [
#timezone local#
#roundtime True#
#monthly#
#jump -13#
#loop 12#
    {time: '#idx "%Y/%m"#',
    rain: #rain#
    },
#jump 1#
#endloop#
    {time: '#idx "%Y/%m"#',
    rain: #rain#
    }],
        xkey: 'time',
        ykeys: ['rain'],
        labels: ['Rain'],
        xLabelAngle: 45,
        hideHover: 'auto',
		postUnits: 'mm',
        resize: true
    });
});
