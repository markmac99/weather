#
# copyright Mark McIntyre, 2023=
#
import pandas as pd
import os
import datetime
import numpy as np
from dateutil.relativedelta import relativedelta

# correction for instrument readout inaccuracy
pressureCorrection = 10


def getRangeValues(df, starttime, mins, doaverage=False):
    endtime = starttime + datetime.timedelta(minutes=mins)
    subdf = df[df.timestamp > pd.Timestamp(starttime, tz='UTC')]
    subdf = subdf[subdf.timestamp <= pd.Timestamp(endtime, tz='UTC')]
    if len(subdf) == 0:
        return {'temp_c': np.nan, 'pressure': np.nan, 'rain_mm': np.nan}
    if doaverage:
        return {'temp_c': subdf.temperature_C.mean(), 'humidity': subdf.humidity.mean(),
            'wind_ave': subdf.wind_avg_km_h.mean(), 'wind_max': subdf.wind_max_km_h.max(), 'pressure': subdf.press_rel.mean(),
            'rain_mm': subdf.rain_mm.max(), 'wind_dir': subdf.wind_dir_deg.mean(),
            'temp_in': subdf.temp_c_in.mean(), 'hum_in': subdf.humidity_in.mean(), 
            'time': subdf.timestamp.max()}
    else:
        return {'temp_c': subdf.iloc[-1].temperature_C, 'humidity': subdf.iloc[-1].humidity,
            'wind_ave': subdf.iloc[-1].wind_avg_km_h, 'wind_max': subdf.iloc[-1].wind_max_km_h, 'pressure': subdf.iloc[-1].press_rel,
            'rain_mm': subdf.iloc[-1].rain_mm, 'wind_dir': subdf.iloc[-1].wind_dir_deg,
            'temp_in': subdf.iloc[-1].temp_c_in, 'hum_in': subdf.iloc[-1].humidity_in, 
            'time': subdf.iloc[-1].timestamp}


def recentTable(df, outdir, period=1):
    now=datetime.datetime.now()
    avgs = False
    tfmt = '%H:%M'
    hord = 'hr'
    hord2 = 'hrs'
    pp = period
    if period > 24:
        hord = 'days'
        hord2 = 'days'
        pp = int(period/24)
    outfname = os.path.join(outdir, f'dragontail-{pp}{hord}-table.js')
    if period == 1:
        freq = 5
        window = 5
        avgs = True # get averages 
        back1hr = now + datetime.timedelta(hours=-period)
    elif period < 25:
        freq = 60 # hourly, if period is 6 or 24
        window = 60
        avgs = True
        back1hr = now + datetime.timedelta(hours=-period)
        back1hr = back1hr.replace(minute=0, second=59, microsecond=0) #  - datetime.timedelta(minutes=1)
    else:
        tfmt = '%Y/%m/%d %H:%M GMT'
        freq = 60 * 24 # daily if period is longer than a day
        back1hr = now + datetime.timedelta(hours=-period)
        window = 24 * 60
        avgs = False
        back1hr = back1hr.replace(minute=0, second=59, microsecond=0) #  - datetime.timedelta(minutes=1)

    seldf = df[df.timestamp > pd.Timestamp(back1hr, tz='UTC')]
    with open(outfname, 'w') as of:
        of.write('$(function() {\n')
        of.write('var table = document.createElement("table");\n')
        of.write('table.className = "table table-striped table-bordered table-hover table-condensed";\n')
        of.write('var header = table.createTHead();\n')
        of.write('header.className = "h4";\n')
        numrows = int((period *60)/freq)
        prevrain = -1
        for r in range(numrows):
            offs = r * freq
            st = min(back1hr + datetime.timedelta(minutes=(offs)), now)
            vals = getRangeValues(seldf, st, window, doaverage=avgs)
            if pd.isna(vals['temp_c']):
                continue
            ts = vals['time'].strftime(tfmt) 
            temp = round(vals['temp_c'], 1)
            hum = int(vals['humidity'])
            wina = round(vals['wind_ave'] * 0.6214, 1)
            winm = round(vals['wind_max'] * 0.6214, 1)
            # rainfall is cumulative
            if prevrain < 0:
                rain = 0.0
            else:
                rain = round(max(vals['rain_mm'] - prevrain, 0), 1)
            prevrain = round(vals['rain_mm'], 1)
            pres = round(vals['pressure'] + pressureCorrection, 1)
            of.write('var row = table.insertRow(0);\n')
            of.write('var cell = row.insertCell(0);\n')
            of.write(f'cell.innerHTML = "{ts}";\n')
            of.write('var cell = row.insertCell(1);\n')
            of.write(f'cell.innerHTML = "{temp} &deg;C";\n')
            of.write('var cell = row.insertCell(2);\n')
            of.write(f'cell.innerHTML = "{hum}%";\n')
            of.write('var cell = row.insertCell(3);\n')
            of.write(f'cell.innerHTML = "{wina} mph";\n')
            of.write('var cell = row.insertCell(4);\n')
            of.write(f'cell.innerHTML = "{winm} mph";\n')
            of.write('var cell = row.insertCell(5);\n')
            of.write(f'cell.innerHTML = "{rain} mm";\n')
            of.write('var cell = row.insertCell(6);\n')
            of.write(f'cell.innerHTML = "{pres} hPa";\n')
        of.write('var row = header.insertRow(0);\n')
        of.write('var cell = row.insertCell(0);\n')
        of.write('cell.innerHTML = "Ave";\n')
        of.write('cell.className = "small";\n')
        of.write('var cell = row.insertCell(1);\n')
        of.write('cell.innerHTML = "Max";\n')
        of.write('cell.className = "small";\n')
        of.write('var row = header.insertRow(0);\n')
        of.write('var cell = row.insertCell(0);\n')
        of.write('cell.innerHTML = "Time";\n')
        of.write('cell.rowSpan = 2;\n')
        of.write('var cell = row.insertCell(1);\n')
        of.write('cell.innerHTML = "Temp";\n')
        of.write('cell.rowSpan = 2;\n')
        of.write('var cell = row.insertCell(2);\n')
        of.write('cell.innerHTML = "Humid";\n')
        of.write('cell.rowSpan = 2;\n')
        of.write('var cell = row.insertCell(3);\n')
        of.write('cell.innerHTML = "Wind mph";\n')
        of.write('cell.colSpan = 2;\n')
        of.write('var cell = row.insertCell(4);\n')
        of.write('cell.innerHTML = "Rain";\n')
        of.write('cell.rowSpan = 2;\n')
        of.write('var cell = row.insertCell(5);\n')
        of.write('cell.innerHTML = "Pressure";\n')
        of.write('cell.rowSpan = 2;\n')
        of.write(f'var outer_div = document.getElementById("table{pp}{hord2}");\n')
        of.write('outer_div.appendChild(table);\n})\n')


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

            of.write(f'    {{time: {int(ts.timestamp()*1000)}, temp: {temp} }}')
            if ts != lastts:
                of.write(',\n')
            else:
                of.write('\n')

        of.write("       ],\n        xkey: 'time',\n        ykeys: ['temp'],\n")
        of.write("       labels: ['Temp'],\n        hideHover: 'auto',\n")
        of.write("       postUnits: '°C',\n        resize: true\n    });\n});\n")

    outfname = os.path.join(outdir, 'dragontailcurrenttemp.txt')
    with open(outfname, 'w') as of:
        of.write(f'{df.iloc[-1].temperature_C} &deg;C')
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
            of.write(f'    {{time: {int(ts.timestamp()*1000)}, {fieldname}: {temp} }}')
            if ts != lastts:
                of.write(',\n')
            else:
                of.write('\n')

        of.write("       ],\n        xkey: 'time',\n        ykeys: ['" + fieldname + "'],\n")
        of.write("       labels: ['" + fieldname + "'],\n        hideHover: 'auto',\n")
        of.write("       xLabelAngle: 45,\n")
        if units == 'hPa':
            of.write("       ymax: 1050, ymin: 950, \n")
        of.write("       postUnits: '" + units + "',\n        resize: true\n")
        of.write("});\n});\n")

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
