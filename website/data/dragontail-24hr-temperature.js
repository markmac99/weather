$(function() {
Morris.Line({
 element: 'dragontail-24hr-temperature',
 data: [
    {time: 1521006872000,
    temp: 3.0    },
    {time: 1521010472000,
    temp: 4.3    },
    {time: 1521014072000,
    temp: 5.6    },
    {time: 1521017672000,
    temp: 7.6    },
    {time: 1521021272000,
    temp: 9.4    },
    {time: 1521024872000,
    temp: 11.1    },
    {time: 1521028472000,
    temp: 12.5    },
    {time: 1521032072000,
    temp: 11.7    },
    {time: 1521035672000,
    temp: 11.7    },
    {time: 1521039272000,
    temp: 11.6    },
    {time: 1521042872000,
    temp: 11.6    },
    {time: 1521046472000,
    temp: 11.1    },
    {time: 1521050072000,
    temp: 10.6    },
    {time: 1521053672000,
    temp: 10.5    },
    {time: 1521057272000,
    temp: 10.1    },
    {time: 1521060872000,
    temp: 9.9    },
    {time: 1521064472000,
    temp: 9.8    },
    {time: 1521068072000,
    temp: 9.8    },
    {time: 1521071672000,
    temp: 9.5    },
    {time: 1521075272000,
    temp: 8.5    },
    {time: 1521078872000,
    temp: 7.7    },
    {time: 1521082472000,
    temp: 7.6    },
    {time: 1521086071000,
    temp: 7.7    },
    {time: 1521089672000,
    temp: 7.7    },
    {time: 1521093272000,
    temp: 7.8    }],
        xkey: 'time',
        ykeys: ['temp'],
        labels: ['Temp'],
        hideHover: 'auto',
		postUnits: '°C',
        resize: true
    });
});
