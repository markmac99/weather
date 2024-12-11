#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source $HOME/venvs/openhabstuff/bin/activate

# done here rather than in python because Parquet rewrites every file every time
# it saves, and so we would have tens of thousands of writes per day, driving up cost
# unacceptably

cd ~/weather/raw

# check parquet file isn't corrupted
yr=$(date +%Y)
python -c "import pandas as pd;df=pd.read_parquet('raw-${yr}.parquet')"
if [ $? == 0 ] ; then 
    echo "backing up to S3"
    aws s3 sync . s3://mjmm-weatherdata  --size-only
else
    echo "parquet file unreadable"
    python $here/sendAnEmail.py markmcintyre99@googlemail.com "weather parquet file corrupt" "alert from weather" weather@wordpresssite
fi
