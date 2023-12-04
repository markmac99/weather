#
# copyright Mark McIntyre, 2023-
#

import pandas as pd
import os
import sys
import datetime


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


if __name__ == '__main__':
    if len(sys.argv) < 2:
        outdir = os.path.expanduser('~/weather/tmp')
    else:
        outdir = os.path.expanduser(sys.argv[1])
    os.makedirs(outdir, exist_ok=True)
    df = pd.read_parquet('https://markmcintyreastro.co.uk/weather/raw/raw-2023.parquet')
    recentTemps(df, outdir)
