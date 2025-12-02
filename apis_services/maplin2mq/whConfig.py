# 
# copyright 2023 mark mcintyre
# 
# edit this file to reflect the location of the files created by rtl_433 and readbmp280
# and the location of the file that will be read by the dummy USB driver for pywws

def loadSQLconfig(bkp=False):
    sqldb = 'weather'
    sqluser = 'wh1080'
    sqlpass = 'redacted'
    if bkp is True:
        sqlserver = 'BACKUPDB'
    else:
        sqlserver = 'PRIMARYDB'
    return sqldb, sqluser, sqlpass, sqlserver


def getLogDir():
    return '~/weather/logs'
