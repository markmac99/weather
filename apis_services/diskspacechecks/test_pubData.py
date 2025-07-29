# copyright Mark McIntyre, 29024-

# tests 

import os
from pubData import getDF, sendDataToMQTT
from mqConfig import hostnames, readConfig

logdir = './logs'
os.makedirs(logdir, exist_ok=True)


def test_getDF():
    hn = hostnames()[0]
    dfpct = getDF(hn, logdir)
    print(dfpct)
    assert dfpct is not False


def test_hostnames():
    x = hostnames()
    assert x[0]=='wordpresssite'


def test_readConfig():
    brok, por, us, pw = readConfig(test=True)
    assert por==1883
    assert brok=='wxsatpi'


def test_pub():
    res = sendDataToMQTT(45.345, 'test', '.')
    assert res
