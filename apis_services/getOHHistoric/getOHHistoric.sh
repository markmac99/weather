#!/bin/bash

# this script should be run on the OpenHab server to extract historical data that can be reloaded into
# the mmwws database if the Maplin station batteries die. 

# adjust the dates accordingly, then run the script. You should end up with "newdata.parquet"

# Now login to the mmwws server, switch to the source directory and  edit convertOHdata.py to have
# matching dates then run the script to load the data into the parquet tables. 

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source ~/.bashrc
conda activate openhabstuff

python $here/convertOHdata.py ./config.txt

scp ./newdata.parquet wordpresssite:weather/tmp