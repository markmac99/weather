#
# copyright Mark McIntyre, 2023-
#

# wind rose creation, after  https://gist.github.com/phobson/41b41bdd157a2bcf6e14

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import datetime
import seaborn
import os
import sys
import platform
import time


def speed_labels(bins, units):   
    labels = []
    for left, right in zip(bins[:-1], bins[1:]):
        if left == bins[0]:
            labels.append('calm')
        elif np.isinf(right):
            labels.append('>{} {}'.format(left, units))
        else:
            labels.append('{} - {} {}'.format(left, right, units))
    return list(labels)


def _convert_dir(directions, N=None):
    if N is None:
        N = directions.shape[0]
    barDir = directions * np.pi/180. - np.pi/N
    barWidth = 2 * np.pi / N
    return barDir, barWidth


def wind_rose(rosedata, wind_dirs, palette=None):
    if palette is None:
        palette = seaborn.color_palette('inferno', n_colors=rosedata.shape[1])
    bar_dir, bar_width = _convert_dir(wind_dirs)

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    ax.set_theta_direction('clockwise')
    ax.set_theta_zero_location('N')

    for n, (c1, c2) in enumerate(zip(rosedata.columns[:-1], rosedata.columns[1:])):
        if n == 0:
            # first column only
            ax.bar(bar_dir, rosedata[c1].values, 
                   width=bar_width,
                   color=palette[0],
                   edgecolor='none',
                   label=c1,
                   linewidth=0)

        # all other columns
        ax.bar(bar_dir, rosedata[c2].values, 
               width=bar_width, 
               bottom=rosedata.cumsum(axis=1)[c1].values,
               color=palette[n+1],
               edgecolor='none',
               label=c2,
               linewidth=0)

    _ = ax.legend(loc=(0.75, 0.95), ncol=2)
    _ = ax.set_xticks(np.radians(np.arange(0,360,45)))
    _ = ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
    return fig


def makeRose(df, outdir, period):
    startdt = datetime.datetime.now() + datetime.timedelta(days=-period)
    df = df[df.timestamp >= pd.Timestamp(startdt,tz='UTC')]

    total_count = df.shape[0]
    calm_count = df.query("wind_max_km_h == 0").shape[0]
    print('Of {} total observations, {} have calm winds.'.format(total_count, calm_count))

    spd_bins = [-1, 0, 5, 10, 15, 20, 25, 30, np.inf]
    spd_labels = speed_labels(spd_bins, units='mph')

    dir_bins = np.arange(-7.5, 370, 15)
    dir_labels = (dir_bins[:-1] + dir_bins[1:]) / 2

    rose = (df.assign(WindSpd_bins=lambda df: pd.cut(df['wind_max_km_h']*0.6215, bins=spd_bins, labels=spd_labels, right=True))
            .assign(WindDir_bins=lambda df: pd.cut(df['wind_dir_deg'], bins=dir_bins, labels=dir_labels, right=False))
            .replace({'WindDir_bins': {360: 0}})
            .groupby(by=['WindSpd_bins', 'WindDir_bins'])
            .size()
            .unstack(level='WindSpd_bins')
            .fillna(0)
            .assign(calm=lambda df: calm_count / df.shape[0])
            .sort_index(axis=1)
            .applymap(lambda x: x / total_count * 100))

    directions = np.arange(0, 360, 15)
    _ = wind_rose(rose, directions)
    if period == 1:
        plt.savefig(os.path.join(outdir, 'rose_24hrs.png'))
    else:
        plt.savefig(os.path.join(outdir, 'rose_7days_nights.png'))


if __name__ =='__main__':
    now = datetime.datetime.now()
    yr = now.year
    if len(sys.argv) < 2:
        outdir = os.path.expanduser('~/weather/tmp')
    else:
        outdir = os.path.expanduser(sys.argv[1])
    os.makedirs(outdir, exist_ok=True)
    rawdir = outdir.replace('data','raw')
    if platform.node() != 'wordpresssite':
        df = pd.read_parquet(f'https://markmcintyreastro.co.uk/weather/raw/raw-{yr}.parquet')
        df2 = pd.read_parquet(f'https://markmcintyreastro.co.uk/weather/raw/raw-{yr-1}.parquet')
    else:
        # current years datafile may be in the process of getting written to
        retries = 0
        while retries < 5:
            try:
                print('loading datafiles')
                df = pd.read_parquet(os.path.join(rawdir, f'raw-{yr}.parquet'))
                break
            except:
                print('file in use, waiting 5s')
                time.sleep(5)
                retries += 1
        if retries == 5:
            print('unable to open datafile, aborting')
            exit(0)
        # only load last years data if needed
        if (now +datetime.timedelta(days=-32)).year != yr:
            df2 = pd.read_parquet(os.path.join(rawdir, f'raw-{yr-1}.parquet'))
            df = pd.concat([df2,df])
    makeRose(df, outdir, 1)
    makeRose(df, outdir, 7)
