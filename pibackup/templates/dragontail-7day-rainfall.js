$(function() {
Morris.Bar({
 element: 'dragontail-7day-rainfall',
 data: [
#timezone local#
#roundtime True#
#daily#
#jump -8#
#loop 7#
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
