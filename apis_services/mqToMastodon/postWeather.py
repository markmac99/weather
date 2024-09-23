#
# Read from MQTT and post to Mastodon
#

from mastodon import Mastodon
import paho.mqtt.client as mqtt
import os
import time
import json
from mqConfig import readConfig

done = 0

MSTOMPH = 2.237


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print("Connected fail with code", rc)


def on_message(client, userdata, message):
    decmsg = json.loads(message.payload.decode("utf-8"))
    #print("received ", decmsg)
    if os.path.isfile('press.txt'):
        lis = open('press.txt', 'r').readlines()
        lastpress = float(lis[0].strip())
        try:
            press = float(decmsg["pressure"])
        except Exception:
            press = 1000
        if lastpress - press > 1:
            trend = 'falling'
        if lastpress - press > 0.1:
            trend = 'falling slowly'
        elif lastpress - press < -1:
            trend = 'rising'
        elif lastpress - press < -0.1:
            trend = 'rising slowly'
        else:
            trend = 'steady'
    else:
        trend = 'steady'
        try:
            lastpress = decmsg["pressure"]
        except Exception:
            lastpress = 1012.632
            press = lastpress
    with open('press.txt', 'w') as outf:
        outf.write(f'{lastpress}\n')
    dtutc = decmsg["obsTimeUtc"]
    wind_ave_mph = decmsg['windSpeed'] * MSTOMPH
    wind_gust_mph = decmsg['windGust'] * MSTOMPH
    winddir = decmsg["windDir"]
    rain_hr = decmsg['precipTotal']
    tempval = decmsg['outsideTemp']
    feelslike = decmsg['feels_like']

    msg = f'Tackley Weather {dtutc} GMT: Temp: {tempval} C, feels like {feelslike} C, '  \
        f'Wind: {winddir}, {wind_ave_mph} mph (ave), {wind_gust_mph} mph (gust), ' \
        f'Humidity: {decmsg["humidity"]}%, Rain (daily) {rain_hr} mm, '\
        f'Press: {press} hPa, {trend}'
    print(msg)

    try:
        tokfile = os.path.expanduser('~/.ssh/mastodon_token.secret')
        mstdn = Mastodon(access_token=tokfile, api_base_url='https://botsin.space/')
        mstdn.status_post(msg)
        global done 
        done = 1
    except Exception as e:
        print('problem connecting to mastodon')
        print(e)


if __name__ == '__main__':
    mqbroker, mqport, mquser, mqpass = readConfig()
    client = mqtt.Client('weather_reporter')
    client.on_connect = on_connect
    client.on_message = on_message
    if mquser != '':
        client.username_pw_set(mquser, mqpass)
    try:
        client.connect(mqbroker, mqport, 60)
        client.subscribe('sensors/bresser_wu')
        client.loop_start()
        while done == 0:
            print('waiting...')
            time.sleep(5)
        client.loop_stop()
    except Exception as e:
        print('problem connecting to mqtt broker')
        print(e)
