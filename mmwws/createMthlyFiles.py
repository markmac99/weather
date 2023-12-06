#
# copyright Mark McIntyre, 2023-
#

import pandas as pd
import os
import sys
import platform
import datetime
import time

from tempPressData import minmaxTemps
from rainData import periodRain
from tableData import monthlySummary


if __name__ == '__main__':
    yr = datetime.datetime.now().year
    if len(sys.argv) < 2:
        outdir = os.path.expanduser('~/weather/tmp')
    else:
        outdir = os.path.expanduser(sys.argv[1])
    rawdir = outdir.replace('data','raw')
    os.makedirs(outdir, exist_ok=True)
    if platform.node() != 'wordpresssite':
        df1 = pd.read_parquet(f'https://markmcintyreastro.co.uk/weather/raw/raw-{yr}.parquet')
        df2 = pd.read_parquet(f'https://markmcintyreastro.co.uk/weather/raw/raw-{yr-1}.parquet')
    else:
        # current years datafile may be in the process of getting written to
        retries = 0
        while retries < 5:
            try:
                print('loading datafiles')
                df1 = pd.read_parquet(os.path.join(rawdir, f'raw-{yr}.parquet'))
                break
            except:
                print('file in use, waiting 5s')
                time.sleep(5)
                retries += 1
        if retries == 5:
            print('unable to open datafile, aborting')
            exit(0)
        df2 = pd.read_parquet(os.path.expanduser(f'~/weather/raw/raw-{yr-1}.parquet'))
    df = pd.concat([df2,df1])

    print('creating 12mth temps')
    minmaxTemps(df, outdir, '12month')
    print('creating 12mth rain')
    periodRain(df, outdir, '12month')
    print('creating allmths table')
    monthlySummary(df, outdir)
    print('done')
