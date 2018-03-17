$(function() {
Morris.Line({
 element: 'dragontail-7day-wind',
 data: [
#hourly#
#timezone local#
#jump -169#
#loop 168#
    {time: #idx#000,
    ave: #wind_ave#,
    gust: #wind_gust#
    },
#jump 1#
#endloop#
    {time: #idx#000,
    ave: #wind_ave#,
    gust: #wind_gust#
    }],
        xkey: 'time',
        ykeys: ['ave','gust'],
        labels: ['Average','Gust'],
        xLabelAngle: 45,
        hideHover: 'auto',
		postUnits: 'mph',
        resize: true
    });
});
