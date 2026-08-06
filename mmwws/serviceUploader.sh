#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
. ~/miniconda3/etc/profile.d/conda.sh
conda activate $HOME/miniconda3/envs/openhabstuff

active=$(ps -ef | grep sendToServices | grep -v grep | awk '{print $2}')
if [ "$active" == "" ] ; then 
    python $here/sendToServices.py $HOME/weather/data
fi
