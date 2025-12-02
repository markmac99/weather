#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source HOMEDIR/venvs/pywws/bin/activate
rm -f /tmp/stopgetwu
python getbresswu.py
