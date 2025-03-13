#
# copyright Mark McIntyre, 2023-
#

import os
import sys
import datetime
import logging
from logging.handlers import RotatingFileHandler

from windData import minmaxWind, recentWind
from tempPressData import recentTemps, periodTemps
from rainData import recentRain, last24hRain
from tableData import recentTable
from sqlInterface import loadDfFromDB


logger = logging.getLogger('weather_logger')


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    fh = RotatingFileHandler(os.path.expanduser('~/logs/weather_logger.log'), maxBytes=51200, backupCount=10)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info('starting')
    now = datetime.datetime.now()
    yr = now.year
    if len(sys.argv) < 2:
        outdir = os.path.expanduser('~/weather/tmp')
    else:
        outdir = os.path.expanduser(sys.argv[1])
    os.makedirs(outdir, exist_ok=True)

    df = loadDfFromDB(days=2)
    logger.info(f'loaded {len(df)} records')

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
