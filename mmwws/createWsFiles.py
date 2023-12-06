#
# copyright Mark McIntyre, 2023-
#

import pandas as pd
import os
import sys
import platform
import datetime
import time

from windData import minmaxWind
from tempPressData import recentTemps, minmaxTemps, periodTemps
from rainData import recentRain, last24hRain, periodRain
from tableData import recentTable


if __name__ == '__main__':
    now = datetime.datetime.now()
    yr = now.year
    if len(sys.argv) < 2:
        outdir = os.path.expanduser('~/weather/tmp')
    else:
        outdir = os.path.expanduser(sys.argv[1])
    os.makedirs(outdir, exist_ok=True)
    rawdir = outdir.replace('data','raw')
    if platform.node() != 'wordpresssite':
        df = pd.read_parquet(f'https://markmcintyreastro.co.uk/weather/raw/raw-{yr}.parquet')
        df2 = pd.read_parquet(f'https://markmcintyreastro.co.uk/weather/raw/raw-{yr-1}.parquet')
    else:
        # current years datafile may be in the process of getting written to
        retries = 0
        while retries < 5:
            try:
                print('loading datafiles')
                df = pd.read_parquet(os.path.join(rawdir, f'raw-{yr}.parquet'))
                break
            except:
                print('file in use, waiting 5s')
                time.sleep(5)
                retries += 1
        if retries == 5:
            print('unable to open datafile, aborting')
            exit(0)
        # only load last years data if needed
        if (now +datetime.timedelta(days=-32)).year != yr:
            df2 = pd.read_parquet(os.path.join(rawdir, f'raw-{yr-1}.parquet'))
            df = pd.concat([df2,df])
    print('creating temperature graphs')
    recentTemps(df, outdir)
    periodTemps(df, outdir, period=24) 
    periodTemps(df, outdir, period=24*7) 
    minmaxTemps(df, outdir, '28day')

    print('creating tables')
    recentTable(df, outdir, period=1) # last hour of data
    recentTable(df, outdir, period=6) # last six hours
    recentTable(df, outdir, period=24) # last day
    recentTable(df, outdir, period=24*31) # last day

    print('creating pressure graphs')
    periodTemps(df, outdir, period=24, datafield='pressure', fieldname='pressure', fnamefrag='pressure', units='hPa')
    periodTemps(df, outdir, period=24*7, datafield='pressure', fieldname='pressure', fnamefrag='pressure', units='hPa')
    periodTemps(df, outdir, period=24*28, datafield='pressure', fieldname='pressure', fnamefrag='pressure', units='hPa')

    print('creating wind graphs')
    minmaxWind(df, outdir, period=24)
    minmaxWind(df, outdir, period=24*7)
    minmaxWind(df, outdir, period=24*28)

    print('creating rainfall graphs')
    recentRain(df, outdir)
    last24hRain(df, outdir)
    periodRain(df, outdir, '7day')
    periodRain(df, outdir, '28day')

    print('done')
