$(function() {
Morris.Bar({
 element: 'dragontail-7day-rainfall',
 data: [
    {time: '2018/03/07',
    rain: 0.3    },
    {time: '2018/03/08',
    rain: 0.6    },
    {time: '2018/03/09',
    rain: 0.6    },
    {time: '2018/03/10',
    rain: 7.8    },
    {time: '2018/03/11',
    rain: 0.3    },
    {time: '2018/03/12',
    rain: 6.6    },
    {time: '2018/03/13',
    rain: 2.1    },
    {time: '2018/03/14',
    rain: 0.3    }],
        xkey: 'time',
        ykeys: ['rain'],
        labels: ['Rain'],
        xLabelAngle: 45,
        hideHover: 'auto',
		postUnits: 'mm',
        resize: true
    });
});
