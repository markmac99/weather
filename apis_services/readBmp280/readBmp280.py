#!/bin/bash

# copyright Mark McIntyre, 2023-

import time
import datetime
import os
import sys
import json
import paho.mqtt.client as mqtt

from mqConfig import readConfig, stationAltitude

from bme280 import bme280, bme280_i2c


def writeLogEntry(logdir, msg):
    with open(os.path.join(logdir, "bmp280.log"), mode='a+', encoding='utf-8') as f:
        nowdt = datetime.datetime.now(datetime.timezone.utc).isoformat()
        f.write(f'{nowdt}: {msg}')


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
            with open(outfname, 'a+') as outf:
                outf.write(json.dumps(data) + '\n')
            sendDataToMQTT(data, logdir)
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
