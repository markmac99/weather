#
# copyright Mark McIntyre, 2023-
#

import pandas as pd
import os
import datetime
from dateutil.relativedelta import relativedelta


def recentRain(df, outdir):
    now=datetime.datetime.now()
    back1hr=now + datetime.timedelta(hours=-1)
    df1hr = df[df.timestamp > pd.Timestamp(back1hr, tz='UTC')]
    outfname = os.path.join(outdir, 'dragontail-recent-rainfall.js')
    with open(outfname, 'w') as of:
        of.write("$(function() {\nMorris.Line({\n element: 'dragontail-recent-rainfall',\n data: [\n")
        lastts = df1hr.iloc[-1].timestamp
        for _, rw in df1hr.iterrows():
            ts = rw.timestamp
            temp = max(rw.rainchg, 0)
            of.write(f'    {{time: {int(ts.timestamp()*1000)}, rain: {temp} }}')
            if ts != lastts:
                of.write(',\n')
            else:
                of.write('\n')

        of.write("       ],\n        xkey: 'time',\n        ykeys: ['rain'],\n")
        of.write("       labels: ['Rainfall'],\n        hideHover: 'auto',\n")
        of.write("       postUnits: 'mm',\n        resize: true\n    });\n});\n")
    return 


def last24hRain(df, outdir):
    now=datetime.datetime.now()
    backdt = now + datetime.timedelta(hours=-25)
    outfname = os.path.join(outdir, 'dragontail-24hr-rainfall.js')
    with open(outfname, 'w') as of:
        of.write("$(function() {\nMorris.Area({\n element: 'dragontail-24hr-rainfall',\n data: [\n")
        numrows = 25
        for r in range(numrows):
            seldf = df[df.timestamp >= pd.Timestamp(backdt, tz='UTC')]
            todt = backdt + datetime.timedelta(hours=1)
            seldf = seldf[seldf.timestamp < pd.Timestamp(todt, tz='UTC')]
            if len(seldf) == 0:
                backdt = todt
                continue
            ts = int(seldf.timestamp.max().timestamp()*1000)
            temp = round(max(seldf.rainchg.sum(),0), 1)
            of.write(f'    {{time: {ts}, rain: {temp} }}')
            if r < (numrows-1):
                of.write(',\n')
            else:
                of.write('\n')
            backdt = todt
        of.write("       ],\n        xkey: 'time',\n        ykeys: ['rain'],\n")
        of.write("       labels: ['Rainfall'],\n        hideHover: 'auto',\n")
        of.write("       postUnits: 'mm',\n        resize: true,\n")
        of.write("fillOpacity: 0.6, pointFillColors: ['black'], pointStrokeColors: ['black'],")
        of.write("lineColors: ['red'], smooth: false });\n});\n")

    backdt = now + datetime.timedelta(hours=-24)
    seldf = df[df.timestamp >= pd.Timestamp(backdt, tz='UTC')]
    outfname = os.path.join(outdir, 'dragontailrecentrain.txt')
    with open(outfname, 'w') as of:
        of.write(f'{round(max(seldf.rainchg.sum(),0), 1)} mm')
    return 


def periodRain(df, outdir, period):
    now=datetime.datetime.now()
    now = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if period == '7day':
        numrows = 7
        dstep = 1
        backdt = now + datetime.timedelta(days = -numrows)
    elif period == '28day':
        numrows = 28
        dstep = 1
        backdt = now + datetime.timedelta(days = -numrows)
    elif period == '90day':
        numrows = 90
        dstep = 1
        backdt = now + datetime.timedelta(days = -numrows)
    else:
        numrows=12
        dstep = 99
        backdt = now + relativedelta(months=-(numrows+1))
    outfname = os.path.join(outdir, f'dragontail-{period}-rainfall.js')
    with open(outfname, 'w') as of:
        of.write("$(function() {\nMorris.Bar({\n element: 'dragontail-" + f'{period}' + "-rainfall',\n data: [\n")
        for r in range(numrows+1):
            seldf = df[df.timestamp >= pd.Timestamp(backdt, tz='UTC')]
            if dstep < 99:
                todt = backdt + datetime.timedelta(days=dstep)
                ts = backdt.strftime("%Y-%m-%d")
            else:
                todt = backdt + relativedelta(months=1)
                ts = backdt.strftime("%Y-%m")
            seldf = seldf[seldf.timestamp < pd.Timestamp(todt, tz='UTC')]
            if len(seldf) == 0:
                backdt = todt
                continue
            totrain = round(max(seldf.rainchg.sum(),0), 1)
            of.write(f'    {{time: \'{ts}\', rain: {totrain} }}')
            if r < (numrows):
                of.write(',\n')
            else:
                of.write('\n')
            backdt = todt
        of.write("       ],\n        xkey: 'time',\n        ykeys: ['rain'],\n")
        of.write("       labels: ['Rainfall'],\n        hideHover: 'auto',\n")
        of.write("       xLabelAngle: 45,\n")
        of.write("       postUnits: 'mm',\n        resize: true\n")
        of.write("});\n});\n")
    return 


def monthlyRain(df, outdir):
    outfname = os.path.join(outdir, 'dragontail-12month-rainfall.js')
    with open(outfname, 'w') as of:
        of.write("$(function() {\nMorris.Bar({\n element: 'dragontail-12month-rainfall',\n data: [\n")
        lastper = df.iloc[-1].period
        for _,rw in df.iterrows():
            per = rw['period']
            perstr = per[:4] + '-' + per[4:]
            totrain = rw['raintot']
            of.write(f'    {{time: \'{perstr}\', rain: {totrain}}}')
            if per != lastper:
                of.write(',\n')
            else:
                of.write('\n')

        of.write("       ],\n        xkey: 'time',\n        ykeys: ['rain'],\n")
        of.write("       labels: ['Rainfall'],\n        hideHover: 'auto',\n")
        of.write("       xLabelAngle: 45,\n")
        of.write("       postUnits: 'mm',\n        resize: true\n")
        of.write("});\n});\n")
    return 
