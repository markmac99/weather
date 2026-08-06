#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
. ~/miniconda3/etc/profile.d/conda.sh
conda activate $HOME/miniconda3/envs/openhabstuff

sudo systemctl stop getweatherdata
outdir=$HOME/weather/raw
tmpdir=$HOME/weather/tmp
yr=$(date +%Y)
mkdir -p $outdir/bkp
cp -r $outdir/raw-$yr.parquet $outdir/bkp/raw-$yr.parquet.$(date +%Y%m%d-%h%m%s)
python -c "from loadOHdata import mergeDataIn;mergeDataIn('$outdir', '$tmpdir', $yr);"
sudo systemctl start getweatherdata
mv $tmpdir/newdata.parquet $outdir/bkp/extradata.parquet.$(date +%Y%m%d-%h%m%s)