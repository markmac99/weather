#
# copyright Mark McIntyre, 2023-
#

import os
import sys
import datetime
import logging
from logging.handlers import RotatingFileHandler

from windData import minmaxWind
from tempPressData import minmaxTemps, periodTemps
from rainData import periodRain
from tableData import recentTable
from windRose import makeRose
from sqlInterface import loadDfFromDB
from tableData import updateMonthlyTable


logger = logging.getLogger('weather_hourly')


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    fh = RotatingFileHandler(os.path.expanduser('~/logs/weather_hourly.log'), maxBytes=51200, backupCount=10)
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

    df = loadDfFromDB(days=32)
    logger.info(f'loaded {len(df)} records')

    logger.info('creating temperature graphs')
    periodTemps(df, outdir, period=24*7) 
    minmaxTemps(df, outdir, '28day')

    logger.info('creating tables')
    recentTable(df, outdir, period=24*31) # last 31 days

    logger.info('creating pressure graphs')
    periodTemps(df, outdir, period=24*7, datafield='pressure', fieldname='pressure', fnamefrag='pressure', units='hPa')
    periodTemps(df, outdir, period=24*28, datafield='pressure', fieldname='pressure', fnamefrag='pressure', units='hPa')

    logger.info('creating wind graphs')
    minmaxWind(df, outdir, period=24*7)
    minmaxWind(df, outdir, period=24*28)

    logger.info('creating rainfall graphs')
    periodRain(df, outdir, '7day')
    periodRain(df, outdir, '28day')
    #periodRain(df, outdir, '90day')

    logger.info('creating wind roses')
    makeRose(df, outdir, 1)
    makeRose(df, outdir, 7)

    logger.info('updating monthly tables')
    currdt = datetime.datetime.now()
    if currdt.hour < 1 and currdt.day == 1:
        currdt = datetime.datetime.now() + datetime.timedelta(days=-1)
    _ = updateMonthlyTable(currdt.year, currdt.month)
    
    logger.info('done')
