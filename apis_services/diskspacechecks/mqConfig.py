# Copyright (c) Mark McIntyre, 2023-


def readConfig(test=False):
    if test:
        from testConfig import broker, username, mqport, passwd
    else:        
        broker = 'someserver.net'
        username = 'mquser'
        passwd = 'mqpass'
        mqport = 1883
    return broker, mqport, username, passwd


def hostnames():
    hn = ['wordpresssite','ukmonhelper2.','calcserver.']
    return hn
