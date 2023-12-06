#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source $HOME/venvs/openhabstuff/bin/activate
sudo systemctl stop getweatherdata
outdir=$HOME/weather/raw
tmpdir=$HOME/weather/tmp
yr=2023
cp $outdir/raw-$yr.parquet $outdir/bkp/raw-$yr.parquet.$(date +%Y%m%d-%h%m%s)
python -c "from convertOHdata import mergeDataIn;mergeDataIn('$outdir', '$tmpdir', $yr);"
sudo systemctl start getweatherdata
mv $tmpdir/alldata.parquet $outdir/bkp/extradata.parquet.$(date +%Y%m%d-%h%m%s)