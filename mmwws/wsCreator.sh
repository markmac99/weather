#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
. ~/miniconda3/etc/profile.d/conda.sh
conda activate $HOME/miniconda3/envs/openhabstuff

active=$(ps -ef | grep createWsFiles | grep -v grep | awk '{print $2}')
if [ "$active" == "" ] ; then 
    python $here/createWsFiles.py $HOME/weather/data
fi
rsync -avz $HOME/weather/data/ wordpresssite:weather/data
