$(function() {
Morris.Bar({
 element: 'dragontail-recent-rainfall',
 data: [
    {time: '11:58',
    rain: 0.0    },
    {time: '12:58',
    rain: 0.0    },
    {time: '13:58',
    rain: 0.0    },
    {time: '14:58',
    rain: 0.3    },
    {time: '15:58',
    rain: 0.3    },
    {time: '16:58',
    rain: 0.0    },
    {time: '17:58',
    rain: 0.0    }],
        xkey: 'time',
        ykeys: ['rain'],
        labels: ['Rain'],
        hideHover: 'auto',
		postUnits: 'mm',
        resize: true
    });
});
