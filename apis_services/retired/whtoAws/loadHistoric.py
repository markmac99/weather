# 
# copyright 2023- Mark McIntyre
#
# This script consumes data from rtl_433 and from my service to read data from a BMP/BME280
# and writes it out into a single-line json file to be consumed by my dummy driver for pywws
# and is also pushed to my AWS server

# The locations of the source files and target file are defined in whConfig

import json 
import paramiko
from scp import SCPClient
import os
import sys
import datetime
import pandas as pd
import numpy as np

from whConfig import loadHistConfig


def loadOneDay(whfile, bpfile, lastwhdata=None, lastbpdata=None):
    whdata = None
    bpdata = None
    try:
        whdata = open(whfile, 'r').readlines()
    except:
        whdata = lastwhdata
    try:
        bpdata = open(bpfile, 'r').readlines()
    except:
        bpdata = lastbpdata

    if len(whdata) == 0:
        whdata = lastwhdata
    if len(bpdata) == 0:
        bpdata = lastbpdata
    jsd = ''
    for li in whdata:
        jsd = jsd + li.strip() + ','
    jsd = '[' + jsd[:-1] + ']'
    whdf = pd.DataFrame(json.loads(jsd))
    whdf.set_index(['time'], inplace=True)
    whdf.drop_duplicates(inplace=True)
    whdf['timestamp']=[datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S').replace(tzinfo=datetime.timezone.utc) for v in whdf.index]
    
    jsd = ''
    for li in bpdata:
        jsd = jsd + li.strip() + ','
    jsd = '[' + jsd[:-1] + ']'
    bpdf = pd.DataFrame(json.loads(jsd))
    bpdf.set_index(['time'], inplace=True)
    bpdf.drop_duplicates(inplace=True)
    bpdf['timestamp']=[datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc) for v in bpdf.index]

    whdf['humidity_in'] = np.interp(x=whdf.timestamp, xp=bpdf.timestamp, fp=bpdf.humidity_in)
    whdf['temp_c_in'] = np.interp(x=whdf.timestamp, xp=bpdf.timestamp, fp=bpdf.temp_c_in)
    whdf['press_rel'] = np.interp(x=whdf.timestamp, xp=bpdf.timestamp, fp=bpdf.press_rel)
    whdf['apressure'] = np.interp(x=whdf.timestamp, xp=bpdf.timestamp, fp=bpdf.apressure)

    whdf['year'] = [v.year for v in whdf.timestamp]
    whdf['month'] = [v.month for v in whdf.timestamp]
    whdf['day'] = [v.day for v in whdf.timestamp]

    whdf['rainchg'] = whdf.rain_mm.diff().fillna(0)
    whdf.loc[whdf.rainchg < -0.31, ['rainchg']] = 0
    return whdf, whdata, bpdata


def loadAndSave(origwhfile, origbpfile, targfile, startdt=None, enddt=None):
    today = datetime.datetime.now().replace(hour=0).replace(minute=0).replace(second=0).replace(microsecond=0)
    if enddt is None:
        enddt = datetime.datetime.now()
    if startdt is not None:
        d1 = startdt.replace(hour=0).replace(minute=0).replace(second=0).replace(microsecond=0)
        d2 = enddt.replace(hour=0).replace(minute=0).replace(second=0).replace(microsecond=0)
        numdays = (d2 - d1).days + 1
        whdf = None
        finished = False
        lastbpdata = None
        lastwhdata = None
        for step in range(numdays):
            thisdt = d1 + datetime.timedelta(days=step)
            print('processing', thisdt.strftime('%Y-%m-%d'))
            if thisdt != today:
                whfile = f'{origwhfile}.{thisdt.strftime("%Y%m%d")}'
                bpfile = f'{origbpfile}.{thisdt.strftime("%Y%m%d")}'
            else: 
                whfile = origwhfile
                bpfile = origbpfile
            if whdf is None:
                whdf, lastwhdata, lastbpdata = loadOneDay(whfile, bpfile)
            else:
                newdf, lastwhdata, lastbpdata = loadOneDay(whfile, bpfile, lastwhdata, lastbpdata)
                whdf = pd.concat([whdf,newdf])
            if finished: 
                whdf = whdf[whdf.timestamp >= startdt.timestamp]
                whdf = whdf[whdf.timestamp <= enddt.timestamp]
                break

    else:
        whdf = loadOneDay(whfile, bpfile)
    whdf.to_parquet(targfile)


def uploadFile(fname, remotedir):
    hn, pth = remotedir.split(':')
    config=paramiko.config.SSHConfig.from_path(os.path.expanduser('~/.ssh/config'))
    sitecfg = config.lookup(hn)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    pkey = paramiko.RSAKey.from_private_key_file(os.path.expanduser(sitecfg['identityfile'][0])) 
    for ret in range(10):
        try:
            c.connect(sitecfg['hostname'], username=sitecfg['user'], pkey=pkey, look_for_keys=False)
            scpcli = SCPClient(c.get_transport())
            scpcli.put(fname, os.path.join(pth, os.path.split(fname)[1]))
            scpcli.close()
            c.close()
        except:
            print('connection failed, retrying')
    return


if __name__ == '__main__':
    whfile, bpfile, targfile, remotedir = loadHistConfig()
    startdt = None
    enddt = None
    if len(sys.argv)> 2:
        startdt = datetime.datetime.strptime(sys.argv[1],'%Y-%m-%dT%H:%M:%SZ')
        enddt = datetime.datetime.now()
    if len(sys.argv)> 3:
        enddt = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%dT%H:%M:%SZ')

    print('processing', startdt, enddt)
    loadAndSave(whfile, bpfile, targfile, startdt, enddt)
    if len(targfile) > 5:
        uploadFile(targfile, remotedir)
