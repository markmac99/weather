
#
# Copyright Mark McIntyre 2023-
#

import pandas as pd
import os
import datetime
import sys
from influxdb import InfluxDBClient


def getMostRecentInfluxData(cfgfile):
    host='ohserver'
    port=8086
    lis = open(cfgfile,'r').readlines()
    startdt = datetime.datetime.strptime(lis[0].strip(), '%Y-%m-%dT%H:%M:%SZ')
    enddt = datetime.datetime.strptime(lis[1].strip(), '%Y-%m-%dT%H:%M:%SZ')

    client = InfluxDBClient(host=host, port=port)
    client.switch_database('openhab')
    res = client.query(f"select mean(value) from rain_b where time > '{startdt}' and time <= '{enddt}' group by time(1m)")
    raindf = pd.DataFrame(res.get_points()).bfill().ffill()
    raindf.sort_index(inplace=True)
    startrain = raindf.iloc[0].mean
    print(f'starting_rain {startrain}')
    res = client.query(f"select mean(value) from BresserWS_temp where time > '{startdt}' and time <= '{enddt}' group by time(1m)")
    tempdf = pd.DataFrame(res.get_points()).bfill().ffill()
    tempdf.sort_index(inplace=True)
    startt = tempdf.iloc[0].mean
    print(f'starting_temp {startt}')
    return startt, startrain


def getDataFromInflux(outdir, r_adj, t_adj, startdt, enddt, host='ohserver', port=8086):

    client = InfluxDBClient(host=host, port=port)
    client.switch_database('openhab')
    res = client.query(f"select mean(value) from rain_b where time > '{startdt}' and time <= '{enddt}' group by time(1m)")
    raindf = pd.DataFrame(res.get_points()).bfill().ffill()
    raindf.rename(columns={'mean':'rain_mm'}, inplace=True)
    if len(raindf)> 0:
        startrain = raindf.iloc[0].rain_mm
    else:
        startrain = 0.0
    print('got rain data')

    res = client.query(f"select mean(value) from BresserWS_temp where time > '{startdt}' and time <= '{enddt}' group by time(1m)")
    tempdf = pd.DataFrame(res.get_points()).bfill().ffill()
    tempdf.rename(columns={'mean':'temperature_C'}, inplace=True)
    starttemp = tempdf.iloc[0].temperature_C
    print('got temp data')

    res = client.query(f"select mean(value) from Bresser_wu_Pressure where time > '{startdt}' and time <= '{enddt}' group by time(1m)")
    pressdf = pd.DataFrame(res.get_points()).bfill().ffill()
    pressdf.rename(columns={'mean':'press_rel'}, inplace=True)
    print('got press data')

    res = client.query(f"select mean(value) from Hum1 where time > '{startdt}' and time <= '{enddt}' group by time(1m)")
    humdf = pd.DataFrame(res.get_points()).bfill().ffill()
    humdf.rename(columns={'mean':'humidity'}, inplace=True)
    print('got humidity data')

    res = client.query(f"select mean(value) from winddir_b where time > '{startdt}' and time <= '{enddt}' group by time(1m)")
    windddf = pd.DataFrame(res.get_points()).bfill().ffill()
    windddf.rename(columns={'mean':'wind_dir_deg'}, inplace=True)
    print('got wind dir data')

    res = client.query(f"select mean(value) from windmax_b where time > '{startdt}' and time <= '{enddt}' group by time(1m)")
    windmdf = pd.DataFrame(res.get_points()).bfill().ffill()
    windmdf.rename(columns={'mean':'wind_max_km_h'}, inplace=True)
    print('got wind max data')

    res = client.query(f"select mean(value) from windavg_b where time > '{startdt}' and time <= '{enddt}' group by time(1m)")
    windadf = pd.DataFrame(res.get_points()).bfill().ffill()
    windadf.rename(columns={'mean':'wind_avg_km_h'}, inplace=True)
    print('got wind avg data')

    # temp_c_in -> temp_c_in
    res = client.query(f"select mean(value) from bmp280_temp_c_in where time > '{startdt}' and time <= '{enddt}' group by time(1m)")
    tempindf = pd.DataFrame(res.get_points()).bfill().ffill()
    tempindf.rename(columns={'mean':'temp_c_in'}, inplace=True)
    print('got indoor temp data')

    # humidity -> humidity_in
    res = client.query(f"select mean(value) from bmp280_humidity_in where time > '{startdt}' and time <= '{enddt}' group by time(1m)")
    humindf = pd.DataFrame(res.get_points()).bfill().ffill()
    humindf.rename(columns={'mean':'humidity_in'}, inplace=True)
    print('got indoor humidity data')

    fulldf = humdf.merge(tempdf, how='outer').merge(pressdf, how='outer').merge(raindf, how='outer')
    fulldf = fulldf.merge(windddf, how='outer').merge(windadf, how='outer').merge(windmdf, how='outer')
    fulldf =fulldf.merge(humindf, how='outer').merge(tempindf, how='outer').bfill().ffill()
    fulldf['battery_ok'] = 128
    fulldf['model'] = 'Fineoffset-WHx080'
    fulldf['id'] = 86.0
    fulldf['mic'] = 'CRC'
    fulldf['subtype'] = 0.0
    fulldf.sort_index(inplace=True)

    fulldf['wind_max_km_h'] = fulldf.wind_max_km_h * 3.6 # convert to km/h
    fulldf['wind_avg_km_h'] = fulldf.wind_avg_km_h * 3.6 # convert to km/h

    #fulldf['press_rel'] = fulldf.press_rel # variance between bresser and bme280
    print(f'adjusting temp by {t_adj - starttemp}')
    fulldf['temperature_C'] = fulldf.temperature_C - starttemp + t_adj # variance between bresser and wh1080
    print(f'adjusting rain by {r_adj - startrain}')
    fulldf['rain_mm'] = fulldf.rain_mm -startrain + r_adj # variance between bresser and wh1080

    fulldf.rain_mm.mask(fulldf.rain_mm > 2000, inplace=True) # remove bad data
    fulldf.rain_mm.mask(fulldf.rain_mm < 0, inplace=True) # remove bad data
    fulldf['rainchg'] = fulldf.rain_mm.diff().fillna(0)
    fulldf.loc[fulldf.rainchg < -0.31, ['rainchg']] = 0

    fulldf['apressure'] = [correctForAltitude(p, t, 80) for p,t in zip(fulldf.press_rel, fulldf.temperature_C)]

    fulldf.set_index(keys=['time'],inplace=True)
    fulldf['timestamp'] = pd.to_datetime(fulldf.index, utc=True)

    if 'rainchg' not in fulldf:
        fulldf['rainchg'] = fulldf.rain_mm.diff().fillna(0)
        fulldf.loc[fulldf.rainchg < -0.31, ['rainchg']] = 0
    if 'year' not in fulldf:
        fulldf['year'] = [v.year for v in fulldf.timestamp]
        fulldf['month'] = [v.month for v in fulldf.timestamp]
        fulldf['day'] = [v.day for v in fulldf.timestamp]

    fulldf.to_parquet(os.path.join(outdir,'newdata.parquet'))
    return 


def correctForAltitude(press, temp, alti):
    # converts sea-level pressure to abs pressure at given altitude
    denom = temp + 273.15 + 0.0065 * alti
    val = (1 - (0.0065 * alti)/denom)
    press_abs = press / pow(val, -5.257)
    return round(press_abs,4)


if __name__ == '__main__':
    cfgfile = sys.argv[1]
    lis = open(cfgfile,'r').readlines()
    startdt = datetime.datetime.strptime(lis[0].strip(), '%Y-%m-%dT%H:%M:%SZ')
    enddt = datetime.datetime.strptime(lis[1].strip(), '%Y-%m-%dT%H:%M:%SZ')

    # adjust these for each processing run - get the offsets from OpenHAB
    t_adj = float(lis[2].strip()) # adjustment to handle the different locations of the stations
    r_adj = float(lis[3].strip()) # adjust rain gauge to balance  -WH1080 minus bresser

    print(f'starting with daterange {startdt} {enddt}')
    getDataFromInflux('.', r_adj, t_adj, startdt, enddt)
    print('done')
