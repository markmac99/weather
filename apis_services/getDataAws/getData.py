#
# Copyright Mark McIntyre 2023-
#

import pandas as pd
import sys
import os
import time
import datetime
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('mqtofile')


def getNewData(datafile, url='http://themcintyres.ddns.net:8081/values'):
    newdata = None
    try:
        newdata = pd.read_json(url)
        newdata.set_index(['time'], inplace=True)
        newdata['timestamp'] = pd.to_datetime(newdata.index)
    except:
        logger.warning('unable to connect to url')
        pass
    df = None
    if os.path.isfile(datafile):
        df = pd.read_parquet(datafile)
        if 'timestamp' not in df:
            df['timestamp'] = pd.to_datetime(df.index)
        if 'rainchg' not in df:
            df['rainchg'] = df.rain_mm.diff().fillna(0)
            df.loc[df.rainchg < -0.31, ['rainchg']] = 0
    else:
        logger.debug('mo old data to load')
    if df is not None and newdata is not None:
        lastrain = df.iloc[-1].rain_mm
        newdata['rainchg'] = newdata.rain_mm - lastrain
        newdata.loc[newdata.rainchg < -0.31, ['rainchg']] = 0
        newdata = pd.concat([df, newdata])
    else:
        logger.debug('no new newdata to concatenate')
    if newdata is not None:
        newdata = newdata.drop_duplicates()
        logger.info(f'saving updated data with {len(newdata)} records')
        newdata.to_parquet(datafile)
    else:
        logger.debug('no newdata')
    
    return newdata


if __name__ == '__main__':
    outdir = '~/weather/raw'
    pause = 30
    if len(sys.argv) > 1:
        outdir = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            pause = int(sys.argv[2])
        except: 
            pass
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    fh = RotatingFileHandler(os.path.expanduser('~/logs/getweatherdata.log'), maxBytes=5243880, backupCount=10)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info(f'capturing data at {pause} intervals to {outdir}')
    keepgoing = True
    while keepgoing:
        yr = datetime.datetime.now().year
        os.makedirs(os.path.expanduser(outdir), exist_ok=True)
        fname = os.path.expanduser(os.path.join(outdir, f'raw-{yr}.parquet'))
        df = getNewData(fname)
        time.sleep(pause)
