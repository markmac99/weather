#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source $HOME/miniconda3/bin/activate openhabstuff
#conda activate ~/miniconda3/envs/openhabstuff
python pubData.py
