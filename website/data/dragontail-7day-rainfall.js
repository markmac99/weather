$(function() {
Morris.Bar({
 element: 'dragontail-7day-rainfall',
 data: [
    {time: '2018/01/16',
    rain: 5.1    },
    {time: '2018/01/17',
    rain: 0.6    },
    {time: '2018/01/18',
    rain: 3.3    },
    {time: '2018/01/19',
    rain: 0.0    },
    {time: '2018/01/20',
    rain: 2.1    },
    {time: '2018/01/21',
    rain: 2.7    },
    {time: '2018/01/22',
    rain: 9.9    },
    {time: '2018/01/23',
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
