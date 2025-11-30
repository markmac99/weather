#!/bin/bash

# copyright Mark McIntyre, 2023-

import time
import datetime
import os
import sys
import json
import paho.mqtt.client as mqtt
import pymysql

from whConfig import loadSQLconfig
from mqConfig import readConfig, stationAltitude

from bme280 import bme280, bme280_i2c


def writeLogEntry(logdir, msg):
    with open(os.path.join(logdir, "bmp280.log"), mode='a+', encoding='utf-8') as f:
        nowdt = datetime.datetime.now(datetime.timezone.utc).isoformat()
        f.write(f'{nowdt}: {msg}')


def postToMySQL(bmpdata, logdir, bkp=False):
    sqldb, sqluser, sqlpass, sqlserver = loadSQLconfig(bkp=bkp)
    conn = pymysql.connect(host=sqlserver, user=sqluser, password=sqlpass, db=sqldb)
    cur = conn.cursor()
    evtdt = datetime.datetime.strptime(bmpdata['time'], '%Y-%m-%dT%H:%M:%SZ')

    result = cur.execute('select press_rel, apressure from wh1080data where press_rel is not null order by time desc limit 1')
    lastdata = cur.fetchone()
    if lastdata:
        # TODO - check for unrealistic wind and pressure changes. 
        # pressure change > 10 hPa is very implausible, as is a value outside the range 950-1080
        prevpress = lastdata[0]
        prevapress = lastdata[1]
        pressdiff = abs(bmpdata['press_rel'] - prevpress)
        if bmpdata['press_rel'] < 900 or bmpdata['press_rel'] > 1100 or pressdiff > 10:
            bmpdata['press_rel'] = prevpress
            bmpdata['apressure'] = prevapress

    sql = "INSERT INTO wh1080data (time, timestamp, humidity_in, temp_c_in, press_rel, apressure, year, month, day) "\
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    vals = (bmpdata['time'], evtdt.strftime('%Y-%m-%d %H:%M:%S'), bmpdata['humidity_in'], bmpdata['temp_c_in'],
            bmpdata['press_rel'], bmpdata['apressure'], evtdt.year, evtdt.month, evtdt.day)
    result = cur.execute(sql, vals)

    if result != 1:
        writeLogEntry(logdir, 'unable to write to mysql table\n')
    else:
        writeLogEntry(logdir, f'wrote {bmpdata} to {sqlserver}\n')
        
    conn.commit()
    conn.close()
    return


# The MQTT callback function. It will be triggered when trying to connect to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print("Connected fail with code", rc)


# the MQ publish function
def on_publish(client, userdata, result):
    #print('data published - {}'.format(result))
    return


def sendDataToMQTT(data, logdir):
    broker, mqport, username, password = readConfig()
    client = mqtt.Client('bmp280_fwd')
    client.on_connect = on_connect
    client.on_publish = on_publish
    if username != '':
        client.username_pw_set(username, password)
    client.connect(broker, mqport, 60)
    try:
        for ele in data:
            topic = f'sensors/bmp280/{ele}'
            ret = client.publish(topic, payload=data[ele], qos=0, retain=False)
    except:
        writeLogEntry(logdir, f'problem sending {ele} value {data[ele]}\n')
    writeLogEntry(logdir, f'sent {data}\n')
    return ret


def getTempPressHum(prvdata = None):
    try:
        data = bme280.read_all()
        humidity, pressure, cTemp = data
    except:
        print('unable to connect to bmp280, check for loose wires')
        humidity = prvdata['hum_in']
        cTemp = prvdata['temp_c_in']
        pressure = prvdata['press_rel']
    if prvdata:
        if abs(cTemp - prvdata['temp_c_in']) > 5:
            writeLogEntry(logdir, f'temp diff too big - {cTemp} to {prvdata["temp_c_in"]}')
            cTemp = prvdata['temp_c_in']
    cpressure = correctForAltitude(pressure, cTemp, stationAltitude())
    now = datetime.datetime.utcnow().isoformat()[:19]+'Z'
    return {'temp_c_in': round(cTemp,4), 'press_rel': round(cpressure,4), 'humidity_in': round(humidity,4), 'time': now, 
            'apressure': round(pressure,4)}



def correctForAltitude(press, temp, alti):
    denom = temp + 273.15 + 0.0065 * alti
    val = (1 - (0.0065 * alti)/denom)
    press_sl = press * pow(val, -5.257)
    return round(press_sl,4)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        outdir = './maplinstn'
        logdir = './logs'
        stopfile = './stopbmp280' # to allow a clean stop from systemd
    else:
        outdir = os.path.join(sys.argv[1], 'maplinstn')
        logdir = os.path.join(sys.argv[1], 'logs')
        stopfile = os.path.join(sys.argv[1], 'stopbmp280')
    runme = True
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(logdir, exist_ok=True)
    if os.path.exists(stopfile):
        os.remove(stopfile)
    outfname = os.path.join(outdir,'bmp280.json')
    bme280_i2c.set_default_i2c_address(0x76)
    bme280_i2c.set_default_bus(1)
    prvdata = None
    try:
        bme280.setup()
        while runme is True:
            data = getTempPressHum(prvdata)
            if os.path.isfile(outfname):
                currdata = json.loads(open(outfname).read())
            else:
                currdata = {}
            dtstamp = datetime.datetime.strptime(data['time'], '%Y-%m-%dT%H:%M:%SZ').timestamp()
            currdata[dtstamp] = data
            with open(outfname, 'w') as outf:
                json.dump(currdata, outf)
            sendDataToMQTT(data, logdir)
            postToMySQL(data, logdir)
            postToMySQL(data, logdir, bkp=True)
            prvdata = data
            time.sleep(60)
            if os.path.isfile(stopfile):
                writeLogEntry(logdir, 'Exiting...\n==========\n')
                os.remove(stopfile)
                runme = False
                break
    except OSError:
        writeLogEntry(logdir, 'unable to connect to bmp280, check wiring\n')
        print('unable to connect to bmp280, check wiring\n')
