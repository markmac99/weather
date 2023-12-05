#
# Copyright Mark McIntyre 2023-
#

import pandas as pd
import os
import datetime


def convertData(outdir):
    fn = '/mnt/c/temp/historic_bresser_data.txt'
    lis = open(fn, 'r').readlines()
    df = None
    for li in lis:
        if len(li) < 2:
            continue # skip blank rows
        spls = li.split()
        if len(spls) == 1 and li[:5] != '-----': 
            print(f'data {spls[0]}')
            # the row contains an element name so set the filename and initialise the dataframe
            outf = os.path.join(outdir, spls[0]+'.csv')
            df = pd.DataFrame(columns=['timestamp','value'])
        elif li[:5] == '-----': 
            # if we find the separator or hit end-of-file, save the dataframe
            print(f'saving to {outf}')
            df.to_csv(outf)
            continue
        elif li == lis[-1]:
            print(f'saving to {outf}')
            df.loc[len(df.index)] = spls
            df.to_csv(outf)
            continue
        else:
            print(f'appending {spls}')
            df.loc[len(df.index)] = spls
    return


def createMergeData(outdir, startdt, enddt):
    tempdf = pd.read_csv(os.path.join(outdir, 'temperature_C.csv'), names=['timeval','temperature_C'],skiprows=1)
    humdf = pd.read_csv(os.path.join(outdir, 'humidity.csv'), names=['timeval','humidity'],skiprows=1)
    pressdf = pd.read_csv(os.path.join(outdir, 'pressure.csv'), names=['timeval','press_rel'],skiprows=1)
    raindf = pd.read_csv(os.path.join(outdir, 'rain.csv'), names=['timeval','rain_mm'],skiprows=1)
    windddf = pd.read_csv(os.path.join(outdir, 'winddir.csv'), names=['timeval','wind_dir_deg'],skiprows=1)
    windmdf = pd.read_csv(os.path.join(outdir, 'windmax.csv'), names=['timeval','wind_max_km_h'],skiprows=1)
    windadf = pd.read_csv(os.path.join(outdir, 'Windspeed.csv'), names=['timeval','wind_avg_km_h'],skiprows=1)
    fulldf = humdf.merge(tempdf).merge(pressdf).merge(raindf).merge(windddf).merge(windadf).merge(windmdf)
    fulldf['battery_ok'] = 128
    fulldf['model'] = 'Fineoffset-WHx080'
    fulldf['id'] = 86.0
    fulldf['mic'] = 'CRC'
    fulldf['subtype'] = 0.0
    fulldf['time']=[datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%dT%H:%M:%SZ') for x in fulldf.timeval/1000]
    fulldf.set_index(['time'],inplace=True)
    fulldf['timestamp']=[pd.Timestamp(datetime.datetime.fromtimestamp(x), tz='UTC') for x in fulldf.timeval/1000]
    fulldf = fulldf.drop(columns=['timeval'])

    seldf = fulldf[fulldf.timestamp >= pd.Timestamp(startdt,tz='UTC')]
    seldf = seldf[seldf.timestamp < pd.Timestamp(enddt,tz='UTC')]

    seldf.rain_mm.mask(seldf.rain_mm > 2000, inplace=True) # remove bad data
    seldf.rain_mm.ffill(inplace=True) # and backfill 
    seldf['wind_max_km_h'] = seldf.wind_max_km_h * 3.6 # convert to km/h
    seldf['wind_avg_km_h'] = seldf.wind_avg_km_h * 3.6 # convert to km/h
    seldf['press_rel'] = seldf.press_rel - 10 # variance between bresser and bme280

    seldf.to_parquet(os.path.join(outdir,'alldata.parquet'))
    return 


if __name__ == '__main__':
    outdir = 'c:/temp/bresserdata'
    os.makedirs(outdir, exist_ok=True)
    #convertData(outdir)
    startdt = datetime.datetime(2023,10,27)
    enddt = datetime.datetime(2023,11,23)
    createMergeData(outdir, startdt, enddt)

"""
yr=2023
df = pd.read_parquet(f'raw-{yr}.parquet')
df.rain_mm.mask((df.rain_mm > 8.0) & (df.rain_mm < 13.3) & (df.timestamp >= pd.Timestamp(datetime.datetime(2023,12,4), tz='UTC')) &
                (df.timestamp < pd.Timestamp(datetime.datetime(2023,12,5), tz='UTC')), inplace=True)
df.rain_mm.ffill(inplace=True)
df.to_parquet(f'raw-{yr}-new.parquet')
"""
