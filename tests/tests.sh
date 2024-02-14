#!/bin/bash

cd ./apis_services/diskspacechecks
echo HOME is $HOME
ls -ltra $HOME
mkdir $HOME/.ssh
cp /sshkeys/* $HOME/.ssh
chmod 0700 $HOME/.ssh && chmod 0600 $HOME/.ssh/*
pip install -r requirements.txt
pip install pytest pytest-cov
pytest -v . 
