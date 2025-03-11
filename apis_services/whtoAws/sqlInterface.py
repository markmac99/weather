import pymysql
import os
import json
import datetime
from whConfig import loadSQLconfig


def postToMySQL(targfile):
    if not os.path.isfile(targfile):
        print('source file not found')
        return 
    
    sqldb, sqluser, sqlpass, sqlserver = loadSQLconfig()

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

    # now get previous rain and work out real change
    result = cur.execute('select rain_mm, temperature_C from wh1080data order by time desc limit 1')
    lastdata = cur.fetchone()
    prevrain = lastdata[0]
    rainchg = whdata['rain_mm'] - prevrain
    if rainchg > -0.31 and rainchg < 50:
        whdata['rainchg'] = rainchg
        
    prevtempc = lastdata[1]
    if whdata['temperature_C'] > 55 or whdata['temperature_C'] < -30 or abs(prevtempc - whdata['temperature_C']) > 10:
        whdata['temperature_C'] = prevtempc

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
