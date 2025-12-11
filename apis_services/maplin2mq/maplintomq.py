# python code to read WH1080 data from MQ, write it to a  JSON file, then 
# post some additional values back to MQ

# copyright Mark McIntyre, 2024

import os
import sys
from paho.mqtt import client as mqtt_client
import datetime
import pymysql
import logging
import logging.handlers

from whConfig import loadSQLconfig, getLogDir
from mqConfig import readConfig
from weatherCalcs import dewPoint, windChill, heatIndex


topicroot = 'sensors/rtl_433_2/P32/C0'
topics = ['time','battery_ok','temperature_C','humidity','wind_dir_deg','wind_avg_km_h','wind_max_km_h','rain_mm']
client_id = 'wh1080_aug'

msgcount = 0

jsonmsg = {'time':None, 'model': 'Fineoffset-WHx080', 'subtype': 0, 'id': 251,
           'battery_ok':None,'temperature_C':None,'humidity':None,
           'wind_dir_deg':None,'wind_avg_km_h':None,'wind_max_km_h':None,'rain_mm':None,
           'mic':'CRC'}

log = logging.getLogger()
log.setLevel(logging.INFO)


def setupLogging():
    print('about to initialise logger')
    logdir = os.path.expanduser(getLogDir())
    os.makedirs(logdir, exist_ok=True)

    logfilename = os.path.join(logdir, 'maplin2mq.log')
    handler = logging.handlers.TimedRotatingFileHandler(logfilename, when='midnight', interval=1) 
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt='%(asctime)s-%(levelname)s-%(module)s-line:%(lineno)d - %(message)s', 
        datefmt='%Y/%m/%d %H:%M:%S')
    handler.setFormatter(formatter)
    log.addHandler(handler)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.WARNING)
    formatter = logging.Formatter(fmt='%(asctime)s-%(levelname)s-%(module)s-line:%(lineno)d - %(message)s', 
        datefmt='%Y/%m/%d %H:%M:%S')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.setLevel(logging.INFO)

    log.info('logging initialised')
    return 


def postToMySQL(whdata, usebkp=False):
    sqldb, sqluser, sqlpass, sqlserver = loadSQLconfig(bkp=usebkp)
    # don't do anything if the SQLserver isn't configured
    if sqlserver == 'NONE':
        return 
    try:
        conn = pymysql.connect(host=sqlserver, user=sqluser, password=sqlpass, db=sqldb)
        cur = conn.cursor()
        evtdt = datetime.datetime.strptime(whdata['time'], '%Y-%m-%d %H:%M:%S')

        # get previous rain and work out change
        result = cur.execute('select rain_mm, temperature_C, press_rel, apressure, wind_avg_km_h, wind_max_km_h from wh1080data where temperature_C is not null order by time desc limit 1')
        lastdata = cur.fetchone()
        if 'rainchg' not in whdata:
            whdata['rainchg'] = 0
        if lastdata:
            prevrain = lastdata[0]
            rainchg = whdata['rain_mm'] - prevrain

            # ignore unrealistic changes
            if rainchg > -0.31 and rainchg < 50:
                whdata['rainchg'] = rainchg

            # check for unrealistic temperature movements    
            prevtempc = lastdata[1]
            if whdata['temperature_C'] > 55 or whdata['temperature_C'] < -30 or abs(prevtempc - whdata['temperature_C']) > 10:
                whdata['temperature_C'] = prevtempc

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
            "timestamp, rainchg, year, month, day) "\
            "VALUES (%s, %s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s, %s,%s, %s,%s, %s)"

        vals = (evtdt.strftime('%Y-%m-%dT%H:%M:%SZ'), whdata['model'], whdata['subtype'], whdata['id'], whdata['battery_ok'], whdata['temperature_C'], whdata['humidity'],
            whdata['wind_dir_deg'], whdata['wind_avg_km_h'], whdata['wind_max_km_h'], whdata['rain_mm'], whdata['mic'],
            evtdt.strftime('%Y-%m-%d %H:%M:%S'), whdata['rainchg'], evtdt.year, evtdt.month, evtdt.day)

        result = cur.execute(sql, vals)

        if result != 1:
            log.info('unable to write to mysql table')
        else:
            log.info(f'wrote {whdata} to {sqlserver}')
            
        conn.commit()
        conn.close()
    except Exception as e:
        log.warning(f'unable to connect to SQLserver {e}')
    return


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log.info("Connected to MQTT Broker!")
        for topic in topics:
            log.info(f'subscribing to {topicroot}/{topic}')
            client.subscribe(f'{topicroot}/{topic}')
    else:
        log.error("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    global msgcount
    thistopic = msg.topic.split('/')[-1]
    lasttime = jsonmsg['time']
    if thistopic == 'time':
        jsonmsg[thistopic] = msg.payload.decode().replace('T', ' ')
    elif thistopic not in ['time', 'mic', 'model', 'subtype', 'id', 'battery_ok']:
        jsonmsg[thistopic] = float(msg.payload.decode())
    elif thistopic in ['subtype', 'id', 'battery_ok']:
        jsonmsg[thistopic] = int(msg.payload.decode())
    else:
        jsonmsg[thistopic] = msg.payload.decode()
    log.info(f'received {jsonmsg[thistopic]}')
    msgcount += 1
    if msgcount > 7 and jsonmsg['time'] != lasttime: 
        log.info(f'processing {jsonmsg}')
        postToMySQL(jsonmsg)
        postToMySQL(jsonmsg, usebkp=True)

        # now add extra data to MQ
        log.info('calculating the additional data')
        t = float(jsonmsg['temperature_C'])
        rh = float(jsonmsg['humidity'])
        v = float(jsonmsg['wind_avg_km_h'])
        client.publish(f'{topicroot}/dew_point', payload=dewPoint(t, rh), qos=0, retain=True)
        wc = windChill(t, v)
        hi = heatIndex(t, rh)
        fl = t
        if wc < t:
            fl = wc
        elif t > 26 and hi > t:
            fl = hi
        client.publish(f'{topicroot}/feals_like', payload=fl, qos=0, retain=True)
        msgcount = 0
        stopfile = os.path.join(os.getenv('TMP', default='/tmp'), 'stopwhfwd')
        if os.path.isfile(stopfile):
            log.info('stopping')
            os.remove(stopfile)
            exit(0)


if __name__ == '__main__':
    setupLogging()
    log.info('connecting to MQ')
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    broker, mqport, username, password = readConfig()
    client.username_pw_set(username, password)
    client.connect(broker, mqport)

    log.info('looping')
    client.loop_forever()
