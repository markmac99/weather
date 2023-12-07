#
# copyright Mark McIntyre, 2023-
#

# various functions to send data to 3rd party services such as the met office, wunderground and openweathermap

import pandas as pd
import requests
import datetime
import configparser
import os
import sys
import platform
import time 

# dateutc must be %Y-%m-%d+%H:%M:%S with the :s encoded as %3A
# units should be imperial - nches, mph, fahrenheit
moTemplate = 'siteid={}&siteAuthenticationKey={}&dateutc={}&softwaretype={}&' \
    'baromin={}&tempf={}&winddir={}&windspeedmph={}&windgustmph={}&' \
    'humidity={}&dailyrainin={}'

HPATOIN = 0.02953
KMHTOMPH = 0.6214
MMTOIN = 1/25.4


def sendToMetOffice(cfgdir, latestdata, rainstart):
    cfg = configparser.ConfigParser()
    cfg.read(os.path.join(cfgdir,'weathersites.ini'))
    siteid = cfg['metoffice']['site id']
    key = cfg['metoffice']['aws pin']
    swtype='mmwws'
    dateutc = latestdata.timestamp.strftime('%Y-%m-%d+%H:%M:%S')
    dateutc = dateutc.replace(':','%3A').replace(':','%3A')
    press = round(latestdata.press_rel * HPATOIN, 1)
    tempf = round(latestdata.temperature_C * 1.8 + 32, 1)
    winddir = latestdata.wind_dir_deg
    wind = round(latestdata.wind_avg_km_h * KMHTOMPH, 1)
    windgust = round(latestdata.wind_max_km_h * KMHTOMPH, 1)
    humidity = latestdata.humidity
    dailyrain = round((latestdata.rain_mm - rainstart)* MMTOIN, 1)
    prepared_data = moTemplate.format(siteid, key, dateutc, swtype, press, tempf, winddir, wind, windgust, humidity, dailyrain)
    print(prepared_data)
    
    try:
        rsp = requests.get('http://wow.metoffice.gov.uk/automaticreading', params=prepared_data, timeout=60)
    except Exception as ex:
        return False, repr(ex)
    if rsp.status_code == 429:
        # UK Met Office server uses 429 to signal duplicate data
        return True, 'repeated data'
    if rsp.status_code != 200:
        return False, 'http status: {:d}'.format(rsp.status_code)
    rsp = rsp.json()
    if rsp:
        return True, 'server response "{!r}"'.format(rsp)
    return True, 'OK'


if __name__ == '__main__':
    now = datetime.datetime.now()
    yr = now.year
    if len(sys.argv) < 2:
        outdir = os.path.expanduser('~/weather/tmp')
    else:
        outdir = os.path.expanduser(sys.argv[1])
    os.makedirs(outdir, exist_ok=True)
    rawdir = outdir.replace('data','raw')
    if platform.node() != 'wordpresssite':
        df = pd.read_parquet(f'https://markmcintyreastro.co.uk/weather/raw/raw-{yr}.parquet')
        df2 = pd.read_parquet(f'https://markmcintyreastro.co.uk/weather/raw/raw-{yr-1}.parquet')
    else:
        # current years datafile may be in the process of getting written to
        retries = 0
        while retries < 5:
            try:
                print('loading datafiles')
                df = pd.read_parquet(os.path.join(rawdir, f'raw-{yr}.parquet'))
                break
            except:
                print('file in use, waiting 5s')
                time.sleep(5)
                retries += 1
        if retries == 5:
            print('unable to open datafile, aborting')
            exit(0)
        # only load last years data if needed
        if (now +datetime.timedelta(days=-32)).year != yr:
            df2 = pd.read_parquet(os.path.join(rawdir, f'raw-{yr-1}.parquet'))
            df = pd.concat([df2,df])

    nowzeroed = now.replace(hour=0, minute=0, second=0, microsecond=0)
    df = df[df.timestamp >= pd.Timestamp(nowzeroed, tz='UTC')]
    rainstart = df.iloc[0].rain_mm
    latestdata=df.iloc[-1]

    sts, msg = sendToMetOffice('.', latestdata, rainstart)
    print('metoffice:', sts, msg)
