#
# copyright Mark McIntyre, 2023-
#

import pandas as pd
import os
import datetime
from dateutil.relativedelta import relativedelta

from tempPressData import getRangeValues
from tableHeaders import amhdr, amrwtempl, amfootr, rerwtempl, refootr

# correction for instrument readout inaccuracy
pressureCorrection = 10


def recentTable(df, outdir, period=1):
    now=datetime.datetime.now()
    avgs = False
    tfmt = '%H:%M'
    hord = 'hr'
    hord2 = 'hrs'
    pp = period
    if period > 24:
        hord = 'days'
        hord2 = 'days'
        pp = int(period/24)
    outfname = os.path.join(outdir, f'dragontail-{pp}{hord}-table.js')
    if period == 1:
        freq = 5
        window = 5
        avgs = True # get averages 
        back1hr = now + datetime.timedelta(hours=-period)
    elif period < 25:
        freq = 60
        window = 60
        if period == 6:
            freq = 30
            window = 30
        avgs = True
        back1hr = now + datetime.timedelta(hours=-period)
        back1hr = back1hr.replace(minute=0, second=59, microsecond=0)
    else:
        tfmt = '%Y/%m/%d %H:%M GMT'
        freq = 60 * 24 # daily if period is longer than a day
        back1hr = now + datetime.timedelta(hours=-period)
        window = 24 * 60
        avgs = False
        back1hr = back1hr.replace(minute=0, second=59, microsecond=0) #  - datetime.timedelta(minutes=1)

    seldf = df[df.timestamp > pd.Timestamp(back1hr, tz='UTC')]
    with open(outfname, 'w') as of:
        of.write(amhdr)
        numrows = int((period *60)/freq)
        prevrain = -1
        for r in range(numrows):
            offs = r * freq
            st = min(back1hr + datetime.timedelta(minutes=(offs)), now)
            vals = getRangeValues(seldf, st, window, doaverage=avgs)
            if pd.isna(vals['temp_c']):
                continue
            ts = vals['time'].strftime(tfmt) 
            temp = round(vals['temp_c'], 1)
            hum = int(vals['humidity'])
            wina = round(vals['wind_ave'] * 0.6214, 1)
            winm = round(vals['wind_max'] * 0.6214, 1)
            # rainfall is cumulative
            if prevrain < 0:
                rain = 0.0
            else:
                rain = round(max(vals['rain_mm'] - prevrain, 0), 1)
            prevrain = round(vals['rain_mm'], 1)
            pres = round(vals['pressure'] + pressureCorrection, 1)
            of.write(rerwtempl.format(ts, temp, hum, wina, winm, rain, pres))
        of.write(refootr.format(pp, hord2))


def monthlySummary(df, outdir):
    now=datetime.datetime.now()
    backdt = now + relativedelta(years=-5)
    backdt = backdt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=1)
    outfname = os.path.join(outdir, 'dragontail-allmonths-table.js')    
    with open(outfname, 'w') as of:
        of.write(amhdr)
        while backdt < now:
            todt = backdt + relativedelta(months=1)
            mthname = backdt.strftime('%Y-%m')
            seldf = df[df.timestamp >= pd.Timestamp(backdt, tz='UTC')]
            seldf = seldf[seldf.timestamp < pd.Timestamp(todt, tz='UTC')]
            if len(seldf) == 0:
                backdt = todt
                continue
            seldf['mthday'] = [x.day for x in seldf.timestamp]
            df2=seldf.groupby(['mthday'])
            rvals=df2.rain_mm.max()-df2.rain_mm.min()
            raindays = int(len(rvals[rvals>0]))
            raintot = round(sum(rvals),0)

            seldf['hour'] = [x.hour for x in seldf.timestamp]
            maxd = round(seldf[(seldf.hour>=9) & (seldf.hour<21)].temperature_C.max(), 1)
            mind = round(seldf[(seldf.hour>=9) & (seldf.hour<21)].temperature_C.min(), 1)
            aved = round(seldf[(seldf.hour>=9) & (seldf.hour<21)].temperature_C.mean(), 1)
            maxn = round(seldf[(seldf.hour<9) | (seldf.hour>=21)].temperature_C.max(), 1)
            minn = round(seldf[(seldf.hour<9) | (seldf.hour>=21)].temperature_C.min(), 1)
            aven = round(seldf[(seldf.hour<9) | (seldf.hour>=21)].temperature_C.mean(), 1)

            outval = amrwtempl.format(mthname, maxd, aved, mind, maxn, aven, minn, raintot, raindays)
            of.write(outval)
            backdt = todt
        of.write(amfootr)

    return 
