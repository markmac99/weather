#
# copyright Mark McIntyre 2023-
#

import pandas as pd
import os
import sys
import datetime


def loadADay(dtval, srcdir):
    fname = os.path.join(os.path.expanduser(srcdir), dtval.strftime('%Y'), dtval.strftime('%Y-%m'), dtval.strftime('%Y-%m-%d.txt'))
    if not os.path.isfile(fname):
        print(f'no data for {dtval.strftime("%Y-%m-%d")}')
        return None
    print(f'processing {dtval.strftime("%Y-%m-%d")}')
    names=['time','battery_ok','humidity_in','temp_c_in','humidity','temperature_C',
        'press_rel','wind_ave','wind_max','wind_dir','rain_mm','spare']
    df = pd.read_csv(fname, names=names)
    df['wind_dir_deg'] = df.wind_dir * 22.5 + 7.5 # convert from direction to angle 
    df['wind_avg_km_h'] = df.wind_ave * 3.6 # convert from m/s to kmh
    df['wind_max_km_h'] = df.wind_max * 3.6 # convert from m/s to kmh
    df['timestamp'] = pd.to_datetime(df.time + 'Z')
    df['time']=[x.strftime('%Y-%m-%dT%H:%M:%SZ') for x in df.timestamp]
    df.set_index(['time'],inplace=True)
    df = df.drop(axis=1, labels=['wind_ave','wind_max','wind_dir','spare'])
    df['model'] = 'Fineoffset-WHx080'
    df['id'] = 86.0
    df['mic'] = 'CRC'
    df['subtype'] = 0.0
    return df


def mergeData():
    olddf = pd.read_parquet('tmp/raw-2023.parquet')
    newdf = pd.read_parquet('raw-2023.parquet')
    nn = pd.concat([olddf, newdf]).drop_duplicates()
    nn.to_parquet('tmp/raw-2023-new.parquet')


def cleanData(yr):
    df = pd.read_parquet(os.path.expanduser(f'~/weather/raw/raw-{yr}.parquet'))

    df.temperature_C.mask(df.temperature_C > 48, inplace=True) # mask bad outdoor temperatures as NaN
    df.temperature_C.mask(df.temperature_C == -22.4, inplace=True) # mask bad outdoor temperatures as NaN
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
    df.to_parquet(os.path.expanduser(f'~/weather/raw/raw-{yr}-adj.parquet'))



if __name__ == '__main__':
    if len(sys.argv) > 1:
        yr = int(sys.argv[1])
    else:
        yr = 2023
    srcdir = 'sampledata'
    currdt = datetime.datetime(int(yr),1,1)
    if yr == 2023:
        enddt = datetime.datetime(2023,12,5)
    else:
        enddt = datetime.datetime(int(yr)+1,1,1)
    newdf = None
    while currdt < enddt:
        currdf = loadADay(currdt, srcdir)
        if currdf is not None:
            if newdf is None:
                newdf = currdf
            else:
                newdf = pd.concat([newdf, currdf])
        currdt = currdt + datetime.timedelta(days=1)
    newdf = newdf.bfill(axis=0).ffill(axis=0)
    newdf.to_parquet(os.path.join(srcdir, f'raw-{yr}.parquet'))
