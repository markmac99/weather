$(function() {
Morris.Line({
 element: 'dragontail-24hr-wind',
 data: [
#hourly#
#timezone local#
#jump -25#
#loop 24#
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
        hideHover: 'auto',
		postUnits: 'mph',
        resize: true
    });
});
