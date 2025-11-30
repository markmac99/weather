import pymysql
import os
import json
import datetime
from whConfig import loadSQLconfig


def postToMySQL(targfile, bkp=False):
    if not os.path.isfile(targfile):
        print('source file not found')
        return 
    
    sqldb, sqluser, sqlpass, sqlserver = loadSQLconfig(bkp=bkp)

    conn = pymysql.connect(host=sqlserver, user=sqluser, password=sqlpass, db=sqldb)
    cur = conn.cursor()

    lis = open(targfile, 'r').readlines()
    whdata = json.loads(lis[-1])
    evtdt = datetime.datetime.strptime(whdata['time'], '%Y-%m-%dT%H:%M:%SZ')
    whdata['year'] = evtdt.year
    whdata['month'] = evtdt.month
    whdata['day'] = evtdt.day
    whdata['timestamp'] = evtdt
    whdata['rainchg'] = 0

    # get previous rain and work out change
    result = cur.execute('select rain_mm, temperature_C, press_rel, apressure, wind_avg_km_h, wind_max_km_h from wh1080data order by time desc limit 1')
    lastdata = cur.fetchone()
    prevrain = lastdata[0]
    rainchg = whdata['rain_mm'] - prevrain

    # ignore unrealistic changes
    if rainchg > -0.31 and rainchg < 50:
        whdata['rainchg'] = rainchg

    # check for unrealistic temperature movements    
    prevtempc = lastdata[1]
    if whdata['temperature_C'] > 55 or whdata['temperature_C'] < -30 or abs(prevtempc - whdata['temperature_C']) > 10:
        whdata['temperature_C'] = prevtempc

    # TODO - check for unrealistic wind and pressure changes. 
    # pressure change > 10 hPa is very implausible, as is a value outside the range 950-1080
    prevpress = lastdata[2]
    prevapress = lastdata[3]
    pressdiff = abs(whdata['press_rel'] - prevpress)
    if whdata['press_rel'] < 900 or whdata['press_rel'] > 1100 or pressdiff > 10:
        whdata['press_rel'] = prevpress
        whdata['apressure'] = prevapress

    # wind speed change of > 10 kmh is unrealistic
    prevwind = lastdata[4]
    prevgust = lastdata[5]
    winddiff = abs(whdata['wind_avg_km_h'] - prevwind)
    if whdata['wind_avg_km_h'] > 120 or winddiff > 50:
        whdata['wind_avg_km_h'] = prevwind
    if whdata['wind_max_km_h'] > 170:
        whdata['wind_max_km_h'] = prevgust

    sql = " INSERT INTO wh1080data (time, model, subtype, id, battery_ok, temperature_C, humidity,"\
        "wind_dir_deg, wind_avg_km_h, wind_max_km_h, rain_mm, mic,"\
        "timestamp, humidity_in, temp_c_in, press_rel, apressure,"\
        "rainchg, year, month, day) VALUES (%s, %s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s, %s,%s, %s,%s, %s,%s, %s,%s, %s)"

    vals = (whdata['time'], whdata['model'], whdata['subtype'], whdata['id'], whdata['battery_ok'], whdata['temperature_C'], whdata['humidity'],
        whdata['wind_dir_deg'], whdata['wind_avg_km_h'], whdata['wind_max_km_h'], whdata['rain_mm'], whdata['mic'],
        evtdt.strftime('%Y-%m-%d %H:%M:%S'), whdata['humidity_in'], whdata['temp_c_in'], whdata['press_rel'], whdata['apressure'],
        whdata['rainchg'], whdata['year'], whdata['month'], whdata['day'])

    result = cur.execute(sql, vals)
    if result != 1:
        print('unable to write to mysql table')

    conn.commit()
    conn.close()

    return
