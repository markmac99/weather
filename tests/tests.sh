#!/bin/bash

cd ./apis_services/diskspacechecks
echo HOME is $HOME
if [ ! -f $HOME/.ssh/config ] ; then 
    mkdir $HOME/.ssh
    cp /sshkeys/* $HOME/.ssh
    chmod 0700 $HOME/.ssh && chmod 0600 $HOME/.ssh/*
fi 
pip install -r requirements.txt
pip install pytest pytest-cov
pytest -v . 
