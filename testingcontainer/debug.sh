#!/bin/bash
kubectl run -i --tty --rm debug --image=busybox --restart=Never --namespace arc-runner-wh -- sh 
