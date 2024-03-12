#
# Copyright Mark McIntyre 2023-
#

import pandas as pd
import os
import time
import datetime
import logging
import json
from logging.handlers import RotatingFileHandler
#import requests
#from urllib3.exceptions import InsecureRequestWarning

from apiConfig import apiUrl, apiKey, basedir, pause

logger = logging.getLogger('mqtofile')


def getNewData(datafile, srcdir, url, key):
    #logger.warning(url)
    newdata = None    
    try:
        #requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        #headers={'x-api-key': key}
        #res = requests.get(url, headers=headers, verify=False)
        #if res.status_code == 200:
        #    newdata = pd.read_json(res.text.strip())
        #    newdata.set_index(['time'], inplace=True)
        #    newdata['timestamp'] = pd.to_datetime(newdata.index)
        #else:
        #    logger.warning('unable to retrieve data')
        rawdata = json.load(open(os.path.expanduser(os.path.join(srcdir, 'weatherdata.json'))))
        newdata=pd.DataFrame([rawdata])
        newdata.set_index(['time'], inplace=True)
        newdata['timestamp'] = pd.to_datetime(newdata.index)
    except Exception as e:
        logger.warning('unable to load source data')
        logger.warning(e)
        return     
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
    return 


if __name__ == '__main__':
    indir = os.path.join(basedir, 'upload')
    outdir = os.path.join(basedir, 'raw')
    os.makedirs(os.path.expanduser(indir), exist_ok=True)
    os.makedirs(os.path.expanduser(outdir), exist_ok=True)
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
        fname = os.path.expanduser(os.path.join(outdir, f'raw-{yr}.parquet'))
        getNewData(fname, indir, apiUrl, apiKey)
        time.sleep(pause)
