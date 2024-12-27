#
# copyright Mark McIntyre 2023-
#

import pandas as pd
import os
import sys
import datetime


def fixBadRain(datadir, yr):
    datafile=f'{datadir}/raw-{yr}.parquet'
    df = pd.read_parquet(datafile)
    df['rainchg'] = df.rain_mm.diff().fillna(0)
    df.loc[df.rainchg < -0.31, ['rainchg']] = 0
    df2 = df[(df.month==2) & (df.rainchg>0.25)]
    df.loc[df2.index, 'rainchg'] = 0
    basename_template='weatherdata_{i}'
    df.to_parquet(datafile, partition_cols=['year','month','day'], existing_data_behavior='delete_matching', basename_template=basename_template)


def fixupRainData():
    yr = 2023
    rawdir = '/home/bitnami/weather/raw'

    # general fixer upper which will need tweaked for every use-case i discover
    #startdt = datetime.datetime(2023, 10, 27)
    #enddt = datetime.datetime(2023, 11, 23)
    #adj = 846.4

    df = pd.read_parquet(os.path.join(rawdir, f'raw-{yr}.parquet'))
#    df.loc[(df.timestamp >=pd.Timestamp(startdt, tz='UTC')) & (df.timestamp < pd.Timestamp(enddt, tz='UTC')), ['rain_mm']] = \
#        df.loc[(df.timestamp >=pd.Timestamp(startdt, tz='UTC')) & (df.timestamp < pd.Timestamp(enddt, tz='UTC')), ['rain_mm']] - adj
#    df.loc[(df.timestamp >=pd.Timestamp(startdt, tz='UTC')) & (df.timestamp < pd.Timestamp(enddt, tz='UTC')), ['rain_mm']] = \
#        df.loc[(df.timestamp >=pd.Timestamp(startdt, tz='UTC')) & (df.timestamp < pd.Timestamp(enddt, tz='UTC')), ['rain_mm']] - adj
    #df.loc[df.rain_mm==28.5, ['rain_mm']] = np.nan
    df.rain_mm.mask(round(df.rain_mm,1) == 8.1, inplace=True)
    df.rain_mm.mask(round(df.rain_mm,1) == 8.5, inplace=True)
    df.rain_mm.mask(round(df.rain_mm,1) == 8.9, inplace=True)
    df.rain_mm.ffill(inplace=True) # and backfill 
    df['rainchg'] = df.rain_mm.diff().fillna(0)
    df.loc[df.rainchg < -0.31, ['rainchg']] = 0
    df.to_parquet(os.path.join(rawdir, f'raw-{yr}.parquet'))


def cleanData(yr, srcdir):
    pqfile = os.path.expanduser(os.path.join(srcdir, f'raw-{yr}.parquet'))
    df = pd.read_parquet(pqfile)

    df.temperature_C.mask(df.temperature_C > 55, inplace=True) # mask bad outdoor temperatures as NaN
    df.temperature_C.mask(df.temperature_C < -30, inplace=True) # mask bad outdoor temperatures as NaN
    df.temperature_C.mask(df.temperature_C == -22.4, inplace=True) # mask bad outdoor temperatures as NaN
    df.temperature_C.mask(df.temperature_C == -14.7, inplace=True) # mask bad outdoor temperatures as NaN
    df.temperature_C.bfill(inplace=True)
    df.temperature_C.ffill(inplace=True)

    df.humidity.mask(df.humidity < 10, inplace=True) # mask bad outdoor humidity
    df.humidity.bfill(inplace=True)
    df.humidity.ffill(inplace=True)

    df.humidity_in.mask(df.humidity_in < 20, inplace=True) # mask bad indoor humidity
    df.humidity_in.bfill(inplace=True)
    df.humidity_in.ffill(inplace=True)

    df.press_rel.mask(df.press_rel < 900, inplace=True) # mask bad pressure
    df.press_rel.bfill(inplace=True)
    df.press_rel.ffill(inplace=True)

    df.wind_avg_km_h.mask(df.wind_avg_km_h > 50, inplace=True) # mask bad wind
    df.wind_avg_km_h.bfill(inplace=True)
    df.wind_avg_km_h.ffill(inplace=True)

    df.wind_max_km_h.mask(df.wind_max_km_h > 70, inplace=True) # mask bad wind
    df.wind_max_km_h.bfill(inplace=True)
    df.wind_max_km_h.ffill(inplace=True)

    df.rain_mm.mask(df.rain_mm > 1000, inplace=True) # mask bad rain
    df.rain_mm.bfill(inplace=True)
    df.rain_mm.ffill(inplace=True)


    df.press_rel.mask(df.press_rel < 950, inplace=True)
    df.press_rel.bfill(inplace=True)
    df.press_rel.ffill(inplace=True)

    df.apressure.mask(df.apressure < 950, inplace=True)
    df.apressure.bfill(inplace=True)
    df.apressure.ffill(inplace=True)

    df.press_rel.mask(df.press_rel > 1060, inplace=True)
    df.press_rel.bfill(inplace=True)
    df.press_rel.ffill(inplace=True)

    df.apressure.mask(df.apressure > 1060, inplace=True)
    df.apressure.bfill(inplace=True)
    df.apressure.ffill(inplace=True)

    df['rainchg'] = df.rain_mm.diff().fillna(0)
    df.loc[df.rainchg < -1, ['rainchg']] = 0
    df.rainchg.mask(df.rainchg > 30, inplace=True)
    df.rainchg.bfill(inplace=True)
    df.rainchg.ffill(inplace=True)

    basename_template='weatherdata_{i}'
    df.to_parquet(pqfile, partition_cols=['year','month','day'],
        existing_data_behavior='delete_matching', basename_template=basename_template)


def addTSColumn(yr):
    datafile = f'raw-{yr}.parquet'
    targdir = os.path.expanduser('~/weather/raw')
    newdata = pd.read_parquet(os.path.join(targdir, datafile))
    newdata['timestamp'] = pd.to_datetime(newdata.index, utc=True)
    basename_template='weatherdata_{i}'
    newdata.to_parquet(os.path.join(targdir, datafile), partition_cols=['year','month','day'], 
        existing_data_behavior='delete_matching', basename_template=basename_template)


def dropNAHum(yr):
    datafile = f'raw-{yr}.parquet'
    targdir = os.path.expanduser('~/weather/raw')
    pfile = os.path.join(targdir, datafile)
    newdata = pd.read_parquet(pfile)
    print(f'currently {len(newdata)} records')
    newdata.dropna(subset=['humidity_in'], inplace=True)
    print(f'now {len(newdata)} records, writing to {pfile}')
    basename_template='weatherdata_{i}'
    newdata.to_parquet(pfile+'_new', partition_cols=['year','month','day'], 
        existing_data_behavior='delete_matching', basename_template=basename_template)


if __name__ == '__main__':
    yr = datetime.datetime.now().year
    if len(sys.argv)>1:
        yr = int(sys.argv[1])
    targdir = os.path.expanduser('~/weather/raw')
    if len(sys.argv)>2:
        targdir = os.path.expanduser(sys.argv[2])
    print(f'processing {yr}, output to {targdir}')
    cleanData(yr, targdir)
