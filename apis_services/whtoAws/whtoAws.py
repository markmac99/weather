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
import time
import logging
from logging.handlers import RotatingFileHandler

from whConfig import loadConfig
from sqlInterface import postToMySQL

log = logging.getLogger('LOGNAME')


def loadAndSave(whfile, bpfile, targfile):
    if os.path.isfile(targfile):
        lis = open(targfile,'r').readlines()
        if len(lis) > 0:
            origdata = json.loads(lis[-1])
        else:
            origdata = {}
            
    if os.path.isfile(whfile):
        lis = json.loads(open(whfile).read())
        if len(lis) > 0:
            whdata = lis[max(lis.keys())]
            origdata.update(whdata)

    if os.path.isfile(bpfile):
        lis = json.loads(open(bpfile).read())
        if len(lis) > 0:
            bpdata = lis[max(lis.keys())]
            origdata.update(bpdata)
            
    if len(origdata) > 0:
        if ' ' in origdata['time']:
            origdata['time'] = origdata['time'].replace(' ','T')
        if 'Z' not in origdata['time']:
            origdata['time'] = origdata['time']+'Z'
        with open(targfile,'w') as outf:
            outf.write(f'{json.dumps(origdata)}')
    return


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
    whfile, bpfile, targfile, remotedir, localdir, intvl = loadConfig()

    log.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    fh = RotatingFileHandler(os.path.expanduser(os.path.join(localdir,'logs/LOGNAME.log')), maxBytes=51200, backupCount=10)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    if os.path.isfile(os.path.join(localdir, 'stopwhtoaws')):
        os.remove(os.path.join(localdir, 'stopwhtoaws'))

    lastwh = None
    lastbp = None
    runme = True
    log.info('starting')
    while runme is True:
        loadAndSave(whfile, bpfile, targfile)
        if len(targfile) > 5:
            #uploadFile(targfile, remotedir)
            try:
                postToMySQL(targfile)
                log.info('saved to primary database')
            except Exception as e:
                log.warning('failed to update mysql')
                log.warning(e)
            try:
                postToMySQL(targfile, bkp=True)
                log.info('saved to backup database')
            except Exception as e:
                log.warning('failed to update mysql 2nd db')
                log.warning(e)
        if os.path.isfile(os.path.join(localdir, 'stopwhtoaws')):
            os.remove(os.path.join(localdir, 'stopwhtoaws'))
            log.info('quitting')
            runme = False
        else:
            time.sleep(60*intvl)
