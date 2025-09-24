# python code to read WH1080 data from MQ, write it to a  JSON file, then 
# post some additional values back to MQ


import os
import json
import sys
from paho.mqtt import client as mqtt_client

from mqConfig import readConfig
from weatherCalcs import correctBadData, dewPoint, windChill, heatIndex
import logging
import logging.handlers

broker, mqport, username, password = readConfig()

datadir = '/home/pi/weather/maplinstn'

topicroot = 'sensors/rtl_433_2/P32/C0'
topics = ['time','battery_ok','temperature_C','humidity','wind_dir_deg','wind_avg_km_h','wind_max_km_h','rain_mm']
client_id = 'wh1080_aug'

msgcount = 0

jsonmsg = {'time' :None, 'model' : 'Fineoffset-WHx080', 'subtype' : 0, 'id' : 251,
           'battery_ok':None,'temperature_C':None,'humidity':None,
           'wind_dir_deg':None,'wind_avg_km_h':None,'wind_max_km_h':None,'rain_mm':None,
           'mic':'CRC'}

log = logging.getLogger()
log.setLevel(logging.INFO)


def setupLogging(logpath):
    print('about to initialise logger')
    logdir = os.path.expanduser(logpath)
    os.makedirs(logdir, exist_ok=True)

    logfilename = os.path.join(logdir, 'wh1080_mq.log')
    handler = logging.handlers.TimedRotatingFileHandler(logfilename, when='D', interval=1) 
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


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            log.info("Connected to MQTT Broker!")
        else:
            log.error("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.username_pw_set(username, password)
    client.connect(broker, mqport)
    return client

def on_publish(client, userdata, result):
    return 


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
    
    msgcount += 1
    if msgcount > 7 and jsonmsg['time'] != lasttime: 
        log.info(jsonmsg)
        if os.path.isfile(os.path.join(datadir, 'weatherdata.json')):
            currdata = open(os.path.join(datadir, 'weatherdata.json'), 'r').readlines()
        else:
            currdata = []
        currdata = [x for x in currdata if len(x) > 1]
        currdata.append(json.dumps(jsonmsg)+'\n')
        open(os.path.join(datadir, 'weatherdata.json'), 'w').writelines(currdata)
        t = float(jsonmsg['temperature_C'])
        rh = float(jsonmsg['humidity'])
        v = float(jsonmsg['wind_avg_km_h'])
        ret = client.publish(f'{topicroot}/dew_point', payload=dewPoint(t, rh), qos=0, retain=False)
        wc = windChill(t, v)
        hi = heatIndex(t, rh)
        fl = t
        if wc < t:
            fl = wc
        elif t > 26 and hi > t:
            fl = hi
        ret = client.publish(f'{topicroot}/feals_like', payload=fl, qos=0, retain=False)
        msgcount = 0
        stopfile = os.path.join(datadir, 'stopwhfwd')
        if os.path.isfile(stopfile):
            log.info('stopping')
            os.remove(stopfile)
            exit(0)


def subscribe(client: mqtt_client):
    for topic in topics:
        client.subscribe(f'{topicroot}/{topic}')
    client.on_message = on_message
    client.on_publish = on_publish


def run(dd):
    global datadir
    datadir = dd
    log.info('connecting to MQ')
    client = connect_mqtt()
    log.info('subscribing')
    subscribe(client)
    log.info('looping')
    client.loop_forever()


if __name__ == '__main__':
    setupLogging(sys.argv[2])
    run(sys.argv[1])
