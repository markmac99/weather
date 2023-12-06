#
# copyright Mark McIntyre, 2023-
#

import pandas as pd
import os
import sys
import platform
import datetime

from tempPressData import minmaxTemps
from rainData import periodRain
from tableData import monthlySummary


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

    minmaxTemps(df, outdir, '12month')
    periodRain(df, outdir, '12month')
    monthlySummary(df, outdir)
