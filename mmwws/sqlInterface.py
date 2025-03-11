import sqlalchemy
import pandas as pd
import datetime

sqldb = 'weather'
sqluser = 'wh1080'
sqlserver = 'localhost'


def loadDfFromDB(days):
    cnx = sqlalchemy.create_engine(f'mysql+pymysql://{sqluser}:redacted@{sqlserver}:3306/{sqldb}')
    refdt = datetime.datetime.now() + datetime.timedelta(days = -(days+1))
    df = pd.read_sql("select time,timestamp,temperature_C,humidity,rain_mm," 
                    "press_rel,wind_max_km_h,wind_avg_km_h,temp_c_in,wind_dir_deg,humidity_in," 
                    f"rainchg,apressure from wh1080data where time > '{refdt}'", cnx)

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
