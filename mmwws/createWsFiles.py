#
# copyright Mark McIntyre, 2023-
#

import pandas as pd
import os
import sys
import platform
import datetime

from windData import minmaxWind
from tempPressData import recentTable, recentTemps, minmaxTemps, periodTemps
from rainData import recentRain, last24hRain, periodRain


if __name__ == '__main__':
    yr = datetime.datetime.now().year
    if len(sys.argv) < 2:
        outdir = os.path.expanduser('~/weather/tmp')
    else:
        outdir = os.path.expanduser(sys.argv[1])
    os.makedirs(outdir, exist_ok=True)
    if platform.node() != 'wordpresssite':
        df1 = pd.read_parquet(f'https://markmcintyreastro.co.uk/weather/raw/raw-{yr}.parquet')
        df2 = pd.read_parquet(f'https://markmcintyreastro.co.uk/weather/raw/raw-{yr-1}.parquet')
    else:
        df1 = pd.read_parquet(os.path.expanduser(f'~/weather/raw/raw-{yr}.parquet'))
        df2 = pd.read_parquet(os.path.expanduser(f'~/weather/raw/raw-{yr-1}.parquet'))
    df = pd.concat([df2,df1])
    recentTemps(df, outdir)
    periodTemps(df, outdir, period=24) 
    periodTemps(df, outdir, period=24*7) 
    minmaxTemps(df, outdir, '28day')
    minmaxTemps(df, outdir, '12month')

    recentTable(df, outdir, period=1) # last hour of data
    recentTable(df, outdir, period=6) # last six hours
    recentTable(df, outdir, period=24) # last day
    recentTable(df, outdir, period=24*31) # last day

    periodTemps(df, outdir, period=24, datafield='pressure', fieldname='pressure', fnamefrag='pressure', units='hPa')
    periodTemps(df, outdir, period=24*7, datafield='pressure', fieldname='pressure', fnamefrag='pressure', units='hPa')
    periodTemps(df, outdir, period=24*28, datafield='pressure', fieldname='pressure', fnamefrag='pressure', units='hPa')

    minmaxWind(df, outdir, period=24)
    minmaxWind(df, outdir, period=24*7)
    minmaxWind(df, outdir, period=24*28)

    recentRain(df, outdir)
    last24hRain(df, outdir)
    periodRain(df, outdir, '7day')
    periodRain(df, outdir, '28day')

    # run only once, on 1st of the month
    periodRain(df, outdir, '12month')
    