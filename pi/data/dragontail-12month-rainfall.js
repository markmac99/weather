$(function() {
Morris.Bar({
 element: 'dragontail-12month-rainfall',
 data: [
    {time: '2017/01',
    rain: 0.3    },
    {time: '2017/02',
    rain: 26.7    },
    {time: '2017/03',
    rain: 19.8    },
    {time: '2017/04',
    rain: 73.8    },
    {time: '2017/05',
    rain: 8.4    },
    {time: '2017/06',
    rain: 1.5    },
    {time: '2017/07',
    rain: 0.0    },
    {time: '2017/08',
    rain: 0.0    },
    {time: '2017/09',
    rain: 28.5    },
    {time: '2017/10',
    rain: 63.0    },
    {time: '2017/11',
    rain: 44.4    },
    {time: '2017/12',
    rain: 45.3    },
    {time: '2018/01',
    rain: 81.3    }],
        xkey: 'time',
        ykeys: ['rain'],
        labels: ['Rain'],
        xLabelAngle: 45,
        hideHover: 'auto',
		postUnits: 'mm',
        resize: true
    });
});
