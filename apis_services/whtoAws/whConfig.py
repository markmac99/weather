# 
# copyright 2023 mark mcintyre
# 
# edit this file to reflect the location of the files created by rtl_433 and readbmp280
# and the location of the file that will be read by the dummy USB driver for pywws

import os


def loadConfig():
    whfile = 'weatherdata.json'
    bpfile = 'bmp280.json'
    targfile = 'weatherdata.json' 
    localdir = '~/weather/maplinstn'
    remotedir = 'wordpresssite:weather/upload/'
    whfile = os.path.join(os.path.expanduser(localdir), whfile)
    bpfile = os.path.join(os.path.expanduser(localdir), bpfile)
    targfile = os.path.join(os.path.expanduser(localdir), '..', targfile)
    return whfile, bpfile, targfile, remotedir


def loadHistConfig():
    whfile = 'weatherdata.json'
    bpfile = 'bmp280.json'
    targfile = 'newdata.parquet' 
    localdir = '~/weather/maplinstn'
    remotedir = 'wordpresssite:weather/tmp/'
    whfile = os.path.join(os.path.expanduser(localdir), whfile)
    bpfile = os.path.join(os.path.expanduser(localdir), bpfile)
    targfile = os.path.join(os.path.expanduser(localdir), '..', targfile)
    return whfile, bpfile, targfile, remotedir
