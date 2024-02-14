#!/bin/bash

cd ./apis_services/diskspacechecks
ls /
ls /github
pip install -r requirements.txt
pip install pytest pytest-cov
pytest -v . 
