#
# copyright Mark McIntyre, 2023-
#

import pandas as pd
import os
import sys
import platform
import datetime
import time
import logging
from logging.handlers import RotatingFileHandler

from tempPressData import minmaxTemps
from rainData import periodRain
from tableData import monthlySummary

logger = logging.getLogger('weather_createMthly')


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    fh = RotatingFileHandler(os.path.expanduser('~/logs/weather_monthly.log'), maxBytes=51200, backupCount=10)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

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
                logger.info('loading datafiles')
                df1 = pd.read_parquet(os.path.join(rawdir, f'raw-{yr}.parquet'))
                break
            except:
                logger.info('file in use, waiting 5s')
                time.sleep(5)
                retries += 1
        if retries == 5:
            logger.warning('unable to open datafile, aborting')
            exit(0)
        df2 = pd.read_parquet(os.path.expanduser(f'~/weather/raw/raw-{yr-1}.parquet'))
    df = pd.concat([df2,df1])
    df.sort_index(inplace=True)

    logger.info('creating 12mth temps')
    minmaxTemps(df, outdir, '12month')
    logger.info('creating 12mth rain')
    periodRain(df, outdir, '12month')
    logger.info('creating allmths table')
    monthlySummary(df, outdir)
    logger.info('done')
