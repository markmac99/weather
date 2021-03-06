$(function() {
Morris.Line({
 element: 'dragontail-24hr-pressure',
 data: [
    {time: 1516654335000,
    pressure: 1017.5    },
    {time: 1516657935000,
    pressure: 1017.9    },
    {time: 1516661535000,
    pressure: 1018.1    },
    {time: 1516665135000,
    pressure: 1017.5    },
    {time: 1516668734000,
    pressure: 1017.2    },
    {time: 1516672335000,
    pressure: 1016.8    },
    {time: 1516675935000,
    pressure: 1016.9    },
    {time: 1516679535000,
    pressure: 1015.8    },
    {time: 1516683135000,
    pressure: 1015.1    },
    {time: 1516686735000,
    pressure: 1014.2    },
    {time: 1516690335000,
    pressure: 1013.8    },
    {time: 1516693935000,
    pressure: 1013.3    },
    {time: 1516697535000,
    pressure: 1013.4    },
    {time: 1516701135000,
    pressure: 1013.4    },
    {time: 1516704735000,
    pressure: 1013.1    },
    {time: 1516708335000,
    pressure: 1012.0    },
    {time: 1516711935000,
    pressure: 1011.7    },
    {time: 1516715535000,
    pressure: 1011.2    },
    {time: 1516719135000,
    pressure: 1011.3    },
    {time: 1516722735000,
    pressure: 1011.1    },
    {time: 1516726335000,
    pressure: 1011.6    },
    {time: 1516729935000,
    pressure: 1012.6    },
    {time: 1516733535000,
    pressure: 1013.2    },
    {time: 1516737135000,
    pressure: 1013.0    },
    {time: 1516740735000,
    pressure: 1012.9    }],
        xkey: 'time',
        ykeys: ['pressure'],
        labels: ['Pressure'],
        hideHover: 'auto',
		xLabelAngle: 45,
		ymax: 1050,
		ymin: 960,
		postUnits: 'hPa',
        resize: true
    });
});
