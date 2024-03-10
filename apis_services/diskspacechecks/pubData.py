#!/bin/bash

# copyright Mark McIntyre, 2023-

import datetime
import os
import paho.mqtt.client as mqtt
import paramiko


from mqConfig import readConfig, hostnames


def getDF(hn, logdir):
    dfpct = 0
    config=paramiko.config.SSHConfig.from_path(os.path.expanduser('~/.ssh/config'))
    sitecfg = config.lookup(hn)
    if 'user' not in sitecfg.keys():
        writeLogEntry(logdir, f'unable to connect to {hn} - no entry in ssh config file')
        return False
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    pkey = paramiko.RSAKey.from_private_key_file(sitecfg['identityfile'][0])
    # print(sitecfg)
    try:
        ssh_client.connect(sitecfg['hostname'], username=sitecfg['user'], pkey=pkey, look_for_keys=False, timeout=10)
        stdin, stdout, stderr = ssh_client.exec_command('df .')
        res = stdout.readlines()
        sizedata = res[1].split()
        tot = float(sizedata[1])
        used = float(sizedata[2])
        writeLogEntry(logdir, f'{tot}, {used}, {used/tot*100.0}')
        dfpct = used/tot
    except Exception:
        writeLogEntry(logdir, f'connection to {sitecfg["hostname"]} failed')
        dfpct = False
    ssh_client.close()
    return dfpct


def writeLogEntry(logdir, msg):
    with open(os.path.join(logdir, 'dscheck.log'), mode='a+', encoding='utf-8') as f:
        nowdt = datetime.datetime.now().isoformat()
        f.write(f'{nowdt}: {msg}\n')


# The MQTT callback function. It will be triggered when trying to connect to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print("Connected fail with code", rc)


# the MQ publish function
def on_publish(client, userdata, result,x,y):
    #print('data published - {}'.format(result))
    return


def sendDataToMQTT(data, hn, logdir):
    broker, mqport = readConfig()
    if broker == 'someserver.net': # not deployed
        broker='wxsatpi'
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id='dschecks')
    client.on_connect = on_connect
    client.on_publish = on_publish
    try:
        client.connect(broker, mqport, 60)
        if hn == 'calcserver':
            hn = 'ukmcalcserver'
        topic = f'servers/{hn}/pctused'
        print(hn, round(data, 2))
        ret = client.publish(topic, payload=round(data,2), qos=0, retain=False)
        writeLogEntry(logdir, f'sent {data}\n')
    except:
        writeLogEntry(logdir, f'send {data} failed\n')
        ret = False
    return ret


if __name__ == '__main__':
    logdir = os.path.expanduser('~/logs')
    os.makedirs(logdir, exist_ok=True)
    hosts = hostnames()
    for hn in hosts:
        dfpct = getDF(hn, logdir)
        if dfpct: 
            sendDataToMQTT(round(dfpct*100,2), hn, logdir)
