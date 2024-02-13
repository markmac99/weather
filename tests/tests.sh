#!/bin/bash

cd ../apis_services/diskspacechecks
pip install -r requirements.txt
pip install pytest pytest-cov
pytest -v 
