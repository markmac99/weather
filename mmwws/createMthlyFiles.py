#
# copyright Mark McIntyre, 2023-
#

#import pandas as pd
#import platform
#import time
import os
import sys
import datetime
import logging
from logging.handlers import RotatingFileHandler

from tempPressData import minmaxTemps
from rainData import periodRain
from tableData import monthlySummary
from sqlInterface import loadDfFromDB


logger = logging.getLogger('weather_createMthly')


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    fh = RotatingFileHandler(os.path.expanduser('~/logs/weather_monthly.log'), maxBytes=51200, backupCount=10)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info('starting')
    yr = datetime.datetime.now().year
    if len(sys.argv) < 2:
        outdir = os.path.expanduser('~/weather/tmp')
    else:
        outdir = os.path.expanduser(sys.argv[1])
    rawdir = outdir.replace('data','raw')
    os.makedirs(outdir, exist_ok=True)

    df = loadDfFromDB(720)
    logger.info(f'loaded {len(df)} records')

    logger.info('creating 12mth temps')
    minmaxTemps(df, outdir, '12month')
    logger.info('creating 12mth rain')
    periodRain(df, outdir, '12month')
    logger.info('creating allmths table')
    monthlySummary(df, outdir)
    logger.info('done')
