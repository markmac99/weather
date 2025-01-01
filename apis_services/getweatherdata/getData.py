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
import shutil
#import requests
#from urllib3.exceptions import InsecureRequestWarning

from apiConfig import apiUrl, apiKey, basedir, pause

logger = logging.getLogger('mqtofile')


def loadHistoricData(whfile, bpfile, targfile):
    whraw = open(whfile, 'r').readlines()
    bpraw = open(bpfile, 'r').readlines()
    bpdata = []
    whdata = []
    for wh in whraw:
        whdata.append(json.loads(wh))
    for bp in bpraw:
        bpdata.append(json.loads(bp))
    bpdf=pd.DataFrame(bpdata)
    whdf=pd.DataFrame(whdata)
    whdf.drop_duplicates(inplace=True)
    bpdf['timestamp']=[datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ') for v in bpdf.time]
    whdf['timestamp']=[datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S') for v in whdf.time]

    tvals = []
    pvals = []
    hvals = []
    avals = []
    for rw, wh in whdf.iterrows():
        tval = wh.timestamp
        bprec = bpdf.iloc[(bpdf['timestamp']-tval).abs().argsort()[:2]]
        tvals.append(sum(bprec.temp_c_in)/2)
        pvals.append(sum(bprec.press_rel)/2)
        hvals.append(sum(bprec.humidity_in)/2)
        avals.append(sum(bprec.apressure)/2)

    whdf['temp_c_in'] = tvals
    whdf['press_rel'] = pvals
    whdf['humidity_in'] = hvals
    whdf['apressure'] = avals
    whdf['year'] = [v.year for v in whdf.timestamp]
    whdf['month'] = [v.month for v in whdf.timestamp]
    whdf['day'] = [v.day for v in whdf.timestamp]
    whdf['rainchg'] = whdf.rain_mm.diff().fillna(0)
    whdf.loc[whdf.rainchg < -0.31, ['rainchg']] = 0
    whdf.set_index(['time'], inplace=True)

    curryr = whdf.year.min()
    currdf = pd.read_parquet(f'/home/bitnami/weather/raw/raw-{curryr}.parquet')
    #currdf = pd.read_parquet(targfile)
    newdf = pd.concat([currdf, whdf])
    newdf.drop_duplicates(inplace=True)
    newdf.to_parquet(targfile, partition_cols=['year','month','day'])
    return 


def addPartition(datafile):
    df = None
    if os.path.isfile(datafile):
        shutil.move(datafile, datafile+'.bkp')
        df = pd.read_parquet(datafile+'.bkp')
        df.sort_index(inplace=True)
        if 'timestamp' not in df:
            df['timestamp'] = pd.to_datetime(df.index, utc=True)
        if 'rainchg' not in df:
            df['rainchg'] = df.rain_mm.diff().fillna(0)
            df.loc[df.rainchg < -0.31, ['rainchg']] = 0
        if 'year' not in df:
            df['year'] = [v.year for v in df.timestamp]
            df['month'] = [v.month for v in df.timestamp]
            df['day'] = [v.day for v in df.timestamp]
        df.to_parquet(datafile, partition_cols=['year','month','day'])


def getNewData(datafile, srcdir, s3loc, url=None, key=None):
    #logger.warning(url)
    newdata = None
    df = None
    try:
        #requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        #headers={'x-api-key': key}
        #res = requests.get(url, headers=headers, verify=False)
        #if res.status_code == 200:
        #    newdata = pd.read_json(res.text.strip())
        #    newdata.set_index(['time'], inplace=True)
        #    newdata['timestamp'] = pd.to_datetime(newdata.index, utc=True)
        #else:
        #    logger.warning('unable to retrieve data')
        rawdata = json.load(open(os.path.expanduser(os.path.join(srcdir, 'weatherdata.json'))))
        newdata=pd.DataFrame([rawdata])
        newdata.set_index(['time'], inplace=True)
        newdata['timestamp'] = pd.to_datetime(newdata.index, utc=True)
        newdata['year'] = [v.year for v in newdata.timestamp]
        newdata['month'] = [v.month for v in newdata.timestamp]
        newdata['day'] = [v.day for v in newdata.timestamp]
        logger.debug('loaded new datafile')
    except Exception as e:
        logger.warning('unable to load source data')
        logger.warning(e)
        return
    
    df = None
    if os.path.isdir(datafile):
        logger.debug(f'loading {datafile}')
        df = pd.read_parquet(datafile)
        df.sort_index(inplace=True)
        df.drop_duplicates(inplace=True)
        if 'timestamp' not in df:
            df['timestamp'] = pd.to_datetime(df.index, utc=True)
        if 'rainchg' not in df:
            df['rainchg'] = df.rain_mm.diff().fillna(0)
            df.loc[df.rainchg < -0.31, ['rainchg']] = 0
        if 'year' not in df:
            df['year'] = [v.year for v in df.timestamp]
            df['month'] = [v.month for v in df.timestamp]
            df['day'] = [v.day for v in df.timestamp]
    else:
        logger.debug('no old data to load')
    if df is not None and newdata is not None:
        logger.debug('adding raindata')
        lastrain = df.iloc[-1].rain_mm
        newdata['rainchg'] = newdata.rain_mm - lastrain
        newdata.loc[newdata.rainchg < -0.31, ['rainchg']] = 0
        newdata = pd.concat([df, newdata])
        newdata.drop_duplicates(inplace=True)
        #logger.debug(f'{lastrain} {newdata.rain_mm} ')
    if df is not None and newdata is None:
        logger.debug('no new data to concatenate')
        newdata = df
    if newdata is not None:
        logger.debug('cleaning new data if needed')
        # mask bad outdoor temperatures as NaN, then backfill with adjacent value
        newdata.temperature_C.mask(newdata.temperature_C > 55, inplace=True) 
        newdata.temperature_C.mask(newdata.temperature_C < -30, inplace=True) 
        newdata.temperature_C.mask(newdata.temperature_C == -22.4, inplace=True)
        newdata.temperature_C.mask(newdata.temperature_C == -14.7, inplace=True)
        newdata.temperature_C.bfill(inplace=True)
        newdata.temperature_C.ffill(inplace=True)

        try:
            newdata['rainchg'] = newdata.rainchg.fillna(0)
        except:
            # above will fail if only one record
            pass
        newdata.drop_duplicates(inplace=True)
        newdata.sort_values(by=['timestamp'], inplace=True)
        logger.info(f'saving updated data with {len(newdata)} records')
        basename_template='weatherdata_{i}'
        newdata.to_parquet(datafile, partition_cols=['year','month','day'], 
            existing_data_behavior='delete_matching', basename_template=basename_template)
        # do not do this here, it rewrites every file once a minute, which is extremely costly
        # newdata.to_parquet(s3loc, partition_cols=['year','month','day'], existing_data_behavior='delete_matching')
    else:
        logger.debug('no data at all')  
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
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info(f'capturing data at {pause} intervals to {outdir}')
    keepgoing = True
    while keepgoing:
        yr = datetime.datetime.now().year
        fname = os.path.expanduser(os.path.join(outdir, f'raw-{yr}.parquet'))
        s3loc = f's3://mjmm-weatherdata/raw-{yr}.parquet'
        getNewData(fname, indir, s3loc, apiUrl, apiKey)
        time.sleep(pause)
