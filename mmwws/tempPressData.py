#
# copyright Mark McIntyre, 2023=
#
import pandas as pd
import os
import datetime
import numpy as np
from dateutil.relativedelta import relativedelta
from conversions import dewPoint, PRESSCORR


def getRangeValues(df, starttime, mins, doaverage=False):
    endtime = starttime + datetime.timedelta(minutes=mins)
    subdf = df[df.timestamp > pd.Timestamp(starttime, tz='UTC')]
    subdf = subdf[subdf.timestamp <= pd.Timestamp(endtime, tz='UTC')]
    if len(subdf) == 0:
        return {'temp_c': np.nan, 'pressure': np.nan, 'rain_mm': np.nan}
    if doaverage:
        return {'temp_c': subdf.temperature_C.mean(), 'humidity': subdf.humidity.mean(),
            'wind_ave': subdf.wind_avg_km_h.mean(), 'wind_max': subdf.wind_max_km_h.max(), 
            'pressure': subdf.press_rel.mean() + PRESSCORR,
            'rain_mm': subdf.rain_mm.max(), 'wind_dir': subdf.wind_dir_deg.mean(),
            'temp_in': subdf.temp_c_in.mean(), 'hum_in': subdf.humidity_in.mean(), 
            'time': subdf.timestamp.max()}
    else:
        return {'temp_c': subdf.iloc[-1].temperature_C, 'humidity': subdf.iloc[-1].humidity,
            'wind_ave': subdf.iloc[-1].wind_avg_km_h, 'wind_max': subdf.iloc[-1].wind_max_km_h, 
            'pressure': subdf.iloc[-1].press_rel + PRESSCORR,
            'rain_mm': subdf.iloc[-1].rain_mm, 'wind_dir': subdf.iloc[-1].wind_dir_deg,
            'temp_in': subdf.iloc[-1].temp_c_in, 'hum_in': subdf.iloc[-1].humidity_in, 
            'time': subdf.iloc[-1].timestamp}


def recentTemps(df, outdir):
    now=datetime.datetime.now()
    back1hr=now + datetime.timedelta(hours=-1)
    df1hr = df[df.timestamp > pd.Timestamp(back1hr, tz='UTC')]
    outfname = os.path.join(outdir, 'dragontail-recent-temperature.js')
    with open(outfname, 'w') as of:
        of.write("$(function() {\nMorris.Line({\n element: 'dragontail-recent-temperature',\n data: [\n")
        lastts = df1hr.iloc[-1].timestamp
        for idx, rw in df1hr.iterrows():
            ts = rw.timestamp
            temp = rw.temperature_C
            dewpoint = round(dewPoint(rw.temperature_C, rw.humidity),1)

            of.write(f'    {{time: {int(ts.timestamp()*1000)}, temp: {temp}, dewpoint: {dewpoint} }}')
            if ts != lastts:
                of.write(',\n')
            else:
                of.write('\n')

        of.write("       ],\n        xkey: 'time',\n        ykeys: ['temp', 'dewpoint'],\n")
        of.write("       labels: ['Temp', 'DewPoint'],\n        hideHover: 'auto',\n")
        of.write("       postUnits: '°C',\n        resize: true\n    });\n});\n")

    outfname = os.path.join(outdir, 'dragontailcurrenttemp.txt')
    with open(outfname, 'w') as of:
        of.write(f'{round(df.iloc[-1].temperature_C, 1)} &deg;C')
    return 


def periodTemps(df, outdir, period, 
                datafield = 'temp_c', fieldname ='temp', fnamefrag = 'temperature', units='°C'):
    now=datetime.datetime.now()
    freq = 60
    hrorday='hr'
    pp = period
    if period > 24:
        freq = 6*60
        if period > 168:
            freq = 24*60
        hrorday = 'day'
        pp = int(period/24)
    back1hr=now + datetime.timedelta(hours=-period)
    seldf = df[df.timestamp > pd.Timestamp(back1hr, tz='UTC')]
    outfname = os.path.join(outdir, f'dragontail-{pp}{hrorday}-{fnamefrag}.js')
    with open(outfname, 'w') as of:
        of.write("$(function() {\nMorris.Line({\n element: 'dragontail-"+ f'{pp}{hrorday}-{fnamefrag}' + "',\n data: [\n")
        numrows = int((period *60)/freq)
        lastts = seldf.iloc[-1].timestamp
        for r in range(numrows):
            offs = r * freq
            st = min(back1hr + datetime.timedelta(minutes=(offs)), now)
            vals = getRangeValues(seldf, st,freq, doaverage=True)
            if pd.isna(vals[datafield]):
                #print(f'nodata {st}')
                continue
            temp = round(vals[datafield],1)
            ts = vals['time']
            if datafield == 'temp_c':
                dewpoint = round(dewPoint(vals[datafield], vals['humidity']),1)
                of.write(f'    {{time: {int(ts.timestamp()*1000)}, {fieldname}: {temp}, \'dewpoint\': {dewpoint} }}')
            else:
                of.write(f'    {{time: {int(ts.timestamp()*1000)}, {fieldname}: {temp}}}')
            if ts != lastts:
                of.write(',\n')
            else:
                of.write('\n')

        if datafield == 'temp_c':
            of.write(f"       ],\n        xkey: 'time',\n        ykeys: [\'{fieldname}\', 'dewpoint'],\n")
            of.write(f"       labels: [\'{fieldname}\','dewpoint'],\n        hideHover: 'auto',\n")
        else:
            of.write("       ],\n        xkey: 'time',\n        ykeys: ['" + fieldname + "'],\n")
            of.write("       labels: ['" + fieldname + "'],\n        hideHover: 'auto',\n")
        of.write("       xLabelAngle: 45,\n")
        if units == 'hPa':
            of.write("       ymax: 1050, ymin: 950, \n")
        of.write("       postUnits: '" + units + "',\n        resize: true\n")
        of.write("});\n});\n")

    if period == 24:
        outfname = os.path.join(outdir, 'dragontailmintemp.txt')
        with open(outfname, 'w') as of:
            of.write(f'{round(seldf.temperature_C.min(),1)} &deg;C')
        outfname = os.path.join(outdir, 'dragontailmaxtemp.txt')
        with open(outfname, 'w') as of:
            of.write(f'{round(seldf.temperature_C.max(),1)} &deg;C')

    return 


def minmaxTemps(df, outdir, period='28day', fnamefrag = 'temperature', units='°C'):
    now=datetime.datetime.now()
    now = now.replace(hour=0, minute=0,second=0,microsecond=0)
    if period == '28day':
        backdt = now + datetime.timedelta(days=-28)
        numrows = 28
    else:
        now = now.replace(day=1)
        backdt = now + relativedelta(months=-13)
        numrows = 14
    seldf = df[df.timestamp > pd.Timestamp(backdt, tz='UTC')]
    outfname = os.path.join(outdir, f'dragontail-{period}-{fnamefrag}.js')
    with open(outfname, 'w') as of:
        of.write("$(function() {\nMorris.Bar({\n element: 'dragontail-"+ f'{period}-{fnamefrag}' + "',\n data: [\n")
        for r in range(numrows):
            seldf = df[df.timestamp >= pd.Timestamp(backdt, tz='UTC')]
            if period == '28day':
                todt = backdt + datetime.timedelta(days=1)
            else: 
                todt = backdt + relativedelta(months=1)
            seldf = seldf[seldf.timestamp < pd.Timestamp(todt, tz='UTC')]
            if len(seldf) == 0:
                print(backdt, todt)
                backdt = todt
                continue
            maxt = round(seldf.temperature_C.max(), 1)
            mint = round(seldf.temperature_C.min(), 1)

            of.write(f'    {{time: \'{backdt.strftime("%Y-%m-%d")}\', max_temp: {maxt}, min_temp: {mint} }}')
            if r < (numrows-1):
                of.write(',\n')
            else:
                of.write('\n')
            backdt = todt

        of.write("       ],\n        xkey: 'time',\n        ykeys: ['max_temp','min_temp'],\n")
        of.write("       labels: ['Max Temp','Min Temp'],\n        hideHover: 'auto',\n")
        of.write("       xLabelAngle: 45,\n")
        of.write("       postUnits: '" + units + "',\n        resize: true\n")
        of.write("});\n});\n")

    return 
