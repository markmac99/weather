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

from windData import minmaxWind, recentWind
from tempPressData import recentTemps, periodTemps
from rainData import recentRain, last24hRain
from tableData import recentTable

logger = logging.getLogger('weather_logger')


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    fh = RotatingFileHandler(os.path.expanduser('~/logs/weather_logger.log'), maxBytes=51200, backupCount=10)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

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
                logger.info('loading datafiles')
                df = pd.read_parquet(os.path.join(rawdir, f'raw-{yr}.parquet'))
                break
            except:
                logger.info('file in use, waiting 5s')
                time.sleep(5)
                retries += 1
        if retries == 5:
            logger.warning('unable to open datafile, aborting')
            exit(0)
        # only load last years data if needed
        if (now +datetime.timedelta(days=-32)).year != yr:
            df2 = pd.read_parquet(os.path.join(rawdir, f'raw-{yr-1}.parquet'))
            df = pd.concat([df2,df])

    df.drop_duplicates(inplace=True)
    df.sort_index(inplace=True)
    logger.info('creating temperature graphs')
    recentTemps(df, outdir)
    periodTemps(df, outdir, period=24) 

    logger.info('creating tables')
    recentTable(df, outdir, period=1) # last hour of data
    recentTable(df, outdir, period=6) # last six hours
    recentTable(df, outdir, period=24) # last day

    logger.info('creating pressure graphs')
    periodTemps(df, outdir, period=24, datafield='pressure', fieldname='pressure', fnamefrag='pressure', units='hPa')

    logger.info('creating wind graphs')
    recentWind(df, outdir)
    minmaxWind(df, outdir, period=24)

    logger.info('creating rainfall graphs')
    recentRain(df, outdir)
    last24hRain(df, outdir)

    logger.info('done')
