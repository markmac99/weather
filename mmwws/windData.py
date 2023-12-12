#
# copyright Mark McIntyre, 2023=
#
import pandas as pd
import os
import datetime

from conversions import KMHTOMPH


def recentWind(df, outdir):
    now=datetime.datetime.now()
    backdt = now + datetime.timedelta(hours=-1)
    seldf = df[df.timestamp >= pd.Timestamp(backdt, tz='UTC')]
    outfname = os.path.join(outdir, 'dragontail-recent-wind.js')
    with open(outfname, 'w') as of:
        of.write("$(function() {\nMorris.Line({\n element: 'dragontail-recent-wind',\n data: [\n")
        lastts = seldf.iloc[-1].timestamp
        for _, rw in seldf.iterrows():
            maxw = round(rw.wind_max_km_h * KMHTOMPH, 1)
            avew = round(rw.wind_avg_km_h * KMHTOMPH, 1)
            ts = int(rw.timestamp.timestamp()*1000)
            of.write(f'    {{time: {ts}, ave: {avew}, gust: {maxw} }}')
            if ts != lastts:
                of.write(',\n')
            else:
                of.write('\n')
        of.write("       ],\n        xkey: 'time',\n        ykeys: ['ave','gust'],\n")
        of.write("       labels: ['Average','Gust'],\n        hideHover: 'auto',\n")
        of.write("       xLabelAngle: 45,\n")
        of.write("       postUnits: 'mph',\n        resize: true\n")
        of.write("});\n});\n")
    return 


def minmaxWind(df, outdir, period=24):
    now=datetime.datetime.now()
    if period == 28*24:
        now = now.replace(hour=0, minute=0,second=0,microsecond=0)
        backdt = now + datetime.timedelta(days=-28)
        numrows = 28
        pp = '28day'
        hstep=24
    elif period == 7*24:
        now = now.replace(hour=0, minute=0,second=0,microsecond=0)
        backdt = now + datetime.timedelta(days=-7)
        numrows = int(period/4)
        pp = '7day'
        hstep=4
    else:
        backdt = now + datetime.timedelta(days=-1)
        numrows = 24
        pp = '24hr'
        hstep=1
    seldf = df[df.timestamp > pd.Timestamp(backdt, tz='UTC')]
    outfname = os.path.join(outdir, f'dragontail-{pp}-wind.js')
    with open(outfname, 'w') as of:
        of.write("$(function() {\nMorris.Line({\n element: 'dragontail-"+ f'{pp}-wind' + "',\n data: [\n")
        for r in range(numrows):
            seldf = df[df.timestamp >= pd.Timestamp(backdt, tz='UTC')]
            todt = backdt + datetime.timedelta(hours=hstep)
            seldf = seldf[seldf.timestamp < pd.Timestamp(todt, tz='UTC')]
            if len(seldf) == 0:
                backdt = todt
                continue
            maxw = round(seldf.wind_max_km_h.max() * KMHTOMPH, 1)
            avew = round(seldf.wind_avg_km_h.max() * KMHTOMPH, 1)
            ts = int(seldf.timestamp.max().timestamp()*1000)
            of.write(f'    {{time: {ts}, ave: {avew}, gust: {maxw} }}')
            if r < (numrows-1):
                of.write(',\n')
            else:
                of.write('\n')
            backdt = todt

        of.write("       ],\n        xkey: 'time',\n        ykeys: ['ave','gust'],\n")
        of.write("       labels: ['Average','Gust'],\n        hideHover: 'auto',\n")
        of.write("       xLabelAngle: 45,\n")
        of.write("       postUnits: 'mph',\n        resize: true\n")
        of.write("});\n});\n")

    if period == 24:
        backdt = now + datetime.timedelta(hours=-12)
        seldf = df[df.timestamp > pd.Timestamp(backdt, tz='UTC')]
        outfname = os.path.join(outdir, 'dragontailrecentwind.txt')
        with open(outfname, 'w') as of:
            of.write(f'{round(seldf.wind_max_km_h.max()*KMHTOMPH,1)} mph')
    return 
