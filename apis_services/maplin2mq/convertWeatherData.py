# convert weatherdata.json into true json file
# copyright Mark McIntyre, 2025

import json
import datetime
import sys

rawdata = open(sys.argv[1]).readlines()
newjs = {}
for r in rawdata:
    js = json.loads(r)
    dtstamp = datetime.datetime.strptime(js['time'], '%Y-%m-%dT%H:%M:%SZ').timestamp()
    newjs[dtstamp] = js
with open(sys.argv[1], 'w') as outf:
    json.dump(newjs, outf)
