import sqlalchemy
import pandas as pd
import datetime
import pymysql
from dateutil.relativedelta import relativedelta


sqldb = 'weather'
sqluser = 'wh1080'
sqlserver = 'localhost'


def loadDfFromDB(days=None, startdt=None, enddt=None, pressdata=False):
    cnx = sqlalchemy.create_engine(f'mysql+pymysql://{sqluser}:redacted@{sqlserver}:3306/{sqldb}')
    if not pressdata:
        if days:
            refdt = datetime.datetime.now() + datetime.timedelta(days = -(days+1))
            df = pd.read_sql("select time,timestamp,temperature_C,humidity,rain_mm," 
                            "press_rel,wind_max_km_h,wind_avg_km_h,temp_c_in,wind_dir_deg,humidity_in," 
                            f"rainchg,apressure from wh1080data where time > '{refdt}' and temperature_C is not null", cnx)
        elif startdt and enddt:
            df = pd.read_sql("select time,timestamp,temperature_C,humidity,rain_mm," 
                            "press_rel,wind_max_km_h,wind_avg_km_h,temp_c_in,wind_dir_deg,humidity_in," 
                            f"rainchg,apressure from wh1080data where time >= '{startdt}' and time <'{enddt}' and temperature_C is not null", cnx)
        else:
            return None
    else:
        if days:
            refdt = datetime.datetime.now() + datetime.timedelta(days = -(days+1))
            df = pd.read_sql("select time,timestamp,press_rel,"
                            f"apressure from wh1080data where time > '{refdt}' and press_rel is not null", cnx)
        elif startdt and enddt:
            df = pd.read_sql(f"select time,timestamp,press_rel,apressure from wh1080data"
                            f" where time >= '{startdt}' and time <'{enddt}' and press_rel is not null", cnx)
        else:
            return None

    # convert time column properly    
    df['truetime'] = [datetime.datetime.strptime(d.replace(' ','T')[:19], '%Y-%m-%dT%H:%M:%S') for d in df.time]
    df.drop(columns=['time'], inplace=True)
    df.rename(columns={'truetime':'time'}, inplace=True)

    # convert timestamp to tz=aware values
    df['ts2'] = [pd.Timestamp(d, tz='UTC') for d in df.timestamp]
    df.drop(columns=['timestamp'], inplace=True)
    df.rename(columns={'ts2':'timestamp'}, inplace=True)

    df.set_index(keys=['time'], inplace=True)
    df.sort_index(inplace=True)
    return df


def loadMonthlyData(years=2):
    cnx = sqlalchemy.create_engine(f'mysql+pymysql://{sqluser}:redacted@{sqlserver}:3306/{sqldb}')
    startdt = datetime.datetime.now() - relativedelta(years=years)
    ym = f'{startdt.year:04d}{startdt.month:02d}'
    df = pd.read_sql(f"select * from mthlydata where period >= '{ym}'", cnx)
    df.sort_values(by='period', ascending=True,inplace=True)
    return df


def dropCurrentRow(table=None, colname=None, colval=None):
    conn = pymysql.connect(host=sqlserver, user=sqluser, password='redacted', db=sqldb)
    cur = conn.cursor()
    result = cur.execute(f"delete from {table} where {colname} = '{colval}'")
    conn.commit()
    conn.close()
    return result


def addToDB(table=None, vals=None):
    if table is None or vals is None:
        return 0
    cnx = sqlalchemy.create_engine(f'mysql+pymysql://{sqluser}:redacted@{sqlserver}:3306/{sqldb}')
    vals.to_sql(table,cnx,schema=f'{sqldb}',if_exists='append', method='multi')
    return 1
