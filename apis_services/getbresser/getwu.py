"""
New script to collect data from WeatherUnderground

"""
import requests
import json
import time
import datetime
from openhab import OpenHAB
import os
import paho.mqtt.client as mqtt

from mqConfig import readConfig
from wuconfig import stationid, getWUkey, getOpenhabURL


LOG_DIRECTORY = os.getenv('LOGDIR', default=os.path.expanduser('~/logs'))
STOPFILE = './stopgetwu'
MAX_RETRIES = 20
SLEEP_TIME = 60 # wunderground limits you to 1500 requests per day = 1 per min


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


def sendDataToMQTT(data):
    broker, mqport, mquser, mqpass = readConfig()
    client = mqtt.Client('bresser_wu')
    client.on_connect = on_connect
    client.on_publish = on_publish
    if mquser != '':
        client.username_pw_set(mquser, mqpass)
    client.connect(broker, mqport, 60)
    topic = f'sensors/bresser_wu/{data[0]}'
    ret = client.publish(topic, payload=data[1], qos=0, retain=False)
    return ret


def sendAllDataToMQTTParent(data):
    broker, mqport, mquser, mqpass = readConfig()
    client = mqtt.Client('bresser_wu')
    client.on_connect = on_connect
    client.on_publish = on_publish
    if mquser != '':
        client.username_pw_set(mquser, mqpass)
    client.connect(broker, mqport, 60)
    topic = 'sensors/bresser_wu'
    ret = client.publish(topic, payload=data, qos=0, retain=False)
    return ret


def writeLogEntry(msg):
    with open(LOG_DIRECTORY+"/getwu.log", mode='a+', encoding='utf-8') as f:
        f.write(msg + '\n')


def correctForAltitude(press, temp, alti):
    denom = temp + 273.15 + 0.0065 * alti
    val = (1 - (0.0065 * alti)/denom)
    press_sl = press * pow(val, -5.257)
    return press_sl


def getDataFromWU():
    baseurl = 'https://api.weather.com/v2/pws/observations/current?'
    wukey = getWUkey()
    url = f'{baseurl}stationId={stationid}&format=json&units=m&apiKey={wukey}&numericPrecision=decimal'
    r = requests.get(url)
    if r.status_code != 200:
        # Not successful. Assume Authentication Error
        writeLogEntry(f'Request Status Error: {str(r.status_code)}')
        return False
    data_dict = json.loads(r.text)['observations'][0]
    dtutc = data_dict['obsTimeUtc']
    solrad = data_dict['solarRadiation']
    windir = data_dict['winddir']
    humid = data_dict['humidity']
    uvidx = data_dict['uv']
    evt_time = datetime.datetime.strptime(dtutc, '%Y-%m-%dT%H:%M:%SZ')

    metdata = data_dict['metric']
    temp = metdata['temp']
    heatIndex = metdata['heatIndex']
    dewpt = metdata['dewpt']
    windChill = metdata['windChill']
    windSpeed = metdata['windSpeed']
    windGust = metdata['windGust']
    pressure = metdata['pressure']
    precipRate = metdata['precipRate']
    precipTotal = metdata['precipTotal']
    elev = metdata['elev']
    lati = data_dict['lat']
    lngi = data_dict['lon']

    #pressure = round(correctForAltitude(pressure, temp, 80),3) not needed

    if temp > 21.1111: # 70F
        feels_like = heatIndex
    elif temp < 16.1111: # 61
        feels_like = windChill
    else:
        feels_like = temp

    writeLogEntry(f'{evt_time},{temp}, {feels_like}, {pressure}, {windSpeed}, {windGust},' 
        f'{windir}, {humid}, {uvidx}, {solrad}, {dewpt}, {precipRate},{precipTotal}')

    # update openhab
    openhab = OpenHAB(getOpenhabURL())
    if openhab:
        OutsideTemp = openhab.get_item('OutsideTemp_wubr')
        FeelsLike = openhab.get_item('OutsideFeelsLike_wubr')
        RelPressure = openhab.get_item('RelPressure2')
        OutsideTemp.state = temp
        FeelsLike.state = feels_like
        RelPressure.state = pressure
    else:
        writeLogEntry('problem connecting to openhab')

    sendDataToMQTT(['outsideTemp', temp])
    sendDataToMQTT(['feels_like', feels_like])
    sendDataToMQTT(['pressure', pressure])
    sendDataToMQTT(['precipTotal', precipTotal])
    sendDataToMQTT(['precipRate', precipRate])
    sendDataToMQTT(['windGust', windGust])
    sendDataToMQTT(['windSpeed', windSpeed])
    sendDataToMQTT(['windDir', windir])
    sendDataToMQTT(['dewPoint', dewpt])
    sendDataToMQTT(['humidity', humid])
    sendDataToMQTT(['UVidx', uvidx])
    sendDataToMQTT(['solarRadiation', solrad])

    sendDataToMQTT(['obsTimeUtc', dtutc])
    sendDataToMQTT(['lat', lati])
    sendDataToMQTT(['lng', lngi])
    sendDataToMQTT(['ele', elev])

    alldata = {"outsideTemp": temp, "feels_like": feels_like, "pressure": pressure, "precipTotal": precipTotal,
                "precipRate": precipRate, "windGust": windGust, "windSpeed": windSpeed, "windDir": windir,
                "dewPoint": dewpt, "humidity": humid, "UVIdx": uvidx, "solarRadiation": solrad, "obsTimeUtc": dtutc}
    writeLogEntry('sending all data')
    sendAllDataToMQTTParent(json.dumps(alldata))

    return True


if __name__ == '__main__':
    writeLogEntry('========\nStarting...')
    os.makedirs(LOG_DIRECTORY, exist_ok=True)
    runme = True
    while runme is True:
        getDataFromWU()
        time.sleep(SLEEP_TIME)
        if os.path.isfile(STOPFILE):
            writeLogEntry('Exiting...')
            os.remove(STOPFILE)
            runme = False
            break
