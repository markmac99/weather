$(function() {
Morris.Bar({
 element: 'dragontail-28day-rainfall',
 data: [
#timezone local#
#roundtime True#
#daily#
#jump -29#
#loop 28#
    {time: '#idx "%Y/%m/%d"#',
    rain: #rain#
    },
#jump 1#
#endloop#
    {time: '#idx "%Y/%m/%d"#',
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
