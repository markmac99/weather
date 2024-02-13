# copyright Mark McIntyre, 29024-

# tests 

import os
from pubData import getDF

logdir = './logs'
os.makedirs(logdir, exist_ok=True)


def test_getDF():
    hn = 'wordpresssite'
    dfpct = getDF(hn, logdir)
    print(dfpct)
    assert dfpct is not False
