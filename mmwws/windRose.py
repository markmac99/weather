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

from conversions import KMHTOMPH
from sqlInterface import loadDfFromDB


def _speedLabels(bins, units):   
    labels = []
    for left, right in zip(bins[:-1], bins[1:]):
        if left == bins[0]:
            labels.append('calm')
        elif np.isinf(right):
            labels.append('>{} {}'.format(left, units))
        else:
            labels.append('{} - {} {}'.format(left, right, units))
    return list(labels)


def _convertDir(directions, N=None):
    if N is None:
        N = directions.shape[0]
    barDir = directions * np.pi/180. - np.pi/N
    barWidth = 2 * np.pi / N
    return barDir, barWidth


def windRose(rosedata, wind_dirs, palette=None):
    if palette is None:
        palette = seaborn.color_palette('inferno', n_colors=rosedata.shape[1])
    bar_dir, bar_width = _convertDir(wind_dirs)

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
    spd_labels = _speedLabels(spd_bins, units='mph')

    dir_bins = np.arange(-7.5, 370, 15)
    dir_labels = (dir_bins[:-1] + dir_bins[1:]) / 2

    rose = (df.assign(WindSpd_bins=lambda df: pd.cut(df['wind_max_km_h']*KMHTOMPH, bins=spd_bins, labels=spd_labels, right=True))
            .assign(WindDir_bins=lambda df: pd.cut(df['wind_dir_deg'], bins=dir_bins, labels=dir_labels, right=False))
            .replace({'WindDir_bins': {360: 0}})
            .groupby(by=['WindSpd_bins', 'WindDir_bins'], observed=False)
            .size()
            .unstack(level='WindSpd_bins')
            .fillna(0)
            .assign(calm=lambda df: calm_count / df.shape[0])
            .sort_index(axis=1)
            .applymap(lambda x: x / total_count * 100))

    directions = np.arange(0, 360, 15)
    _ = windRose(rose, directions)
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

    df = loadDfFromDB(days=7)
    
    makeRose(df, outdir, 1)
    makeRose(df, outdir, 7)
