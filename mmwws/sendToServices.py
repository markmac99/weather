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
import logging
from logging.handlers import RotatingFileHandler

from conversions import dewPoint, CtoF, KMHTOMPH, MMTOIN, HPATOINHG
from sqlInterface import loadDfFromDB


logger = logging.getLogger('weather_services')

# dateutc must be %Y-%m-%d+%H:%M:%S with the :s encoded as %3A
# units should be imperial - inHg, mph, fahrenheit
moTemplate = 'siteid={}&siteAuthenticationKey={}&dateutc={}&softwaretype={}&' \
    'baromin={}&tempf={}&winddir={}&windspeedmph={}&windgustmph={}&' \
    'humidity={}&dailyrainin={}&dewpointf={}'


def sendToMetOffice(cfgdir, latestdata, rainstart):
    cfg = configparser.ConfigParser()
    cfg.read(os.path.join(cfgdir,'weathersites.ini'))
    siteid = cfg['metoffice']['site id']
    key = cfg['metoffice']['aws pin']
    swtype='mmwws'
    dateutc = latestdata.timestamp.strftime('%Y-%m-%d+%H:%M:%S')
    dateutc = dateutc.replace(':','%3A').replace(':','%3A')
    press = round(latestdata.press_rel * HPATOINHG, 1)
    tempf = round(CtoF(latestdata.temperature_C), 1)
    winddir = latestdata.wind_dir_deg
    wind = round(latestdata.wind_avg_km_h * KMHTOMPH, 1)
    windgust = round(latestdata.wind_max_km_h * KMHTOMPH, 1)
    humidity = latestdata.humidity
    dailyrain = round((latestdata.rain_mm - rainstart)* MMTOIN, 1)
    dewpointf = round(CtoF(dewPoint(latestdata.temperature_C, latestdata.humidity)), 1)
    prepared_data = moTemplate.format(siteid, key, dateutc, swtype, press, tempf, winddir, wind, windgust, humidity, dailyrain, dewpointf)
    
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


# units should be imperial - inHg, mph, fahrenheit
wuTemplate = 'ID={}&PASSWORD={}&dateutc=now&action=updateraw&' \
    'baromin={}&tempf={}&winddir={}&windspeedmph={}&windgustmph={}&' \
    'humidity={}&dailyrainin={}&dewptf={}'


def sendToWunderground(cfgdir, latestdata, rainstart):
    cfg = configparser.ConfigParser()
    cfg.read(os.path.join(cfgdir,'weathersites.ini'))
    siteid = cfg['underground']['station']
    key = cfg['underground']['password']
    press = round(latestdata.press_rel * HPATOINHG, 1)
    tempf = round(CtoF(latestdata.temperature_C), 1)
    winddir = latestdata.wind_dir_deg
    wind = round(latestdata.wind_avg_km_h * KMHTOMPH, 1)
    windgust = round(latestdata.wind_max_km_h * KMHTOMPH, 1)
    humidity = latestdata.humidity
    dailyrain = round((latestdata.rain_mm - rainstart)* MMTOIN, 1)
    dewpointf = round(CtoF(dewPoint(latestdata.temperature_C, latestdata.humidity)), 1)
    prepared_data = wuTemplate.format(siteid, key, press, tempf, winddir, wind, windgust, humidity, dailyrain, dewpointf)
    
    try:
        rsp = requests.get('https://rtupdate.wunderground.com/weatherstation/updateweatherstation.php', 
                           params=prepared_data, timeout=60)
    except Exception as ex:
        return False, repr(ex)
    if rsp.status_code == 429:
        # UK Met Office server uses 429 to signal duplicate data
        return True, 'repeated data'
    if rsp.status_code != 200:
        return False, 'http status: {:d}'.format(rsp.status_code)
    rsp = rsp.text
    if rsp:
        return True, 'server response "{!r}"'.format(rsp)
    return True, 'OK'



def sendToOpenWeatherMap(cfgdir, latestdata, rainstart):
    cfg = configparser.ConfigParser()
    cfg.read(os.path.join(cfgdir,'weathersites.ini'))
    siteid = cfg['openweathermap']['station id']
    key = cfg['openweathermap']['api key']
    dt = int(latestdata.timestamp.timestamp())
    press = round(latestdata.press_rel,1)
    tempc = round(latestdata.temperature_C, 1)
    winddir = latestdata.wind_dir_deg
    wind = round(latestdata.wind_avg_km_h / 3.6, 1)
    windgust = round(latestdata.wind_max_km_h / 3.6, 1)
    humidity = latestdata.humidity
    dailyrain = round((latestdata.rain_mm - rainstart), 1)
    dewpointc = round(dewPoint(latestdata.temperature_C, latestdata.humidity), 1)
    prepared_data = {
        "station_id": f"{siteid}", 
        "dt": dt, 
        "pressure": press, 
        "temperature": tempc, 
        "wind_deg": winddir,
        "wind_speed": wind, 
        "wind_gust": windgust,
        "humidity": humidity,
        "rain_24h": dailyrain, 
        "dew_point": dewpointc
    }
    
    try:
        url = 'https://api.openweathermap.org/data/3.0/measurements'
        with requests.Session() as session:
            session.headers.update({'Content-Type': 'application/json'})
            session.params.update({'appid': key})
            rsp = session.post(url, json=[prepared_data], timeout=60)
    except Exception as ex:
        return False, repr(ex)
    if rsp.status_code == 429:
        # UK Met Office server uses 429 to signal duplicate data
        return True, 'repeated data'
    if rsp.status_code != 204:
        return False, 'http status: {:d} {}'.format(rsp.status_code, rsp.text)
    rsp = rsp.text
    if rsp:
        return True, 'server response "{!r}"'.format(rsp)
    return True, 'OK'


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    fh = RotatingFileHandler(os.path.expanduser('~/logs/weather_services.log'), maxBytes=51200, backupCount=10)
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

    df = loadDfFromDB(1)
    logger.info(f'loaded {len(df)} records')

    nowzeroed = now.replace(hour=0, minute=0, second=0, microsecond=0)
    df = df[df.timestamp >= pd.Timestamp(nowzeroed, tz='UTC')]
    rainstart = df.iloc[0].rain_mm
    latestdata=df.iloc[-1]

    sts, msg = sendToMetOffice('.', latestdata, rainstart)
    logger.info(f'metoffice: {sts} {msg}')
    sts, msg = sendToWunderground('.', latestdata, rainstart)
    logger.info(f'wunderground: {sts} {msg}')
    sts, msg = sendToOpenWeatherMap('.', latestdata, rainstart)
    logger.info(f'openweathermap: {sts} {msg}')
