#
# Copyright Mark McIntyre 2023-
#

import pandas as pd
import os


def mergeDataIn(outdir, tmpdir, yr):
    df = pd.read_parquet(os.path.join(outdir, f'raw-{yr}.parquet'))
    df2 = pd.read_parquet(os.path.join(tmpdir, 'newdata.parquet'))
    df3 = pd.concat([df, df2])
    df3 = df3.sort_index()
    df3.drop_duplicates(inplace=True)
    basename_template='weatherdata_{i}'
    df3.to_parquet(os.path.join(outdir, f'raw-{yr}.parquet'), partition_cols=['year','month','day'], 
            existing_data_behavior='delete_matching', basename_template=basename_template)
    return
