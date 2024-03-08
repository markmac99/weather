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
import datetime

from whConfig import loadConfig


def loadAndSave(whfile, bpfile, targfile):
    whdata = None
    bpdata = None
    try:
        lis = open(whfile, 'r').readlines()
        whdata = json.loads(lis[-1])
    except Exception:
        pass
    try:
        lis = open(bpfile, 'r').readlines()
        bpdata = json.loads(lis[-1])
    except Exception:
        pass
    #print(whdata, bpdata)
    if whdata and bpdata:
        whdata.update(bpdata)
        #print(whdata)
        with open(targfile,'w') as outf:
            outf.write('{}'.format(json.dumps(whdata)))


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
    whfile, bpfile, targfile, remotedir = loadConfig()
    runme = True
    print('running at', datetime.datetime.now().strftime('%Y%m%d-%H%M%S.%f'))
    loadAndSave(whfile, bpfile, targfile)
    if len(targfile) > 5:
        uploadFile(targfile, remotedir)
