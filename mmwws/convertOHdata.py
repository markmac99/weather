#
# Copyright Mark McIntyre 2023-
#

import pandas as pd
import os
import datetime
import sys


def convertData(outdir):
    fn = os.path.join(outdir, 'historic_bresser_data.txt')
    print('reading and separating the file')
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


def createMergeData(outdir, startdt, enddt, t_adj=0, r_adj=0):
    print('merging the separated data')
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

    seldf['wind_max_km_h'] = seldf.wind_max_km_h * 3.6 # convert to km/h
    seldf['wind_avg_km_h'] = seldf.wind_avg_km_h * 3.6 # convert to km/h

    seldf['press_rel'] = seldf.press_rel - 10 # variance between bresser and bme280
    seldf['temperature_C'] = seldf.temperature_C + t_adj # variance between bresser and wh1080
    seldf['rain_mm'] = seldf.rain_mm + r_adj # variance between bresser and wh1080

    seldf.rain_mm.mask(seldf.rain_mm > 2000, inplace=True) # remove bad data
    seldf.rain_mm.mask(seldf.rain_mm < 0, inplace=True) # remove bad data
    seldf.rain_mm.ffill(inplace=True) # and backfill 
    seldf.rain_mm.bfill(inplace=True) # and forward fill

    seldf.to_parquet(os.path.join(outdir,'alldata.parquet'))
    return 


def mergeDataIn(outdir, tmpdir, yr):
    df = pd.read_parquet(os.path.join(outdir, f'raw-{yr}.parquet'))
    df2 = pd.read_parquet(os.path.join(tmpdir, 'alldata.parquet'))
    df3 = pd.concat([df, df2])
    df3 = df3.sort_index()
    df3.to_parquet(os.path.join(outdir, f'raw-{yr}.parquet'))



if __name__ == '__main__':
    if len(sys.argv) < 2:
        tmpdir = os.path.expanduser('~/weather/tmp')
    else:
        tmpdir = os.path.expanduser(sys.argv[1])
    os.makedirs(tmpdir, exist_ok=True)

    # adjust these for each processing run
    t_adj = 1.2 # adjustment to handle the different locations of the stations
    r_adj = 17.4 - 1184.4 # adjust rain gauge to balance 
    startdt = datetime.datetime(2023,12,6,6,16,25)
    enddt = datetime.datetime(2023,12,6,9,7,30)

    print('starting')
    convertData(tmpdir)
    createMergeData(tmpdir, startdt, enddt, t_adj, r_adj)
    print('done')
